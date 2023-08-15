import pymongo

import random
db_connection = pymongo.MongoClient("localhost", 27017)
database = db_connection["auctionProject"]
collection = database["user_data"]

if __name__ == '__main__':



    for i in range(10):
        user_id = random.randint(10, 10000)
        email: str = "bob"+str(i)+"@gmail.com"
        password: str = "12345"
        phone: int = 4576795

        user_info:str = "User is Bob"+str(i)+" id : "+str(user_id)

        data_form = {"_id": user_id, "email": email, "password": password, "phone": phone,"info":user_info}

        ids = collection.insert_one(data_form)
        print("inserted id :", ids.inserted_id)