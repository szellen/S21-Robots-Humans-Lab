from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person
# Will create three concurrently running threads on the server
# One for new connection
# One for receiving messages
# One for sending messages

# GLOBAL CONSTANTS
HOST = ''
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ = 512

# GLOBAL VARIABLES
nao = []
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def send_messages_to_nao(msg, name):
    """
    Send new messages to clients to
    :param msg: bytes["utf8"]
    :param name: String
    :return: None
    """
    for person in nao:
        if (person.name + ": ") != name:
            client = person.client
            client.send(bytes(name, "utf8") + msg)


def client_communication(person):
    """
    Thread to handle all messages from client
    :param client : Person
    :return : None
    """

    client = person.client

    # Get person's name
    name = client.recv(BUFSIZ).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} has joined the server!", "utf8")
    send_messages_to_nao(msg, "")

    if name == "nao":
        nao.append(person)

    run = True
    while run:
        try:
            msg = client.recv(BUFSIZ)
            if msg == bytes("quit", "utf8"):
                client.close()
                if person.name == "nao":
                    nao.remove(person)
                persons.remove(person)
                print(f"[DISCONNECTED] {name} disconnected")
                run = False
            else:
                print(f"{name} : ", msg.decode("utf8"))
                send_messages_to_nao(msg, name + ": ")
        except Exception as e:
            print("[EXCEPTION1]", e)
            run = False

def wait_for_connection():
    """
    Wait for connection from new clients, start new thread once connected
    :param SERVER : SOCKET
    :return : None
    """

    run = True
    while run:
        try:
            client, client_addr = SERVER.accept()
            person = Person(client_addr, client) # Name is set as none and will be assigned later
            persons.append(person)
            print(f"[CONNECTION] {client_addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION2]", e)
            run = False
    print("SERVER CRASHED")

if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) # listen for connections
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
    print("SERVER EXIT")
