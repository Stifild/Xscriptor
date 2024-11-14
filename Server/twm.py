from Server.iop import InputOutputProcessor as IOP
import smtplib, imaplib, email


class TellWithMeCommandCompiler:
    """
    This class need for compiling command.
    """

    def compileCommand(self, flag: str, data=None):
        """
        This method compiles command based on the provided flag and data.
        """
        if flag == "IC":
            command = f"IC::::{data}"
        elif flag == "FIN":
            command = "FIN::::0.0.0"
        elif flag == "ACK":
            command = "ACK::::0.0.0"
        elif flag == "EDCN":
            command = "EDCN::::0.0.0"
        elif flag == "INF":
            command = f"INF::::{data}"
        elif flag == "ERR":
            command = f"ERR::::{data}"
        else:
            raise ValueError(f"Unknown flag: {flag}")
        return command


class TellWithMeReceiveDecoder:
    """
    This class need for decode received command.
    """

    def getFlagFromCommand(self, command: str):
        """
        This method get flag from command.
        """
        return command.split("::::")[0]

    def getCommandFromCommand(self, command: str):
        """
        This method get command from command.
        """
        return command.split("::::")[1]

    def getSubjectFromEmail(self, email: str):
        """
        This method get subject from email.
        """
        return email.split("\n")[2].split(":")[1]


class TellWithMeIdentificator:
    """
    This class need for identification of computer.
    """

    def generateAddress(self, computerInfo: dict):
        """
        This method generate identification address of computer.
        """
        io = IOP()
        self.twmcd = io.load_json("./data/twmcd.json")

        for address, data, f in self.twmcd.items(), range(255):
            for s in range(255):
                for t in range(255):
                    if address == f"{f}.{s}.{t}":
                        continue
                    else:
                        self.twmcd[f"{f}.{s}.{t}"] = computerInfo
                        io.save_json("./data/twmcd.json", self.twmcd)
                        return f"{f}.{s}.{t}"

    def RemoveAddress(self, address: str):
        """
        This method remove identification address of computer.
        """
        io = IOP()
        self.twmcd = io.load_json("./data/twmcd.json")
        del self.twmcd[address]
        io.save_json("./data/twmcd.json", self.twmcd)

    def GetOsByAddress(self, address: str):
        """
        This method get OS of computer by address.
        """
        io = IOP()
        self.twmcd = io.load_json("./data/twmcd.json")
        return self.twmcd[address]["os"]


class TellWithMeCommunicator(
    TellWithMeCommandCompiler, TellWithMeReceiveDecoder, TellWithMeIdentificator
):
    """
    This class need for communication between computers.
    """

    def send(self, command: str, address: str, flag: str, log_message: str):
        """
        This method send command to another computer.
        """
        message = f"From: xscriptor.smtp.twm@mail.ru\nTo: xscriptor.smtp.twm@mail.ru\nSubject: 0.0.0:{address}:{flag}\n\n{log_message}(|||){self.compileCommand(flag, command)}"
        server = smtplib.SMTP("smtp.mail.ru", 25)
        server.starttls()
        server.login("xscriptor.smtp.twm@mail.ru", "adfe38Z0XEbrLgZ1ekSx")
        server.sendmail(
            "xscriptor.smtp.twm@mail.ru", "xscriptor.smtp.twm@mail.ru", message
        )
        server.quit()
    
    def check_for_messages(self) -> bool:
        """
        This method checks for the presence of new messages.
        """
        mail = imaplib.IMAP4_SSL("imap.mail.ru")
        mail.login("xscriptor.smtp.twm@mail.ru", "adfe38Z0XEbrLgZ1ekSx")
        mail.select("inbox")
        _, data = mail.search(None, "ALL")
        mail_ids = data[0]
        id_list = mail_ids.split()
        mail.logout()
        return len(id_list) > 0

    def receive(self):
        """
        This method receive command from another computer.
        """
        io = IOP()
        mail = imaplib.IMAP4_SSL("imap.mail.ru")
        mail.login("xscriptor.smtp.twm@mail.ru", "adfe38Z0XEbrLgZ1ekSx")
        mail.select("inbox")
        _, data = mail.search(None, "ALL")
        mail_ids = data[0]
        id_list = mail_ids.split()
        if not id_list:
            return 0, 0
        latest_email_id = id_list[-1]
        _, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode("utf-8")
        email_message = email.message_from_string(raw_email_string)
        
        rawEmailReceive = str(email_message.get_payload()).split("(|||)")
        (
            self.send(
            None,
            self.getSubjectFromEmail(rawEmailReceive[0]).split(":")[0].strip(),
            "ACK",
            "Message received",
            )
            if self.getFlagFromCommand(rawEmailReceive[1]) != "EDCN" or self.getFlagFromCommand(rawEmailReceive[1]) != "ACK"
            else None
        )
        if self.getFlagFromCommand(rawEmailReceive[1]) == "IND":
            address = self.generateAddress(
            self.getCommandFromCommand(rawEmailReceive[1])
            )
            name = self.getCommandFromCommand(rawEmailReceive[1])["name"]
            self.send(
            {"address": address, "name": name},
            "255.255.255",
            "INF",
            "Address generated",
            )
        if self.getFlagFromCommand(rawEmailReceive[1]) == "EDCN":
            self.RemoveAddress(
            self.getSubjectFromEmail(rawEmailReceive[0]).split(":")[0].strip()
            )
        if self.getFlagFromCommand(rawEmailReceive[1]) == "IR":
            result = self.getCommandFromCommand(rawEmailReceive[1]), self.getFlagFromCommand(rawEmailReceive[1])
        elif self.getFlagFromCommand(rawEmailReceive[1]) == "ERR":
            result = self.getCommandFromCommand(rawEmailReceive[1]), self.getFlagFromCommand(rawEmailReceive[1])
        else:
            result = 0, 0
        
        # Delete email if address is 0.0.0
        if self.getSubjectFromEmail(rawEmailReceive[0]).split(":")[0].strip() == "0.0.0":
            mail.store(latest_email_id, "+FLAGS", "\\Deleted")
            mail.expunge()
        
        io.addRecordToEventLog(f"Incoming message: {email_message.get_payload()}")
        mail.logout()
        return result


class TellWithMe(
    TellWithMeCommunicator,
): ...
