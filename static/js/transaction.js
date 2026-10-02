document.addEventListener('DOMContentLoaded', function () {
    const formatter = new Intl.NumberFormat('id-ID');

    function formatCurrency(value) {
        const digits = String(value).replace(/\./g, '').replace(/[^0-9]/g, '');
        if (!digits) return '';
        return formatter.format(digits);
    }

    function stripCurrency(value) {
        return String(value).replace(/\./g, '').replace(/[^0-9]/g, '');
    }

    function formatRupiah(num) {
        const n = Math.round(Number(num) || 0);
        return 'Rp ' + formatter.format(n);
    }

    function normalizeInitialValue(value) {
        if (!value) return '';
        const integerPart = String(value).split('.')[0];
        return integerPart.replace(/[^0-9]/g, '');
    }

    function parseLocalDate(value) {
        if (!value) return null;
        const parts = String(value).split('-');
        if (parts.length !== 3) return null;
        const year = parseInt(parts[0], 10);
        const month = parseInt(parts[1], 10) - 1;
        const day = parseInt(parts[2], 10);
        if (isNaN(year) || isNaN(month) || isNaN(day)) return null;
        return new Date(year, month, day);
    }

    function formatLocalDate(date) {
        const yyyy = date.getFullYear();
        const mm = String(date.getMonth() + 1).padStart(2, '0');
        const dd = String(date.getDate()).padStart(2, '0');
        return yyyy + '-' + mm + '-' + dd;
    }

    function setupCurrencyFields(form, onUpdate) {
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
                if (typeof onUpdate === 'function') onUpdate();
            });
            field.addEventListener('blur', function () {
                this.value = formatCurrency(this.value);
            });
        });
        form.addEventListener('submit', function () {
            fields.forEach(function (field) {
                field.value = stripCurrency(field.value);
            });
        });
        return fields;
    }

    function setupAutoDueDate(form, schemesData) {
        const pinjamInput = form.querySelector('[name$="tanggal_pinjam"]');
        const schemeSelect = form.querySelector('[name$="scheme"]');
        const jatuhTempoInput = form.querySelector('[name$="tanggal_jatuh_tempo"]');
        if (!pinjamInput || !schemeSelect || !jatuhTempoInput) return;
        if (!schemesData) return;

        function recalc() {
            const pinjamValue = pinjamInput.value;
            const schemeValue = schemeSelect.value;
            if (!pinjamValue || !schemeValue) return;
            const scheme = schemesData[schemeValue];
            if (!scheme || !scheme.durasi) return;
            const pinjamDate = parseLocalDate(pinjamValue);
            if (!pinjamDate) return;
            pinjamDate.setDate(pinjamDate.getDate() + parseInt(scheme.durasi, 10));
            jatuhTempoInput.value = formatLocalDate(pinjamDate);
        }

        pinjamInput.addEventListener('change', recalc);
        schemeSelect.addEventListener('change', recalc);
    }

    function setupLiveSelect(input) {
        const selectId = input.getAttribute('data-select-target');
        const select = document.getElementById(selectId);
        if (!select) return;

        const allOptions = Array.from(select.options).map(function (opt) {
            return {
                value: opt.value,
                text: opt.textContent,
                textLower: opt.textContent.toLowerCase(),
            };
        });

        function render(term) {
            const currentValue = select.value;
            const termLower = String(term || '').toLowerCase().trim();
            select.innerHTML = '';
            allOptions.forEach(function (item) {
                if (item.value === '' || !termLower || item.textLower.indexOf(termLower) !== -1) {
                    const opt = document.createElement('option');
                    opt.value = item.value;
                    opt.textContent = item.text;
                    if (item.value === currentValue) {
                        opt.selected = true;
                    }
                    select.appendChild(opt);
                }
            });
        }

        input.addEventListener('input', function () {
            render(this.value);
        });
    }

    function initEditForm(form, schemesData) {
        setupCurrencyFields(form);
        setupAutoDueDate(form, schemesData);
    }

    function initCreateForm(form, schemesData) {
        setupCurrencyFields(form, updatePreview);
        setupAutoDueDate(form, schemesData);

        document.querySelectorAll('[data-live-select]').forEach(function (input) {
            setupLiveSelect(input);
        });

        const customerModeNew = document.getElementById('customerModeNew');
        const customerModeExisting = document.getElementById('customerModeExisting');
        const customerNewSection = document.getElementById('customerNewSection');
        const customerExistingSection = document.getElementById('customerExistingSection');
        const customerSearchInput = document.getElementById('existingCustomerSearch');

        function toggleCustomerSections() {
            if (!customerModeNew || !customerModeExisting) return;
            if (customerModeNew.checked) {
                customerNewSection.classList.remove('d-none');
                customerExistingSection.classList.add('d-none');
            } else {
                customerNewSection.classList.add('d-none');
                customerExistingSection.classList.remove('d-none');
            }
            if (customerSearchInput) {
                customerSearchInput.value = '';
                customerSearchInput.dispatchEvent(new Event('input'));
            }
        }
        if (customerModeNew) customerModeNew.addEventListener('change', toggleCustomerSections);
        if (customerModeExisting) customerModeExisting.addEventListener('change', toggleCustomerSections);

        const collateralModeNew = document.getElementById('collateralModeNew');
        const collateralModeExisting = document.getElementById('collateralModeExisting');
        const collateralNewSection = document.getElementById('collateralNewSection');
        const collateralExistingSection = document.getElementById('collateralExistingSection');
        const collateralSearchInput = document.getElementById('existingCollateralSearch');

        function toggleCollateralSections() {
            if (!collateralModeNew || !collateralModeExisting) return;
            if (collateralModeNew.checked) {
                collateralNewSection.classList.remove('d-none');
                collateralExistingSection.classList.add('d-none');
            } else {
                collateralNewSection.classList.add('d-none');
                collateralExistingSection.classList.remove('d-none');
            }
            if (collateralSearchInput) {
                collateralSearchInput.value = '';
                collateralSearchInput.dispatchEvent(new Event('input'));
            }
        }
        if (collateralModeNew) collateralModeNew.addEventListener('change', toggleCollateralSections);
        if (collateralModeExisting) collateralModeExisting.addEventListener('change', toggleCollateralSections);

        const uangInput = form.querySelector('[name$="uang_pinjaman"]');
        const schemeSelect = form.querySelector('[name$="scheme"]');
        if (uangInput) uangInput.addEventListener('input', updatePreview);
        if (schemeSelect) schemeSelect.addEventListener('change', updatePreview);

        function updatePreview() {
            const elPinjaman = document.getElementById('previewPinjaman');
            const elBunga = document.getElementById('previewBunga');
            const elAdmin = document.getElementById('previewAdmin');
            const elTotal = document.getElementById('previewTotal');
            const elTebus = document.getElementById('previewTebus');
            if (!elPinjaman) return;
            if (!uangInput || !schemeSelect) return;

            const uang = parseInt(stripCurrency(uangInput.value), 10) || 0;
            const schemeValue = schemeSelect.value;
            const scheme = schemesData[schemeValue];

            if (!scheme) {
                elPinjaman.textContent = formatRupiah(uang);
                elBunga.textContent = formatRupiah(0);
                elAdmin.textContent = formatRupiah(0);
                elTotal.textContent = formatRupiah(0);
                elTebus.textContent = formatRupiah(uang);
                return;
            }

            const bunga = Math.round(uang * parseFloat(scheme.bunga) / 100);
            const admin = Math.round(parseFloat(scheme.biaya_admin));
            const total = bunga + admin;
            const tebus = uang + total;

            elPinjaman.textContent = formatRupiah(uang);
            elBunga.textContent = formatRupiah(bunga);
            elAdmin.textContent = formatRupiah(admin);
            elTotal.textContent = formatRupiah(total);
            elTebus.textContent = formatRupiah(tebus);
        }

        updatePreview();
    }

    const schemesData = window.transactionSchemesData || {};
    const editForm = document.getElementById('transactionForm');
    const createForm = document.getElementById('trxForm');

    if (editForm) {
        initEditForm(editForm, schemesData);
    }
    if (createForm) {
        initCreateForm(createForm, schemesData);
    }
});