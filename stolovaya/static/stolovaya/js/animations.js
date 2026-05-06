document.addEventListener('DOMContentLoaded', () => {
    // Анимация добавления в корзину
    const addButtons = document.querySelectorAll('.add-to-cart');
    addButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            btn.style.transform = 'scale(0.9)';
            btn.style.background = '#2ecc71';
            setTimeout(() => {
                btn.style.transform = '';
                btn.style.background = '';
            }, 200);
        });
    });

    // Плавное появление карточек с задержкой
    const cards = document.querySelectorAll('.dish-card');
    cards.forEach((card, i) => {
        card.style.animationDelay = `${i * 0.05}s`;
    });
});