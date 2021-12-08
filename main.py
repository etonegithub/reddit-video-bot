import pymongo

import app_gui
import file_functions
import data_scraper
import video_editing
import wx

client = pymongo.MongoClient("mongodb+srv://admin:adminpassword@reddit-video-data.qaodr.mongodb.net"
                             "/reddit-data?retryWrites=true&w=majority")
db = client['reddit-data']
posts = db.posts


def process(subreddit: str, time_frame: str, num_posts: int, num_comments: int):
    post = data_scraper.get_submissions(subreddit, time_frame, num_posts, num_comments)

    if not posts.find({'title': post['title']}).count() > 0:
        print("added post data")
        posts.insert_one(post)

    if not file_functions.is_dir_empty('files/question') and not file_functions.is_dir_empty('files/comments'):
        print("clearing dir")
        file_functions.clear_dir('files/question', False)
        file_functions.clear_dir('files/comments', True)

    print(post)

    # select_comments = []
    # for comment_num in range(int(num_comments)):
    #     print("wow")
    #     print(post['comments'][comment_num])
    #     select_comments.append(post['comments'][comment_num])

    # video_editing.set_settings((1920, 1080), "gray")
    video_editing.create_final_video(post)

    exit()


# WAX STUFF
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Youtube Compilation Editor Toolkit')
        panel = wx.Panel(self)

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        h_sizer_subreddit = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer_comments = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer_time_period = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer_post_rank = wx.BoxSizer(wx.HORIZONTAL)

        # self.text_box_subreddit_title = wx.StaticText(panel, label='Enter target subreddit:')
        # v_sizer.Add(self.text_box_subreddit_title, 0, wx.ALL | wx.EXPAND, 5)

        self.text_box_subreddit_prompt = wx.StaticText(panel, label='reddit.com/r/')
        h_sizer_subreddit.Add(self.text_box_subreddit_prompt, 1, wx.ALL | wx.EXPAND, 10)
        self.text_ctrl_subreddit_prompt = wx.TextCtrl(panel, value='AskReddit')
        h_sizer_subreddit.Add(self.text_ctrl_subreddit_prompt, 3, wx.ALL | wx.EXPAND, 5)
        v_sizer.Add(h_sizer_subreddit, 0, wx.ALL | wx.EXPAND, 5)

        self.text_box_num_comments = wx.StaticText(panel, label='Number of comments included: ')
        h_sizer_comments.Add(self.text_box_num_comments, 1, wx.ALL | wx.EXPAND, 10)
        self.text_ctrl_num_comments = wx.TextCtrl(panel, value='1')
        h_sizer_comments.Add(self.text_ctrl_num_comments, 3, wx.ALL | wx.EXPAND, 5)
        v_sizer.Add(h_sizer_comments, 0, wx.ALL | wx.EXPAND, 5)

        self.text_box_time_period_prompt = wx.StaticText(panel, label='Time period for \'hot\' filter: ')
        h_sizer_time_period.Add(self.text_box_time_period_prompt, 1, wx.ALL | wx.EXPAND, 10)
        choices = ["all", "hour", "day", "week", "month", "year"]
        self.combo_box_time_period = wx.ComboBox(panel, choices=choices, value='week')
        h_sizer_time_period.Add(self.combo_box_time_period, 3, wx.ALL | wx.EXPAND, 5)
        v_sizer.Add(h_sizer_time_period, 0, wx.ALL | wx.EXPAND, 5)

        self.text_box_post_rank_prompt = wx.StaticText(panel, label='What rank post: ')
        h_sizer_post_rank.Add(self.text_box_post_rank_prompt, 1, wx.ALL | wx.EXPAND, 10)
        self.text_ctrl_post_rank = wx.TextCtrl(panel, value='1')
        h_sizer_post_rank.Add(self.text_ctrl_post_rank, 3, wx.ALL | wx.EXPAND, 5)
        v_sizer.Add(h_sizer_post_rank, 0, wx.ALL | wx.EXPAND, 5)

        btn = wx.Button(panel, label='Create video')
        btn.Bind(wx.EVT_BUTTON, self.on_press)
        v_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(v_sizer)

        self.Show()

    def on_press(self, event):
        subreddit_submitted = self.text_ctrl_subreddit_prompt.GetValue()
        time_frame_submitted = self.combo_box_time_period.GetValue()
        num_post_submitted = self.text_ctrl_post_rank.GetValue()
        num_comments_submitted = self.text_ctrl_num_comments.GetValue()
        if subreddit_submitted is None or time_frame_submitted is None \
                or num_post_submitted is None or num_comments_submitted is None:
            print("You are missing an entry.")
        else:
            print(f'You entered: "{subreddit_submitted}, {num_comments_submitted}"')
            process(subreddit_submitted, time_frame_submitted, int(num_post_submitted), int(num_comments_submitted))


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
