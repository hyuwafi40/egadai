document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('transactionForm');
    if (!form) return;

    const schemesData = window.transactionSchemesData || {};

    function formatCurrency(value) {
        const digits = value.replace(/\./g, '').replace(/[^0-9]/g, '');
        if (!digits) return '';
        return new Intl.NumberFormat('id-ID').format(digits);
    }

    function stripCurrency(value) {
        return value.replace(/\./g, '').replace(/[^0-9]/g, '');
    }

    function normalizeInitialValue(value) {
        if (!value) return '';
        const integerPart = value.split('.')[0];
        const digits = integerPart.replace(/[^0-9]/g, '');
        return digits;
    }

    const currencyFields = form.querySelectorAll('[data-currency]');
    currencyFields.forEach(function (field) {
        const initial = field.value;
        if (initial) {
            field.value = formatCurrency(normalizeInitialValue(initial));
        }
        field.addEventListener('input', function () {
            const cursorPos = this.selectionStart;
            const before = this.value.length;
            this.value = formatCurrency(this.value);
            const after = this.value.length;
            const newPos = cursorPos + (after - before);
            this.setSelectionRange(newPos, newPos);
        });
        field.addEventListener('blur', function () {
            this.value = formatCurrency(this.value);
        });
    });

    form.addEventListener('submit', function () {
        currencyFields.forEach(function (field) {
            field.value = stripCurrency(field.value);
        });
    });

    const pinjamInput = form.querySelector('[name="tanggal_pinjam"]');
    const schemeSelect = form.querySelector('[name="scheme"]');
    const jatuhTempoInput = form.querySelector('[name="tanggal_jatuh_tempo"]');

    function autoCalculateDueDate() {
        if (!pinjamInput || !schemeSelect || !jatuhTempoInput) return;
        const pinjamValue = pinjamInput.value;
        const schemeValue = schemeSelect.value;
        if (!pinjamValue || !schemeValue) return;
        const duration = schemesData[schemeValue];
        if (!duration) return;
        const pinjamDate = new Date(pinjamValue);
        if (isNaN(pinjamDate.getTime())) return;
        pinjamDate.setDate(pinjamDate.getDate() + parseInt(duration, 10));
        const yyyy = pinjamDate.getFullYear();
        const mm = String(pinjamDate.getMonth() + 1).padStart(2, '0');
        const dd = String(pinjamDate.getDate()).padStart(2, '0');
        jatuhTempoInput.value = yyyy + '-' + mm + '-' + dd;
    }

    if (pinjamInput) {
        pinjamInput.addEventListener('change', autoCalculateDueDate);
    }
    if (schemeSelect) {
        schemeSelect.addEventListener('change', autoCalculateDueDate);
    }
});