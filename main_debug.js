require('dotenv').config();
const { app, BrowserWindow } = require('electron')

function createWindow() {
  console.log('🚀 Создание окна Electron...');
  
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    show: false, // Сначала не показываем
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  })

  win.once('ready-to-show', () => {
    console.log('✅ Окно готово к отображению');
    win.show();
  });

  win.loadFile('index.html').then(() => {
    console.log('✅ HTML файл загружен');
  }).catch((err) => {
    console.error('❌ Ошибка загрузки HTML:', err);
  });
  
  // Открываем DevTools для отладки
  win.webContents.openDevTools();
}

app.whenReady().then(() => {
  console.log('✅ Electron готов');
  createWindow();
});

app.on('window-all-closed', () => {
  console.log('🔚 Все окна закрыты');
  if (process.platform !== 'darwin') app.quit()
});

console.log('🔧 main.js загружен');
