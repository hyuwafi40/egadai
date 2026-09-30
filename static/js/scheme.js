document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('schemeForm');
    if (!form) return;

    const currencyFields = form.querySelectorAll('[data-currency]');
    const formatter = new Intl.NumberFormat('id-ID');

    function stripValue(value) {
        return value.replace(/\./g, '');
    }

    function formatValue(value) {
        const digits = stripValue(value).replace(/[^0-9]/g, '');
        if (!digits) return '';
        return formatter.format(digits);
    }

    currencyFields.forEach(function (field) {
        const initial = field.value;
        if (initial) {
            field.value = formatValue(String(initial));
        }

        field.addEventListener('input', function () {
            const cursorPos = this.selectionStart;
            const before = this.value.length;
            const formatted = formatValue(this.value);
            this.value = formatted;
            const after = formatted.length;
            const newPos = cursorPos + (after - before);
            this.setSelectionRange(newPos, newPos);
        });

        field.addEventListener('blur', function () {
            this.value = formatValue(this.value);
        });
    });

    form.addEventListener('submit', function () {
        currencyFields.forEach(function (field) {
            field.value = stripValue(field.value).replace(/[^0-9]/g, '');
        });
    });
});