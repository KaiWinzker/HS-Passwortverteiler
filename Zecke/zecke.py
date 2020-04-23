"""
    Dieses Programm wurde von Kai Winzker erstellt und dient dem Senden 
    von Passwörten für Stutentischen Germien.
    Copyright (C) 2020 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 3 as published by
    the Free Software Foundation.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License.
    If not, see <https://www.gnu.org/licenses/>.
 """

from argparse import ArgumentError
from email.mime.text import MIMEText
import smtplib
import string
import random

rights = "zecke  Copyright (C) 2020  Kai Winzker\n"
rights +="This program comes with ABSOLUTELY NO WARRANTY; for details see <https://www.gnu.org/licenses/>.\n"
rights +="This is free software, and you are welcome to redistribute it.\n"

class HsServer(object):
    
    server = None
    address = None
    port = None
    user = None
    password = None
    emailAdresse = None
    passwordPool = string.ascii_uppercase
    #passwordPool += "[]<>=&@:-)(}{|~+%" 
    passwordPool += string.digits
    
    passwordList = []
    def __init__(self,user, password ,emailAddresse, address = "smtp.hs-fulda.de", port = 587):
        self.address = address
        self.port = port
        self.user = user
        self.password = password
        self.emailAddresse = emailAddresse
    
    def __enter__(self): 
        self.open() 
        return self
  
    def __exit__(self,exception_type, exception_value, traceback):
        self.close()
        
    def open(self):
        self.server = smtplib.SMTP(self.address,port=self.port)
        if self.server.starttls()[0] != 220:
            raise smtplib.SMTPNotSupportedError("can't activate starttls")
        self.server.login(self.user, self.password)
        print("Login erfolgreich")
        
    def close(self):
        self.server.close()
    
    def sendMessage(self, message:MIMEText):
        message.as_string()
        self.server.sendmail(self.user,message["To"],message.as_string())
        print("send message to: '"+ message["To"]+"'")
        
    def sendRandom(self, message:MIMEText, replacer = "XXXXXX"):
        password = self.passWord()
        message.set_payload(message.get_payload().replace(replacer, password))
        self.server.sendmail(self.user,message["To"],message.as_string())
        print("send random to: '"+ message["To"]+"'")
    
    def passWord(self, length = 20):
        word = ""
        for i in range(length):
            word += random.choice(self.passwordPool)
        return word
    
    def sendMultyRandom(self, users):
        contend = []
        for user in users:
            message = self.standartMessage(user)
            if message['To'].endswith("hs-fulda.de"):
                contend.append(self.sendRandom(message))
            else:
                print("invalid user")
                msg = MIMEText("Bitte sende umgehend deine Hs-Email an "+self.emailAddresse+"\nAntworte nicht auf diese Email es wird keiner lesen können.\n Ohne die richtige Mailadresse kannst du nicht im Hs-Gremien abstimmen")
                msg["To"] = user
                msg['From'] = self.emailAddresse
                msg["Subject"] = "HS-Gremien WICHTIG!!"
                print(user)
                self.sendMessage(msg)
    
    def standartMessage(self, user):
        password = self.passWord(6)
        msg = MIMEText("Diese Mail wurde automatisch generiert, antworten Sie nicht darauf.\n Ihre Verifizierungscode für die nächste Sitzung sind: "+password)
        msg['Subject'] = "Verifizierungscode Hs-Gremien-Sitzung"
        msg['To'] = user
        msg['From'] = self.emailAddresse
        self.passwordList.append(password+":::"+user)
        return msg
        
            
if __name__ == '__main__':
    print(rights)
    print("Benutze dieses Programm nur von deinem Privatrechner!!!")
    print("Bevor die Mail gesendet werden kann, musst du dich erst einloggen:")
    fdnummer = input("gebe deine  fdnummer ein: ")
    import getpass
    passwort = getpass.getpass('Password:')
    email = input("noch deine volle E-Mail-Adresse: ")
    print("Zu sendende E-Mails im Format :E-Mail,E-Mail,E-Mail")
    emails = input("E-Mails: ")
    emails = emails.replace(" ", "")
    emails = emails.replace(";",",")
    emails = emails.split(",")
    with HsServer(fdnummer, passwort, email) as server:
        server.sendMultyRandom(emails)
        
        print("\n\n\n\n\n\n\n folgende Passwörter wurden versand:")
        for p in server.passwordList:
            if p.endswith("hs-fulda.de"):
                print(p)
            
    
        
    
    
    
    
    
        