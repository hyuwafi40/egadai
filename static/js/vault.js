document.addEventListener('DOMContentLoaded', function () {
    const modalEl = document.getElementById('categoryFormModal');
    if (!modalEl) return;
    const form = document.getElementById('categoryForm');
    const titleEl = document.getElementById('categoryFormModalTitle');
    const nameInput = document.getElementById('categoryFormName');
    const codeInput = document.getElementById('categoryFormCode');
    const descriptionInput = document.getElementById('categoryFormDescription');
    const createUrl = form.getAttribute('data-create-url');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);

    function clearErrors() {
        modalEl.querySelectorAll('[data-error-for]').forEach(function (el) {
            el.textContent = '';
        });
    }

    function showErrors(errors) {
        Object.keys(errors).forEach(function (field) {
            const el = modalEl.querySelector('[data-error-for="' + field + '"]');
            if (!el) return;
            const msgs = errors[field].map(function (e) {
                return e.message;
            });
            el.textContent = msgs.join(', ');
        });
    }

    function resetForm() {
        form.reset();
        form.setAttribute('action', createUrl);
        titleEl.textContent = 'Tambah Kategori';
        clearErrors();
    }

    document.querySelectorAll('[data-category-create]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            resetForm();
            modal.show();
        });
    });

    document.querySelectorAll('[data-category-edit]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            resetForm();
            form.setAttribute('action', btn.getAttribute('data-url'));
            titleEl.textContent = 'Edit Kategori';
            nameInput.value = btn.getAttribute('data-name') || '';
            codeInput.value = btn.getAttribute('data-code') || '';
            descriptionInput.value = btn.getAttribute('data-description') || '';
            modal.show();
        });
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        clearErrors();
        const url = form.getAttribute('action');
        const formData = new FormData(form);
        const csrf = formData.get('csrfmiddlewaretoken');
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData,
        })
            .then(function (response) {
                return response.json().then(function (data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function (result) {
                if (result.data && result.data.success) {
                    modal.hide();
                    if (window.showToast) window.showToast('Sukses', result.data.message, 'success');
                    setTimeout(function () {
                        window.location.reload();
                    }, 600);
                } else {
                    if (result.data && result.data.errors) showErrors(result.data.errors);
                    if (window.showToast) window.showToast('Gagal', 'Periksa kembali data Anda.', 'danger');
                }
            })
            .catch(function () {
                if (window.showToast) window.showToast('Gagal', 'Terjadi kesalahan.', 'danger');
            });
    });
});