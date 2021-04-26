import netifaces as ni

from flask import Flask, request

from copy import deepcopy

from time import sleep, time

INTER_MOVE_THRESHOLD = 0.5
LATENCY = 0.555

app = Flask(__name__)

timestamp = []
recognition_timestamp = []

bpm = 90
sample_count = 10

@app.route("/", methods=["GET"])
def index():
    return "Rock Paper Scissor Server"

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

@app.route("/timestamps", methods=["GET"])
def get_timestamps():
    return str(timestamp)

@app.route("/addTimestamp", methods=["GET"])
def add_timestamp():
    global timestamp
    timestamp.append(request.args.get("data"))
    # move = request.args.get("data").split("_")[0]
    # timestamp.append(move + "_" + str(time()))
    # print(move + "_" + str(time()))
    sleep(1)
    res = compute_results()
    return res

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

@app.route("/latency", methods=["GET"])
def latency():
    timeClient = float(request.args.get("time"))
    timeServer = time()
    print("Latency: {}".format(timeClient - timeServer))
    return "{}".format(timeClient - timeServer)

@app.route("/clearTimestamps", methods=["GET"])
def clear_timestamps():
    global timestamp
    timestamp.clear()
    return "Timestamp cleared"

def compute_results():
    min_time = 9999
    human_move = "NaN"
    human_land_time = 0
    human_time = 0
    move_idx = -1

    rt_copy = deepcopy(recognition_timestamp)

    robot_move = timestamp[len(timestamp) - 1].split("_")[0]
    robot_time = float(timestamp[len(timestamp) - 1].split("_")[1]) - LATENCY

    # rt_copy.reverse()
    for idx, entry in enumerate(rt_copy):
        human_time_temp = float(entry.split("_")[1])

        if min_time > abs(robot_time - human_time_temp):
            human_time = human_time_temp
            human_move = entry.split("_")[0]
            min_time = abs(robot_time - human_time)
            move_idx = idx
    
    for i in range(move_idx, 0, -1):
        if (float(rt_copy[i].split("_")[1]) - float(rt_copy[i - 1].split("_")[1])) < INTER_MOVE_THRESHOLD:
            print((float(rt_copy[i].split("_")[1]) - float(rt_copy[i - 1].split("_")[1])))
            continue
        else:
            human_land_time = float(rt_copy[i].split("_")[1])
            print("Final Move: " + str(human_land_time))
            break

    print("Human Move: {} Robot Move: {} Human Time: {} Robot Time: {}".format(human_move, robot_move, human_time, robot_time))
    if robot_move == human_move:
        return "Draw: " + str(human_time - robot_time) + " | " + str(human_land_time - robot_time)
    elif (robot_move == "Rock" and human_move == "Paper") or (robot_move == "Paper" and human_move == "Scissor") or (robot_move == "Scissor" and human_move == "Rock"):
        return "Human Wins: " + str(human_time - robot_time) + " | " + str(human_land_time - robot_time)
    else:
        return "Robot Wins: " + str(human_time - robot_time) + " | " + str(human_land_time - robot_time)

if __name__ == "__main__":
    host_ip = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']
    host_port = 5000
    app.run(host_ip, host_port)