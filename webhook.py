from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Webhook aktif!", 200

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return request.args.get('hub.challenge', 'No challenge'), 200
    if request.method == 'POST':
        data = request.get_json()
        print("Pesan masuk:", data)
        return 'OK', 200

if __name__ == '__main__':
    app.run(port=5000)
# Jalankan aplikasi Flask pada port 5000