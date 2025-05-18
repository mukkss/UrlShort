const shortenButton = document.getElementById('shortenButton');
const longUrlInput = document.getElementById('longUrlInput');
const resultContainer = document.getElementById('result-container');
const shortUrlOutput = document.getElementById('short-url-output');
const errorMessageDiv = document.getElementById('error-message');

shortenButton.addEventListener('click', async () => {
    const longUrl = longUrlInput.value.trim();
    errorMessageDiv.style.display = 'none'; // Hide previous errors
    resultContainer.style.display = 'none'; // Hide previous results
    shortUrlOutput.innerHTML = ''; // Clear previous output

    if (!longUrl) {
        errorMessageDiv.textContent = 'Please enter a URL.';
        errorMessageDiv.style.display = 'block';
        return;
    }

    try {
        const response = await fetch('/shorten', { // Make sure this matches your FastAPI endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ long_url: longUrl }),
        });

        if (response.ok) {
            const data = await response.json();
            const shortUrl = data.short_url;
            shortUrlOutput.innerHTML = `<a href="${shortUrl}" target="_blank">${shortUrl}</a>`;
            resultContainer.style.display = 'block';
        } else {
            const errorData = await response.json();
            errorMessageDiv.textContent = errorData.detail || 'An error occurred while shortening the URL.';
            errorMessageDiv.style.display = 'block';
        }
    } catch (error) {
        console.error('Network or parsing error:', error);
        errorMessageDiv.textContent = 'Could not connect to the server or parse response. Please try again.';
        errorMessageDiv.style.display = 'block';
    }
});