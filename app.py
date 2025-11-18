from flask import Flask, request, jsonify
import json
import os
import requests  # <-- 1. Import requests

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Ambil semua kredensial dari .env
VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN")
ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")

# Pastikan token ada
if not VERIFY_TOKEN or not ACCESS_TOKEN or not PHONE_NUMBER_ID:
    print("ERROR: Pastikan semua variabel .env (VERIFY_TOKEN, ACCESS_TOKEN, PHONE_NUMBER_ID) sudah diisi")
    exit()

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # ... (Logika GET Anda sama, tidak berubah) ...
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            print("VERIFICATION_FAILED")
            return "Forbidden", 403

    elif request.method == 'POST':
        # Ini adalah bagian untuk menerima pesan masuk
        data = request.get_json()
        
        # Cetak data yang masuk (untuk debugging)
        print("Received message data:")
        print(json.dumps(data, indent=2))

        # --- LOGIKA BALAS PESAN DIMULAI DI SINI ---
        
        try:
            # Periksa apakah ini pesan teks
            if (data.get('entry') and 
                data['entry'][0].get('changes') and 
                data['entry'][0]['changes'][0].get('value') and 
                data['entry'][0]['changes'][0]['value'].get('messages') and
                data['entry'][0]['changes'][0]['value']['messages'][0]):
                
                message = data['entry'][0]['changes'][0]['value']['messages'][0]
                
                # Hanya balas jika tipenya 'text'
                if message.get('type') == 'text':
                    # Ambil nomor pengirim
                    from_number = message['from']
                    
                    # Ambil isi pesan
                    msg_body = message['text']['body']
                    
                    # Buat balasan
                    reply_body = f"Anda mengirim: '{msg_body}'. Webhook berhasil!"
                    
                    # Panggil fungsi untuk mengirim balasan
                    send_whatsapp_message(from_number, reply_body)
                    
        except Exception as e:
            print(f"Error memproses pesan: {e}")
            pass # Jangan crash, lanjutkan saja

        # Kirim balasan 'OK' (200) agar Meta tahu kita sudah menerima
        return "OK", 200

# Fungsi baru untuk mengirim pesan
def send_whatsapp_message(to_number, text_message):
    print(f"Mengirim balasan ke {to_number}...")
    
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "body": text_message
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    # Cetak respons dari Meta (untuk debugging pengiriman)
    print(f"Status Code Kirim: {response.status_code}")
    print(f"Response Body Kirim: {response.json()}")

# ... (Bagian 'if __name__ == "__main__":' Anda sama, tidak berubah) ...
if __name__ == '__main__':
    app.run(port=5000, debug=True)