document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('video_file');
    const dropZone = document.getElementById('drop-zone');
    const filePreview = document.getElementById('file-name-preview');

    if (dropZone && fileInput) {
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                filePreview.textContent = 'Selected File: ' + this.files[0].name;
            }
        });
    }
});