from datetime import datetime
import os
import mongoengine as db_engine

from db_interface import DatabaseInterface
from dotenv import load_dotenv

class User(db_engine.Document):
    """Create a User document collection"""
    email = db_engine.StringField()
    password = db_engine.StringField()
    role = db_engine.StringField()
    username = db_engine.StringField()

    def to_json(self):
        return {
            "role": self.role,
            "email": self.email,
            "password": self.password,
            "username": self.username
        }

class MongoDBProvider(DatabaseInterface):
    """Implements the [DatabaseInterface] methods to persist data on a mongoDB database."""
    def __init__(self) -> None:
        self.user = None

    def connect(self):
        try:
            load_dotenv()
            print('Connecting Mongo')
            DB_URI = os.getenv('MONGO_URI')
            db_engine.connect(host=DB_URI)
            print('Mongo Db successfully connected')
            return (True, "Connection Successful")

        except(Exception) as err:
            print(f'Error: {err}')
            return (False, "Error")

    def create(self, location: str, data: dict):        
        try:
            username,email,password,role = data['data']
            self.user = User(
                username = username,
                email = email,
                password = password,
                role = role
            )
            self.user.save()
            return (True, 'Created')

        except (Exception) as error:
            print(error)
            return (False, "Error")

    def read(self,location: str):
        """Read a given user by id(location)"""
        try:
            if location is None:
                raise Exception()
            data = {'list':[]}
            for user in User.objects:
                if user.to_json().get('email') == location:
                    data['list'].append(user.to_json()) 

            return (True, 'Read Successful', data)
        
        except (Exception) as error:
            print(error)
            return (False, "Error", {})

    def update(self, location: str, data: dict):
        """Update user info"""
        pass
        # try:
        #     contact_name = data['contact'][1]  # from the test
        #     contact_number = data['contact'][0]
        #     self.book = Odds.objects(contact_name=contact_name).first()
        #     self.book.update(contact_name=contact_name, contact_number=contact_number)
        #     return (True, 'Update Successful')

        # except (Exception) as error:
        #     print(error)
        #     return (False, "Error")

    def delete(self,location: str, data: dict):
        """Delete a user"""
        pass
        # try:
        #     contact_name = data['contact'][0]  # from the test
        #     self.book = Odds.objects(contact_name=contact_name).first()
        #     self.book.delete()
        #     return (True, 'Delete Successful')

        # except (Exception) as error:
        #     print(error)
        #     return (False, "Error")

    def disconnect(self):
        return (True, "Disconnected")


