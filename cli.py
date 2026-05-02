"""
Repin 2.0: Generative Digital Art Studio
----------------------------------------
A professional GAN-based MNIST generation tool with a high-fidelity CLI interface.
Optimized for PyTorch 2.0+ and Intel XPU.

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
from datetime import datetime

# --- ФИКС КОДИРОВКИ ДЛЯ WINDOWS ---
if sys.platform == "win32":
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- ИМПОРТЫ ДЛЯ КРАСИВОГО ИНТЕРФЕЙСА (RICH) ---
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.table import Table
from rich import print as rprint
from rich.align import Align
from rich import box

console = Console()

# --- 1. АППАРАТНАЯ НАСТРОЙКА (Multi-Platform Support) ---
def get_device():
    if hasattr(torch, "xpu") and torch.xpu.is_available():
        return torch.device("xpu"), "xpu"
    if torch.cuda.is_available():
        return torch.device("cuda"), "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps"), "mps"
    
    # Оптимизация для CPU
    torch.set_num_threads(os.cpu_count() or 4)
    return torch.device("cpu"), "cpu"

device, device_type = get_device()

# Настройка bfloat16 (поддерживается на XPU, CUDA >= Ampere, и частично на CPU)
# Для MPS и старых CUDA будем использовать float16 или float32
def get_autocast_dtype(d_type):
    if d_type in ['xpu', 'cuda', 'cpu']:
        return torch.bfloat16
    return torch.float16

dtype = get_autocast_dtype(device_type)

# --- 2. НАСТРОЙКИ МОДЕЛИ ---
latent_size = 64
hidden_size = 256
image_size = 28 * 28
WEIGHTS_PATH = 'weights/repin_weights.pth'
OUTPUT_DIR = 'generated_art'

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

# --- 4. ФУНКЦИИ ИНТЕРФЕЙСА ---

def print_header():
    console.clear()
    
    # Классический блочный ASCII-арт в цветах триколора
    header_text = r"""
[bold white]██████╗ ███████╗██████╗ ██╗███╗   ██╗[/bold white]
[bold white]██╔══██╗██╔════╝██╔══██╗██║████╗  ██║[/bold white]
[bold blue]██████╔╝█████╗  ██████╔╝██║██╔██╗ ██║[/bold blue]
[bold blue]██╔══██╗██╔══╝  ██╔═══╝ ██║██║╚██╗██║[/bold blue]
[bold red]██║  ██║███████╗██║     ██║██║ ╚████║[/bold red]
[bold red]╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝[/bold red]
"""
    
    # Статусная строка
    status_table = Table(show_header=False, box=None, padding=(0, 1))
    status_table.add_row(
        f"[bold magenta]Device:[/bold magenta] [cyan]{str(device).upper()}[/cyan]",
        f"[bold magenta]Precision:[/bold magenta] [cyan]{str(dtype).split('.')[-1].upper()}[/cyan]",
        f"[bold magenta]Version:[/bold magenta] [white]v2.1[/white]"
    )

    panel = Panel(
        Group(
            Align.center(header_text.strip()),
            Align.center(status_table)
        ),
        border_style="bright_blue",
        padding=(0, 1),
        title="[bold yellow]System Status[/bold yellow]"
    )
    console.print(panel)
    console.print()

def train_model(num_epochs):
    batch_size = 128
    
    console.print("[cyan]Подготовка датасета MNIST...[/cyan]")
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])
    
    mnist = torchvision.datasets.MNIST(root='./data', train=True, transform=transform, download=True)
    data_loader = torch.utils.data.DataLoader(
        dataset=mnist, batch_size=batch_size, shuffle=True, drop_last=True,
        pin_memory=(device_type in ['cuda', 'xpu']), num_workers=0
    )
    
    G = Generator().to(device)
    D = Discriminator().to(device)
    
    criterion = nn.BCELoss()
    d_optimizer = torch.optim.AdamW(D.parameters(), lr=0.0002, betas=(0.5, 0.999), weight_decay=1e-4)
    g_optimizer = torch.optim.AdamW(G.parameters(), lr=0.0002, betas=(0.5, 0.999), weight_decay=1e-4)
    
    total_steps = len(data_loader)
    
    console.print(f"[bold green]Начинаем обучение на {num_epochs} эпох...[/bold green]\n")
    
    # Красивый и компактный прогресс бар
    with Progress(
        SpinnerColumn(spinner_name="dots"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40, pulse_style="bright_blue"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=True # Убирает бар после завершения для компактности
    ) as progress:
        
        task_epoch = progress.add_task("[bold blue]Эпохи...", total=num_epochs)
        task_batch = progress.add_task("[bold yellow]Батчи...", total=total_steps)
        
        for epoch in range(num_epochs):
            progress.reset(task_batch)
            for i, (images, _) in enumerate(data_loader):
                current_batch_size = images.size(0)
                images = images.view(current_batch_size, -1).to(device, non_blocking=True)
                
                real_labels = torch.ones(current_batch_size, 1).to(device)
                fake_labels = torch.zeros(current_batch_size, 1).to(device)
                
                # --- Discriminator ---
                with torch.autocast(device_type=device_type, dtype=dtype):
                    outputs = D(images)
                    d_loss_real = criterion(outputs, real_labels)
                    
                    z = torch.randn(current_batch_size, latent_size).to(device)
                    fake_images = G(z)
                    outputs = D(fake_images.detach())
                    d_loss_fake = criterion(outputs, fake_labels)
                    
                    d_loss = d_loss_real + d_loss_fake
                
                d_optimizer.zero_grad(set_to_none=True)
                d_loss.backward()
                d_optimizer.step()
                
                # --- Generator ---
                with torch.autocast(device_type=device_type, dtype=dtype):
                    z = torch.randn(current_batch_size, latent_size).to(device)
                    fake_images = G(z)
                    outputs = D(fake_images)
                    g_loss = criterion(outputs, real_labels)
                
                g_optimizer.zero_grad(set_to_none=True)
                g_loss.backward()
                g_optimizer.step()
                
                # Обновляем прогресс батчей
                progress.update(
                    task_batch, 
                    advance=1, 
                    description=f"[bold yellow]Батчи (D_Loss: {d_loss.item():.2f}, G_Loss: {g_loss.item():.2f})"
                )
            
            # Обновляем прогресс эпох
            progress.update(task_epoch, advance=1)
            
    # Сохранение весов
    torch.save(G.state_dict(), WEIGHTS_PATH)
    console.print(f"\n[bold green]✅ Обучение завершено! Веса сохранены в {WEIGHTS_PATH}[/bold green]")
    input("\nНажмите Enter, чтобы вернуться в меню...")

def generate_images(batch_size):
    if not os.path.exists(WEIGHTS_PATH):
        console.print(f"[bold red]❌ Ошибка: Файл весов '{WEIGHTS_PATH}' не найден. Сначала обучите модель![/bold red]")
        input("\nНажмите Enter, чтобы вернуться в меню...")
        return
        
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    G = Generator().to(device)
    G.load_state_dict(torch.load(WEIGHTS_PATH, map_location=device, weights_only=True))
    G.eval()
    
    with console.status(f"[bold cyan]Генерация батча из {batch_size} изображений...", spinner="aesthetic"):
        z = torch.randn(batch_size, latent_size).to(device)
        
        with torch.no_grad(), torch.autocast(device_type=device_type, dtype=dtype):
            generated_flat = G(z)
            
        # Восстанавливаем форму изображений (B, C, H, W)
        generated_images = generated_flat.view(-1, 1, 28, 28).cpu()
        
        # Денормализация из [-1, 1] в [0, 1]
        generated_images = (generated_images + 1) / 2.0
        
        # Увеличиваем масштаб в 8 раз (с 28x28 до 224x224) без размытия
        generated_images = F.interpolate(generated_images, scale_factor=8, mode='nearest')
        
        # Вычисляем сколько колонок сделать в сетке
        nrow = int(batch_size ** 0.5) if batch_size > 1 else 1
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{OUTPUT_DIR}/repin_batch_{batch_size}_{timestamp}.png"
        
        vutils.save_image(generated_images, filename, nrow=nrow, padding=2, normalize=False)
        time.sleep(0.5) # Небольшая пауза для визуального эффекта
        
    console.print(f"[bold green]✨ Успех! Сгенерировано {batch_size} изображений.[/bold green]")
    console.print(f"📁 Файл сохранен: [bold yellow]{filename}[/bold yellow]")
    input("\nНажмите Enter, чтобы вернуться в меню...")

# --- 5. DEBUG & BENCHMARK MENU ---

def inspect_model():
    table_params = Table(title="[bold yellow]Гиперпараметры модели[/bold yellow]", border_style="cyan", box=box.ROUNDED)
    table_params.add_column("Параметр", style="magenta")
    table_params.add_column("Значение", style="white")
    
    table_params.add_row("Latent Vector (Размер шума)", str(latent_size))
    table_params.add_row("Hidden Units (Скрытые слои)", str(hidden_size))
    table_params.add_row("Image Resolution (Выход)", f"{int(image_size**0.5)}x{int(image_size**0.5)}")
    table_params.add_row("Device (Устройство)", str(device).upper())
    
    G = Generator().to(device)
    total_params = sum(p.numel() for p in G.parameters())
    
    console.print(table_params)
    console.print(f"\n[bold green]Общее количество параметров модели:[/bold green] [white]{total_params:,}[/white]")
    input("\nНажмите Enter, чтобы вернуться...")

def benchmark_batches():
    batch_size = IntPrompt.ask("[bold cyan]Выберите размер батча[/bold cyan]", choices=["2", "3", "16", "32", "64"], default=32)
    num_iters = IntPrompt.ask("[bold cyan]Введите количество батчей для теста[/bold cyan]", default=100)
    
    G = Generator().to(device)
    G.eval()
    z = torch.randn(batch_size, latent_size).to(device)
    
    console.print(f"\n[yellow]Запуск бенчмарка (Device: {device_type.upper()}, Batch: {batch_size}, Iters: {num_iters})...[/yellow]")
    
    # Warm-up
    with torch.no_grad(), torch.autocast(device_type=device_type, dtype=dtype):
        for _ in range(5):
            _ = G(z)
    
    if device_type == 'cuda': torch.cuda.synchronize()
    elif device_type == 'xpu': torch.xpu.synchronize()
    
    start_time = time.time()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("[cyan]Тестирование...", total=num_iters)
        
        with torch.no_grad(), torch.autocast(device_type=device_type, dtype=dtype):
            for _ in range(num_iters):
                _ = G(z)
                progress.update(task, advance=1)
                
    if device_type == 'cuda': torch.cuda.synchronize()
    elif device_type == 'xpu': torch.xpu.synchronize()
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_latency = (total_time / num_iters) * 1000
    samples_per_sec = (batch_size * num_iters) / total_time
    
    res_table = Table(title="[bold green]Результаты замера скорости[/bold green]", border_style="bright_blue", box=box.ROUNDED)
    res_table.add_column("Метрика", style="cyan")
    res_table.add_column("Значение", style="bold white")
    
    res_table.add_row("Общее время", f"{total_time:.4f} сек")
    res_table.add_row("Средняя задержка (Latency)", f"{avg_latency:.2f} мс/батч")
    res_table.add_row("Пропускная способность", f"{samples_per_sec:.2f} изобр./сек")
    
    console.print(res_table)
    input("\nНажмите Enter, чтобы вернуться...")

def debug_menu():
    while True:
        print_header()
        table = Table(
            title="[bold red]ВНУТРЕННЕЕ DEBUG МЕНЮ[/bold red]", 
            border_style="red", 
            box=box.ROUNDED,
            width=45,
            show_header=True,
            header_style="bold white"
        )
        table.add_column("ID", justify="center", style="bold white", width=4)
        table.add_column("Инструмент", style="red")
        
        table.add_row("1", "Инспекция конфигурации")
        table.add_row("2", "Замер скорости (Benchmark)")
        table.add_row("0", "Назад в главное меню")
        
        console.print(Align.center(table))
        choice = Prompt.ask("\n[bold red]DEBUG>>>[/bold red]", choices=["1", "2", "0"], default="0")
        
        if choice == "1": inspect_model()
        elif choice == "2": benchmark_batches()
        elif choice == "0": break

# --- 6. СПРАВКА ---
    print_header()
    table = Table(title="Справка по Repin 2.0 CLI", show_header=True, header_style="bold magenta")
    table.add_column("Команда", style="cyan")
    table.add_column("Описание", style="green")
    
    table.add_row("--help", "Показать это сообщение")
    table.add_row("Поддержка", "CUDA, XPU (Intel), MPS (Apple Silicon), CPU")
    table.add_row("Меню [1]", "Режим обучения GAN модели на MNIST")
    table.add_row("Меню [2]", "Генерация новых арт-объектов на основе обученных весов")
    table.add_row("Меню [3]", "Debug Menu: Инспекция и Бенчмарки")
    table.add_row("Меню [0]", "Выход из приложения")
    
    console.print(table)
    console.print("\n[dim]Для запуска в интерактивном режиме просто выполните: python cli.py[/dim]")

# --- 5. ГЛАВНЫЙ ЦИКЛ ПРОГРАММЫ ---
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_help()
        return

    while True:
        print_header()
        
        table = Table(
            show_header=True, 
            header_style="bold magenta", 
            box=box.ROUNDED,
            expand=False,
            border_style="bright_blue",
            width=45
        )
        
        table.add_column("ID", justify="center", style="bold green", width=4)
        table.add_column("Действие", style="cyan")
        
        table.add_row("1", "Обучить модель (Train)")
        table.add_row("2", "Сгенерировать арт (Gen)")
        table.add_row("3", "Debug Menu (Dev)")
        table.add_row("0", "Выход (Exit)")
        
        console.print(Align.center(table))
        console.print()
        
        choice = Prompt.ask("[bold yellow]>>> Выберите действие[/bold yellow]", choices=["1", "2", "3", "0"], default="2")
        
        if choice == "1":
            epochs = IntPrompt.ask("[bold cyan]Введите количество эпох для обучения[/bold cyan]", default=50)
            train_model(epochs)
            
        elif choice == "2":
            size = IntPrompt.ask("[bold cyan]Размер батча (кол-во картинок)[/bold cyan]", choices=["1", "16", "32", "64"], default=16)
            generate_images(size)
        
        elif choice == "3":
            debug_menu()
            
        elif choice == "0":
            console.print("[bold magenta]До встречи! Художник Репин ушел отдыхать.[/bold magenta]")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Программа прервана пользователем.[/bold red]")