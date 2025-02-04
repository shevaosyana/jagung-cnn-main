// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const predictBtn = document.getElementById('predictBtn');
    const previewImage = document.getElementById('previewImage');
    const resultSection = document.querySelector('.result-section');
    const diseaseType = document.getElementById('diseaseType');
    const confidence = document.getElementById('confidence');
    const details = document.getElementById('details');

    // Handle click on upload box
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#2980b9';
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#3498db';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = '#3498db';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // Handle file selection
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    // Handle file processing
    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Mohon upload file gambar');
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImage.src = e.target.result;
            resultSection.style.display = 'flex';
        };
        reader.readAsDataURL(file);

        // Enable predict button
        predictBtn.disabled = false;
    }

    // Handle prediction
    predictBtn.addEventListener('click', async() => {
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            predictBtn.disabled = true;
            predictBtn.textContent = 'Menganalisis...';

            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            // Update results
            diseaseType.textContent = result.class;
            confidence.textContent = `${(result.confidence * 100).toFixed(2)}%`;
            details.textContent = result.details;
            resultSection.style.display = 'flex';

        } catch (error) {
            alert('Error dalam memproses gambar. Silakan coba lagi.');
        } finally {
            predictBtn.disabled = false;
            predictBtn.textContent = 'Analisis Daun';
        }
    });
});