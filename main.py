import pymongo
import data_scraper
import video_editing


client = pymongo.MongoClient("mongodb+srv://admin:adminpassword@reddit-video-data.qaodr.mongodb.net"
                     "/reddit-data?retryWrites=true&w=majority")
db = client['reddit-data']
posts = db.posts

if posts.count_documents({}) == 0:
    print("added post data")
    posts.insert_one(data_scraper.get_submission())

# video_editing.build_tts("hello")

# video_editing.build_picture("hello", False)

video_editing.picture_to_video()
