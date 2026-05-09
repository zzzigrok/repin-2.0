# 🔌 Интеграция со сторонними проектами

> [!NOTE]
> Хотя Repin 2.0 поставляется как самостоятельное CLI-приложение, его базовая архитектура (чистый PyTorch) позволяет легко извлечь нейронные сети и использовать их в ваших собственных проектах: ботах, веб-сервисах или других пайплайнах.

## 📋 Оглавление
1. [Извлечение модели](#-извлечение-модели)
2. [Пример: Telegram-бот](#-пример-telegram-бот)
3. [Пример: FastAPI сервер](#-пример-fastapi-сервер)

---

## 📦 Извлечение модели

Чтобы использовать модель вне `cli.py`, вам нужно скопировать класс `Generator` и загрузить сохраненные веса (`repin_weights.pth`).

```python
import torch
import torch.nn as nn
from PIL import Image
import torchvision.transforms as transforms

# 1. Копируем архитектуру (из cli.py)
class Generator(nn.Module):
    def __init__(self, latent_size, hidden_size, image_size):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.Linear(latent_size, hidden_size),
            nn.ReLU(True),
            nn.Linear(hidden_size, hidden_size * 2),
            nn.ReLU(True),
            nn.Linear(hidden_size * 2, image_size),
            nn.Tanh()
        )

    def forward(self, x):
        return self.main(x)

# 2. Инициализация и загрузка весов
device = torch.device('cpu') # или 'cuda', 'xpu'
generator = Generator(latent_size=64, hidden_size=256, image_size=784).to(device)

try:
    generator.load_state_dict(torch.load('repin_weights.pth', map_location=device))
    generator.eval()
except FileNotFoundError:
    print("Ошибка: Сначала нужно обучить модель в cli.py!")

# 3. Функция генерации одной картинки
def generate_single_image() -> Image:
    with torch.no_grad():
        z = torch.randn(1, 64).to(device)
        fake_images = generator(z)
        fake_images = fake_images.view(fake_images.size(0), 1, 28, 28)

        # Денормализация [-1, 1] -> [0, 1]
        fake_images = (fake_images + 1) / 2.0

        # Конвертация в PIL Image
        img_tensor = fake_images[0].squeeze().cpu()
        img_pil = transforms.ToPILImage()(img_tensor)

        # Апскейл (Nearest Neighbor)
        img_pil = img_pil.resize((224, 224), Image.Resampling.NEAREST)
        return img_pil
```

---

## 🤖 Пример: Telegram-бот (aiogram 3.x)

С помощью кода выше вы можете легко создать бота, который генерирует арт по команде.

```python
import asyncio
import io
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile

# Предварительно вставьте сюда код инициализации Generator и generate_single_image() из раздела выше

TOKEN = "ВАШ_ТОКЕН_БОТА"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("art"))
async def send_art(message: types.Message):
    await message.answer("Генерирую шедевр... 🎨")

    # Генерируем картинку
    img = generate_single_image()

    # Сохраняем в буфер памяти (не на диск)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    # Отправляем пользователю
    photo = BufferedInputFile(buf.read(), filename="repin_art.png")
    await message.reply_photo(photo=photo, caption="Ваш уникальный ИИ-арт от Repin 2.0!")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
```

---

## 🌐 Пример: FastAPI сервер

Если вы хотите интегрировать генератор в веб-приложение.

```python
from fastapi import FastAPI
from fastapi.responses import Response
import io

# Предварительно вставьте сюда код инициализации Generator и generate_single_image()

app = FastAPI(title="Repin 2.0 API")

@app.get("/generate", responses={200: {"content": {"image/png": {}}}})
async def generate_art_endpoint():
    """Возвращает одну сгенерированную картинку в формате PNG"""
    img = generate_single_image()

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    image_bytes = buf.getvalue()

    return Response(content=image_bytes, media_type="image/png")

# Запуск: uvicorn main:app --reload
```

---

## 🏗 Пример: Использование в Jupyter Notebook (Colab)
Многие исследователи предпочитают работать в Jupyter-средах. Вы можете легко импортировать модель и использовать ее для экспериментов с латентным пространством.

```python
# 1. Сначала клонируем репозиторий в Colab и переходим в папку
!git clone https://github.com/zzzigrok/repin-2.0.git
%cd repin-2.0

# 2. Обучаем модель прямо из терминала Colab (или загружаем свои веса)
!python cli.py # (потребуется модифицировать скрипт для неинтерактивного режима)
# ИЛИ загрузите 'repin_weights.pth' в корень папки руками.

# 3. В следующей ячейке:
import torch
import matplotlib.pyplot as plt
from cli import Generator, latent_size

# Инициализируем генератор
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
G = Generator(latent_size=latent_size, hidden_size=256, image_size=784).to(device)
G.load_state_dict(torch.load('repin_weights.pth', map_location=device))
G.eval()

# Генерируем 10 картинок
z = torch.randn(10, latent_size).to(device)
with torch.no_grad():
    images = G(z).view(-1, 28, 28).cpu().numpy()

# Визуализация
fig, axes = plt.subplots(1, 10, figsize=(15, 3))
for i, ax in enumerate(axes):
    ax.imshow(images[i], cmap='gray')
    ax.axis('off')
plt.show()
```

<p align="center">
  <a href="INDEX.md">← Назад: Главная</a><br/>
  <sub>Repin 2.0 • Integration Guide • 2026</sub>
</p>
