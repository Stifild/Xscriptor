from configs import ROLE
from Server.twm import TellWithMe as SeTWM
from Subord.twm import TellWithMe as SuTWM
import threading, os, subprocess, socket

if ROLE == "Server":
    twm = SeTWM()
    subprocess.Popen(["python3", "Server/main.py"])
    checkMail = threading.Timer(3.5, twm.receive())
    while True:
        receive, flag = checkMail.start()
        
         
else:
    twm = SuTWM()
    twm.send(twm.compileCommand("IND", socket.gethostname()), "0.0.0", "IND", "Hi Server! Can you give me an address?")
    checkMail = threading.Timer(3.5, twm.receive())
    while True:
        receive, flag = checkMail.start()
        os.system(receive)