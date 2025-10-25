from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

# SENİN API ANAHTARIN GÜVENLİ BİR ŞEKİLDE BURADA
ETSY_API_KEY = "34axrr0o1tzjvfcdn2mexpp4"
ETSY_API_URL = "https://openapi.etsy.com/v3/application/listings/"

@app.route('/get-listing-details', methods=['POST'])
def get_listing_details():
    data = request.json
    listing_id = data.get('listing_id')

    if not listing_id:
        return jsonify({"error": "Listing ID is required."}), 400

    headers = {
        'x-api-key': ETSY_API_KEY
    }
    
    # İSTENEBİLECEK EN DEĞERLİ VERİLERİ İSTİYORUZ: Mağaza, Resimler, Etiketler
    params = {
        'includes': 'Shop,Images,taxonomy_path,tags'
    }

    try:
        response = requests.get(f"{ETSY_API_URL}{listing_id}", headers=headers, params=params)
        response.raise_for_status()
        listing_data = response.json()

        # MÜMKÜN OLAN TÜM VERİLERİ TEMİZ BİR ŞEKİLDE AYIKLA
        shop_data = listing_data.get('shop', {})
        main_image = listing_data.get('images', [{}])[0]

        cleaned_data = {
            "title": listing_data.get("title", "N/A"),
            "description": listing_data.get("description", "N/A"),
            "url": listing_data.get("url", "#"),
            "price": f"{listing_data.get('price', {}).get('amount', 0) / listing_data.get('price', {}).get('divisor', 100)} {listing_data.get('price', {}).get('currency_code', '')}",
            "quantity": listing_data.get("quantity", "N/A"),
            "views": listing_data.get("views", "N/A"),
            "num_favorers": listing_data.get("num_favorers", "N/A"),
            "tags": listing_data.get("tags", []),
            "category": " > ".join(listing_data.get("taxonomy_path", [])),
            "creation_date": datetime.fromtimestamp(listing_data.get('creation_timestamp', 0)).strftime('%Y-%m-%d'),
            "shop_name": shop_data.get('shop_name', 'N/A'),
            "shop_url": shop_data.get('url', '#'),
            "main_image_url": main_image.get('url_fullxfull', '')
        }
        return jsonify(cleaned_data)

    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"Could not fetch data. Check your Listing ID. (HTTP {e.response.status_code})"}), 500
    except Exception as e:
        return jsonify({"error": f"An unknown error occurred: {str(e)}"}), 500
