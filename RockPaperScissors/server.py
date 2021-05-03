from flask import Flask, request
# import netifaces as ni

from rock_paper_scissor import main as runRoPSGame
from rock_paper_scissor import startSample
app = Flask(__name__)


@app.route("/")
def index():
    return "Server start"

@app.route("/startGame")
def runGame():
    runRoPSGame()
    return "Game completed"

@app.route("/playSampleRhythm")
def showSample():
    startSample()
    return "Sample Complete"


if __name__ == "__main__":
    # app.run(host="192.168.86.77", port=6000, debug=True)
    app.run(host="192.168.86.77", port=5500,debug=True)

    