# 🎨 Repin 2.0: Generative Digital Art Studio

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/pytorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Style](https://img.shields.io/badge/UI-Rich-magenta.svg)](https://github.com/Textualize/rich)
[![Website](https://img.shields.io/badge/Live-Demo-blueviolet.svg)](https://zzzigrok.github.io/repin-2.0/)

**Repin 2.0** — это профессиональная GAN-студия для создания цифрового искусства на базе архитектуры MNIST GAN. Проект сочетает в себе мощь PyTorch и эстетичный CLI-интерфейс, превращая генерацию нейросетевых изображений в творческий процесс.

### 🌐 [Посетите наш сайт-визитку](https://zzzigrok.github.io/repin-2.0/)

---

## 🖼 Галерея генераций
Здесь представлены примеры работы модели, сгенерированные через встроенный CLI:

| Batch 32 (Showcase) | Batch 64 (Showcase) |
|:---:|:---:|
| ![Batch 32](web/assets/gallery/showcase_32.png) | ![Batch 64](web/assets/gallery/showcase_64.png) |

---

## 🚀 Основные возможности
- **Интуитивный CLI**: Полноценное интерактивное меню на базе библиотеки `rich`.
- **Высокая производительность**: Оптимизировано для `torch.xpu` (Intel GPU) и поддерживает `bfloat16`.
- **Debug Menu**: Встроенные инструменты для бенчмаркинга и инспекции архитектуры модели.
- **Масштабирование**: Автоматическое увеличение сгенерированных изображений в 8 раз (до 224x224) без потери четкости.

## 📖 Документация
Мы подготовили исчерпывающие руководства для пользователей и разработчиков:

- [🚀 **Быстрый старт**](docs/tutorials/getting_started.md) — создайте свой первый арт за минуту.
- [🧠 **Архитектура**](docs/architecture.md) — технические подробности устройства GAN.
- [⚙️ **Использование CLI**](docs/usage.md) — подробное описание команд и флагов.
- [🛠 **Устранение неполадок**](docs/troubleshooting.md) — если что-то пошло не так.
- [🎓 **Полное оглавление**](docs/INDEX.md) — навигация по всей базе знаний.

## 🛠 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/zzzigrok/repin-2.0.git
cd repin-2.0
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Запуск
```bash
# Запуск интерактивного меню
python cli.py
```

## 📁 Структура проекта
- `cli.py` — единый файл приложения (логика + интерфейс).
- `docs/` — техническая документация, туториалы и ассеты.
- `weights/` — директория с весами модели.
- `generated_art/` — галерея ваших работ.
- `web/` — исходный код сайта-визитки.

## 🤝 Участие в разработке
Мы приветствуем вклад в развитие проекта! См. [CONTRIBUTING.md](docs/CONTRIBUTING.md) для получения подробностей.

---
<sub>Разработано в рамках TAS Beta. Repin Project • 2026</sub>

