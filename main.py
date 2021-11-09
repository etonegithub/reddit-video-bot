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
    posts.insert_one(data_scraper.get_submissions("askreddit", "week", 1, 5))

video_files_dir = 'files'

if not file_functions.is_dir_empty(video_files_dir):
    file_functions.clear_dir(video_files_dir)

post = posts.find_one()
print(post)
post_title = post['title']

tts_file_name = "text.mp3"
video_editing.build_tts(post_title, video_files_dir, tts_file_name)

picture_file_name = "image.png"
video_editing.build_picture(post_title, video_files_dir, picture_file_name)

video_file_name = "video.mp4"
video_editing.picture_to_video(video_files_dir, picture_file_name, video_file_name)

full_video_file_name = "full_video.mp4"
video_editing.stitch_video_and_audio(video_files_dir, video_file_name, tts_file_name, full_video_file_name)
