document.addEventListener('DOMContentLoaded', () => {
    // Reveal animations on scroll
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                
                // If it's a terminal line, we might want to trigger something else later
                if (entry.target.classList.contains('line')) {
                    entry.target.style.opacity = '1';
                }
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal').forEach(el => {
        observer.observe(el);
    });

    // Terminal typing animation simulation
    const terminalLines = document.querySelectorAll('.terminal-body .line');
    const terminalSection = document.querySelector('.terminal-section');

    const terminalObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            terminalLines.forEach((line, index) => {
                setTimeout(() => {
                    line.style.opacity = '1';
                    line.style.transform = 'translateY(0)';
                }, index * 800);
            });
        }
    }, { threshold: 0.5 });

    if (terminalSection) {
        terminalObserver.observe(terminalSection);
    }

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Parallax effect for hero images
    document.addEventListener('mousemove', (e) => {
        const moveX = (e.clientX - window.innerWidth / 2) / 50;
        const moveY = (e.clientY - window.innerHeight / 2) / 50;
        
        const img1 = document.querySelector('.img-1');
        const img2 = document.querySelector('.img-2');
        
        if (img1) img1.style.transform = `translate(${moveX}px, ${moveY}px)`;
        if (img2) img2.style.transform = `translate(${moveX * 1.5}px, ${moveY * 1.5}px) translate(10%, -10%)`;
    });
});
