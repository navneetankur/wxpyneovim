import threading,wx
from time import sleep
from wx.richtext import RichTextCtrl
from wx.richtext import RichTextRange as rtr
class Main:
    def main(self):
        app = wx.App()
        frm = self.frame = wx.Frame(None, title='hi')
        pnl = self.pnl = wx.Panel(self.frame)
        tc = RichTextCtrl(self.pnl)
        tc.SetSize(800,500)
        pnl.SetSize(800,500)
        frm.Fit()
        print(pnl.ClientSize)
        print(frm.ClientSize)
        # sizer = wx.BoxSizer()
        # sizer.Add(tc,flag=wx.EXPAND)
        # self.pnl.SetSizer(sizer)
        tc.EnableImages(True)
        # tc.AppendText('  \n'*10)
        pos = tc.XYToPosition(89,1)
        tc.SetFont(wx.Font(wx.FontInfo().FaceName('Source Code Pro')))
        tc.WriteText('hello')
        print(pos)
        print(tc.PositionToXY(0))
        tc.SetFont(wx.Font(wx.FontInfo().FaceName('Times New Roman')))
        tc.Clear()
        tc.WriteText('hello')
        # tc.SetInsertionPoint(2)
        # tc.WriteText('p')
        self.frame.Show()
        app.MainLoop()

    def draw(self):
        dc = wx.ClientDC(self.frame)
        dc.DrawText('hi',5,5)
    def one(self):
        wx.CallAfter(self.draw)
        # self.draw()

Main().main()
