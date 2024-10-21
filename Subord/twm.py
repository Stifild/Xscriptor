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
        if flag == "IR":
            command = f"IR::::{data}"
        elif flag == "FIN":
            command = f"FIN::::{data}"
        elif flag == "ACK":
            command = f"ACK::::{data}"
        elif flag == "EDCN":
            command = f"EDCN::::{data}"
        elif flag == "INF":
            command = f"INF::::{data}"
        elif flag == "ERR":
            command = f"ERR::::{data}"
        elif flag == "IND":
            command = f"IND::::{data}"
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
    myAddress: str = "255.255.255"

    def send(self, command: str, address: str, flag: str, log_message: str):
        """
        This method send command to another computer.
        """
        message = f"From: xscriptor.smtp.twm@mail.ru\nTo: xscriptor.smtp.twm@mail.ru\nSubject: {self.myAddress}:{address}:{flag}\n\n{log_message}(|||){self.compileCommand(flag, command)}"
        server = smtplib.SMTP("smtp.mail.ru", 25)
        server.starttls()
        server.login("xscriptor.smtp.twm@mail.ru", "adfe38Z0XEbrLgZ1ekSx")
        server.sendmail(
            "xscriptor.smtp.twm@mail.ru", "xscriptor.smtp.twm@mail.ru", message
        )
        server.quit()

    def receive(self):
        """
        This method receive command from another server.
        """
        mail = imaplib.IMAP4_SSL("imap.mail.ru")
        mail.login("xscriptor.smtp.twm@mail.ru", "adfe38Z0XEbrLgZ1ekSx")
        mail.select("inbox")
        _, data = mail.search(None, "ALL")
        mail_ids = data[0]
        id_list = mail_ids.split()
        latest_email_id = id_list[-1]
        _, data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1]
        raw_email_string = raw_email.decode("utf-8")
        rawEmailReceive = raw_email_string.split("(|||)")

        subject = self.getSubjectFromEmail(raw_email_string)
        recipient_address = subject.split(":")[1]

        if recipient_address != self.myAddress:
            return None, None

        flag = self.getFlagFromCommand(rawEmailReceive[1])
        command = self.getCommandFromCommand(rawEmailReceive[1])

        if flag == "INF":
            result = (command, flag)
        elif flag == "EDCN":
            exit()
        elif flag == "IC":
            result = (command, flag)
        elif flag == "ERR":
            result = (command, flag)
        else:
            result = (None, None)

        # Mark the email as deleted
        mail.store(latest_email_id, '+FLAGS', '\\Deleted')
        mail.expunge()
        mail.logout()

        return result


class TellWithMe(
    TellWithMeCommunicator,
): ...
