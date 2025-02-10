from Server.iop import InputOutputProcessor as IOP
import smtplib, imaplib, email


class TellWithMeCommandCompiler:
    """
    Class for compiling command.
    """

    @staticmethod
    def compile_command(flag: str, data=None):
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
    Class for decode received command.
    """

    @staticmethod
    def get_flag_from_command(command: str):
        """
        This method get flag from command.
        """
        return command.split("::::")[0]

    @staticmethod
    def get_command_from_command(command: str):
        """
        This method get command from command.
        """
        return command.split("::::")[1]

    @staticmethod
    def get_subject_from_email(email: str):
        """
        This method get subject from email.
        """
        return email.split("\n")[2].split(":")[1]


class TellWithMeIdentifier:
    """
    Class for identification of computer.
    """
    def __init__(self):
        io = IOP()
        self.twmcd = io.load_json("./data/twmcd.json")

    def generate_address(self, computerInfo: dict):
        """
        This method generate identification address of computer.
        """
        io = IOP()

        for address, data, f in self.twmcd.items(), range(255):
            for s in range(255):
                for t in range(255):
                    if address == f"{f}.{s}.{t}":
                        continue
                    else:
                        self.twmcd[f"{f}.{s}.{t}"] = computerInfo
                        io.save_json("./data/twmcd.json", self.twmcd)
                        return f"{f}.{s}.{t}"

    def remove_address(self, address: str):
        """
        This method remove identification address of computer.
        """
        io = IOP()
        del self.twmcd[address]
        io.save_json("./data/twmcd.json", self.twmcd)

    def get_os_by_address(self, address: str):
        """
        This method get OS of computer by address.
        """
        return self.twmcd[address]["os"]


class TellWithMeCommunicator(
    TellWithMeCommandCompiler, TellWithMeReceiveDecoder, TellWithMeIdentifier
):
    """
    Class for communication between computers.
    """

    def __init__(self):
        super().__init__()
        io = IOP()
        env = io.load_json("./data/env.json")
        self.emailAddress = env["email"]["address"]
        self.emailPassword = env["email"]["password"]
        self.emailSMTP = env["email"]["smtp"]
        self.emailIMAP = env["email"]["imap"]

    def send(self, command: str | None, address: str, flag: str, log_message: str):
        """
        This method send command to another computer.
        """
        message = f"From: {self.emailAddress}\nTo: {self.emailAddress}\nSubject: 0.0.0:{address}:{flag}\n\n{log_message}(|||){self.compile_command(flag, command)}"
        server = smtplib.SMTP(self.emailSMTP["host"], self.emailSMTP["port"])
        server.starttls()
        server.login(self.emailAddress, self.emailPassword)
        server.sendmail(
            self.emailAddress, self.emailAddress, message
        )
        server.quit()

    def check_for_messages(self) -> bool:
        """
        This method checks for the presence of new messages.
        """
        mail = imaplib.IMAP4_SSL(self.emailIMAP["host"], self.emailIMAP["port"])
        mail.login(self.emailAddress, self.emailPassword)
        mail.select("INBOX")
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
        mail = imaplib.IMAP4_SSL(self.emailIMAP["host"], self.emailIMAP["port"])
        mail.login(self.emailAddress, self.emailPassword)
        mail.select("INBOX")
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
            self.get_subject_from_email(rawEmailReceive[0]).split(":")[0].strip(),
            "ACK",
            "Message received",
            )
            if self.get_flag_from_command(rawEmailReceive[1]) != "EDCN" or self.get_flag_from_command(rawEmailReceive[1]) != "ACK"
            else None
        )
        if self.get_flag_from_command(rawEmailReceive[1]) == "IND":
            address = self.generate_address(
                {
                    "os": self.get_command_from_command(rawEmailReceive[1]).split(", ")[1],
                    "name": self.get_command_from_command(rawEmailReceive[1]).split(", ")[0]
                }
            )
            name = self.get_command_from_command(rawEmailReceive[1]).split(", ")[0]
            self.send(
            f"{address}, {name})",
            "255.255.255",
            "INF",
            "Address generated",
            )
        if self.get_flag_from_command(rawEmailReceive[1]) == "EDCN":
            self.remove_address(
            self.get_subject_from_email(rawEmailReceive[0]).split(":")[0].strip()
            )
        if self.get_flag_from_command(rawEmailReceive[1]) == "IR":
            result = self.get_command_from_command(rawEmailReceive[1]), self.get_flag_from_command(rawEmailReceive[1])
        elif self.get_flag_from_command(rawEmailReceive[1]) == "ERR":
            result = self.get_command_from_command(rawEmailReceive[1]), self.get_flag_from_command(rawEmailReceive[1])
        else:
            result = 0, 0

        # Delete email if address is 0.0.0
        if self.get_subject_from_email(rawEmailReceive[0]).split(":")[0].strip() == "0.0.0":
            mail.store(latest_email_id, "+FLAGS", "\\Deleted")
            mail.expunge()

        io.addRecordToEventLog(f"Incoming message: {email_message.get_payload()}")
        mail.logout()
        return result


class TellWithMe(
    TellWithMeCommunicator,
): ...
