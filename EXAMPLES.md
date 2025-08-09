# 🎯 ПРАКТИЧЕСКИЕ ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ OPEN INTERPRETER

## 🚀 БЫСТРЫЙ СТАРТ

### 1. Запуск сервера
```bash
# Основной сервер
python server.py

# Простой сервер для тестирования
python simple_server.py

# Через bat файл
start.bat
```

### 2. Подключение к WebSocket
```javascript
// Подключение к серверу
const socket = new WebSocket('ws://localhost:8765');
```

---

## 🔧 СИСТЕМНЫЕ ПРИМЕРЫ

### Мониторинг системы
```python
# Получить информацию о системе
system_report()

# Проверить использование ресурсов
get_memory_usage()
get_disk_usage()
get_cpu_usage()

# Список процессов
list_processes()
```

### Управление процессами
```python
# Завершить процесс
kill_process("chrome.exe")

# Перезапустить проводник
restart_explorer()

# Очистить временные файлы
clear_temp()
```

### Установка программ
```python
# Установить Python пакет
install_package("requests")

# Автоустановка недостающих пакетов
auto_install_missing()

# Установка программ через winget
install_software()
```

---

## 🖱️ GUI АВТОМАТИЗАЦИЯ

### Управление мышью
```python
# Клик по координатам
click_at(500, 300)

# Клик по изображению
click_image("button.png", confidence=0.8)

# Перемещение мыши
move(100, 200)

# Найти и кликнуть
find_and_click("icon.png")
```

### Управление клавиатурой
```python
# Ввод текста
type_text("Hello, World!")

# Нажатие клавиш
press_key("enter")
press_key("space")

# Горячие клавиши
press_keys(['ctrl', 'a'])  # Выделить все
press_keys(['ctrl', 'c'])  # Копировать
press_keys(['ctrl', 'v'])  # Вставить
press_keys(['ctrl', 's'])  # Сохранить
press_keys(['alt', 'tab']) # Переключить окно
```

### Скриншоты
```python
# Быстрый скриншот
take_screenshot()

# Скриншот с именем файла
take_screenshot("my_screenshot.png")
```

### Буфер обмена
```python
# Копировать текст
copy("Текст для копирования")

# Вставить текст
pasted_text = paste()
```

---

## 📁 ФАЙЛОВЫЕ ОПЕРАЦИИ

### Создание и редактирование файлов
```python
# Создать файл
create_file("test.txt", "Содержимое файла")

# Читать файл
content = read_file("test.txt")

# Редактировать файл
edit_file("test.txt", "Новое содержимое")
```

### Поиск файлов
```python
# Поиск по паттерну
files = search_files("*.txt")

# Поиск в конкретной директории
files = search_files("*.py", "C:/Users/user/Documents")

# Умный поиск
results = smart_search("example", "files")
```

### Работа с архивами
```python
# Создать ZIP архив
import zipfile
with zipfile.ZipFile('archive.zip', 'w') as zipf:
    zipf.write('file.txt')

# Распаковать архив
with zipfile.ZipFile('archive.zip', 'r') as zipf:
    zipf.extractall('extracted/')
```

---

## 🌐 СЕТЕВЫЕ ОПЕРАЦИИ

### HTTP запросы
```python
# GET запрос
response = requests.get('https://api.github.com/users/octocat')
data = response.json()

# POST запрос
response = requests.post('https://httpbin.org/post', 
                        data={'key': 'value'})

# Загрузка файла
download_large_file('https://example.com/file.zip', 'file.zip')
```

### Сетевая диагностика
```python
# Проверить интернет
if check_internet():
    print("Интернет работает")

# Получить IP адрес
ip = get_ip()

# Сканировать порт
if scan_port("localhost", 80):
    print("Порт 80 открыт")
```

### FTP операции
```python
# Подключение к FTP
import ftplib
ftp = ftplib.FTP('ftp.example.com')
ftp.login('username', 'password')

# Загрузить файл
with open('file.txt', 'rb') as f:
    ftp.storbinary('STOR file.txt', f)
```

---

## 🎵 МУЛЬТИМЕДИА ПРИМЕРЫ

### Музыкальные приложения
```python
# Найти и запустить музыку
find_and_launch_music_app()

# Найти конкретное приложение
app = find_application("Spotify")
if app:
    print(f"Найдено: {app['name']}")
```

### Управление воспроизведением
```python
# Воспроизвести
control_media('play')

# Пауза
control_media('pause')

# Следующий трек
control_media('next')

# Предыдущий трек
control_media('previous')

# Управление громкостью
control_media('volume_up')
control_media('volume_down')
control_media('mute')
```

### Звук и речь
```python
# Воспроизвести звук
play_sound("sound.wav")

# Синтез речи
text_to_speech("Привет, мир!")
```

---

## 🌍 ВЕБ-АВТОМАТИЗАЦИЯ

### Selenium автоматизация
```python
# Запуск браузера
from selenium import webdriver
driver = webdriver.Chrome()

# Перейти на сайт
driver.get('https://www.google.com')

# Найти элемент
element = driver.find_element(By.NAME, 'q')

# Ввести текст
element.send_keys('Open Interpreter')

# Нажать Enter
element.send_keys(Keys.RETURN)

# Выполнить JavaScript
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Сделать скриншот
driver.save_screenshot('screenshot.png')

# Закрыть браузер
driver.quit()
```

### Puppeteer (Node.js)
```python
# Запуск браузера
const browser = await puppeteer.launch();

# Создать страницу
const page = await browser.newPage();

# Перейти на сайт
await page.goto('https://example.com');

# Сделать скриншот
await page.screenshot({path: 'screenshot.png'});

# Получить заголовок
const title = await page.title();

# Закрыть браузер
await browser.close();
```

### Chrome отладка
```python
# Подключиться к существующему Chrome
connect_to_existing_chrome()

# Запустить Chrome с отладкой
start_chrome_with_debugging()

# Получить все вкладки
tabs = get_all_tabs()

# Получить содержимое страницы
content = get_page_content()
```

---

## 🖼️ ОБРАБОТКА ИЗОБРАЖЕНИЙ

### OCR (Распознавание текста)
```python
# Распознать текст с изображения
import pytesseract
from PIL import Image

image = Image.open('screenshot.png')
text = pytesseract.image_to_string(image, lang='rus+eng')
print(text)

# Получить данные изображения
data = pytesseract.image_to_data(image)
```

### Обработка изображений
```python
# PIL/Pillow
from PIL import Image

# Открыть изображение
img = Image.open('image.jpg')

# Изменить размер
img_resized = img.resize((800, 600))

# Обрезать
img_cropped = img.crop((100, 100, 500, 400))

# Сохранить
img_resized.save('resized.jpg')

# OpenCV
import cv2

# Читать изображение
img = cv2.imread('image.jpg')

# Изменить размер
resized = cv2.resize(img, (800, 600))

# Сохранить
cv2.imwrite('resized.jpg', resized)
```

### Поиск изображений на экране
```python
# Найти изображение на экране
location = pyautogui.locateOnScreen('button.png')

if location:
    # Кликнуть по найденному изображению
    center = pyautogui.center(location)
    pyautogui.click(center)
```

---

## 📊 РАБОТА С ДАННЫМИ

### Pandas анализ
```python
import pandas as pd

# Читать CSV файл
df = pd.read_csv('data.csv')

# Показать первые строки
print(df.head())

# Статистика
print(df.describe())

# Фильтрация
filtered = df[df['column'] > 100]

# Сохранить результат
filtered.to_csv('filtered_data.csv')
```

### NumPy вычисления
```python
import numpy as np

# Создать массив
arr = np.array([1, 2, 3, 4, 5])

# Математические операции
mean = np.mean(arr)
std = np.std(arr)

# Случайные числа
random_numbers = np.random.randn(1000)
```

### Машинное обучение
```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Подготовить данные
X = df[['feature1', 'feature2']]
y = df['target']

# Разделить на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Обучить модель
model = LinearRegression()
model.fit(X_train, y_train)

# Предсказания
predictions = model.predict(X_test)
```

### Визуализация
```python
import matplotlib.pyplot as plt

# Линейный график
plt.plot(x, y)
plt.title('График')
plt.xlabel('X')
plt.ylabel('Y')
plt.savefig('graph.png')
plt.show()

# Гистограмма
plt.hist(data, bins=20)
plt.title('Гистограмма')
plt.savefig('histogram.png')
plt.show()
```

---

## 🔒 БЕЗОПАСНОСТЬ

### Криптография
```python
from cryptography.fernet import Fernet

# Генерация ключа
key = Fernet.generate_key()
cipher = Fernet(key)

# Шифрование
encrypted = cipher.encrypt(b"Секретное сообщение")

# Расшифрование
decrypted = cipher.decrypt(encrypted)
```

### Хеширование
```python
import hashlib

# MD5 хеш
md5_hash = hashlib.md5(b"Hello World").hexdigest()

# SHA256 хеш
sha256_hash = hashlib.sha256(b"Hello World").hexdigest()
```

### SSH соединение
```python
import paramiko

# Создать SSH клиент
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Подключиться
ssh.connect('hostname', username='user', password='password')

# Выполнить команду
stdin, stdout, stderr = ssh.exec_command('ls -la')
output = stdout.read().decode()

# Закрыть соединение
ssh.close()
```

---

## ⚡ СПЕЦИАЛЬНЫЕ ФУНКЦИИ

### Массовая автоматизация
```python
# Список действий для автоматизации
actions = [
    {'type': 'click', 'x': 100, 'y': 200},
    {'type': 'type', 'text': 'Hello'},
    {'type': 'key', 'key': 'enter'},
    {'type': 'command', 'command': 'echo "Done"'}
]

# Выполнить массовую автоматизацию
results = mass_automation(actions)
```

### Умный поиск
```python
# Поиск файлов
files = smart_search("document", "files")

# Поиск в интернете
web_results = smart_search("Open Interpreter", "web")
```

### Мониторинг системы
```python
# Получить информацию о системе
info = system_monitor()
print(f"CPU: {info['cpu']}%")
print(f"Memory: {info['memory']}%")
print(f"Disk: {info['disk']}%")
```

### VS Code автоматизация
```python
# Открыть VS Code
open_vscode()

# Открыть файл в VS Code
open_vscode("C:/path/to/file.py")

# Найти окно VS Code
window = find_vscode_window()

# Сфокусироваться на VS Code
focus_vscode()

# Редактировать файл
edit_file("test.py", "print('Hello, World!')")
```

---

## 🎯 КОМПЛЕКСНЫЕ ПРИМЕРЫ

### Автоматизация работы с браузером
```python
# Полный пример автоматизации веб-задачи
def automate_web_task():
    # Запустить браузер
    driver = webdriver.Chrome()
    
    # Перейти на сайт
    driver.get('https://example.com')
    
    # Найти форму
    form = driver.find_element(By.ID, 'search-form')
    
    # Ввести данные
    input_field = form.find_element(By.NAME, 'query')
    input_field.send_keys('Open Interpreter')
    
    # Отправить форму
    submit_button = form.find_element(By.TYPE, 'submit')
    submit_button.click()
    
    # Дождаться результатов
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "results"))
    )
    
    # Сделать скриншот
    driver.save_screenshot('results.png')
    
    # Закрыть браузер
    driver.quit()
```

### Автоматизация обработки файлов
```python
# Обработка множества файлов
def process_files():
    # Найти все текстовые файлы
    files = search_files("*.txt")
    
    for file in files:
        # Читать файл
        content = read_file(file)
        
        # Обработать содержимое
        processed = content.upper()
        
        # Создать новый файл
        new_file = file.replace('.txt', '_processed.txt')
        create_file(new_file, processed)
        
        print(f"Обработан: {file}")
```

### Автоматизация мультимедиа
```python
# Полная автоматизация музыкального плеера
def music_automation():
    # Найти и запустить музыку
    if find_and_launch_music_app():
        print("Музыкальное приложение запущено")
        
        # Воспроизвести
        control_media('play')
        
        # Подождать 30 секунд
        time.sleep(30)
        
        # Следующий трек
        control_media('next')
        
        # Увеличить громкость
        control_media('volume_up')
    else:
        print("Музыкальное приложение не найдено")
```

---

## 🚨 ОТЛАДКА И ОШИБКИ

### Обработка ошибок
```python
try:
    # Попытка выполнить команду
    result = execute_command("some_command")
    print(f"Успешно: {result}")
except Exception as e:
    print(f"Ошибка: {e}")
    # Попробовать альтернативный способ
    alternative_result = execute_command("alternative_command")
```

### Проверка доступности функций
```python
# Проверить доступность модуля
try:
    import pyautogui
    print("PyAutoGUI доступен")
except ImportError:
    print("PyAutoGUI не установлен")
    install_package("pyautogui")
```

### Логирование
```python
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Логировать действия
logger.info("Выполняю команду")
try:
    result = some_command()
    logger.info(f"Команда выполнена: {result}")
except Exception as e:
    logger.error(f"Ошибка: {e}")
```

---

## 🎉 ЗАКЛЮЧЕНИЕ

Эти примеры демонстрируют **МАКСИМАЛЬНУЮ ФУНКЦИОНАЛЬНОСТЬ** Open Interpreter:

✅ **Автоматизация GUI** - управление мышью, клавиатурой, экраном  
✅ **Веб-автоматизация** - работа с браузерами, Selenium, Puppeteer  
✅ **Обработка данных** - анализ, ML, визуализация  
✅ **Мультимедиа** - музыка, видео, звук, речь  
✅ **Безопасность** - криптография, сетевые инструменты  
✅ **Системные операции** - процессы, файлы, сеть  
✅ **Специальные функции** - массовая автоматизация, мониторинг  

**ИИ агент становится невероятно мощным и функциональным!** 🚀

---

*Примеры созданы на основе анализа кода Open Interpreter v1.0* 