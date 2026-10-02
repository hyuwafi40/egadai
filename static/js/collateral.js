document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('input[type="file"][name="photo"]');
    const preview = document.getElementById('photoPreview');
    if (!input || !preview) return;
    input.addEventListener('change', function () {
        const file = this.files && this.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function (event) {
            preview.src = event.target.result;
            preview.classList.remove('d-none');
        };
        reader.readAsDataURL(file);
    });
});