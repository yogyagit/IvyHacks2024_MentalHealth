from modal import method, enter
from modal_image import image, stub

@stub.cls(image = image, gpu="T4", container_idle_timeout=300)
class AtlasClient:
    @enter()
    def enter(self):
        """
        Initializes and connects the AtlasClient to a MongoDB Atlas cluster using
        environment variables for security credentials. The method sets up the MongoClient
        with a connection URI constructed from encoded credentials.

        Raises:
            Exception: If the MongoClient cannot be initialized due to missing or incorrect credentials.
        """
        from pymongo import MongoClient
        from urllib.parse import quote_plus

        self.client = None
        username = "ys5250"
        password = "letsHack@1997"  # Example password with special characters
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password)

        uri = f"mongodb+srv://{encoded_username}:{encoded_password}@mongogenai.d2rck3r.mongodb.net/"

        # Initialize MongoClient with the Atlas connection string
        self.client = MongoClient(uri)
        print('AtlasClient initialized with URI from environment variable.')

    @method()
    def insert_user_data(self, database_name='ThinkWell_AI', collection_name='user_data', user_id=None, firstname=None, lastname=None, email_id=None):
        """
        Inserts or updates user data in a specified MongoDB collection. If the user does not exist, a new document is created.
        If the user exists, the total_sessions field of the user's document is incremented.

        Parameters:
            database_name (str): Name of the database to use.
            collection_name (str): Name of the collection to use.
            user_id (str): The unique identifier of the user.
            firstname (str): First name of the user.
            lastname (str): Last name of the user.
            email_id (str): Email ID of the user.

        Returns:
            int: The current number of sessions after the insert or update.

        Raises:
            Exception: If the MongoClient has not been initialized.
        """
        if not self.client:
            raise Exception("MongoClient is not initialized. Call enter() method first.")

        db = self.client[database_name]
        collection = db[collection_name]
        filter = {'user_id': user_id}
        document = collection.find_one(filter)

        if document is None:
            print("User Not Found")
            new_document = {
                'user_id': user_id,
                'first_name': firstname,
                'last_name': lastname,
                'email_id': email_id,
                'total_sessions': 1
            }
            collection.insert_one(new_document)
            print("New document inserted.")
            curr_session_number = 1
        else:
            updated_document = collection.find_one_and_update(
                filter,
                {'$inc': {'total_sessions': 1}},
                return_document=True
            )
            curr_session_number = updated_document['total_sessions']
            print("Document found and updated:", updated_document)
            print("Previous session number:", curr_session_number)

        return curr_session_number

    @method()
    def insert_documents(self, database_name='ThinkWell_AI', collection_name='user_session_history', session_id=None, user_id=None, session_transcript=None):
        """
        Inserts a new document into a specified collection and database. The document contains session-specific data for a user.

        Parameters:
            database_name (str): The name of the database.
            collection_name (str): The name of the collection.
            session_id (str): The session identifier.
            user_id (str): The user identifier.
            session_transcript (str): The transcript of the session.

        Raises:
            Exception: If the MongoClient has not been initialized or if there is an error during the insert operation.
        """
        if not self.client:
            raise Exception("MongoClient is not initialized. Call enter() method first.")

        db = self.client[database_name]
        collection = db[collection_name]
        try:
            new_document = {
                'user_id': user_id,
                'session_id': session_id,
                'session_transcript': session_transcript
            }
            collection.insert_one(new_document)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    @method()
    def ping(self):
        """
        Sends a ping command to the MongoDB server to check the connection.

        Raises:
            Exception: If the ping command fails or if the connection to the database is not active.
        """
        return self.client.admin.command('ping')

    @method()
    def close_connection(self):
        """
        Closes the connection to the MongoDB database.

        Usage:
            Typically called to cleanly shutdown the database connection when the client instance is no longer needed.
        """
        self.client.close()


# For local testing
# @stub.local_entrypoint()
# def main():
#     model = AtlasClient()
#     dict_list = [
#         {"ingredients": "Sauce", "shop": "TJ"},
#         {"ingredients": "Cheese", "shop": "Target"}]
#     model.insert_documents.remote(collection_name = 'Pizza', database_name = 'Food', documents = dict_list )
