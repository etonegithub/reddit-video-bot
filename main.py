import pymongo
import file_functions
import data_scraper
import video_editing


client = pymongo.MongoClient("mongodb+srv://admin:adminpassword@reddit-video-data.qaodr.mongodb.net"
                     "/reddit-data?retryWrites=true&w=majority")
db = client['reddit-data']
posts = db.posts

if posts.count_documents({}) == 0:
    print("added post data")
    posts.insert_one(data_scraper.get_submission())

post = posts.find_one()
print(post)
post_title = post['title']

video_editing.build_tts(post_title)

video_editing.build_picture(post_title, False)

video_editing.picture_to_video()

video_editing.stitch_video_and_audio()
