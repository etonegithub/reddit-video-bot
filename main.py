from pymongo import MongoClient
import data_scraper


client = MongoClient("mongodb+srv://admin:adminpassword@reddit-video-data.qaodr.mongodb.net"
                     "/reddit-data?retryWrites=true&w=majority")
db = client['reddit-data']
posts = db.posts

if posts.count_documents({}) == 0:
    print("added post data")
    posts.insert_one(data_scraper.get_submission())


