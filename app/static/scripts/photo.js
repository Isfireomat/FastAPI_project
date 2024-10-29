const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const thumbnail = document.getElementById('thumbnail');
const dropText = document.getElementById('drop-text');
const extraImagesHeader = document.getElementById('extra-images-header');
const extraImagesContainer = document.getElementById('extra-images-container');
const extraImages = document.getElementById('extra-images');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
});

dropArea.addEventListener('dragenter', highlight, false);
dropArea.addEventListener('dragleave', unhighlight, false);
dropArea.addEventListener('dragover', highlight, false);
dropArea.addEventListener('drop', unhighlight, false);
dropArea.addEventListener('drop', handleDrop, false);
dropArea.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', handleFiles, false);

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight() {
    dropArea.classList.add('highlight');
}

function unhighlight() {
    dropArea.classList.remove('highlight');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function handleFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
            displayImage(file);
            uploadFile(file);
        } else {
            alert('Пожалуйста, загрузите файл изображения.');
        }
    }
}

function displayImage(file) {
    const reader = new FileReader();
    reader.onload = function(event) {
        thumbnail.src = event.target.result;
        thumbnail.style.display = 'block';
        dropText.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('photo', file);

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Отображаем результат плагиата
        if (data.result !== undefined) {
            document.getElementById('plagiarism-result').textContent = `Плагиат на ${data.result} %`;
        } else {
            document.getElementById('plagiarism-result').textContent = '';
        }
     
        if (data.picture) {
            extraImagesHeader.style.display = 'block';
            extraImagesContainer.style.display = 'block';
            extraImages.innerHTML = ''; 
            const extraImage = document.createElement('img');
            extraImage.src = 'data:image/jpeg;base64,' + data.picture; 
            extraImage.className = 'extra-thumbnail';
            extraImages.appendChild(extraImage);
        } else {
            extraImagesHeader.style.display = 'none';
            extraImagesContainer.style.display = 'none';
            extraImages.innerHTML = ''; 
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при загрузке.');
    });
}
