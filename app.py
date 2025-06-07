from flask import Flask, request, jsonify, render_template
from aquabotBackend import BeautyBot

app = Flask(__name__)

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
    addressStyle = data.get('addressStyle', '')
    city = data.get('city', '')
    waitingForConcern = data.get('waitingForConcern', False)
    waitingForSubQuestion = data.get('waitingForSubQuestion', False)
    currentSubQuestion = data.get('currentSubQuestion', None)
    message = data.get('message', '')
    bot = BeautyBot(addressStyle, city, waitingForConcern, waitingForSubQuestion, currentSubQuestion)
    response = bot.getHealthAdvice(message)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False, port=3000)