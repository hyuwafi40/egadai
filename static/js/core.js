function showToast(title, message, type = 'info') {
    if (typeof bootstrap === 'undefined') {
        console.warn('showToast: Bootstrap belum dimuat.');
        return;
    }

    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) return;

    const toastId = 'toast-' + Date.now() + '-' + Math.floor(Math.random() * 1000);

    let iconClass = 'fa-circle-info text-primary';
    if (type === 'success') iconClass = 'fa-circle-check text-success';
    if (type === 'danger') iconClass = 'fa-circle-xmark text-danger';
    if (type === 'warning') iconClass = 'fa-triangle-exclamation text-warning';

    const wrapper = document.createElement('div');
    wrapper.id = toastId;
    wrapper.className = 'toast glass-card border-0 shadow-lg mb-2 toast-animate-in';
    wrapper.setAttribute('role', 'alert');
    wrapper.setAttribute('aria-live', 'assertive');
    wrapper.setAttribute('aria-atomic', 'true');

    const header = document.createElement('div');
    header.className = 'toast-header bg-transparent border-bottom-0 pb-0 pt-3 px-3';

    const icon = document.createElement('i');
    icon.className = 'fa-solid ' + iconClass + ' me-2 fs-6';

    const titleEl = document.createElement('strong');
    titleEl.className = 'me-auto text-dark fs-7';
    titleEl.textContent = title;

    const small = document.createElement('small');
    small.className = 'text-muted fs-8';
    small.textContent = 'Just now';

    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'btn-close ms-2';
    closeBtn.setAttribute('data-bs-dismiss', 'toast');
    closeBtn.setAttribute('aria-label', 'Close');

    header.appendChild(icon);
    header.appendChild(titleEl);
    header.appendChild(small);
    header.appendChild(closeBtn);

    const body = document.createElement('div');
    body.className = 'toast-body fs-8 text-muted pt-1 pb-3 px-3';
    body.textContent = message;

    wrapper.appendChild(header);
    wrapper.appendChild(body);
    toastContainer.appendChild(wrapper);

    const bsToast = new bootstrap.Toast(wrapper, { delay: 3500 });
    bsToast.show();

    wrapper.addEventListener('hide.bs.toast', function () {
        wrapper.classList.remove('toast-animate-in');
        wrapper.classList.add('toast-animate-out');
    });

    wrapper.addEventListener('hidden.bs.toast', function () {
        wrapper.remove();
    });
}

window.showToast = showToast;

document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebarNav = document.getElementById('sidebarNav');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    const desktopSidebar = window.matchMedia('(min-width: 992px)');
    const backgroundElements = [
        document.querySelector('.glass-nav'),
        document.querySelector('.main-content-wrapper'),
        document.querySelector('.app-shell > footer')
    ].filter(Boolean);

    function setSidebarExpanded(expanded, returnFocus) {
        if (!sidebarNav || !sidebarOverlay) return;
        const isOpen = !desktopSidebar.matches && expanded;
        sidebarNav.classList.toggle('active', isOpen);
        sidebarOverlay.classList.toggle('active', isOpen);
        sidebarNav.inert = !desktopSidebar.matches && !isOpen;
        document.body.classList.toggle('sidebar-open', isOpen);
        backgroundElements.forEach(function (element) {
            element.inert = isOpen;
        });

        if (isOpen) {
            sidebarNav.setAttribute('role', 'dialog');
            sidebarNav.setAttribute('aria-modal', 'true');
        } else {
            sidebarNav.removeAttribute('role');
            sidebarNav.removeAttribute('aria-modal');
        }

        if (sidebarToggleBtn) {
            sidebarToggleBtn.setAttribute('aria-expanded', String(isOpen));
            sidebarToggleBtn.setAttribute(
                'aria-label',
                isOpen ? 'Tutup navigasi' : 'Buka navigasi'
            );
        }

        if (isOpen) {
            const firstItem = sidebarNav.querySelector('a.nav-item-link, button.nav-item-link');
            if (firstItem) firstItem.focus();
        } else if (returnFocus && sidebarToggleBtn) {
            sidebarToggleBtn.focus();
        }
    }

    setSidebarExpanded(false, false);

    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', function () {
            setSidebarExpanded(!sidebarNav.classList.contains('active'), false);
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function () {
            setSidebarExpanded(false, true);
        });
    }

    if (sidebarNav) {
        sidebarNav.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && sidebarNav.classList.contains('active')) {
                setSidebarExpanded(false, true);
                return;
            }

            if (event.key === 'Tab' && sidebarNav.classList.contains('active')) {
                const focusableItems = Array.from(
                    sidebarNav.querySelectorAll('a[href], button:not([disabled])')
                );
                if (!focusableItems.length) {
                    event.preventDefault();
                    return;
                }

                const firstItem = focusableItems[0];
                const lastItem = focusableItems[focusableItems.length - 1];
                if (event.shiftKey && document.activeElement === firstItem) {
                    event.preventDefault();
                    lastItem.focus();
                } else if (!event.shiftKey && document.activeElement === lastItem) {
                    event.preventDefault();
                    firstItem.focus();
                }
            }
        });
        sidebarNav.querySelectorAll('a.nav-item-link').forEach(function (link) {
            link.addEventListener('click', function () {
                if (!desktopSidebar.matches) setSidebarExpanded(false, false);
            });
        });
    }

    desktopSidebar.addEventListener('change', function () {
        setSidebarExpanded(false, false);
    });

    document.querySelectorAll('[data-django-message]').forEach(function (el) {
        const tags = el.getAttribute('data-tags') || 'info';
        const text = el.getAttribute('data-text') || '';
        let type = 'info';
        if (tags.indexOf('success') !== -1) {
            type = 'success';
        } else if (tags.indexOf('error') !== -1 || tags.indexOf('danger') !== -1) {
            type = 'danger';
        } else if (tags.indexOf('warning') !== -1) {
            type = 'warning';
        }
        const title = tags ? (tags.charAt(0).toUpperCase() + tags.slice(1)) : 'Info';
        showToast(title, text, type);
        el.remove();
    });

    const tableSearchInput = document.getElementById('tableSearchInput');
    const tableBody = document.getElementById('tableBody');

    if (tableSearchInput && tableBody) {
        tableSearchInput.addEventListener('input', function (e) {
            const searchTerm = e.target.value.toLowerCase();
            const rows = tableBody.getElementsByTagName('tr');

            Array.from(rows).forEach(function (row) {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    const dashboardForm = document.getElementById('dashboardForm');
    if (dashboardForm) {
        dashboardForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const keywordField = document.getElementById('filterKeyword');
            const keyword = (keywordField && keywordField.value) || 'All Filters';
            showToast('Filter Applied', 'Table results updated for "' + keyword + '".', 'success');
        });
    }

    const resetFiltersBtn = document.getElementById('resetFiltersBtn');
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', function () {
            if (dashboardForm) dashboardForm.reset();
            if (tableSearchInput) {
                tableSearchInput.value = '';
                tableSearchInput.dispatchEvent(new Event('input'));
            }
            showToast('Filters Reset', 'All search criteria cleared.', 'info');
        });
    }

    const newEntryBtn = document.getElementById('newEntryBtn');
    if (newEntryBtn) {
        newEntryBtn.addEventListener('click', function () {
            showToast('New Entry', 'Creation drawer launched.', 'info');
        });
    }

    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', function () {
            showToast('Export Initiated', 'Generating report for current view...', 'success');
        });
    }

    const notificationBtn = document.getElementById('notificationBtn');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function () {
            showToast('Notifications', 'You have unread system alerts.', 'info');
        });
    }

    document.addEventListener('click', function (e) {
        const placeholderLink = e.target.closest('a.nav-item-link[href="#"]');
        if (placeholderLink) {
            e.preventDefault();
            return;
        }

        const viewBtn = e.target.closest('.btn-action-view');
        if (viewBtn) {
            const id = viewBtn.getAttribute('data-id');
            showToast('Record Details', 'Opening details modal for record ' + id, 'info');
        }

        const deleteBtn = e.target.closest('.btn-action-delete');
        if (deleteBtn) {
            const id = deleteBtn.getAttribute('data-id');
            const row = deleteBtn.closest('tr');
            if (row) {
                row.style.transition = 'opacity 0.4s ease';
                row.style.opacity = '0';
                setTimeout(function () {
                    row.remove();
                    showToast('Record Deleted', 'Successfully removed ' + id, 'danger');
                }, 400);
            }
        }
    });

    const paginationList = document.getElementById('paginationList');
    if (paginationList) {
        paginationList.addEventListener('click', function (e) {
            const link = e.target.closest('.page-link');
            if (link && !link.parentElement.classList.contains('disabled')) {
                e.preventDefault();
                const items = paginationList.querySelectorAll('.page-item');
                items.forEach(function (item) {
                    item.classList.remove('active');
                });
                if (!isNaN(link.textContent)) {
                    link.parentElement.classList.add('active');
                    showToast('Page Switched', 'Navigated to page ' + link.textContent, 'info');
                }
            }
        });
    }
});