import time
from datetime import datetime
import json

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth.decorators import login_required
from security_db.models import Security, PyfolioUser

# Create your views here.

@login_required
def home(request):
    user = PyfolioUser.objects.get(id=request.user.id)

    tickers = [investment.security.ticker for investment in user.investments]
    amounts = [investment.amount for investment in user.investments]

    options = {
        'series': amounts,
        'labels': tickers,
        'chart': {
            'type': 'donut',
        },
        'responsive': [{
            'breakpoint': 480,
            'options': {
                'chart': {
                    'width': 200
                },
                'legend': {
                    'position': 'bottom'
                }
            }
        }]
    };

    return render(request, 'home.html', {'pie_options': json.dumps(options)})


def browse(request):
    #all_securities = Security.objects.order_by(ticker).all()
    all_securities = Security.objects.all()
    paginator = Paginator(all_securities, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'browse.html', {'page_obj': page_obj})



def security(request, ticker):
    try:
        security = Security.get_by_ticker(ticker) 
        prices = security.prices()
    except:
        # TODO: correct exception
        raise Http404("Security does not exist")

    # build candleplot data
    data = []
    for price in prices:
        #timestamp = int(time.mktime(price.date.timetuple()))
        timestamp = str(datetime(price.date.year, price.date.month, price.date.day))
        candle = [price.open, price.low, price.high, price.close]
        data.append({"x": timestamp, "y": candle})

    candle_options = {
            "series": [{
                "data": data
            }],
            "chart": {
                "type": "candlestick",
                "id": "candles",
                "toolbar": {
                    "autoSelected": "pan",
                    "show": "false"
                }
            },
            "title": {
                "text": security.name,
                "align": "left"
            },
            "xaxis": {
                "type": "datetime"
            }
    }

    return render(request, 
                  'security.html', {'security': security,
                                    'candle_options': json.dumps(candle_options)}
                  )
