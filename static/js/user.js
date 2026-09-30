document.addEventListener('DOMContentLoaded', function () {
    const modalEl = document.getElementById('userFormModal');
    if (!modalEl) return;
    const form = document.getElementById('userForm');
    const titleEl = document.getElementById('userFormModalTitle');
    const hintEl = modalEl.querySelector('[data-user-form-hint]');
    const usernameInput = document.getElementById('userFormUsername');
    const emailInput = document.getElementById('userFormEmail');
    const jobInput = document.getElementById('userFormJob');
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
        titleEl.textContent = 'Tambah User';
        if (hintEl) hintEl.classList.remove('d-none');
        clearErrors();
    }

    document.querySelectorAll('[data-user-create]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            resetForm();
            modal.show();
        });
    });

    document.querySelectorAll('[data-user-edit]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            resetForm();
            form.setAttribute('action', btn.getAttribute('data-url'));
            titleEl.textContent = 'Edit User';
            if (hintEl) hintEl.classList.add('d-none');
            usernameInput.value = btn.getAttribute('data-username') || '';
            emailInput.value = btn.getAttribute('data-email') || '';
            jobInput.value = btn.getAttribute('data-job') || '';
            modal.show();
        });
    });

    document.querySelectorAll('[data-user-reset-password]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const username = btn.getAttribute('data-username') || 'user ini';
            if (!window.confirm('Reset password ' + username + ' ke password default?')) return;
            const url = btn.getAttribute('data-url');
            const csrf = document.querySelector('[name="csrfmiddlewaretoken"]');
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrf ? csrf.value : '',
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    if (data.success) {
                        if (window.showToast) window.showToast('Sukses', data.message, 'success');
                    } else {
                        if (window.showToast) window.showToast('Gagal', 'Reset password gagal.', 'danger');
                    }
                });
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