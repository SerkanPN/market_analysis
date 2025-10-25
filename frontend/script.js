const API_BASE_URL = '';

const listingIdInput = document.getElementById('listingId');
const analyzeBtn = document.getElementById('analyzeBtn');
const loader = document.getElementById('loader');
const resultsContainer = document.getElementById('resultsContainer');

analyzeBtn.addEventListener('click', handleAnalysis);

async function handleAnalysis() {
    const listing_id = listingIdInput.value.trim();
    if (!listing_id) {
        alert('Please provide a Listing ID.');
        return;
    }

    loader.classList.remove('hidden');
    resultsContainer.innerHTML = '';

    try {
        const response = await fetch(`${API_BASE_URL}/get-listing-details`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ listing_id: listing_id })
        });
        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }
        displayResults(data);

    } catch (error) {
        resultsContainer.innerHTML = `<p class="error">${error.message}</p>`;
    } finally {
        loader.classList.add('hidden');
    }
}

function displayResults(data) {
    resultsContainer.innerHTML = `
        <div class="result-card">
            <div class="result-image">
                <img src="${data.main_image_url}" alt="${data.title}" />
            </div>
            <div class="result-details">
                <h3><a href="${data.url}" target="_blank">${data.title}</a></h3>
                <p><strong>Shop:</strong> <a href="${data.shop_url}" target="_blank">${data.shop_name}</a></p>
                <table>
                    <tr><td><strong>Price:</strong></td><td>${data.price}</td></tr>
                    <tr><td><strong>Stock:</strong></td><td>${data.quantity}</td></tr>
                    <tr><td><strong>Views:</strong></td><td>${data.views}</td></tr>
                    <tr><td><strong>Favorites:</strong></td><td>${data.num_favorers}</td></tr>
                    <tr><td><strong>Created:</strong></td><td>${data.creation_date}</td></tr>
                </table>
                <p><strong>Category:</strong> ${data.category}</p>
                <div class="tags-container">
                    <strong>Tags:</strong>
                    ${data.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
            </div>
        </div>
    `;
}
