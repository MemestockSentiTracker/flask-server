
import json
import yfinance as yf
from flask import Flask, request, render_template, g, redirect, Response, abort

app = Flask(__name__)

@app.route('/')
def homepage():
    return "<h1>hello world</h1>"

@app.route('/price/<stock>')
def get_stock_price(stock):
  
    s = yf.Ticker(stock)
    hist = s.history(period="3mo")
    db = hist.to_dict()

    price = dict()
    for day, p in db['Close'].items():
        price[str(day)[:10]] = round(p, 2)
    
    data = {
        'statusCode': 200,
        'body': {
            # 'text': text,
            # 'scores': s,
            'stock': stock,
            'price_date': str(price)
        }
    }

  
    return Response(json.dumps(data))

from textblob import TextBlob

@app.route('/sentiscore')
def get_senti_score():
    request_data = request.get_json()
    if not request_data:
        return Response(json.dumps({"msg": 'no request data'}))

    text = request_data['text'] if 'text' in request_data else ''
    blob = TextBlob(text)
    s = []
    for sentence in blob.sentences:
        s.append(sentence.sentiment.polarity)

    data = {
        'statusCode': 200,
        'body': {
            'text': text,
            'scores': s,
        }
    }  
    return Response(json.dumps(data))

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)