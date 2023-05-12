from pymongo import MongoClient
from urllib.parse import quote_plus

# username = quote_plus('collab')
# password = quote_plus('newpassword')

conn = MongoClient("mongodb+srv://testuser:newpassword@cluster0.qlblf.mongodb.net/collab?retryWrites=true&w=majority")
