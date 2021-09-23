import time
import pyupbit
import datetime

access = "aqoS4xZuPqGQblne6gAYzptfrgL9rEWtCcv7u9RI"
secret = "Pq8MFd0bVDYimcKyLSjS3v6sYxS8FTFkT2LXFzsa"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
market_name = "KRW-ETH"
coin_name = "ETH"
k = 0.1
fee = 0.0005
min_order_cost = 5000
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(market_name)
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price(market_name, k)
            current_price = get_current_price(market_name)
            if target_price < current_price:
                krw_amount = get_balance("KRW")
                if krw_amount > min_order_cost:
                    upbit.buy_market_order(market_name, krw_amount*(1-fee))
        else:
            my_coin_total_price = get_balance(coin_name) * get_current_price(market_name)
            if my_coin_total_price > min_order_cost:
                upbit.sell_market_order(market_name, get_balance(coin_name)*(1-fee))
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)