from __future__ import division
import numpy as np
from naoqi import ALProxy
import time
import motion
import random
import almath

Nao_ip = "192.168.86.35"
PORT=9559
rock_joint = [0,0]
paper_joint=[1,1.7]
scissor_joint=[1,-1]

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
# @param iteration: number of total beats (prior + last three move)
# @param offset: time till start the first movement
def movement(bps,iteration,offset,motionProxy):
    priorBeat = iteration-3 
    names      = ["RShoulderPitch", "RElbowRoll", "RHand","RWristYaw"]
    rShoulderPitchJoints = [0.05,0.7] #shoulder pitch joint for pose A and B
    rElbowRollJoints = [1.5,0.9] #elbow roll joint for pose A and B

    pitchFullData = rShoulderPitchJoints*iteration # n iterations
    rollFullData=rElbowRollJoints*iteration  # n iterations
    
    choiceJoint= makeRandomChoice()

    handFulldata = [0] * (iteration*2-1)
    handFulldata.append(choiceJoint[0])
    wristFulldata = [0] * (iteration*2-1)
    wristFulldata.append(choiceJoint[1])

    angleLists = [pitchFullData,rollFullData,handFulldata,wristFulldata] #combine all joints data
    # timeList = np.linspace(offset,(1/speed)*iteration*2+offset,iteration*2,endpoint=False).tolist()
    timePerBeat = 60/bps
    startMove = offset
    endMove = offset+timePerBeat*iteration*2
    timeList = np.arange(startMove, endMove, timePerBeat).tolist()
    print (timeList)
    times      = [timeList,timeList,timeList,timeList] #chocie is only visible at the last timestamp
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)


def main():
    tts = ALProxy("ALTextToSpeech", Nao_ip, PORT)
    motionProxy = ALProxy("ALMotion", Nao_ip, PORT)
    postureProxy = ALProxy("ALRobotPosture", Nao_ip, PORT)
    memory = ALProxy("ALMemory",Nao_ip, PORT)

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
    # Movement
    movement(bps=120,iteration=3,offset=1,motionProxy=motionProxy)

if __name__ == "__main__":
    main()