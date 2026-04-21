# 🎬 Video Downloader Bot

Telegram бот для скачивания видео и аудио с YouTube, TikTok, Instagram и сотен других платформ.

## ✨ Возможности

- 📥 Скачивание видео в выбранном качестве (144p, 360p, 720p, 1080p, 1440p, 2160p)
- 🔊 Скачивание только аудио с обложкой и метаданными
- ⚡ Асинхронная обработка — бот не зависает во время скачивания
- 👥 Поддержка нескольких пользователей одновременно
- 🌐 Поддержка сотен платформ через yt-dlp

## 🛠 Технологии

- [aiogram 3.x](https://docs.aiogram.dev/) — фреймворк для Telegram ботов
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — скачивание видео
- [ffmpeg](https://ffmpeg.org/) — обработка медиафайлов

## 🚀 Запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/ashamam/downloadVidsBot.git
cd downloadVidsBot
```

### 2. Установить зависимости
```bash
pip install -r requirements.txt
```

### 3. Установить ffmpeg
```bash
# Ubuntu/Debian
sudo apt install ffmpeg
```

### 4. Создать файл .env
```
TOKEN=ваш_токен_от_BotFather
```

### 5. Создать папку для файлов
```bash
mkdir files
```

### 6. Запустить бота
```bash
python main.py
```

## 📖 Использование

1. Отправь боту ссылку на видео
2. Выбери качество или нажми 🔊 Audio
3. Получи файл!
