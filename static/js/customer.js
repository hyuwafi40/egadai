document.addEventListener('DOMContentLoaded', function () {
    function setupPreview(inputName, previewId) {
        const input = document.querySelector('input[type="file"][name="' + inputName + '"]');
        const preview = document.getElementById(previewId);
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
    }

    setupPreview('photo', 'photoPreview');
    setupPreview('selfie', 'selfiePreview');
});