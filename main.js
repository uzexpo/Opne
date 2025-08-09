require('dotenv').config();
const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');

// API Keys access
const openaiKey = process.env.OPENAI_API_KEY;
const claudeKey = process.env.CLAUDE_API_KEY;
const geminiKey = process.env.GEMINI_API_KEY;
const deepseekKey = process.env.DEEPSEEK_API_KEY;

let mainWindow;
let pythonServer = null;

function createWindow() {
  // Создаем главное окно
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    alwaysOnTop: false,
    frame: true,
    transparent: false,
    resizable: true,
    title: 'Open Interpreter - AI Agent',
    icon: path.join(__dirname, 'assets', 'icon.svg'),
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
      webSecurity: false
    },
    show: false // Не показываем окно сразу
  });

  // Загружаем HTML файл
  mainWindow.loadFile('index.html');
  
  // Показываем окно когда готово
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    console.log('🚀 Open Interpreter Electron приложение запущено!');
  });

  // Открываем DevTools в режиме разработки
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  // Обработка закрытия окна
  mainWindow.on('closed', () => {
    mainWindow = null;
    // Останавливаем Python сервер при закрытии приложения
    if (pythonServer) {
      pythonServer.kill();
      console.log('🔚 Python сервер остановлен');
    }
  });
}

// Функция запуска Python сервера
function startPythonServer() {
  return new Promise((resolve, reject) => {
    console.log('🔧 Запуск Python сервера...');
    
    // Путь к Python серверу
    const serverPath = path.join(__dirname, 'server.py');
    
    // Проверяем существование файла
    if (!fs.existsSync(serverPath)) {
      reject(new Error('Файл server.py не найден!'));
      return;
    }

    // Определяем правильный путь к Python
    const isWindows = process.platform === 'win32';
    let pythonPath;
    
    if (isWindows) {
      // Путь к Python в виртуальном окружении на Windows
      const venvPath = path.join(__dirname, '..', '.venv', 'Scripts', 'python.exe');
      pythonPath = fs.existsSync(venvPath) ? venvPath : 'python';
    } else {
      // Для Linux/Mac
      const venvPath = path.join(__dirname, '..', '.venv', 'bin', 'python');
      pythonPath = fs.existsSync(venvPath) ? venvPath : 'python3';
    }

    console.log('🐍 Используем Python:', pythonPath);

    // Запускаем Python сервер
    pythonServer = spawn(pythonPath, [serverPath], {
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: true
    });

    // Обработка вывода сервера
    pythonServer.stdout.on('data', (data) => {
      const output = data.toString();
      console.log('📡 Сервер:', output);
      
      // Отправляем статус в главное окно
      if (mainWindow) {
        mainWindow.webContents.send('server-status', {
          type: 'output',
          message: output
        });
      }
    });

    pythonServer.stderr.on('data', (data) => {
      const error = data.toString();
      console.error('❌ Ошибка сервера:', error);
      
      if (mainWindow) {
        mainWindow.webContents.send('server-status', {
          type: 'error',
          message: error
        });
      }
    });

    pythonServer.on('close', (code) => {
      console.log(`🔚 Python сервер завершен с кодом ${code}`);
      if (mainWindow) {
        mainWindow.webContents.send('server-status', {
          type: 'closed',
          code: code
        });
      }
    });

    // Ждем немного для запуска сервера
    setTimeout(() => {
      console.log('✅ Python сервер запущен!');
      resolve();
    }, 2000);
  });
}

// IPC обработчики
ipcMain.handle('start-server', async () => {
  try {
    await startPythonServer();
    return { success: true, message: 'Сервер запущен успешно!' };
  } catch (error) {
    console.error('❌ Ошибка запуска сервера:', error);
    return { success: false, message: error.message };
  }
});

ipcMain.handle('stop-server', () => {
  if (pythonServer) {
    pythonServer.kill();
    pythonServer = null;
    return { success: true, message: 'Сервер остановлен!' };
  }
  return { success: false, message: 'Сервер не был запущен!' };
});

ipcMain.handle('get-server-status', () => {
  return {
    isRunning: pythonServer !== null,
    pid: pythonServer ? pythonServer.pid : null
  };
});

// Обработка выбора файла
ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'Все файлы', extensions: ['*'] },
      { name: 'Текстовые файлы', extensions: ['txt', 'md', 'py', 'js', 'html', 'css'] },
      { name: 'Изображения', extensions: ['png', 'jpg', 'jpeg', 'gif', 'bmp'] }
    ]
  });
  
  if (!result.canceled) {
    return result.filePaths[0];
  }
  return null;
});

// Обработка сохранения файла
ipcMain.handle('save-file', async (event, defaultPath) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    defaultPath: defaultPath || 'output.txt',
    filters: [
      { name: 'Текстовые файлы', extensions: ['txt'] },
      { name: 'Все файлы', extensions: ['*'] }
    ]
  });
  
  if (!result.canceled) {
    return result.filePath;
  }
  return null;
});

// Обработка системных команд
ipcMain.handle('system-command', async (event, command) => {
  return new Promise((resolve) => {
    const child = spawn(command, [], { shell: true });
    
    let output = '';
    let error = '';
    
    child.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    child.stderr.on('data', (data) => {
      error += data.toString();
    });
    
    child.on('close', (code) => {
      resolve({
        success: code === 0,
        output: output,
        error: error,
        code: code
      });
    });
  });
});

// Инициализация приложения
app.whenReady().then(async () => {
  console.log('🚀 Инициализация Open Interpreter...');
  
  // Создаем окно
  createWindow();
  
  // Автоматически запускаем Python сервер
  try {
    await startPythonServer();
    console.log('✅ Сервер запущен автоматически!');
  } catch (error) {
    console.error('⚠️ Не удалось автоматически запустить сервер:', error.message);
    // Показываем диалог с ошибкой
    dialog.showErrorBox('Ошибка запуска сервера', 
      'Не удалось автоматически запустить Python сервер.\n' +
      'Попробуйте запустить сервер вручную через меню.');
  }
});

// Обработка активации приложения (macOS)
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Обработка закрытия всех окон
app.on('window-all-closed', () => {
  // Останавливаем Python сервер
  if (pythonServer) {
    pythonServer.kill();
    console.log('🔚 Python сервер остановлен при закрытии приложения');
  }
  
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Обработка необработанных исключений
process.on('uncaughtException', (error) => {
  console.error('❌ Необработанная ошибка:', error);
  dialog.showErrorBox('Критическая ошибка', 
    'Произошла необработанная ошибка:\n' + error.message);
});

console.log('🔧 main.js загружен и готов к работе!');
