document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-delete-trigger]').forEach(function (trigger) {
        trigger.addEventListener('click', function () {
            const modalSelector = trigger.getAttribute('data-delete-modal');
            const url = trigger.getAttribute('data-delete-url');
            const name = trigger.getAttribute('data-delete-name') || 'item ini';
            const reload = trigger.getAttribute('data-delete-reload') !== 'false';
            const modalEl = modalSelector ? document.querySelector(modalSelector) : null;
            if (!modalEl) return;
            const form = modalEl.querySelector('form[data-delete-form]');
            const nameEl = modalEl.querySelector('[data-delete-name]');
            if (form) {
                form.setAttribute('action', url);
                form.dataset.reload = reload ? 'true' : 'false';
            }
            if (nameEl) nameEl.textContent = name;
            bootstrap.Modal.getOrCreateInstance(modalEl).show();
        });
    });

    document.addEventListener('submit', function (event) {
        const form = event.target;
        if (!form.matches('form[data-delete-form]')) return;
        event.preventDefault();
        const csrfInput = form.querySelector('[name="csrfmiddlewaretoken"]');
        const url = form.getAttribute('action');
        if (!url) return;
        const shouldReload = form.dataset.reload !== 'false';
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfInput ? csrfInput.value : '',
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then(function (response) {
                return response.json().then(function (data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function (result) {
                const modalEl = form.closest('.modal');
                if (result.data && result.data.success) {
                    if (modalEl) bootstrap.Modal.getOrCreateInstance(modalEl).hide();
                    if (window.showToast) window.showToast('Sukses', result.data.message, 'success');
                    if (shouldReload) {
                        setTimeout(function () {
                            window.location.reload();
                        }, 600);
                    }
                } else {
                    const msg = (result.data && result.data.message) || 'Gagal menghapus.';
                    if (window.showToast) window.showToast('Gagal', msg, 'danger');
                }
            })
            .catch(function () {
                if (window.showToast) window.showToast('Gagal', 'Terjadi kesalahan.', 'danger');
            });
    });
});