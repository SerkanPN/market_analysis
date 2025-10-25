from flask import Flask, request, jsonify
from flask_cors import CORS
import shopify
import os
import time

# Selenium kütüphanelerini import et
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# --- SHOPIFY AYARLARI ---
SHOPIFY_API_KEY = os.environ.get('SHOPIFY_API_KEY', 'YOUR_API_KEY')
SHOPIFY_PASSWORD = os.environ.get('SHOPIFY_PASSWORD', 'YOUR_API_PASSWORD')
SHOPIFY_STORE_NAME = os.environ.get('SHOPIFY_STORE_NAME', 'YOUR_STORE_NAME')
SHOP_URL = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_PASSWORD}@{SHOPIFY_STORE_NAME}.myshopify.com/admin"

# --- API ENDPOINT'LERİ ---

@app.route('/analyze-shopee', methods=['POST'])
def analyze_shopee():
    data = request.json
    keyword = data.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    url = f"https://shopee.co.id/search?keyword={keyword.replace(' ', '+')}"

    # --- SELENIUM KODU BAŞLIYOR ---
    try:
        # Chrome ayarları (Render'da çalışması için önemli)
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Tarayıcıyı göstermeden arka planda çalıştır
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Chrome sürücüsünü otomatik olarak kur ve başlat
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        driver.get(url)
        time.sleep(3) # Sayfanın tam olarak yüklenmesi için 3 saniye bekle

        # Sayfanın HTML içeriğini al
        html = driver.page_source
        driver.quit() # Tarayıcıyı kapat
        # --- SELENIUM KODU BİTİYOR ---

        soup = BeautifulSoup(html, 'html.parser')
        
        products = soup.find_all('div', class_='col-xs-2-4 shopee-search-item-result__item')
        if not products:
             return jsonify([{"name": "No products found, Shopee might have blocked the request.", "price": "N/A", "sales": "N/A"}])

        results = []
        for product in products[:10]:
            try:
                name_div = product.find('div', class_='ie3A+n bM+74g')
                price_div = product.find('div', class_='vioxXd rVL_cV')
                sales_div = product.find('div', class_='r6HknA uEPGHT')

                name = name_div.text if name_div else 'N/A'
                price = price_div.text if price_div else 'N/A'
                sales = sales_div.text if sales_div else 'N/A'
                
                results.append({"name": name, "price": f"Rp{price}", "sales": sales})
            except Exception:
                continue

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": f"An error occurred with Selenium: {str(e)}"}), 500

@app.route('/fetch-shopify', methods=['GET'])
def fetch_shopify():
    try:
        if 'YOUR_API_KEY' in SHOP_URL:
            # Shopify bilgileri girilmemişse, sahte veri döndür.
            return jsonify([
                {"name": "Demo Product 1: Awesome T-Shirt", "price": "25.00 USD"},
                {"name": "Demo Product 2: Cool Mug", "price": "15.50 USD"}
            ])
            
        shopify.ShopifyResource.set_site(SHOP_URL)
        products = shopify.Product.find(limit=5)
        results = [{"name": p.title, "price": f"{p.variants[0].price} {p.currency}"} for p in products]
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": f"Failed to connect to Shopify: {e}"}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)