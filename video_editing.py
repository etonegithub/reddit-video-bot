from PIL import Image, ImageDraw
import gtts
import cv2
from moviepy.editor import *


def build_tts(text):
    tts = gtts.gTTS(text)
    tts.save("files/text.mp3")


def build_picture(text, is_comment):
    img = Image.new("RGB", (500, 500), color="gray")
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 0), stroke_width=5)

    img.save("files/image.png")


def picture_to_video():
    frame_size = (500, 500)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter('files/video.mp4', fourcc, 20, frame_size)

    for x in range(0, 100):
        img = cv2.imread('files/image.png')
        out.write(img)

    out.release()


def stitch_video_and_audio():
    video_clip = VideoFileClip("files/video.mp4")
    audio_clip = AudioFileClip("files/text.mp3")
    full_clip = video_clip.set_audio(audio_clip)
    full_clip.write_videofile("files/fullvideo.mp4")
