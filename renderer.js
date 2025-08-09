require('dotenv').config();
const fs = require('fs');
const path = require('path');

console.log('🔧 Загрузка Chat Interface...');

// Загружаем конфигурацию
let config = { wsPort: 8765, wsHost: 'localhost' };
try {
  const configPath = path.join(__dirname, 'config', 'local.json');
  if (fs.existsSync(configPath)) {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    console.log('✅ Конфигурация загружена:', config);
  }
} catch (error) {
  console.warn('⚠️ Ошибка загрузки конфигурации, используем дефолт:', error);
}

// WebSocket URL из конфигурации или переменной окружения
const WS_PORT = process.env.OI_WS_PORT || config.wsPort || 8765;
const WS_HOST = process.env.OI_WS_HOST || config.wsHost || 'localhost';
const WS_URL = `ws://${WS_HOST}:${WS_PORT}`;

console.log(`🔗 WebSocket URL: ${WS_URL}`);

let socket = null;
let isConnecting = false;
let reconnectAttempts = 0;
const maxReconnectAttempts = 5;

// DOM элементы
let messagesContainer;
let messageInput;
let sendBtn;
let statusElement;

// Ждем загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
  console.log('📄 DOM загружен');
  
  // Получаем элементы
  messagesContainer = document.getElementById('messages');
  messageInput = document.getElementById('messageInput');
  sendBtn = document.getElementById('sendBtn');
  clearBtn = document.getElementById('clearBtn');
  statusElement = document.getElementById('status');
  
  // Настраиваем обработчики
  setupEventListeners();
  
  // Подключаемся к серверу
  connectToServer();
});

function setupEventListeners() {
  // Отправка сообщения по кнопке
  sendBtn.addEventListener('click', sendMessage);
  
  // Очистка чата по кнопке
  clearBtn.addEventListener('click', clearMessages);
  
  // Горячие клавиши
  document.addEventListener('keydown', (e) => {
    // Ctrl+L - очистка
    if (e.ctrlKey && e.key === 'l') {
      e.preventDefault();
      clearMessages();
      return;
    }
    
    // Escape - сброс ввода
    if (e.key === 'Escape') {
      messageInput.value = '';
      messageInput.focus();
      return;
    }
  });
  
  // Отправка сообщения по Enter
  messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });
  
  console.log('📋 Обработчики событий настроены');
}

function connectToServer() {
  if (isConnecting || socket?.readyState === WebSocket.OPEN) {
    return;
  }
  
  isConnecting = true;
  updateStatus('🔄 Подключение к серверу...');
  console.log(`🔗 Попытка подключения к ${WS_URL}`);
  console.debug('🔧 [DEBUG] Создание WebSocket соединения...');
  
  try {
    socket = new WebSocket(WS_URL);
    console.debug('🔧 [DEBUG] WebSocket объект создан:', socket);
    
    socket.onopen = () => {
      console.log('✅ Подключение установлено');
      console.debug('🔧 [DEBUG] socket.onopen - готовность:', socket.readyState);
      isConnecting = false;
      reconnectAttempts = 0;
      updateStatus('✅ Подключено');
      enableInput();
    };
    
    socket.onmessage = (event) => {
      console.debug('🔧 [DEBUG] Получено сообщение:', event.data);
      try {
        const data = JSON.parse(event.data);
        console.debug('🔧 [DEBUG] Разобранные данные:', data);
        handleServerMessage(data);
      } catch (e) {
        console.error('Ошибка парсинга сообщения:', e);
      }
    };
    
    socket.onclose = (event) => {
      console.log('❌ Соединение закрыто. Код:', event.code, 'Причина:', event.reason);
      console.debug('🔧 [DEBUG] socket.onclose - детали:', {
        code: event.code,
        reason: event.reason,
        wasClean: event.wasClean,
        reconnectAttempts: reconnectAttempts
      });
      isConnecting = false;
      disableInput();
      
      if (reconnectAttempts < maxReconnectAttempts) {
        updateStatus(`🔄 Переподключение... (${reconnectAttempts + 1}/${maxReconnectAttempts})`);
        console.debug(`🔧 [DEBUG] Попытка переподключения ${reconnectAttempts + 1}/${maxReconnectAttempts}`);
        reconnectAttempts++;
        setTimeout(() => connectToServer(), 2000);
      } else {
        updateStatus('❌ Не удалось подключиться к серверу');
        console.error('❌ [ERROR] Превышено максимальное количество попыток переподключения');
        addMessage('error', `Сервер недоступен. Убедитесь, что server.py запущен на ${WS_URL}`);
      }
    };
    
    socket.onerror = (error) => {
      console.error('❌ [ERROR] Ошибка WebSocket:', error);
      console.debug('🔧 [DEBUG] socket.onerror - состояние соединения:', socket.readyState);
      isConnecting = false;
      updateStatus('❌ Ошибка подключения');
    };
    
  } catch (error) {
    console.error('Ошибка создания WebSocket:', error);
    isConnecting = false;
    updateStatus('❌ Ошибка подключения');
  }
}

function handleServerMessage(data) {
  const { type, message, content } = data;
  console.debug('🔧 [DEBUG] Обработка сообщения типа:', type);
  
  switch (type) {
    case 'system':
      hideTyping();
      addMessage('system', message);
      break;
    case 'user_echo':
      // Пользовательское сообщение уже отображено
      console.debug('🔧 [DEBUG] Получено эхо пользовательского сообщения');
      break;
    case 'processing':
      addMessage('system', message);
      showTyping();
      break;
    case 'response':
      hideTyping();
      addMessage('assistant', message);
      break;
    case 'stream_start':
      hideTyping();
      console.debug('🔧 [DEBUG] Начало потокового вывода');
      // Создаем новое сообщение ассистента для потокового обновления
      addMessage('assistant', '');
      break;
    case 'stream_chunk':
      // Обновляем последнее сообщение ассистента с новым контентом
      updateLastMessage(content || message);
      break;
    case 'stream_end':
      hideTyping();
      console.debug('🔧 [DEBUG] Завершение потокового вывода');
      break;
    case 'error':
      hideTyping();
      addMessage('error', message);
      break;
    case 'stream':
      // Для потокового ответа
      hideTyping();
      updateLastMessage('assistant', message);
      break;
    default:
      console.warn('⚠️ [WARN] Неизвестный тип сообщения:', type, data);
      addMessage('system', `Неизвестное сообщение: ${JSON.stringify(data)}`);
  }
}

function sendMessage() {
  const message = messageInput.value.trim();
  console.debug('🔧 [DEBUG] sendMessage вызвана с:', message);
  
  // Проверки безопасности
  if (!message) {
    console.debug('🔧 [DEBUG] Пустое сообщение - отмена отправки');
    return;
  }
  
  // Проверка критичных команд
  if (isCriticalCommand(message)) {
    const confirmed = confirm(`⚠️ ВНИМАНИЕ: Это потенциально опасная команда:\n"${message}"\n\nВы уверены, что хотите выполнить её?`);
    if (!confirmed) {
      console.debug('🔧 [DEBUG] Критичная команда отменена пользователем');
      addMessage('system', '⚠️ Выполнение критичной команды отменено');
      return;
    }
  }
  
  if (!socket) {
    console.error('❌ [ERROR] WebSocket не создан');
    addMessage('error', 'WebSocket не инициализирован');
    return;
  }
  
  if (socket.readyState !== WebSocket.OPEN) {
    console.error('❌ [ERROR] WebSocket не подключен, состояние:', socket.readyState);
    addMessage('error', 'Нет соединения с сервером');
    return;
  }
  
  // Добавляем сообщение пользователя в чат
  addMessage('user', message);
  console.debug('🔧 [DEBUG] Сообщение добавлено в UI');
  
  // Показываем индикатор обработки
  showTyping();
  
  // Отправляем на сервер
  const messageData = { message };
  console.debug('🔧 [DEBUG] Отправка данных:', messageData);
  
  try {
    socket.send(JSON.stringify(messageData));
    console.debug('✅ [DEBUG] Сообщение отправлено успешно');
  } catch (error) {
    console.error('❌ [ERROR] Ошибка отправки:', error);
    addMessage('error', 'Ошибка отправки сообщения');
  }
  
  // Очищаем поле ввода
  messageInput.value = '';
}

function addMessage(type, content) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `message ${type}`;
  
  const contentDiv = document.createElement('div');
  contentDiv.className = 'content';
  
  // Используем форматирование для всех типов сообщений
  if (type === 'assistant' || type === 'system') {
    contentDiv.innerHTML = formatMessage(content);
  } else {
    contentDiv.textContent = content;
  }
  
  messageDiv.appendChild(contentDiv);
  messagesContainer.appendChild(messageDiv);
  scrollToBottom();
}

function showTyping() {
  // Удаляем предыдущий индикатор печати
  hideTyping();
  
  const typingDiv = document.createElement('div');
  typingDiv.className = 'message assistant typing';
  typingDiv.id = 'typing-indicator';
  typingDiv.innerHTML = `
    <span>Печатает</span>
    <div class="typing-dots">
      <span></span>
      <span></span>
      <span></span>
    </div>
  `;
  
  messagesContainer.appendChild(typingDiv);
  scrollToBottom();
}

function hideTyping() {
  const typingIndicator = document.getElementById('typing-indicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

function updateLastMessage(content) {
  const messageElements = messagesContainer.querySelectorAll('.message.assistant .content');
  if (messageElements.length > 0) {
    const lastElement = messageElements[messageElements.length - 1];
    lastElement.innerHTML = formatMessage(content);
    console.debug('Обновлено последнее сообщение ассистента:', content.substring(0, 100) + '...');
  } else {
    // Если нет сообщений ассистента, создаем новое
    addMessage(content, 'assistant');
    console.debug('Создано новое сообщение ассистента');
  }
  scrollToBottom();
}

function formatMessage(content) {
  if (!content) return '';
  
  // Базовое форматирование для markdown
  let formatted = content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
    
  // Форматирование блоков кода
  formatted = formatted.replace(/```(\w+)?\n?([\s\S]*?)```/g, (match, lang, code) => {
    return `<pre><code class="language-${lang || 'text'}">${code.trim()}</code></pre>`;
  });
  
  return formatted;
}

function scrollToBottom() {
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateStatus(status) {
  statusElement.textContent = status;
}

function enableInput() {
  messageInput.disabled = false;
  sendBtn.disabled = false;
  clearBtn.disabled = false;
  messageInput.focus();
}

function disableInput() {
  messageInput.disabled = true;
  sendBtn.disabled = true;
  clearBtn.disabled = true;
}

function clearMessages() {
  console.debug('🔧 [DEBUG] Очистка сообщений чата');
  messagesContainer.innerHTML = '';
  addMessage('system', '🧹 Чат очищен');
  messageInput.focus();
}

function showTyping() {
  // Показываем индикатор печатания
  if (!document.getElementById('typing-indicator')) {
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message assistant';
    typingDiv.innerHTML = '🤖 Генерирую ответ<span class="dots">...</span>';
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
}

function hideTyping() {
  const typingIndicator = document.getElementById('typing-indicator');
  if (typingIndicator) {
    typingIndicator.remove();
  }
}

// Проверка критичных команд
function isCriticalCommand(message) {
  const criticalPatterns = [
    /rm\s+-rf\s+/i,
    /del\s+\/[sf]/i,
    /format\s+[c-z]:/i,
    /sudo\s+rm/i,
    /shutdown/i,
    /reboot/i
  ];
  
  return criticalPatterns.some(pattern => pattern.test(message));
}

// Инициализация
console.log('🚀 Chat Interface готов к запуску');
