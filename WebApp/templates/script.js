document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append("file", file);

    fetch('/process', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '';
        if (data.error) {
            resultDiv.innerHTML = '<p>' + data.error + '</p>';
        } else {
            resultDiv.innerHTML += '<p>Matched images: ' + data.matched_images.join(', ') + '</p>';
            resultDiv.innerHTML += '<p>Unmatched faces count: ' + data.unmatched_count + '</p>';
        }
    })
    .catch(error => console.error('Error:', error));
});