document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('paymentForm');
    if (!form) return;

    const formatter = new Intl.NumberFormat('id-ID');

    function formatCurrency(value) {
        const digits = String(value).replace(/\./g, '').replace(/[^0-9]/g, '');
        if (!digits) return '0';
        return formatter.format(digits);
    }

    function stripCurrency(value) {
        return String(value).replace(/\./g, '').replace(/[^0-9]/g, '');
    }

    function normalizeInitialValue(value) {
        if (!value) return '';
        const integerPart = String(value).split('.')[0];
        return integerPart.replace(/[^0-9]/g, '');
    }

    const fields = form.querySelectorAll('[data-currency]');
    fields.forEach(function (field) {
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
        fields.forEach(function (field) {
            field.disabled = false;
            field.readOnly = false;
            field.value = stripCurrency(field.value);
        });
    });

    const jumlahInput = form.querySelector('[name="jumlah_bayar"]');
    const tipeSelect = form.querySelector('[name="tipe_pembayaran"]');
    const sisaBayar = parseFloat(window.paymentSisaBayar || 0);
    const presets = form.querySelectorAll('[data-payment-preset]');

    function setAmount(amount) {
        if (!jumlahInput) return;
        const rounded = Math.round(amount);
        if (rounded <= 0) {
            jumlahInput.value = '';
            return;
        }
        jumlahInput.value = formatCurrency(String(rounded));
    }

    function setJumlahReadOnly(isReadOnly) {
        if (!jumlahInput) return;
        jumlahInput.readOnly = isReadOnly;
        if (isReadOnly) {
            jumlahInput.style.backgroundColor = 'rgba(0, 0, 0, 0.05)';
            jumlahInput.style.cursor = 'not-allowed';
        } else {
            jumlahInput.style.backgroundColor = '';
            jumlahInput.style.cursor = '';
        }
    }

    function syncTipeLunas() {
        if (!tipeSelect) return;
        if (tipeSelect.value === 'lunas') {
            setAmount(sisaBayar);
            setJumlahReadOnly(true);
        } else {
            setJumlahReadOnly(false);
        }
    }

    if (tipeSelect) {
        tipeSelect.addEventListener('change', syncTipeLunas);
        syncTipeLunas();
    }

    presets.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const mode = btn.getAttribute('data-payment-preset');
            if (mode === 'lunas') {
                if (tipeSelect) tipeSelect.value = 'lunas';
                setAmount(sisaBayar);
                setJumlahReadOnly(true);
            } else if (mode === 'half') {
                if (tipeSelect && tipeSelect.value === 'lunas') {
                    tipeSelect.value = 'cicilan';
                }
                setJumlahReadOnly(false);
                setAmount(sisaBayar * 0.5);
            } else {
                if (tipeSelect && tipeSelect.value === 'lunas') {
                    tipeSelect.value = 'cicilan';
                }
                setJumlahReadOnly(false);
                setAmount(parseFloat(mode) || 0);
            }
        });
    });
});