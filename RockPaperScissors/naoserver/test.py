from client import Client
import time
from threading import Thread


c1 = Client("nao")
c2 = Client("Reco")
c3 = Client("AppleWatch")


def update_messages():
    msgs = []
    run = True
    while run:
        time.sleep(0.1)
        new_messages = c1.get_messages()
        msgs.extend(new_messages)

        for msg in new_messages:
            print(msg)

            if msg == c1.name + ": " + "quit":
                run = False
                break

Thread(target=update_messages).start()


c1.send_message("Hi")
time.sleep(3)
c2.send_message("Rock")
time.sleep(3)
c3.send_message("155")
time.sleep(3)
c2.send_message("Paper")
time.sleep(2)
c1.disconnect()
time.sleep(2)
c2.disconnect()
time.sleep(2)
c3.disconnect()
