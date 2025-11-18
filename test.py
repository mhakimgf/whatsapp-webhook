import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Ganti <access token> dengan token Anda yang sebenarnya
# Ambil semua kredensial dari .env
VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN")
ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")

# 2. URL Endpoint (pastikan Phone Number ID Anda sudah benar)
url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

# 3. Headers (sebagai dictionary Python)
headers = {
    'Authorization': f"Bearer {ACCESS_TOKEN}",
    'Content-Type': 'application/json'
}

# 4. Data (sebagai dictionary Python)
#    Library 'requests' akan otomatis mengubahnya menjadi JSON
# data = {
#     "messaging_product": "whatsapp",
#     "to": "628112340504",
#     "type": "template",
#     "template": {
#         "name": "hello_world",
#         "language": {
#             "code": "en_US"
#         }
#     }
# }
# 4. Data (TIPE TEKS BIASA - INI YANG AKAN BERHASIL)
data = {
    "messaging_product": "whatsapp",
    "to": "81220815825",
    # "to": "628112340504",
    "type": "text",  # <--- Ganti jadi Teks
    "text": {
        "body": "Ini adalah pesan tes dari test.py!" 
    }
}
# 5. Kirim request POST
#    Menggunakan 'json=data' adalah cara terbaik
response = requests.post(url, headers=headers, json=data)

# 6. Tampilkan hasil dari server
print(f"Status Code: {response.status_code}")
print("Response Body:")
try:
    # Tampilkan balasan dalam format JSON yang rapi
    print(json.dumps(response.json(), indent=2))
except requests.exceptions.JSONDecodeError:
    # Jika balasan bukan JSON (misal: error teks)
    print(response.text)