import websocket
import re
import os
from driver import Driver
from subprocess import Popen

try:
    import thread
except ImportError:
    import _thread as thread
import time

driver = Driver()

def on_error(ws, error):
    driver.stop()
    print(error)

def on_close(ws):
    driver.stop()
    print("### closed ###")

def handle_kbsignal(ws, kbsignal):
    print('kbsignal: ' + str(kbsignal))
    search = re.search('\"key\":(\d+),\"pulse\":\"(\w+)\"', kbsignal)
    if search is not None:
        key = search.group(1)
        pulse = search.group(2)
        print('Key: ' + key + " - pulse: " + pulse)
        signals.get(str(key), unknown)(pulse, key)
    else:
        print("Invalid kbsignal")

def enable_engine(pulse, key):
    print('enabling engine')
    driver.stop()

def disable_engine(pulse, key):
    print('disabling engine')
    driver.stop()

def up(pulse, key):
    if pulse == 'down':
        driver.move_forward()
    elif pulse == 'up':
        driver.stop(Driver.LINEAR)

def down(pulse, key):
    if pulse == 'down':
        driver.move_backward()
    elif pulse == 'up':
        driver.stop(Driver.LINEAR)

def left(pulse, key):
    if pulse == 'down':
        driver.move_left()
    elif pulse == 'up':
        driver.stop(Driver.ANGULAR)

def right(pulse, key):
    if pulse == 'down':
        driver.move_right()
    elif pulse == 'up':
        driver.stop(Driver.ANGULAR)

def unknown(pulse, key):
    print('unknown keyboard signal')

def play_audio(pulse, key):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if pulse == "down":
        Popen(["rosrun", "sound_play", "play.py", os.path.join(current_dir, "audio", str(key) + ".wav")])

signals = { '38': up,
            '40': down,
            '37': left,
            '39': right,
            '69': enable_engine,
            '68': disable_engine,
            '49': play_audio,
            '50': play_audio,
            '51': play_audio,
            '52': play_audio,
            '53': play_audio,
            '54': play_audio
            }

def start():
    driver.start()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://hackweek-reminder-bot.herokuapp.com/socket.io/?EIO=3&transport=websocket&robot=true",
                              on_message = handle_kbsignal,
                              on_error = on_error,
                              on_close = on_close)
    while True:
        ws.run_forever()
