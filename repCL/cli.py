"""
Repin 2.0 (Colab Fork): Студия генеративного цифрового искусства
---------------------------------------------------
Облегченная версия для Google Colab.
Оптимизировано для обучения и быстрой генерации.

(c) 2026 Repin Project
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torchvision.utils as vutils
import os
import time
import sys
import argparse
from datetime import datetime

# --- RICH INTERFACE ---
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
    from rich.panel import Panel
    console = Console()
except ImportError:
    # Fallback for environments without rich
    class SimpleConsole:
        def print(self, *args, **kwargs): print(*args)
        def status(self, text, spinner=None):
            print(text)
            class Dummy:
                def __enter__(self): return self
                def __exit__(self, *args): pass
            return Dummy()
    console = SimpleConsole()

# --- 1. АППАРАТНАЯ НАСТРОЙКА ---
def get_device():
    if torch.cuda.is_available():
        # Оптимизации для CUDA (T4)
        torch.backends.cudnn.benchmark = True
        return torch.device("cuda"), "cuda"
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return torch.device("xpu"), "xpu"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps"), "mps"
    return torch.device("cpu"), "cpu"

device, device_type = get_device()
# На T4 Tensor Cores отлично работают с float16
dtype = torch.float16 if device_type == 'cuda' else (torch.bfloat16 if device_type == 'xpu' else torch.float32)

# --- 2. НАСТРОЙКИ ---
latent_size = 64
hidden_size = 256
image_size = 28 * 28
WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), 'weights', 'repin_weights.pth')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'generated_art')

# --- 3. АРХИТЕКТУРА ---
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size * 2),
            nn.ReLU(),
            nn.Linear(hidden_size * 2, image_size),
            nn.Tanh()
        )
    def forward(self, x):
        return self.net(x)

class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(image_size, hidden_size * 2),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_size * 2, hidden_size),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_size, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x)

# --- 4. ФУНКЦИИ ---

def train_model(num_epochs=500):
    batch_size = 128
    console.print(f"[cyan]Загрузка MNIST и начало обучения ({num_epochs} эпох) на {device}...[/cyan]")
    if device_type == 'cuda':
        console.print("[cyan]Активированы оптимизации для T4 (Mixed Precision, cuDNN Benchmark)...[/cyan]")
    
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])
    
    mnist = torchvision.datasets.MNIST(root='./data', train=True, transform=transform, download=True)
    # Используем pin_memory=True и num_workers для ускорения загрузки данных на GPU
    num_workers = 2 if device_type == 'cuda' else 0
    data_loader = torch.utils.data.DataLoader(
        dataset=mnist, 
        batch_size=batch_size, 
        shuffle=True, 
        drop_last=True,
        pin_memory=(device_type == 'cuda'),
        num_workers=num_workers
    )
    
    G = Generator().to(device)
    D = Discriminator().to(device)
    
    criterion = nn.BCELoss()
    d_optimizer = torch.optim.Adam(D.parameters(), lr=0.0002, betas=(0.5, 0.999))
    g_optimizer = torch.optim.Adam(G.parameters(), lr=0.0002, betas=(0.5, 0.999))
    
    # Инициализация GradScaler для Mixed Precision Training (только для CUDA)
    scaler = torch.amp.GradScaler('cuda') if device_type == 'cuda' else None
    
    # Simple progress tracking
    start_time = time.time()
    for epoch in range(num_epochs):
        for i, (images, _) in enumerate(data_loader):
            # non_blocking=True ускоряет перенос данных на GPU
            images = images.view(batch_size, -1).to(device, non_blocking=True)
            real_labels = torch.ones(batch_size, 1, device=device)
            fake_labels = torch.zeros(batch_size, 1, device=device)
            
            # --- Train Discriminator ---
            d_optimizer.zero_grad()
            if device_type == 'cuda':
                with torch.amp.autocast('cuda', dtype=dtype):
                    outputs = D(images)
                    d_loss_real = criterion(outputs, real_labels)
                    z = torch.randn(batch_size, latent_size, device=device)
                    fake_images = G(z)
                    outputs = D(fake_images.detach())
                    d_loss_fake = criterion(outputs, fake_labels)
                    d_loss = d_loss_real + d_loss_fake
                
                scaler.scale(d_loss).backward()
                scaler.step(d_optimizer)
            else:
                outputs = D(images)
                d_loss_real = criterion(outputs, real_labels)
                z = torch.randn(batch_size, latent_size, device=device)
                fake_images = G(z)
                outputs = D(fake_images.detach())
                d_loss_fake = criterion(outputs, fake_labels)
                d_loss = d_loss_real + d_loss_fake
                d_loss.backward()
                d_optimizer.step()
            
            # --- Train Generator ---
            g_optimizer.zero_grad()
            if device_type == 'cuda':
                with torch.amp.autocast('cuda', dtype=dtype):
                    z = torch.randn(batch_size, latent_size, device=device)
                    fake_images = G(z)
                    outputs = D(fake_images)
                    g_loss = criterion(outputs, real_labels)
                
                scaler.scale(g_loss).backward()
                scaler.step(g_optimizer)
                scaler.update()
            else:
                z = torch.randn(batch_size, latent_size, device=device)
                fake_images = G(z)
                outputs = D(fake_images)
                g_loss = criterion(outputs, real_labels)
                g_loss.backward()
                g_optimizer.step()
            
        if (epoch + 1) % 10 == 0:
            elapsed = time.time() - start_time
            console.print(f"Epoch [{epoch+1}/{num_epochs}] | Time: {elapsed:.1f}s | d_loss: {d_loss.item():.4f} | g_loss: {g_loss.item():.4f}")
            start_time = time.time()
            
    os.makedirs(os.path.dirname(WEIGHTS_PATH), exist_ok=True)
    torch.save(G.state_dict(), WEIGHTS_PATH)
    console.print(f"[bold green]Обучение завершено! Веса: {WEIGHTS_PATH}[/bold green]")

def generate_images(batch_size=16):
    if not os.path.exists(WEIGHTS_PATH):
        console.print("[bold red]Ошибка: Веса не найдены![/bold red]")
        return
        
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    G = Generator().to(device)
    G.load_state_dict(torch.load(WEIGHTS_PATH, map_location=device, weights_only=True))
    G.eval()
    
    with torch.no_grad():
        z = torch.randn(batch_size, latent_size, device=device)
        generated = G(z).view(-1, 1, 28, 28).cpu()
        generated = (generated + 1) / 2.0
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(OUTPUT_DIR, f"colab_gen_{timestamp}.png")
    vutils.save_image(generated, filename, nrow=4, normalize=False)
    console.print(f"[bold green]Готово! Сохранено в {filename}[/bold green]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Repin Colab Simple CLI")
    parser.add_argument("--train", action="store_true", help="Запустить обучение")
    parser.add_argument("--gen", action="store_true", help="Запустить генерацию")
    parser.add_argument("--epochs", type=int, default=500, help="Количество эпох (default: 500)")
    parser.add_argument("--batch", type=int, default=16, help="Размер батча для генерации")
    
    args = parser.parse_args()
    
    if args.train:
        train_model(args.epochs)
    elif args.gen:
        generate_images(args.batch)
    else:
        # Default behavior if no args: train then gen
        console.print("[yellow]Аргументы не указаны. Запуск режима по умолчанию: обучение + генерация.[/yellow]")
        train_model(args.epochs)
        generate_images(args.batch)
