from computer import Computer
import smtplib, imaplib, email
import os, subprocess

class TellWithMe:
    '''
    This class need for communication between computers.
    '''
    def __init__(self): ...

    def send(self, command: str): 
        '''
        This method send command to another computer.
        '''
        message = f"Subject: Command Execution\n\n{command}"
        server = smtplib.SMTP('smtp.mail.ru', 587)
        server.starttls()
        server.login("xscriptor.smtp.twm@mail.ru", "ic7pCamjEjvdn4a52djU")
        server.sendmail("xscriptor.smtp.twm@mail.ru", "xscriptor.smtp.twm@mail.ru", message)
        server.quit()
    
    

class TellWithMeScripter(TellWithMe):
    '''
    This class is script creator for TellWithMe.
    '''
    def __init__(self): ...

    def crate_bridge(self): ...
