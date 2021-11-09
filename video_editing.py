from PIL import Image, ImageDraw
import gtts
import cv2
from moviepy.editor import *
import os


def build_tts(text: str, file_dir: str, file_name: str) -> None:
    tts = gtts.gTTS(text)

    file_path = os.path.join(file_dir, file_name)
    tts.save(file_path)


def build_picture(text: str, file_dir: str, file_name: str) -> None:
    img = Image.new("RGB", (500, 500), color="gray")
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 0), stroke_width=5)

    file_path = os.path.join(file_dir, file_name)
    img.save(file_path)


def picture_to_video(file_dir: str, img_file_name: str, file_name: str) -> None:
    frame_size = (500, 500)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    file_path = os.path.join(file_dir, file_name)
    # file_path = "files/video.mp4"
    out = cv2.VideoWriter(file_path, fourcc, 20, frame_size)

    img_file_path = os.path.join(file_dir, img_file_name)
    for x in range(0, 100):
        img = cv2.imread(img_file_path)
        out.write(img)

    out.release()


def stitch_video_and_audio(file_dir: str, video_file_name: str, audio_file_name: str, file_name: str) -> None:
    video_path = os.path.join(file_dir, video_file_name)
    print(video_path)
    audio_path = os.path.join(file_dir, audio_file_name)
    print(audio_path)

    video_clip = VideoFileClip('files/video.mp4')
    audio_clip = AudioFileClip(audio_path)
    full_clip = video_clip.set_audio(audio_clip)

    file_path = os.path.join(file_dir, file_name)
    full_clip.write_videofile(file_path)
