import pymongo
import ssl

class DBase:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://Yana:ShalomAleichem2022@cluster0.9hjy5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
        self.db = self.client["reminder_db"]
        self.users = self.db["users"]

    def add_new_user(self, user_id):
        new_user = {
            "id" : user_id,
            "reminders" : []
        }

        self.users.insert_one(new_user)

    def add_new_reminder(self, user_id, reminder):
        reminder_list = self.users.find_one({"id" : user_id})["reminders"]

        reminder_list.append(reminder)

        query = {"id" : user_id}
        params = {"$set" : {"reminders" : reminder_list}}

        self.users.update_one(query, params)

    def get_user_object(self, user_id):
        return self.users.find_one({"id" : user_id})

    def delete_reminder(self, user_id, reminder_id):
        reminder_list = self.users.find_one({"id" : user_id})["reminders"]

        reminder_list.pop(reminder_id)

        query = {"id" : user_id}
        params = {"$set" : {"reminders" : reminder_list}}

        self.users.update_one(query, params)

    def get_all_users(self):
        return [x for x in self.users.find()]

    def update_reminders_list(self, user_id, reminder_list):
        query = {"id" : user_id}
        params = {"$set" : {"reminders" : reminder_list}}

        self.users.update_one(query, params)

