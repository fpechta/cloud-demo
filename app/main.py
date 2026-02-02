from flask import Flask, render_template, jsonify
from azure.storage.blob import BlobServiceClient
import os
import datetime
import requests

app = Flask(__name__)

# Azure Blob Storage Connection
AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
CONTAINER_NAME = "health-logs"

def log_to_blob(message):
    """Logs zu Azure Blob Storage schreiben"""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(
            container=CONTAINER_NAME,
            blob=f"log-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        )
        blob_client.upload_blob(message)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/')
def index():
    """Dashboard anzeigen"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Health Check Endpoint für Edeka Services"""
    services = [
        {"name": "EDEKA Hauptwebsite", "url": "https://www.edeka.de", "category": "Public"},
        {"name": "EDEKA Online-Shop", "url": "https://www.edeka24.de", "category": "E-Commerce"},
        {"name": "EDEKA Verbund", "url": "https://verbund.edeka", "category": "Corporate"}
    ]
    
    results = []
    for service in services:
        try:
            response = requests.get(service['url'], timeout=10)  # Timeout auf 10s erhöht
            status = "UP" if response.status_code == 200 else "DOWN"
            response_time = round(response.elapsed.total_seconds() * 1000, 2)
        except Exception as e:
            status = "DOWN"
            response_time = 0
            print(f"Error checking {service['name']}: {e}")  # Debug
        
        results.append({
            "name": service['name'],
            "category": service['category'],
            "status": status,
            "response_time": response_time,
            "timestamp": datetime.datetime.now().isoformat()
        })
    
    # Log zu Azure Blob Storage
    log_message = f"Health check at {datetime.datetime.now()}: {results}"
    log_to_blob(log_message)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)