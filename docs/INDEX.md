# 🎨 Repin 2.0: Генеративное Искусство на базе GAN
<p align="center">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 350" width="100%" height="100%">
      <defs>
          <linearGradient id="r-grad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#00e5ff" />
              <stop offset="50%" stop-color="#0055ff" />
              <stop offset="100%" stop-color="#ff00ff" />
          </linearGradient>
          <linearGradient id="text-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#ffffff" />
              <stop offset="100%" stop-color="#b8c6e5" />
          </linearGradient>
          <linearGradient id="line-grad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ff00ff" stop-opacity="0.8"/>
              <stop offset="50%" stop-color="#00e5ff" stop-opacity="0.5"/>
              <stop offset="100%" stop-color="#00ff88" stop-opacity="0.1"/>
          </linearGradient>
          <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="6" result="blur" />
              <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
              </feMerge>
          </filter>
          <filter id="glow-subtle" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
              </feMerge>
          </filter>
          <style>
              @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap');
              @keyframes pulse-opacity {
                  0%, 100% { fill-opacity: 0.1; transform: scale(0.9); }
                  50% { fill-opacity: 0.8; transform: scale(1.05); }
              }
              @keyframes flow {
                  to { stroke-dashoffset: -40; }
              }
              @keyframes float {
                  0%, 100% { transform: translateY(0px); }
                  50% { transform: translateY(-8px); }
              }
              @keyframes flicker {
                  0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% { opacity: 1; text-shadow: 0 0 10px #00ff88, 0 0 20px #00ff88; }
                  20%, 24%, 55% { opacity: 0.5; text-shadow: none; }
              }
              .anim-float { animation: float 6s ease-in-out infinite; }
              .data-flow { stroke-dasharray: 6 12; animation: flow 1s linear infinite; }
              .data-flow-slow { stroke-dasharray: 4 15; animation: flow 2s linear infinite reverse; }
              .noise-pixel { transform-origin: center; transform-box: fill-box; animation: pulse-opacity 2s ease-in-out infinite; }
              .version-text { animation: flicker 7s infinite; }
              .font-title { font-family: 'Space Grotesk', sans-serif; font-weight: 700; }
              .font-mono { font-family: 'JetBrains Mono', monospace; }
          </style>
      </defs>
      <g opacity="0.4" class="anim-float">
          <path d="M 50 175 Q 150 50 350 175 T 850 175" fill="none" stroke="#2a2d3e" stroke-width="1" />
          <path d="M 50 175 Q 150 300 350 175 T 850 175" fill="none" stroke="#2a2d3e" stroke-width="1" />
          <circle cx="150" cy="112" r="2" fill="#4a5070" />
          <circle cx="250" cy="112" r="2" fill="#4a5070" />
          <circle cx="150" cy="238" r="2" fill="#4a5070" />
          <circle cx="250" cy="238" r="2" fill="#4a5070" />
      </g>
      <g class="anim-float">
          <g opacity="0.7">
              <path d="M 280 120 L 360 120" fill="none" stroke="url(#line-grad)" stroke-width="3" class="data-flow" />
              <path d="M 280 180 L 360 180" fill="none" stroke="url(#line-grad)" stroke-width="2" class="data-flow" style="animation-duration: 1.5s;" />
              <path d="M 280 240 L 360 240" fill="none" stroke="url(#line-grad)" stroke-width="1.5" class="data-flow-slow" />
          </g>
          <g transform="translate(100, 75)" fill="url(#r-grad)" filter="url(#glow)">
              <rect x="-24" y="24" width="20" height="20" rx="4" class="noise-pixel" style="animation-delay: 0.1s;" />
              <rect x="-48" y="96" width="20" height="20" rx="4" class="noise-pixel" style="animation-delay: 0.5s;" />
              <rect x="144" y="0" width="20" height="20" rx="4" class="noise-pixel" style="animation-delay: 0.3s;" />
              <rect x="120" y="168" width="20" height="20" rx="4" class="noise-pixel" style="animation-delay: 0.7s;" />
              <rect x="48" y="192" width="20" height="20" rx="4" class="noise-pixel" style="animation-delay: 0.2s;" />
              <rect x="0" y="0" width="20" height="20" rx="4" />
              <rect x="24" y="0" width="20" height="20" rx="4" />
              <rect x="48" y="0" width="20" height="20" rx="4" />
              <rect x="72" y="0" width="20" height="20" rx="4" />
              <rect x="96" y="0" width="20" height="20" rx="4" />
              <rect x="0" y="24" width="20" height="20" rx="4" />
              <rect x="120" y="24" width="20" height="20" rx="4" />
              <rect x="0" y="48" width="20" height="20" rx="4" />
              <rect x="120" y="48" width="20" height="20" rx="4" />
              <rect x="0" y="72" width="20" height="20" rx="4" />
              <rect x="24" y="72" width="20" height="20" rx="4" />
              <rect x="48" y="72" width="20" height="20" rx="4" />
              <rect x="72" y="72" width="20" height="20" rx="4" />
              <rect x="96" y="72" width="20" height="20" rx="4" />
              <rect x="0" y="96" width="20" height="20" rx="4" />
              <rect x="72" y="96" width="20" height="20" rx="4" />
              <rect x="0" y="120" width="20" height="20" rx="4" />
              <rect x="96" y="120" width="20" height="20" rx="4" />
              <rect x="0" y="144" width="20" height="20" rx="4" />
              <rect x="120" y="144" width="20" height="20" rx="4" />
              <rect x="0" y="168" width="20" height="20" rx="4" />
              <rect x="120" y="168" width="20" height="20" rx="4" />
          </g>
          <g transform="translate(380, 160)">
              <text x="0" y="0" class="font-title" font-size="88" fill="url(#text-grad)" letter-spacing="6">REPIN</text>
              <text x="325" y="0" class="font-title version-text" font-size="88" fill="#00ff88" filter="url(#glow-subtle)">2.0</text>
              <text x="5" y="45" class="font-mono" font-size="20" fill="#6a7894" letter-spacing="4" font-weight="700">GENERATIVE DIGITAL ART STUDIO</text>
          </g>
          <g transform="translate(385, 240)" class="font-mono" font-size="12" font-weight="700">
              <rect x="0" y="0" width="90" height="28" rx="6" fill="#151320" stroke="#ff0055" stroke-width="1.5" />
              <text x="45" y="18" fill="#ff0055" text-anchor="middle" filter="url(#glow-subtle)">NOISE (z)</text>
              <path d="M 96 14 L 124 14" fill="none" stroke="#4a5070" stroke-width="1.5" class="data-flow" />
              <rect x="130" y="0" width="110" height="28" rx="6" fill="#101820" stroke="#00e5ff" stroke-width="1.5" />
              <text x="185" y="18" fill="#00e5ff" text-anchor="middle" filter="url(#glow-subtle)">GENERATOR (G)</text>
              <path d="M 246 14 L 274 14" fill="none" stroke="#4a5070" stroke-width="1.5" class="data-flow" />
              <rect x="280" y="0" width="90" height="28" rx="6" fill="#101a15" stroke="#00ff88" stroke-width="1.5" />
              <text x="325" y="18" fill="#00ff88" text-anchor="middle" filter="url(#glow-subtle)">ART (224x)</text>
          </g>
      </g>
  </svg>
</p>


> [!TIP]
> **Repin 2.0** — это открытая исследовательская платформа на базе Генеративно-состязательных сетей (GAN), созданная для студентов и начинающих специалистов в области Machine Learning. Наша цель — сделать изучение Deep Learning увлекательным, прозрачным и доступным через практическую работу с датасетом MNIST.

## 📋 Полное оглавление

### Основная документация
1. [🧠 Архитектура системы](architecture.md) — глубокое погружение в нейронные сети, математику потерь и потоки данных.
2. [⚙️ Руководство по использованию](usage.md) — как работать с CLI-интерфейсом и его возможностями.
3. [📡 Справочник API](api_reference.md) — детальное описание всех классов, функций и параметров.
4. [🔧 Решение проблем](troubleshooting.md) — диагностика и устранение неполадок.

### Туториалы
5. [🎓 Список туториалов](tutorials/README.md) — пошаговые инструкции для быстрого старта.
6. [🚀 Быстрый старт](tutorials/getting_started.md) — первая генерация за минуту.
7. [🏋️ Обучение с нуля](tutorials/training.md) — полный цикл обучения GAN.
8. [🎛 Гиперпараметры](tutorials/hyperparameters.md) — настройка обучения для достижения лучших результатов.
9. [🖼 Руководство по генерации](tutorials/generation_guide.md) — продвинутые техники генерации арта.

### Для разработчиков
10. [📝 История изменений](CHANGELOG.md) — все версии и релизы проекта.
11. [🤝 Руководство контрибьютора](CONTRIBUTING.md) — как внести вклад в проект.
12. [❓ FAQ](faq.md) — часто задаваемые вопросы.
13. [🌟 Лучшие практики](best_practices.md) — советы по настройке и использованию.
14. [🔌 Интеграция](integration.md) — примеры интеграции с ботами и API.
15. [📚 Глоссарий](#-глоссарий) — основные термины и понятия.

---

## 🔬 Исследовательская философия

Вместо закрытых систем мы предлагаем полностью прозрачный инструмент. **Repin 2.0** — это не просто генератор картинок, а учебное пособие, которое позволяет:
- **Разобраться в MLP**: Увидеть, как полносвязные слои преобразуют шум в осмысленные формы.
- **Освоить PyTorch**: Изучить современные практики написания тренировочных циклов и оптимизации моделей.
- **Протестировать железо**: Испробовать возможности ускорения вычислений на Intel XPU и других архитектурах.

Мы верим, что открытость кода и знаний — это кратчайший путь к инновациям в ИИ.

### Ключевые особенности

| Функция | Описание |
| :--- | :--- |
| **Open Source** | Полностью открытый исходный код с подробными комментариями. |
| **Intel XPU** | Автодетекция и использование `torch.xpu` для аппаратного ускорения на Intel GPU. |
| **bfloat16** | Обучение на современной смешанной точности для экономии ресурсов. |
| **Interactive CLI** | Инструментарий на базе `rich` для визуального контроля процесса обучения. |
| **Educational Docs** | Набор материалов, объясняющих "почему" и "как", а не только "что нажать". |

---

## 🛠 Быстрая установка

### Системные требования

| Компонент | Минимум | Рекомендуется |
| :--- | :--- | :--- |
| **Python** | 3.8+ | 3.10+ |
| **PyTorch** | 2.0 | 2.1+ |
| **ОЗУ** | 4 ГБ | 8 ГБ |
| **Диск** | 500 МБ (данные + веса) | 1 ГБ |
| **GPU** | — (CPU подходит) | Intel XPU (Arc/Flex) |

### Установка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/zzzigrok/repin-2.0.git
cd repin-2.0

# 2. (Рекомендуется) Создайте виртуальное окружение
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Установите зависимости
pip install torch torchvision rich
```

---

## 📂 Структура проекта

```
Repin 2.0/
├── cli.py                 # Логика нейросети и CLI интерфейс
├── README.md              # Краткое описание проекта
├── LICENSE                # Лицензия MIT
├── GEMINI.md              # Инструкции для ИИ-агентов
│
├── weights/               # Предобученные веса генератора
│   └── repin_weights.pth  # Файл весов (~2.1 МБ)
│
├── data/                  # Директория для датасета MNIST
│
├── generated_art/         # Результаты вашей генерации
│
├── web/                   # Исходный код сайта проекта
│
└── docs/                  # Техническая документация
    ├── INDEX.md           # ← Вы здесь
    ├── architecture.md    # Описание GAN
    ├── usage.md           # Работа с CLI
    └── tutorials/         # Пошаговые гайды
```

---

## 🔗 Схема навигации по документации

```mermaid
flowchart LR
    INDEX["📋 INDEX.md"]
    ARCH["🧠 Архитектура"]
    USAGE["⚙️ Использование"]
    API["📡 API"]
    TROUBLE["🔧 Проблемы"]
    TUTS["🎓 Туториалы"]
    GS["🚀 Быстрый старт"]
    TRAIN["🏋️ Обучение"]
    HYPER["🎛 Гиперпараметры"]
    GENGUIDE["🖼 Генерация"]
    CHANGE["📝 Changelog"]
    CONTRIB["🤝 Contributing"]
    FAQ["❓ FAQ"]
    BEST["🌟 Лучшие практики"]
    INTEG["🔌 Интеграция"]

    INDEX --> ARCH
    INDEX --> USAGE
    INDEX --> API
    INDEX --> TROUBLE
    INDEX --> TUTS
    TUTS --> GS
    TUTS --> TRAIN
    TUTS --> HYPER
    TUTS --> GENGUIDE
    INDEX --> CHANGE
    INDEX --> CONTRIB
    INDEX --> FAQ
    INDEX --> BEST
    INDEX --> INTEG

    style INDEX fill:#1a1a2e,stroke:#00e5ff,color:#fff
    style TUTS fill:#1a2e1a,stroke:#00ff88,color:#fff
    style ARCH fill:#2e1a2e,stroke:#ff88ff,color:#fff
```

---

## 🧠 Глоссарий

| Термин | Описание |
| :--- | :--- |
| **GAN** | Generative Adversarial Network — архитектура из двух конкурирующих нейросетей. |
| **Generator** | Нейросеть, создающая новые данные из случайного шума. |
| **Discriminator** | Нейросеть-«критик», обучающаяся отличать реальные данные от сгенерированных. |
| **MNIST** | Классическая база данных 70 000 рукописных цифр (28×28 пикселей). |
| **Latent Vector** | Вектор скрытого пространства (шум), из которого Генератор создает изображение. |
| **Latent Space** | Многомерное пространство, из которого Генератор сэмплирует входные данные. |
| **Epoch** | Один полный проход по всему тренировочному датасету. |
| **Batch** | Подмножество данных, обрабатываемое за один шаг оптимизации. |
| **BCELoss** | Binary Cross-Entropy Loss — функция потерь для бинарной классификации. |
| **AdamW** | Продвинутый оптимизатор с decoupled weight decay регуляризацией. |
| **bfloat16** | Brain Floating Point — 16-битный формат, оптимизированный для глубокого обучения. |
| **Upscaling** | Увеличение разрешения изображения (28×28 → 224×224). |
| **Nearest Neighbor** | Метод интерполяции, сохраняющий резкость пикселей при увеличении. |
| **MLP** | Multi-Layer Perceptron — полносвязная нейронная сеть прямого распространения. |
| **XPU** | Универсальный ускоритель Intel для вычислений на GPU. |
| **Weight Decay** | Техника регуляризации, предотвращающая переобучение модели. |

---

## 🗺 Roadmap

| Версия | Статус | Описание |
| :--- | :--- | :--- |
| **1.0** | ✅ Завершена | Базовый GAN + CLI интерфейс |
| **2.0** | ✅ Текущая | Art Upscaling, bfloat16, Intel XPU, Rich CLI |
| **2.1** | 🔜 Планируется | Conditional GAN (генерация конкретной цифры), сохранение промежуточных чекпоинтов |
| **3.0** | 💡 Идея | Convolutional GAN (DCGAN), генерация в высоком разрешении |

<p align="center">
  <a href="architecture.md">Далее: Архитектура системы →</a><br/>
  <sub>Repin 2.0 • Documentation • 2026</sub>
</p>
