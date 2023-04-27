from pya3 import *
import talib as ta
from time import sleep
import datetime
from blog.models import *

# Required Details
api_key = "Zq4pSklHqS9BJptGOPFH87ZQH2Ql8bDo6Dnbpyl55MXnvBO9nWQ7ClxWHaluviuXiOGNAlRR0ZpK2d9PJzRaIkyBakSJ61osnNWUmsDz6VFOHOB9nlPG9eknG5KCOcrd"         # Get from https://a3.aliceblueonline.com      After Login go to "Apps" section and create API
user_id = "AB032684"
EMA_CROSS_SCRIP = "IOC-EQ"
quantity=0
count = 0


f = open('StockCode.json')
data=json.load(f)
CompanyNames=data.keys()


def buy_signal(ins_scrip,quantity):
    print("Inside buy_signal function")
    print(alice.place_order(transaction_type=TransactionType.Buy,
                          instrument=ins_scrip,
                          quantity=quantity,
                          order_type=OrderType.Limit,
                          product_type=ProductType.Delivery,
                          price=1.0,
                          trigger_price=None,
                          stop_loss=None,
                          square_off=None,
                          trailing_sl=None,
                          is_amo=False,
                          order_tag='buy'))


def sell_signal(ins_scrip,quantity):
    print("Inside sell_signal function")
    print(alice.place_order(transaction_type=TransactionType.Sell,
                            instrument=ins_scrip,
                            quantity=quantity,
                            order_type=OrderType.Limit,
                            product_type=ProductType.Delivery,
                            price=5000.0,
                            trigger_price=None,
                            stop_loss=None,
                            square_off=None,
                            trailing_sl=None,
                            is_amo=False,
                            order_tag='sell'))


def calculate_ema(prices, days, smoothing=2):
    ema = []
    for i in range(days):
        # ema.append(sum(prices[:days]) / days)
        ema.append(prices[0])
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) + ema[-1] * (1 - (smoothing / (1 + days))))
    return ema


def EMA_algo(ins_scrip):
    global quantity
    from_datetime = datetime.datetime.now() - datetime.timedelta(days=60)        # From last & days
    to_datetime = datetime.datetime.now()       # To now
    interval = "1"          # ["1", "D"]
    df = alice.get_historical(ins_scrip, from_datetime, to_datetime, interval, indices=False)
    

    # df["ema_5"] = calculate_ema(df["close"], 5)
    # df["ema_13"] = calculate_ema(df["close"], 13)
    df["ema_5"] = ta.EMA(df["close"], timeperiod=5)
    df["ema_13"] = ta.EMA(df["close"], timeperiod=13)
    # print(ema1, ema2)
    print(df)

    for i in df.index[-2:-1]:
        print(df["ema_5"][i], df["ema_13"][i], df["ema_5"][i-1], df["ema_13"][i-1])
        if (df["ema_5"][i] > df["ema_13"][i]) and (df["ema_5"][i-1] <= df["ema_13"][i-1]):
            while True:
                now = datetime.datetime.now()
                print(now.hour, now.minute)
                if now.hour >= 9 and now.minute >= 15:
                    buy_signal(ins_scrip,quantity)
                    break
            count=+1
            #connection.execute("INSERT INTO transactions VALUES (?,?,?)", (EMA_CROSS_SCRIP, 'BUY', now))

        if (df["ema_5"][i] < df["ema_13"][i]) and (df["ema_5"][i-1] >= df["ema_13"][i-1]):
            while True:
                now = datetime.datetime.now()
                print(now.hour, now.minute)
                if now.hour >= 9 and now.minute >= 15:
                    sell_signal(ins_scrip,quantity)
                    break
            count = +1
            #connection.execute("INSERT INTO transactions VALUES (?,?,?)", (EMA_CROSS_SCRIP, 'SELL', now))


def main():
    global alice, user_id, api_key, EMA_CROSS_SCRIP, count,quantity

    while True:
        now = datetime.datetime.now()
        print(now.hour)
        if now.hour == 9 and now.hour < 10:
            alice = Aliceblue(user_id=user_id, api_key=api_key)
            print(alice.get_session_id())       # Get Session ID

            alice.get_contract_master("NSE")
            alice.get_contract_master("BSE")
            alice.get_contract_master("INDICES")

            obj=portfolioDb.objects.all()
            for i in obj:

               cmp=i.cmpnay 
               for j in cmp.items():
                 quantity=j[1]
                 ins_scrip = alice.get_instrument_by_symbol('NSE', EMA_CROSS_SCRIP)
                 EMA_algo(ins_scrip)
        
        sleep(60 * 60)


# if (__name__ == '__main__'):
#     global connection
#     main()

