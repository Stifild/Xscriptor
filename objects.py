import subprocess

class computer:
    def __init__(self, name, type):
        self.name = name
        self.type = type
    def poweroff(self):
        subprocess.run(["bin/bash", "./sh-scripts/poweroff.sh"])
        exit()
    def reboot(self):
        subprocess.run(["bin/bash", "./sh-scripts/reboot.sh"])
        exit()
    def custom(self, file_name):
        try:
            subprocess.run(["bin/bash", "./sh-scripts/" + file_name])
        except:
            print("Error: File not found.")
        