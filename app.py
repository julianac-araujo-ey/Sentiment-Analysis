from flask import Flask, request, render_template
from utils import getScore

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST'])
def post_tweet():
    input_text = request.form['input_text']
    ps = getScore(text=input_text)
    positive_per = round(ps['pos'], 1) * 100
    negative_per = round(ps['neg'], 1) * 100
    neutral_per = round(ps['neu'], 1) * 100

    return render_template('sentiment.html', positive=positive_per, negative=negative_per,
                           neutral=neutral_per)


@app.route('/test')
def test():
    return 'flask is working properly'


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000, threaded=True)
