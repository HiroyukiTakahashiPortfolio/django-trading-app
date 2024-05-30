# trading/views.py

import requests
from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import base64

def get_crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '1'
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data['prices']

def plot_chart(prices):
    x = [price[0] for price in prices]
    y = [price[1] for price in prices]

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label='Bitcoin Price')
    plt.xlabel('Time')
    plt.ylabel('Price in USD')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + string.decode('utf-8')

    return uri

def home(request):
    prices = get_crypto_data()
    chart = plot_chart(prices)
    return render(request, 'trading/home.html', {'chart': chart})
