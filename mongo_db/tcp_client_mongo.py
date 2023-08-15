import socket
import json

class TCPclient():
    def __init__(self, sms):
        self.target_ip = 'localhost'
        self.target_port = 9998
        self.input_checking(sms)
        
    def run_client(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        client.connect((self.target_ip, self.target_port))
        return client
    
    def input_checking(self,sms):
        if sms == "gad":
            self.get_all_data(sms)
        elif sms == "login":
            self.login(sms)
        elif sms == "register":
            self.registration(sms)
        else:
            print("Invalid Option")

    def get_all_data(self,sms):
        client = self.run_client()
        sms = bytes(sms, "utf-8")
        client.send(sms)
        recv_data_from_server = client.recv(4096)
        print (recv_data_from_server.decode("utf-8"))
        client.close

    def login(self,info):
        try:
            print("This is Login Form!")
            login_email = input("Enter your email to login: ")
            login_password = input("Enter your password to login: ")

            client = self.run_client()
            sms = info+" "+login_email+" "+login_password
            sms = bytes(sms, "utf-8")
            client.send(sms)

            recv_from_server = client.recv(4096)
            print(recv_from_server.decode("utf-8"))
            client.close
        
        except Exception as err:
            print(err)

    def registration(self,info):
        try:
            print("This is registration form!")
            user_email = input("Enter your email to register: ")
            user_password = input("Enter your password to register: ")
            user_age = int(input("Enter your age: "))
            phone = int(input("Enter your phone number: "))
            money = int(input("Enter your money at least $500:")) 
            point = int(input("how many points do you want to buy(1 point = 1$):"))

            client = self.run_client()
            sms = info+" "+user_email+" "+user_password+" "+str(user_age)+" "+str(phone)+str
            sms = bytes(sms, "utf-8")
            client.send(sms)

            recv_from_server = client.recv(4096)
            print(recv_from_server.decode("utf-8"))
            client.close


        except Exception as err:
            print(err)
        
if __name__ == '__main__':
    while True:
        sms = input("Enter some data to send:")
        tcp_client = TCPclient(sms)
        tcp_client.run_client()
