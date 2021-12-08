import textwrap

from PIL import Image, ImageDraw, ImageFont
import gtts
import cv2
from moviepy.editor import *
import os
import file_functions

files_dir_name = 'files'
question_files_dir_name = 'files/question'
comments_files_dir_name = 'files/comments'
comment_dir_base_name = 'comment'

tts_file_name = "audio.mp3"
picture_file_name = "image.png"
video_file_name = "video.mp4"
full_video_file_name = "audio_video.mp4"

settings = {
    'resolution': (1920, 1080),
    'background_color': "black",
    'text_color': "white",
    'subreddit_text_color': "cyan",
    'author_text_color': "yellow",
    'question_text_align': 'center',
    'comment_text_align': 'left',
    'question_font_size': 84,
    'comment_font_size': 42,
    'corner_font_size': 21,
    'frame_rate': 20
}


def set_settings(res: (str, str), bg_clr: str, fnt_sz: int, fps: int) -> None:
    settings['resolution'] = res
    settings['background_color'] = bg_clr
    settings['comment_font_size'] = fnt_sz
    settings['frame_rate'] = fps


def create_final_video(post: dict) -> None:
    build_question_clip(post)
    build_comment_clips(post['comments'], post['subreddit'])
    stitch_questions_and_comments(question_files_dir_name, full_video_file_name, comments_files_dir_name, full_video_file_name)


def build_tts(text: str, file_dir: str, file_name: str) -> None:
    tts = gtts.gTTS(text)
    file_path = os.path.join(file_dir, file_name)
    tts.save(file_path)


def build_question_picture(text: str, author_name: str, score: int, subreddit_name: str, file_dir: str, file_name: str) -> None:
    img = Image.new("RGB", settings['resolution'], color=settings['background_color'])
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('Gidole-master/Resources/GidoleFont/Gidole-Regular.ttf', size=settings['question_font_size'])
    multiline_text_list = textwrap.wrap(text, width=30)
    multiline_text_string = "\n".join(multiline_text_list)
    d.text((150, settings['resolution'][1] / 4), multiline_text_string, fill=settings['text_color'], stroke_width=1,
           font=font, align=settings["question_text_align"])
    d.text((25, (settings['resolution'][1] / 4) - 100), author_name, fill=settings['author_text_color'],
           stroke_width=1, font=font, align="left")
    d.text((250, (settings['resolution'][1] / 4) - 250), subreddit_name, fill=settings['subreddit_text_color'],
           stroke_width=1, font=font, alight="left")

    file_path = os.path.join(file_dir, file_name)
    img.save(file_path)


def build_comment_picture(text: str, author_name: str, score: int, subreddit_name: str, file_dir: str, file_name: str) -> None:
    img = Image.new("RGB", settings['resolution'], color=settings['background_color'])
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype('Gidole-master/Resources/GidoleFont/Gidole-Regular.ttf', size=settings['comment_font_size'])
    small_font = ImageFont.truetype('Gidole-master/Resources/GidoleFont/Gidole-Regular.ttf', size=settings['corner_font_size'])
    multiline_text_list = textwrap.wrap(text, width=60)
    multiline_text_string = "\n".join(multiline_text_list)
    d.text((50, settings['resolution'][1] / 4), multiline_text_string, fill=settings['text_color'], stroke_width=1,
           font=font, align=settings['comment_text_align'])
    d.text((25, (settings['resolution'][1] / 4) - 50), author_name, fill=settings['author_text_color'],
           stroke_width=1, font=font, align="left")
    d.text((25, 25), subreddit_name, fill=settings['subreddit_text_color'], stroke_width=1, font=small_font, alight="left")

    file_path = os.path.join(file_dir, file_name)
    img.save(file_path)


def picture_to_video(file_dir: str, img_file_name: str, result_file_name: str) -> None:
    frame_size = settings['resolution']
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    result_file_path = os.path.join(file_dir, result_file_name)
    # file_path = "files/video.mp4"
    out = cv2.VideoWriter(result_file_path, fourcc, settings['frame_rate'], frame_size)

    img_file_path = os.path.join(file_dir, img_file_name)
    for x in range(0, 100):
        img = cv2.imread(img_file_path)
        out.write(img)

    out.release()


def stitch_video_and_audio(file_dir: str, video_file: str, audio_file: str, result_file_name: str) -> None:
    video_path = os.path.join(file_dir, video_file)
    # print(video_path)
    audio_path = os.path.join(file_dir, audio_file)
    # print(audio_path)

    # video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration
    # print(audio_duration)
    audio_duration_in_frames = audio_duration * settings['frame_rate']
    # print(audio_duration_in_frames)

    trimmed_video_path = os.path.join(file_dir, "trimmed_video.mp4")
    ffmpeg_tools.ffmpeg_extract_subclip(video_path, 0, audio_duration, targetname=trimmed_video_path)
    video_clip = VideoFileClip(trimmed_video_path)
    video_duration = video_clip.duration
    # print(video_duration)

    full_clip = video_clip.set_audio(audio_clip)

    file_path = os.path.join(file_dir, result_file_name)
    full_clip.write_videofile(file_path)


def build_question_clip(post: dict) -> None:
    build_tts(post["title"], question_files_dir_name, tts_file_name)
    build_question_picture(post["title"], post["author"], post["score"], post["subreddit"], question_files_dir_name, picture_file_name)
    picture_to_video(question_files_dir_name, picture_file_name, video_file_name)
    stitch_video_and_audio(question_files_dir_name, video_file_name, tts_file_name, full_video_file_name)


def build_comment_clips(comments: list, subreddit: str) -> None:
    for idx, comment in enumerate(comments):
        comment_dir_name = comment_dir_base_name + str(idx + 1)
        file_functions.create_dir(comments_files_dir_name, comment_dir_name)
        # print(comment_dir_name)
        build_single_comment_clip(comment, subreddit, comment_dir_name)
    return


# seems redundant to have separate question and comment functions now, but in the future i want question and comment
#   pictures to be built differently/look different
def build_single_comment_clip(comment: dict, subreddit: str, comment_dir_name) -> None:
    dir_path = os.path.join(comments_files_dir_name, comment_dir_name)
    build_tts(comment['body'], dir_path, tts_file_name)
    build_comment_picture(comment['body'], comment['author'], comment['score'], subreddit, dir_path, picture_file_name)
    picture_to_video(dir_path, picture_file_name, video_file_name)
    stitch_video_and_audio(dir_path, video_file_name, tts_file_name, full_video_file_name)
    return


def stitch_questions_and_comments(question_dir_path: str, question_video_file_name: str, comments_dir_path: str, comments_video_file_name: str) -> None:
    question_file_path = os.path.join(question_dir_path, question_video_file_name)
    video_clips = [VideoFileClip(question_file_path)]
    for dir_name in os.listdir(comments_dir_path):
        comment_file_path = os.path.join(comments_dir_path, dir_name, comments_video_file_name)
        video_clips.append(VideoFileClip(comment_file_path))
    merged_video = concatenate_videoclips(video_clips)
    result_path = os.path.join(files_dir_name, "final_video.mp4")
    merged_video.write_videofile(result_path)
