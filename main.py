import re
import time
import ccxt as ccxt
from telethon import TelegramClient, sync

import chatGPT
import config

client = TelegramClient('Testtest2', config.api_id, config.api_hash).start()
bybit = ccxt.bybit({
    'enableRateLimit': True,
    'apiKey': config.api_key,
    'secret': config.secret_key
})

ids = []
my_message_ids = []
dialogs = []


def find_dialogs():
    for dialog in client.get_dialogs():
        if dialog.name.startswith("FOXCRYPTOSIGNAL") or dialog.name.startswith("79 SIGNALS") or dialog.name.startswith(
                "Cryptosignals.Org") or dialog.name.startswith("Wolfx Signals"):
            dialogs.append(dialog)


def get_last_messages_from_dialogs():
    for dialog in dialogs:
        messages = client.get_messages(dialog, 1)
        for m in messages:
            message = str(m.message).upper()
            if message.find("ENTRY") != -1 and message.find("LEVERAGE") != -1 and m.id not in ids:
                ids.append(m.id)
                print(dialog.name)
                print(m.id)
                client.send_message("me", message)
                return True
    return False


def check_if_message_is_correct():
    message = client.get_messages("me", 1)[0].message.upper()
    if message.find("ENTRY") != -1 and message.find("LEVERAGE") != -1 and client.get_messages("me", 1)[0].id not in my_message_ids:
        my_message_ids.append(client.get_messages("me", 1)[0].id)
        info = chatGPT.get_message_info().replace("+", "").replace("TO", "").replace("STOP LOSS: ", "").split("\n")
        coin = info[0].replace("SYMBOL: ", "").replace("USDT", "").replace("/", "")
        order_type = info[1].replace("SIDE: ", "").replace("SIDE:", "")
        entry = info[2].replace("-", ",").replace("ENTRY ZONE: ", "").split(",")
        targets = info[3].replace("TAKE PROFITS: ", "").replace("TAKE PROFIT: ", "").split(", ")
        stop_loss = info[4].replace("STOP LOSS: ", "").replace("SP LOSS: ", "")

        print("check if correct")
        print(coin)
        print(order_type)
        print(entry)
        print(targets)
        print(stop_loss)
        symbol = coin + "USDT"

        set_position_mode_to_one_way(symbol)
        set_margin_mode_and_leverage(symbol)
        create_position(symbol, order_type, entry, targets, stop_loss)


def create_position(symbol, order_type, entry, targets, stop_loss):
    balance_USDT = bybit.fetch_free_balance()['USDT']
    print("USDT BALANCE: " + str(balance_USDT))
    print("Symbol: " + symbol)
    if order_type.find("LONG") or order_type.find("BUY"):
        side = "buy"
        op = "sell"
    else:
        side = "sell"
        op = "buy"
    print("Side: " + side)
    price = bybit.fetch_ticker(symbol)['last']
    print("Price now: " + str(price))
    qty = round(100 / price, 3)
    print("Qty: " + str(qty))
    print("#################################################")
    print("Entry 1: " + str(entry[0]))
    print(price)
    print("Entry 2: " + str(entry[1]))
    for t in targets:
        print(t)

    bybit.cancel_all_orders(symbol)
    bybit.create_order(symbol, "market", side, qty, params={"stopLoss": stop_loss})
    create_targets(symbol, op, targets)


def create_targets(symbol, op, targets):
    while 1 == 1:
        time.sleep(5)
        qty = float(bybit.fetch_positions(symbol)[0]['info']['size']) / (len(targets))
        if qty > 0:
            print("TAKE PROFITY")
            print("QTY: " + str(qty))
            time.sleep(5)
            for t in targets:
                print("Targets: " + str(t))
                bybit.create_order(symbol, "limit", op, qty, float(t), params={"reduceOnly": True})
            print("Targety ustawione")
            break

def set_margin_mode_and_leverage(symbol):
    positionInfo = str(bybit.fetch_position(symbol)).split("marginMode': '")[1]
    margin_mode = positionInfo.split("'")[0]
    if margin_mode != "isolated":
        bybit.set_margin_mode("ISOLATED", symbol + ":USDT", params={'leverage': 10})
    else:
        bybit.set_leverage(3.58, symbol)
        bybit.set_leverage(10, symbol)


def set_position_mode_to_one_way(symbol):
    if bybit.fetch_position(symbol)['info']['positionIdx'] == "1":
        bybit.set_position_mode(False, symbol + ":USDT")
        print("Position mode set to One-Way")
    else:
        print("Position mode is One-Way")

#########################################################################################
find_dialogs()

while 1 == 1:
    try:
        get_last_messages_from_dialogs()
        check_if_message_is_correct()
        time.sleep(5)
    except Exception as e:
        client.send_message("me", "Cos sie zjebało")
        print("Nie dziala")
        pass

client.disconnect()