import time
import subprocess
from gpiozero import MotionSensor

pir = MotionSensor(4)
flag = 1
def open_program(path_name):
    return subprocess.Popen(path_name,stdout=subprocess.PIPE,shell=True)

def close_program(p):
    p.terminate()

while True:
    pir.wait_for_motion()
    print("Motion Detected Starting Mirror")
    path_name="/home/pi/Project/start.sh"
    if flag==1:
        p=open_program(path_name)
        flag=2
    if(len(p)==0):
        p=open_program(path_name)
    else:
        print("Program Already Running")
    #command = "python /home/pi/Desktop/Project/project.py"
    #subprocess.call(command, shell= True)
    time.sleep(600)
    pir.wait_for_no_motion()
    print("Motion Not Detected Terminating Mirror")
    if p:
        close_program(p)

    