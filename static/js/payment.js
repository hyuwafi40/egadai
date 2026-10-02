document.addEventListener('DOMContentLoaded', function () {
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

    const form = document.getElementById('paymentForm');
    if (form) {
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

        const jumlahInput = form.querySelector('[name="jumlah_bayar"]');
        const tipeSelect = form.querySelector('[name="tipe_pembayaran"]');
        const metodeSelect = form.querySelector('[name="metode_pembayaran"]');
        const sisaBayar = parseFloat(window.paymentSisaBayar || 0);
        const presets = form.querySelectorAll('[data-payment-preset]');

        function setAmount(amount) {
            if (!jumlahInput) return;
            let rounded = Math.round(amount);
            if (rounded <= 0) {
                jumlahInput.value = '';
                return;
            }
            if (sisaBayar > 0 && rounded > sisaBayar) {
                rounded = Math.round(sisaBayar);
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

        function getNumericJumlah() {
            if (!jumlahInput) return 0;
            const raw = stripCurrency(jumlahInput.value);
            const num = parseFloat(raw);
            return isNaN(num) ? 0 : num;
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

        const confirmModalEl = document.getElementById('paymentConfirmModal');
        const confirmModal = confirmModalEl
            ? bootstrap.Modal.getOrCreateInstance(confirmModalEl)
            : null;
        const confirmJumlah = document.getElementById('confirmJumlah');
        const confirmTipe = document.getElementById('confirmTipe');
        const confirmMetode = document.getElementById('confirmMetode');
        const confirmSubmitBtn = document.getElementById('confirmSubmitBtn');
        const submitBtn = document.getElementById('paymentSubmitBtn');
        let formConfirmed = false;

        function showInlineError(message) {
            if (!jumlahInput) return;
            let errEl = jumlahInput.parentElement.querySelector('[data-inline-error]');
            if (!errEl) {
                errEl = document.createElement('div');
                errEl.setAttribute('data-inline-error', '1');
                errEl.className = 'text-danger fs-8 mt-1';
                jumlahInput.parentElement.appendChild(errEl);
            }
            errEl.textContent = message;
        }

        function clearInlineError() {
            if (!jumlahInput) return;
            const errEl = jumlahInput.parentElement.querySelector('[data-inline-error]');
            if (errEl) {
                errEl.textContent = '';
            }
        }

        form.addEventListener('submit', function (event) {
            if (formConfirmed) {
                fields.forEach(function (field) {
                    field.disabled = false;
                    field.readOnly = false;
                    field.value = stripCurrency(field.value);
                });
                return;
            }
            event.preventDefault();

            const jumlah = getNumericJumlah();
            if (jumlah <= 0) {
                showInlineError('Jumlah bayar wajib diisi dan lebih besar dari 0.');
                if (jumlahInput) jumlahInput.focus();
                return;
            }
            clearInlineError();

            if (jumlah > sisaBayar) {
                showInlineError('Jumlah bayar melebihi sisa bayar.');
                if (jumlahInput) jumlahInput.focus();
                return;
            }

            if (!confirmModal) {
                formConfirmed = true;
                form.requestSubmit();
                return;
            }
            if (confirmJumlah && jumlahInput) {
                confirmJumlah.textContent = 'Rp ' + jumlahInput.value;
            }
            if (confirmTipe && tipeSelect) {
                const opt = tipeSelect.options[tipeSelect.selectedIndex];
                confirmTipe.textContent = opt ? opt.textContent : '-';
            }
            if (confirmMetode && metodeSelect) {
                const opt = metodeSelect.options[metodeSelect.selectedIndex];
                confirmMetode.textContent = opt ? opt.textContent : '-';
            }
            confirmModal.show();
        });

        if (confirmSubmitBtn) {
            confirmSubmitBtn.addEventListener('click', function () {
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i><span>Menyimpan...</span>';
                }
                formConfirmed = true;
                confirmModal.hide();
                form.requestSubmit();
            });
        }
    }

    const chooseSearchInput = document.getElementById('chooseSearchInput');
    const chooseTableBody = document.getElementById('chooseTableBody');
    const chooseEmptyFilteredRow = document.getElementById('chooseEmptyFilteredRow');
    const chooseCountNumber = document.getElementById('chooseCountNumber');
    if (chooseSearchInput && chooseTableBody) {
        const dataRows = Array.from(
            chooseTableBody.querySelectorAll('tr[data-search-text]')
        );
        let debounceTimer = null;
        chooseSearchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            const value = this.value.trim().toLowerCase();
            debounceTimer = setTimeout(function () {
                let visible = 0;
                dataRows.forEach(function (row) {
                    const text = row.getAttribute('data-search-text') || '';
                    const match = !value || text.indexOf(value) !== -1;
                    row.style.display = match ? '' : 'none';
                    if (match) visible += 1;
                });
                if (chooseCountNumber) {
                    chooseCountNumber.textContent = String(visible);
                }
                if (chooseEmptyFilteredRow) {
                    const shouldShow = value && dataRows.length > 0 && visible === 0;
                    chooseEmptyFilteredRow.style.display = shouldShow ? '' : 'none';
                }
            }, 200);
        });
    }
});