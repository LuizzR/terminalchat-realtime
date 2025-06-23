import getpass
import pysher
import os
import json 
from termcolor import colored
from dotenv import load_dotenv
from pusher import Pusher

load_dotenv(dotenv_path='credentials.env')

class terminalChat():
    pusher = None
    channel = None
    chatroom = None
    clientPusher = None
    user = None
    users = {
        "ricki": "12345",
        "troyake": "123456",
    }
    chatrooms = ["test"]
    
    ''' The entry point of the application'''
    def main(self):
        self.login()
        self.selectChatroom()
        while True:
            self.getInput()
    
    ''' This function handles login to the system. In a real-world app, 
        you might need to connect to API's or a database to verify users '''

    def initPusher(self):
        self.pusher = Pusher(app_id=os.getenv('PUSHER_APP_ID', None), key=os.getenv('PUSHER_APP_KEY', None), secret=os.getenv('PUSHER_APP_SECRET', None), cluster=os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher = pysher.Pusher(os.getenv('PUSHER_APP_KEY', None), os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher.connection.bind('pusher:connection_established', self.connectHandler)
        self.clientPusher.connect()

    def connectHandler(self, data):
        self.channel = self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage', self.pusherCallback)

    def pusherCallback(self, message):
        message = json.loads(message)
        if message['user'] != self.user:
            print(colored("{}: {}".format(message['user'], message['message']), "blue"))
            print(colored("{}: ".format(self.user), "green"))
    
    def login(self):
        username = input("Por favor, coloque seu nome: ")
        password = getpass.getpass("Por favor, coloque %s's sua senha:" % username)
        if username in self.users:
            if self.users[username] == password:
                self.user = username
            else:
                print(colored("Shhh senha errada!", "red"))
                self.login()
        else:
            print(colored("Username errado ein!", "red"))
            self.login()
    
    ''' This function is used to select which chatroom you would like to connect to '''
    def selectChatroom(self):
        print(colored("Info! Salas disponíveis %s" % str(self.chatrooms), "blue"))
        chatroom = input(colored("Por favor, escolha uma sala de conversa: ", "green"))
        if chatroom in self.chatrooms:
            self.chatroom = chatroom
            self.initPusher()
        else:
            print(colored("Sala de conversa não encontratada :(", "red"))
            self.selectChatroom()
                
    ''' This function is used to get the user's current message '''
    def getInput(self):
        message = input(colored("{}: ".format(self.user), "green"))
        self.pusher.trigger(self.chatroom, u'newmessage', {"Usuário": self.user, "Mensagem": message})

if __name__ == "__main__":
        terminalChat().main()
