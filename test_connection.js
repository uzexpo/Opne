const WebSocket = require('ws');

console.log('🧪 Тестирование подключения к Open Interpreter серверу...');

const ws = new WebSocket('ws://localhost:8765');

ws.on('open', function open() {
  console.log('✅ Подключен к серверу на порту 8765!');
  
  // Отправим тестовое сообщение
  const testMessage = {
    message: "Привет! Как дела? Сделай скриншот экрана."
  };
  
  console.log('📤 Отправляю тестовое сообщение:', testMessage.message);
  ws.send(JSON.stringify(testMessage));
});

ws.on('message', function message(data) {
  try {
    const response = JSON.parse(data.toString());
    console.log('📥 Получен ответ от сервера:');
    console.log('   Тип:', response.type);
    console.log('   Сообщение:', response.message);
    
    if (response.type === 'response') {
      console.log('🎉 ТЕСТ УСПЕШЕН! Сервер отвечает и выполняет команды!');
      ws.close();
    }
  } catch (e) {
    console.log('📥 Сырой ответ:', data.toString());
  }
});

ws.on('error', function error(err) {
  console.error('❌ Ошибка подключения:', err.message);
});

ws.on('close', function close() {
  console.log('🔌 Соединение закрыто');
  process.exit(0);
});

// Таймаут для завершения теста
setTimeout(() => {
  console.log('⏰ Тест завершен по таймауту');
  ws.close();
}, 30000);
