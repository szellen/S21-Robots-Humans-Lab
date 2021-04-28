# Importing System Libraries
from copy import deepcopy
from time import sleep, time
from datetime import datetime
from requests import get

# Importing 3rd-Party Libraries
import netifaces as ni
from flask import Flask, request

ROBOT_SERVER_IP = "http://192.168.86.77:5500/runGame"

# System Synchronization Parameters
LATENCY = 0.555

# Auxiliary Variables 
timestamp = []
recognition_timestamp = []
bpm_timestamp = []

# Game Parameters
bpm = 90
sample_count = 10
game_start_time = 0
round_count = 0

game_logs = []


app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Rock Paper Scissor Server"

# -----------------------------------------------
# Game Setting APIs
# -----------------------------------------------
@app.route("/bpm", methods=["GET"])
def get_bpm():
    return str(bpm)

@app.route("/setBpm", methods=["GET"])
def set_bpm():
    global bpm
    bpm = request.args.get("bpm")
    return "BPM set to " + bpm

@app.route("/sampleCount", methods=["GET"])
def get_sample_count():
    return str(sample_count)

@app.route("/setSampleCount", methods=["GET"])
def set_sample_count():
    global sample_count
    sample_count = request.args.get("sampleCount")
    return "Sample count set to " + sample_count

# -----------------------------------------------
# Robot Movement Timestamp APIs
# -----------------------------------------------
@app.route("/timestamps", methods=["GET"])
def get_timestamps():
    return str(timestamp)

@app.route("/addTimestamp", methods=["GET"])
def add_timestamp():
    global timestamp
    timestamp.append(request.args.get("data"))
    
    sleep(2)

    round_count, winner, robot_move, human_move, move_delay, robot_rhythm, human_rhythm = compute_results()

    game_result = "Round Count: {} | Winner: {} | Robot's Move: {} | Human's Move: {} | Move Delay: {} | Robot's Rhythm: {} | Human's Rhythm: {}".format(round_count, winner, robot_move, human_move, move_delay, robot_rhythm, human_rhythm)
    print(game_result)

    return winner + "_" + str(move_delay) + "_" + str(human_rhythm - robot_rhythm)

@app.route("/clearTimestamps", methods=["GET"])
def clear_timestamps():
    global timestamp
    timestamp.clear()
    return "Timestamp cleared"

# -----------------------------------------------
# Human Gesture Recognition Timestamp APIs
# -----------------------------------------------
@app.route("/recognitionTimestamps", methods=["GET"])
def get_recognition_timestamps():
    return str(recognition_timestamp)

@app.route("/addRecognitionTimestamp", methods=["GET"])
def add_recognition_timestamp():
    global recognition_timestamp
    recognition_timestamp.append(request.args.get("data"))
    return "Recognition Timestamp added"

@app.route("/clearRecognitionTimestamps", methods=["GET"])
def clear_recognition_timestamps():
    global recognition_timestamp
    recognition_timestamp.clear()
    return "Recognition Timestamp cleared"

# -----------------------------------------------
# Human BPM Estimation Timestamp APIs
# -----------------------------------------------
@app.route("/BPMTimestamps", methods=["GET"])
def get_BPM_timestamps():
    return str(bpm_timestamp)

@app.route("/addBPMTimestamp", methods=["GET"])
def add_bpm_timestamp():
    global bpm_timestamp
    bpm_timestamp.append(request.args.get("data"))
    return "BPM Timestamp added"
    
@app.route("/clearBPMTimestamps", methods=["GET"])
def clear_bpm_timestamps():
    global bpm_timestamp
    bpm_timestamp.clear()
    return "BPM Timestamps cleared"

# -----------------------------------------------
# Miscellaneous APIs
# -----------------------------------------------
@app.route("/latency", methods=["GET"])
def latency():
    timeClient = float(request.args.get("time"))
    timeServer = time()
    print("Latency: {}".format(timeClient - timeServer))
    return "{}".format(timeClient - timeServer)

@app.route("/gamelogs")
def get_game_logs():
    global game_logs
    return str(game_logs)

@app.route("/startGame")
def start_game():
    global game_start_time, round_count
    game_start_time = str(datetime.now())
    round_count = 0
    get(ROBOT_SERVER_IP)
    return "Done"

def compute_results():
    global round_count

    robot_data = timestamp[len(timestamp) - 1]
    robot_move = robot_data.split("_")[0]
    robot_time = float(robot_data.split("_")[1]) - LATENCY

    rt = deepcopy(recognition_timestamp)
    bt = deepcopy(bpm_timestamp)

    bpm_time = 0
    bpm_value = 0

    gesture_time = 0
    gesture_value = "NaN"

    # Estimating BPM Value and Timestamp
    min_time = 9999
    for idx, entry in enumerate(bt):
        temp_bpm = float(entry.split("_")[0])
        temp_time = float(entry.split("_")[1])

        if abs(robot_time - temp_time) < min_time:
            min_time = abs(temp_time - robot_time)
            bpm_time = temp_time
            bpm_value = temp_bpm
    clear_bpm_timestamps()

    # Estimating Gesture Value and Timestamp
    min_time = 9999
    for idx, entry in enumerate(rt):
        temp_gesture = entry.split("_")[0]
        temp_time = float(entry.split("_")[1])

        if abs(robot_time - temp_time) < min_time:
            min_time = abs(temp_time - robot_time)
            gesture_time = temp_time
            gesture_value = temp_gesture
    clear_recognition_timestamps()

    round_count += 1
    robot_move = robot_move
    human_move = gesture_value
    move_delay = bpm_time - robot_time
    robot_rhythm = bpm
    human_rhythm = bpm_value
    winner = evaluate_winner(robot_move, human_move)

    game_logs.append(
        {
            'game_start_time': game_start_time,
            'round_count': round_count,
            'winner': winner,
            'robot_move': robot_move,
            'human_move': human_move,
            'move_delay': move_delay,
            'robot_rhythm': robot_rhythm,
            'human_rhythm': human_rhythm
        }
    )

    return round_count, winner, robot_move, human_move, move_delay, robot_rhythm, human_rhythm


def evaluate_winner(robot_move, human_move):
    if robot_move == human_move:
        return "Draw"
    elif (robot_move == "Rock" and human_move == "Paper") or (robot_move == "Paper" and human_move == "Scissor") or (robot_move == "Scissor" and human_move == "Rock"):
        return "Human"
    else:
        return "Robot"

if __name__ == "__main__":
    host_ip = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']
    host_port = 5000
    app.run(host_ip, host_port)