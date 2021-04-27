from __future__ import division
import numpy as np
from naoqi import ALProxy
import time
import motion
import random
import almath
import requests

server_ip = "http://192.168.86.178:5000/"
Nao_ip = "192.168.86.35"
PORT=9559

ROUNDS_PER_GAME= 5
human_wins=0
robot_wins=0
draw=0

rock_joint = [0,0]
paper_joint=[1,1.7]
scissor_joint=[1,-1]
rShoulderPitchJoints = [0.05,0.7] #shoulder pitch joint for pose A and B
rElbowRollJoints = [1.5,0.9] #elbow roll joint for pose A and B

tts = ALProxy("ALTextToSpeech", Nao_ip, PORT)
motionProxy = ALProxy("ALMotion", Nao_ip, PORT)
postureProxy = ALProxy("ALRobotPosture", Nao_ip, PORT)


# randomly select 'rock','paper' and 'scissor' and return pre-defined joint data for corresponding choise
def getRandomChoice():
    choice = random.randint(0,2)
    # choice = 0
    if choice ==0:
        return "Rock", rock_joint
    elif choice == 1:
        return "Paper", paper_joint
    elif choice ==2:
        return "Scissor",scissor_joint


# Specified joint data and time series data for robot movement
# @param bps: rhythm speed in bps
# @param iteration: number of total beats 
def playEachRound(bpm):
    names      = ["RShoulderPitch", "RElbowRoll", "RHand","RWristYaw"]

    choice, choiceJoint= getRandomChoice() #make random choice
    print (choice)

    pitch = rShoulderPitchJoints*3 
    roll = rElbowRollJoints*3  

    hand = [0,0,0,0,0]
    hand.append(choiceJoint[0]) #add choice joint
    wrist = [0,0,0,0,0]
    wrist.append(choiceJoint[1])
    angleLists = [pitch,roll,hand,wrist] #combine all joints data
  
    timePerBeat = 60/(bpm*2)
    startMove = 1 
    endMove = startMove+timePerBeat*6
    timeList = np.arange(startMove, endMove, timePerBeat).tolist()[0:6]
    times      = [timeList,timeList,timeList,timeList] 

    id=motionProxy.post.angleInterpolation(names, angleLists, times, True)
    motionProxy.wait(id,0)

    sendTimestamp(choice)

def showSampleBeat(bpm,iteration):
    names      = ["RShoulderPitch", "RElbowRoll"]
    angleLists = [rShoulderPitchJoints*iteration,rElbowRollJoints*iteration] #combine all joints data

    timePerBeat = 60/(bpm*2)
    startMove = 1 
    endMove = startMove+timePerBeat*iteration*2
    timeList = np.arange(startMove, endMove, timePerBeat).tolist()[0:iteration*2]
    times      = [timeList,timeList]

    id2 = motionProxy.post.angleInterpolation(names, angleLists, times, True)
    return id2


def sendTimestamp(action):
    timestamp = time.time()
    # print(timestamp)
    res = requests.get(server_ip + "addTimestamp?data=" + action + "_" + str(timestamp))
    print(res.text)
    result = res.text.split("|")[0]
    tts.say(str(result))

    global human_wins, robot_wins, draw
    if result == "I Win":
        robot_wins += 1
    elif result == "You Win":
        human_wins += 1
    elif result == "Draw":
        draw += 1



## get result from server and speak accordingly
def informResult(result):
    if result == "OK":
        tts.say("Good rhythm")
    elif result == "slow":#user is slow
        tts.say("too slow")
    elif result == "fast": #user is fast
        tts.say("too fast")


def main():
    #############################
    # Init posture
    motionProxy.wakeUp()
    postureProxy.goToPosture("Stand", 0.5)

    global human_wins, robot_wins, draw
    human_wins = 0
    robot_wins = 0
    draw = 0

    #############################
    # Greeting
    # tts.say("Hi, Do you want to play Rock Paper Scissor with me?")
    # tts.say("Hi")
    # time.sleep(1.0)

    #############################
    # Game session starts
    bpm = requests.get(server_ip+"bpm").text
    print (bpm)
    # bpm=60

    tts.say("Here is the sample beat")
    time.sleep(1.0)
    id_sample = showSampleBeat(bpm=int(bpm),iteration=5)
    motionProxy.wait(id_sample,0)
    time.sleep(1.0)

    for i in range(ROUNDS_PER_GAME):
        tts.say("Round start")
        playEachRound(bpm=int(bpm))
        time.sleep(1.0)
    
    tts.say("You won {} times, lost {} times, and the game was a draw {} times.".format(human_wins, robot_wins, draw))

if __name__ == "__main__":
    main()