document.addEventListener('DOMContentLoaded', function () {
    const generateBtn = document.getElementById('generate-btn');
    const inputText = document.getElementById('input-text');
    const generationStatus = document.getElementById('generation-status');
    const generatedTextDiv = document.getElementById('generated-text');
    const actionButtonsDiv = document.getElementById('action-buttons');
    const retryBtn = document.getElementById('retry-btn');
    const downloadBtn = document.getElementById('download-btn');
    const shareBtn = document.getElementById('share-btn');

    generateBtn.addEventListener('click', function () {
        const text = inputText.value.trim();
        if (text === '') {
            alert('Please enter text to generate content.');
            return;
        }

        generateBtn.disabled = true;
        generationStatus.innerHTML = '<div class="spinner-border text-success" role="status"><span class="visually-hidden">Generating..</span></div>Generation in progress...';
        generatedTextDiv.style.display = 'none';
        actionButtonsDiv.style.display = 'none';

        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ input_text: text })
        })
        .then(response => response.json())
        .then(data => {
            generationStatus.innerHTML = '';
            if (data.generated_text) {
                generatedTextDiv.style.display = 'block';
                generatedTextDiv.innerText = data.generated_text;
                actionButtonsDiv.style.display = 'block';
                generatedTextDiv.classList.remove('alert-secondary', 'alert-danger');
                generatedTextDiv.classList.add('alert-success', 'animate__animated', 'animate__fadeIn');
            } else if (data.error) {
                generatedTextDiv.style.display = 'block';
                generatedTextDiv.classList.remove('alert-secondary');
                generatedTextDiv.classList.add('alert-danger', 'animate__animated', 'animate__shakeX');
                generatedTextDiv.innerText = data.error;
            }
            generateBtn.disabled = false;
        })
        .catch(error => {
            console.error('Erreur:', error);
            generationStatus.innerHTML = '<span class="badge bg-danger animate__animated animate__shakeX">Error during text generation.</span>';
            generateBtn.disabled = false;
        });
    });

    if (retryBtn) {
        retryBtn.addEventListener('click', function () {
            generatedTextDiv.style.display = 'none';
            actionButtonsDiv.style.display = 'none';
            inputText.value = '';
        });
    }

    if (downloadBtn) {
        downloadBtn.addEventListener('click', function () {
            const text = generatedTextDiv.innerText;
            const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'generated_text.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
    }

    if (shareBtn) {
        shareBtn.addEventListener('click', function () {
            const text = generatedTextDiv.innerText;
            if (navigator.share) {
                navigator.share({
                    title: 'Generated Text',
                    text: text,
                })
                .then(() => console.log('Text shared successfully'))
                .catch((error) => console.error('Error during sharing:', error));
            } else {
                alert('Sharing is not supported on this browser');
            }
        });
    }
});
