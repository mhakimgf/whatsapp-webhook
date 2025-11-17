from flask import Flask, request, jsonify
import json
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

# BUAT TOKEN VERIFIKASI ANDA DI SINI
# Ini adalah string rahasia yang hanya Anda dan Meta yang tahu
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Ini adalah bagian verifikasi webhook
        # Meta akan mengirimkan 'hub.mode', 'hub.challenge', dan 'hub.verify_token'
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        # Periksa apakah mode adalah 'subscribe' dan token-nya benar
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            # Jika benar, kembalikan 'hub.challenge'
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Jika salah, kembalikan 'Forbidden'
            print("VERIFICATION_FAILED")
            return "Forbidden", 403

    elif request.method == 'POST':
        # Ini adalah bagian untuk menerima pesan masuk
        data = request.get_json()

        # Cetak data yang masuk ke terminal (untuk debugging)
        print("Received message data:")
        print(json.dumps(data, indent=2))

        # Proses data pesan di sini (misalnya, balas pesan)
        # ... (logika bisnis Anda) ...

        # Kirim balasan 'OK' (200) agar Meta tahu kita sudah menerima
        return "OK", 200

if __name__ == '__main__':
    # Jalankan server di port 5000 (default Flask)
    app.run(port=5000, debug=True)