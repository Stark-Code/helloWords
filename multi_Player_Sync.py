import datetime
import time


def sync_Start():
    while True:
        seconds = int(time.time())
        # print(seconds)
        if seconds % 10 == 0:
            print('10 seconds interval found')
            return True
        time.sleep(1)
