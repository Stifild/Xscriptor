class WinCommands:
    def poweroff(self):
        return 'shutdown -s -t 0'
    def restart(self):
        return 'shutdown -r -t 0'
    def logout(self):
        return 'shutdown -l'

class UnixCommands:
    def poweroff(self):
        return 'systemctl poweroff'
    def restart(self):
        return 'systemctl reboot'
    def logout(self):
        return 'systemctl logout'

class Computer(WinCommands, UnixCommands):
    def __init__(self, os_name, name):
        if os_name == 'Windows':
            self.__class__ = WinCommands
        else:
            self.__class__ = UnixCommands
        self.name = name
    