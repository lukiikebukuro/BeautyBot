from flask import Flask, request, jsonify, render_template
from aquabotBackend import BeautyBot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify_city', methods=['POST'])
def verify_city():
    data = request.get_json()
    bot = BeautyBot("", "")
    city = bot.match_city(data.get('city', ''))
    return jsonify({'valid': city is not None, 'city': city})

@app.route('/get_hardness', methods=['POST'])
def get_hardness():
    data = request.get_json()
    bot = BeautyBot("", data.get('city', ''))
    reply = bot.get_hardness_reply(data.get('city', ''))
    return jsonify({'reply': reply})

@app.route('/beautybot', methods=['POST'])
def beautybot():
    data = request.get_json()
    print(f"Debug: Otrzymane dane: {data}")
    addressStyle = data.get('addressStyle', '')
    city = data.get('city', '')
    waitingForCategory = data.get('waitingForCategory', False)
    waitingForProblem = data.get('waitingForProblem', False)
    selectedCategory = data.get('selectedCategory', '')
    message = data.get('message', '')
    bot = BeautyBot(addressStyle, city, waitingForCategory, waitingForProblem, selectedCategory)
    print(f"Debug: Wywołuję getHealthAdvice z message='{message}'")
    response = bot.getHealthAdvice(message)
    return jsonify(response)

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)