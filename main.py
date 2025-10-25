from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__, static_folder='frontend')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json', 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest'
}

@app.route('/analyze-store', methods=['POST'])
def analyze_store():
    data = request.json
    store_url = data.get('store_url')
    if not store_url or 'shopee.co.id' not in store_url:
        return jsonify({"error": "Please provide a valid Shopee Indonesia store URL."}), 400
    try:
        username = store_url.strip('/').split('/')[-1].split('?')[0]
        shop_detail_url = f'https://shopee.co.id/api/v4/shop/get_shop_detail?username={username}'
        shop_response = requests.get(shop_detail_url, headers=HEADERS)
        shop_response.raise_for_status()
        shop_data = shop_response.json()['data']
        shop_id = shop_data['shopid']
        items_url = f'https://shopee.co.id/api/v4/shop/search_items?limit=30&offset=0&shopid={shop_id}'
        items_response = requests.get(items_url, headers=HEADERS)
        items_response.raise_for_status()
        items_data = items_response.json()['items']
        results = {
            "shop_info": {"name": shop_data.get('name', 'N/A'), "follower_count": shop_data.get('follower_count', 0), "rating_star": round(shop_data.get('rating_star', 0), 2), "total_products": shop_data.get('item_count', 0)},
            "products": []
        }
        for item in items_data:
            price = item['price'] / 100000
            results['products'].append({"name": item['name'], "price": f"Rp{int(price):,}".replace(',', '.'), "sold": item.get('historical_sold', 0), "likes": item.get('liked_count', 0), "image": f"https://cf.shopee.co.id/file/{item['image']}_tn"})
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": f"Could not fetch data. The store might be private or the URL is incorrect. Details: {str(e)}"}), 500

@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
