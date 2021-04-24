from __future__ import division
import numpy as np
from naoqi import ALProxy
import time
import motion
import random
import almath
import requests

from datetime import datetime

server_ip = "http://192.168.86.178:5000/"
Nao_ip = "192.168.86.35"
PORT=9559
rock_joint = [0,0]
paper_joint=[1,1.7]
scissor_joint=[1,-1]
rShoulderPitchJoints = [0.05,0.7] #shoulder pitch joint for pose A and B
rElbowRollJoints = [1.5,0.9] #elbow roll joint for pose A and B

tts = ALProxy("ALTextToSpeech", Nao_ip, PORT)
motionProxy = ALProxy("ALMotion", Nao_ip, PORT)
postureProxy = ALProxy("ALRobotPosture", Nao_ip, PORT)
memory = ALProxy("ALMemory",Nao_ip, PORT)

# randomly select 'rock','paper' and 'scissor' and return pre-defined joint data for corresponding choise
def makeRandomChoice():
    choice = random.randint(0,2)
    if choice ==0:
        print ("rock")
        return rock_joint
    elif choice == 1:
        print ("paper")
        return paper_joint
    elif choice ==2:
        print ("scissor")
        return scissor_joint


# Specified joint data and time series data for robot movement
# @param bps: rhythm speed in bps
# @param iteration: number of total beats 
def playEachRound(bpm,iteration):
    names      = ["RShoulderPitch", "RElbowRoll", "RHand","RWristYaw"]
    pitchFullData = rShoulderPitchJoints*iteration # n iterations
    rollFullData=rElbowRollJoints*iteration  # n iterations
    
    choiceJoint= makeRandomChoice() #make random choice

    handFulldata = [0] * (iteration*2-1)
    handFulldata.append(choiceJoint[0])
    wristFulldata = [0] * (iteration*2-1)
    wristFulldata.append(choiceJoint[1])
    angleLists = [pitchFullData,rollFullData,handFulldata,wristFulldata] #combine all joints data
  
    timePerBeat = 60/(bpm*2)
    startMove = 1 
    endMove = startMove+timePerBeat*iteration*2
    timeList = np.arange(startMove, endMove, timePerBeat).tolist()[0:iteration*2]
    times      = [timeList,timeList,timeList,timeList] #chocie is only visible at the last timestamp
    
    motionProxy.angleInterpolation(names, angleLists, times, True)


def showSampleBeat(bpm,iteration):
    names      = ["RShoulderPitch", "RElbowRoll"]
    pitchFullData = rShoulderPitchJoints*iteration # n iterations
    rollFullData=rElbowRollJoints*iteration  # n iterations

    angleLists = [pitchFullData,rollFullData] #combine all joints data
    timePerBeat = 60/(bpm*2)
    startMove = 1 
    endMove = startMove+timePerBeat*iteration*2
    timeList = np.arange(startMove, endMove, timePerBeat).tolist()[0:iteration*2]
    times      = [timeList,timeList]

    sendTimestamp("START: ")
    id=motionProxy.post.angleInterpolation(names, angleLists, times, True)
    motionProxy.wait(id,0)
    sendTimestamp("STOP: ")

def sendTimestamp(identifier):
    timestamp = datetime.now().time()
    res = requests.get(server_ip + "addTimestamp?timestamp=" +identifier + str(timestamp))
    print(res)

def main():
    #############################
    # Init posture
    motionProxy.wakeUp()
    postureProxy.goToPosture("Stand", 0.5)

    #############################
    # Greeting
    # tts.say("Hi, Do you want to play Rock Paper Scissor with me?")
    tts.say("Hi")
    time.sleep(1.0)

    #############################
    # Game session starts
    # bpm = requests.get(server_ip+"bpm").text
    bpm=60

    # tts.say("Here is the sample beat")
    # time.sleep(1.0)
    showSampleBeat(bpm=int(bpm),iteration=20)

    # time.sleep(1.0)
    # tts.say("Round start")
    # playEachRound(bpm=int(bpm),iteration=3)

if __name__ == "__main__":
    main()