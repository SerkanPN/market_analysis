// DOM Elementlerini Seçme
const shopeeKeywordInput = document.getElementById('shopeeKeyword');
const analyzeShopeeBtn = document.getElementById('analyzeShopeeBtn');
const shopeeLoader = document.getElementById('shopeeLoader');
const shopeeResultsTable = document.getElementById('shopeeResultsTable');

const fetchShopifyBtn = document.getElementById('fetchShopifyBtn');
const shopifyLoader = document.getElementById('shopifyLoader');
const shopifyResultsTable = document.getElementById('shopifyResultsTable');

// Backend sunucumuzun adresi (Şu an yerel bilgisayarımızda çalışıyor)
const API_BASE_URL = 'http://127.0.0.1:5001';

// Olay Dinleyicileri (Event Listeners)
analyzeShopeeBtn.addEventListener('click', handleShopeeAnalysis);
fetchShopifyBtn.addEventListener('click', handleShopifyFetch);

// --- Shopee Analiz Fonksiyonu (GERÇEK) ---
async function handleShopeeAnalysis() {
    const keyword = shopeeKeywordInput.value.trim();
    if (!keyword) {
        alert('Please enter a keyword to analyze.');
        return;
    }

    shopeeLoader.classList.remove('hidden');
    shopeeResultsTable.classList.add('hidden');
    shopeeResultsTable.querySelector('tbody').innerHTML = '';

    try {
        const response = await fetch(`${API_BASE_URL}/analyze-shopee`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keyword: keyword })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        populateTable(shopeeResultsTable, data, ['name', 'price', 'sales']);

    } catch (error) {
        console.error('Error fetching Shopee data:', error);
        alert('Failed to fetch data from Shopee. Check the console for details.');
    } finally {
        shopeeLoader.classList.add('hidden');
        shopeeResultsTable.classList.remove('hidden');
    }
}

// --- Shopify Ürün Çekme Fonksiyonu (GERÇEK) ---
async function handleShopifyFetch() {
    shopifyLoader.classList.remove('hidden');
    shopifyResultsTable.classList.add('hidden');
    shopifyResultsTable.querySelector('tbody').innerHTML = '';

    try {
        const response = await fetch(`${API_BASE_URL}/fetch-shopify`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        populateTable(shopifyResultsTable, data, ['name', 'price']);

    } catch (error) {
        console.error('Error fetching Shopify data:', error);
        alert('Failed to fetch data from Shopify. Check the console for details.');
    } finally {
        shopifyLoader.classList.add('hidden');
        shopifyResultsTable.classList.remove('hidden');
    }
}

// Tabloyu gelen veriyle dolduran yardımcı fonksiyon (Değişiklik yok)
function populateTable(tableElement, data, columns) {
    const tbody = tableElement.querySelector('tbody');
    tbody.innerHTML = ''; 

    data.forEach(item => {
        const row = document.createElement('tr');
        columns.forEach(col => {
            const cell = document.createElement('td');
            cell.textContent = item[col] || '';
            row.appendChild(cell);
        });
        tbody.appendChild(row);
    });
}