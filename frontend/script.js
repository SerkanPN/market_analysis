const storeUrlInput = document.getElementById('storeUrl');
const analyzeBtn = document.getElementById('analyzeBtn');
const loader = document.getElementById('loader');
const resultsContainer = document.getElementById('resultsContainer');

analyzeBtn.addEventListener('click', handleAnalysis);

async function handleAnalysis() {
    const store_url = storeUrlInput.value.trim();
    if (!store_url) {
        alert('Please enter a store URL.');
        return;
    }

    loader.classList.remove('hidden');
    resultsContainer.innerHTML = '';

    try {
        const response = await fetch('/analyze-store', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ store_url: store_url })
        });
        const data = await response.json();

        if (data.error) { throw new Error(data.error); }
        displayResults(data);

    } catch (error) {
        resultsContainer.innerHTML = `<p class="error">${error.message}</p>`;
    } finally {
        loader.classList.add('hidden');
    }
}

function displayResults(data) {
    // Mağaza Karnesi
    const shopInfoHtml = `
        <div class="shop-info-card">
            <div class="info-item"><h4>Store Name</h4><p>${data.shop_info.name}</p></div>
            <div class="info-item"><h4>Followers</h4><p>${data.shop_info.follower_count.toLocaleString()}</p></div>
            <div class="info-item"><h4>Rating</h4><p>${data.shop_info.rating_star} ★</p></div>
            <div class="info-item"><h4>Total Products</h4><p>${data.shop_info.total_products}</p></div>
        </div>
    `;

    // Ürün Grid'i
    let productsHtml = '<div class="product-grid">';
    data.products.forEach(p => {
        productsHtml += `
            <div class="product-card">
                <img src="${p.image}" alt="${p.name}">
                <div class="product-details">
                    <h5>${p.name}</h5>
                    <p>${p.price}</p>
                    <div class="product-stats">
                        <span>🛒 Sold: ${p.sold.toLocaleString()}</span>
                        <span>❤️ Likes: ${p.likes.toLocaleString()}</span>
                    </div>
                </div>
            </div>
        `;
    });
    productsHtml += '</div>';

    resultsContainer.innerHTML = shopInfoHtml + productsHtml;
}
