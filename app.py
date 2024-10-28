from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# Your Imgur API credentials
IMGUR_ACCESS_TOKEN = "91d1a9d2c4c818a932999d40ea80b780b18a2f94"

def upload_image_to_imgur(image_data):
    """Uploads the image to Imgur and returns the link."""
    url = "https://api.imgur.com/3/image"
    headers = {
        "Authorization": f"Bearer {IMGUR_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Prepare the data for the request
    data = {
        "image": image_data.split(",")[1],  # Use base64 string
        "type": "base64"
    }
    
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        return None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """Endpoint to handle image uploads."""
    data = request.json.get("image")
    if not data:
        return jsonify({"error": "No image data found"}), 400

    image_url = upload_image_to_imgur(data)
    
    if image_url:
        return jsonify({"link": image_url}), 200
    else:
        return jsonify({"error": "Failed to upload image"}), 500

if __name__ == "__main__":
    app.run(debug=True)
