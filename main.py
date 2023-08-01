from flask import Flask, request, jsonify
import requests
from kite_trade import *
from datetime import  datetime
import os

def telegrammessage(message):
    token = os.getenv("TelegramToken")
    chat_id = os.getenv("chatid")
    send = 'https://api.telegram.org/bot'+token+'/sendMessage?chat_id='+chat_id+'&parse_mode=MarkdownV2&text='+message
    response = requests.get(send)
    return response.json()
app = Flask(__name__)


@app.route(f'/bluealgocapital', methods=['POST'])
def handle_post_request():
    data = request.get_json()
    print("Tradingview log")
    d = data[0]
    print(str(d))
    if d.get("buy_or_sell") == 'BUY':
        kite = KiteApp(enctoken=str(d.get("enctoken")))
        if d.get("product_type") == "MIS":
            product = kite.PRODUCT_MIS
        if d.get("product_type") == "NRML":
            product = kite.PRODUCT_NRML
        if d.get("exchange") == "NSE":
            exchange = kite.EXCHANGE_NSE
        if d.get("exchange") == "NFO":
            exchange = kite.EXCHANGE_NFO
        if d.get("exchange") == "MCX":
            exchange = kite.EXCHANGE_MCX



        try:

            order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                     exchange=exchange,
                                     tradingsymbol=d.get("tradingsymbol"),
                                     transaction_type=kite.TRANSACTION_TYPE_BUY,
                                     quantity=int(d.get("quantity")),
                                     product=product,
                                     order_type=kite.ORDER_TYPE_MARKET,
                                     price=None,
                                     validity=None,
                                     disclosed_quantity=None,
                                     trigger_price=None,
                                     squareoff=None,
                                     stoploss=None,
                                     trailing_stoploss=None,
                                     tag="pinepro")

            print(f'{order} at [{datetime.now()}]')
            # now = datetime.now()
            #
            # # Convert the datetime object to a string
            # date_string = now.strftime("%Y-%m-%d %H:%M:%S.%f")
            #
            # # Escape the dashes
            # escaped_string = date_string.replace("-", "\\-").replace(".", "\\.")

            telegrammessage(f'Buy order of {d.get("tradingsymbol")} placed with quantity {d.get("quantity")} ,order id is {order}')
        except Exception as e:
            print(f"Erro:{e}")
            telegrammessage(f'send valid messaage or order failed') #todo send valid error to telegram
    if d.get("buy_or_sell") == 'SELL':
        kite = KiteApp(enctoken=str(d.get("enctoken")))
        if d.get("product_type") == "MIS":
            product = kite.PRODUCT_MIS
        if d.get("product_type") == "NRML":
            product = kite.PRODUCT_NRML
        if d.get("exchange") == "NSE":
            exchange = kite.EXCHANGE_NSE
        if d.get("exchange") == "NFO":
            exchange = kite.EXCHANGE_NFO
        if d.get("exchange") == "MCX":
            exchange = kite.EXCHANGE_MCX
        try:

            order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                     exchange=exchange,
                                     tradingsymbol=d.get("tradingsymbol"),
                                     transaction_type=kite.TRANSACTION_TYPE_SELL,
                                     quantity=int(d.get("quantity")),
                                     product=product,
                                     order_type=kite.ORDER_TYPE_MARKET,
                                     price=None,
                                     validity=None,
                                     disclosed_quantity=None,
                                     trigger_price=None,
                                     squareoff=None,
                                     stoploss=None,
                                     trailing_stoploss=None,
                                     tag="pinepro")

            print(f'{order} at [{datetime.now()}]')
            telegrammessage(f'Placed {order} at [{datetime.now()}]')
        except Exception as e:
            print(f"Erro:{e}")
            telegrammessage(f'send valid messaage or order failed') #todo send valid error to telegram



    if d.get("closeall") is True:
        kite = KiteApp(enctoken=d.get("enctoken"))
        position = kite.positions()
        for item in position['day']:
            if item['exchange'] == 'NFO':
                if item['quantity'] > 0:
                    print(f"Placing sell order for {item['tradingsymbol']} with quantity {item['quantity']}")
                    telegrammessage(f"Placing sell order for {item['tradingsymbol']} with quantity {item['quantity']}")

                    order = kite.place_order(variety=kite.VARIETY_REGULAR,
                                             exchange=item['exchange'],
                                             tradingsymbol=item['tradingsymbol'],
                                             transaction_type=kite.TRANSACTION_TYPE_SELL,
                                             quantity=item['quantity'],
                                             product=item['product'],
                                             order_type=kite.ORDER_TYPE_MARKET,
                                             price=None,
                                             validity=None,
                                             disclosed_quantity=None,
                                             trigger_price=None,
                                             squareoff=None,
                                             stoploss=None,
                                             trailing_stoploss=None,
                                             tag="pinepro")

                    print(f'{order} at [{datetime.now()}]')
                    telegrammessage(f'Placed {order} at [{datetime.now()}]')

                    # Replace with your function call to place a sell order
                elif item['quantity'] < 0:
                    print(f"Placing buy order for {item['tradingsymbol']} with quantity {abs(item['quantity'])}")
                    # Replace with your function call to place a buy order
                else:
                    print(f"No action for {item['tradingsymbol']} as quantity is 0")


    return '200'



# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=80)
