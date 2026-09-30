document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-live-search]').forEach(function (input) {
        const targetSelector = input.getAttribute('data-target');
        const target = targetSelector ? document.querySelector(targetSelector) : null;
        if (!target) return;
        input.addEventListener('input', function () {
            const term = this.value.trim().toLowerCase();
            const rows = target.querySelectorAll('tbody tr');
            rows.forEach(function (row) {
                if (row.querySelector('td[colspan]')) return;
                const text = row.textContent.toLowerCase();
                row.style.display = !term || text.includes(term) ? '' : 'none';
            });
        });
    });
});