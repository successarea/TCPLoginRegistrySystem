import socket
import subprocess
import pymongo
import json

db_connection = pymongo.MongoClient("localhost",27017)
database = db_connection["auctionProject"]
collection = database["user_data"]


class TCPserver():
    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9998
        self.toSave = {}

    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen()
        print('server listen on port:{} and ip:{}'.format(self.server_port,self.server_ip))

        try:
            while True:
                client,address = server.accept()
                print("Accepted connection from - {} : {}".format(address[0],address[1]))
                self.handle_client(client)
                # break

        except Exception as err:
            print(err)

    def handle_client(self,client_socket):
        data_list = []
        with client_socket as sock:
            from_client = sock.recv(1024)
            data_list = from_client.decode("utf-8").split(" ")
            print("Received data from client:", data_list)

            if data_list[0] == "gad":
                self.get_all_data(sock)
            elif data_list[0] == "login":
                self.login_checking(sock,data_list)
            elif data_list[0] == "register":
                self.registration_check(sock,data_list)
            else:
                sms = bytes("Invalid Option","utf-8")
                sock.send(sms)

    def get_all_data(self,sock):
        data:dict = {}
        
        for i in collection.find({},{"_id":0,"email":1,"phone":1,"info":1}):
            id = len(data)
            data_form = {"email":i["email"],"phone_number":i["phone"],"user_info":i["info"]}
            data.update({id:data_form})
        print(data)

        str_data = json.dumps(data)
        str_data = bytes(str_data,"utf-8")
        sock.send(str_data)

    def login_checking(self,sock,data_list):
        login_email = data_list[1]
        login_password = data_list[2]

        flag = -1
        sms = {}
        for i in collection.find({},{"_id":0,"email":1,"password":1,"info":1}):
            print(i)
            if i["email"] == login_email and i["password"] == login_password:
                flag = 1
                sms = {"email":i["email"], "info":i["info"]}
                sms = json.dumps(sms)
                break
        if flag == 1:
                str_data = bytes(sms, "utf-8")
                sock.send(str_data)

        else:
            str_data = bytes("Email and password not found", "utf-8")
            sock.send(str_data)
            
    def registration_check(self,sock,data_list):
        r_email = data_list[1]
        r_password = data_list[2]
        r_age = data_list[3]
        r_phone = data_list[4]
        r_info = "User "+r_email+" is "+r_age+" years old"
        flag = -1

        for i in collection.find({},{"_id":0,"email":1}):
             if r_email == i["email"]:
                flag = 1
                str_data = bytes("Your Email already exits! ", "utf-8")
                sock.send(str_data)
                break
             
        if flag == -1:
            data_form = {"email": r_email, "password": r_password, "age":r_age, "phone": r_phone,"info":r_info}
            ids = collection.insert_one(data_form)
            print("inserted id :", ids.inserted_id)
            sms = "Registration done successfully! "+r_info
            str_data = bytes(sms, "utf-8")
            sock.send(str_data)
        
        else :
            print('reg fails')
            str_data = bytes("Registration fails. Try Again!", "utf-8")
            sock.send(str_data)


            





            

if __name__ == '__main__':
    tcp_server = TCPserver()
    tcp_server.main()