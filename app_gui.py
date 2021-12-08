import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='testing')
        panel = wx.Panel(self)

        my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(panel)
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        btn = wx.Button(panel, label='Press Me')
        btn.Bind(wx.EVT_BUTTON, self.on_press)
        my_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(my_sizer)

        self.Show()

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything.")
        else:
            print(f'You typed: "{value}"')


def main():
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
