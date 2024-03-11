from pymongo import MongoClient
from datetime import datetime

MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "dermadata"
MONGODB_COLLECTION = "chatdata"

class DB:
    def __init__(self):
        mongo_client = MongoClient(MONGODB_URI)
        ostello_ml_db = mongo_client[DB_NAME]

        self.db_client = ostello_ml_db[MONGODB_COLLECTION]

    def get_last_history(self, room_id, limit):
        return self.db_client.find_one({
            "roomid": room_id
        }, {
            "_id": 0,
            "roomid": 1,
            "history": {"$slice": -limit},
        })

    def get_room(self, room_id, limit, skip, chat_limit, chat_skip):
        if room_id is not None:
            rooms = self.db_client.find_one({
                "roomid": room_id
            }, {
                "_id": 0,
                "roomid": 1,
                "followUpQuestions": 1,
                "chat_count": {"$size": "$history"},
                "history": {"$slice": [{"$reverseArray": "$history"}, chat_skip, chat_limit]}
            })

            return rooms, 1
        else:
            count = self.db_client.count_documents({})
            rooms = self.db_client.find({}, {
                "_id": 0,
                "roomid": 1,
                "followUpQuestions": 1,
                "chat_count": {"$size": "$history"},
                "history": {"$slice": [{"$reverseArray": "$history"}, chat_skip, chat_limit]},
                "time_stamp":1,
            }).limit(limit).skip(skip)

            rooms_list = []

            for room_data in rooms:
                rooms_list.append(room_data)
            
            rooms_list = sorted(rooms_list, key=lambda x: x['time_stamp'],reverse=True)

            return rooms_list, count

    def create_room(self, data):
        return self.db_client.insert_one(data)

    def append_message_to_room(self, room_id, msg,time_stamp):
        for chat in msg:
            self.db_client.update_one({
                "roomid": room_id
            }, {
                "$push": {"history": chat, "conversation_history": chat},
                "$set": {"time_stamp": time_stamp}
            })

    def set_summary_to_room(self, room_id, follow_ups):
        return self.db_client.update_one({
            "roomid": room_id
        }, {
            "$set": {"followUpQuestions": follow_ups},
        })

    def set_follow_ups_to_room(self, room_id, follow_ups):
        return self.db_client.update_one({
            "roomid": room_id
        }, {
            "$set": {"followUpQuestions": follow_ups},
        })
    def update_user_data(self, userid, data):
        # Check if the user already exists in the database
        existing_user = self.db_client.find_one({"userid": userid})

        if existing_user:
            # If the user exists, update their data
            self.db_client.update_one({"userid": userid}, {"$set": data})
        else:
            # If the user doesn't exist, insert a new document
            data["userid"] = userid
            self.db_client.insert_one(data)

    def get_user_data(self, userid):
        # Retrieve and return user data based on userid
        user_data = self.db_client.find_one({"userid": userid})
        return user_data
    
    def get_user_room(self, userid):
        # Retrieve and return user data based on userid
        user_data = self.db_client.find_one({"roomid": userid})
        return user_data
    
    def delete_documents_by_userid(self, user_id):
        self.db_client.delete_many({"userid": user_id})
    
    def delete_documents_by_roomid(self, user_id):
        self.db_client.delete_many({"roomid": user_id})
         # Return the number of deleted 
        
db_client = DB()
