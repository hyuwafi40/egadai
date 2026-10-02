document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.querySelector('[data-password-toggle]');
    if (!toggle) return;

    const password = document.getElementById(toggle.getAttribute('aria-controls'));
    if (!password) return;

    toggle.addEventListener('click', function () {
        const isVisible = password.type === 'password';
        password.type = isVisible ? 'text' : 'password';
        toggle.setAttribute('aria-pressed', String(isVisible));
        toggle.setAttribute(
            'aria-label',
            isVisible ? 'Sembunyikan password' : 'Tampilkan password'
        );
        toggle.textContent = isVisible ? 'Sembunyikan' : 'Tampilkan';
    });
});
