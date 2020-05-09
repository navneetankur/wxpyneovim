import threading,wx
from time import sleep
from wx.richtext import RichTextCtrl
from wx.richtext import RichTextRange as rtr
class Main:
    def main(self):
        app = wx.App()
        frm = self.frame = wx.Frame(None, title='hi')
        # pnl = self.pnl = wx.Panel(self.frame)
        self.frame.Bind(wx.EVT_PAINT, self.OnPaint)
        print(frm.ClientSize)
        # sizer = wx.BoxSizer()
        # sizer.Add(tc,flag=wx.EXPAND)
        # self.pnl.SetSizer(sizer)
        # tc.AppendText('  \n'*10)
        # tc.SetInsertionPoint(2)
        # tc.WriteText('p')
        self.frame.Show()
        app.MainLoop()
    def OnPaint(self, e):
        dc = wx.PaintDC(self.frame)
        dc.SetTextForeground('black')
        dc.SetTextBackground('red')
        # dc.SetBackground(wx.Brush('red'))
        dc.SetBackgroundMode(wx.SOLID)
        dc.DrawText('hello world',0,0)

    def draw(self):
        dc = wx.ClientDC(self.frame)
        dc.DrawText('hi',5,5)
    def one(self):
        wx.CallAfter(self.draw)
        # self.draw()

Main().main()
