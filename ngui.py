import wx
from wx.richtext import RichTextCtrl
import threading

class NGUI:
    def __init__(self, nbr, events, title='Title', width=350, height=250):
        self.app = wx.App()
        self.font = wx.Font(wx.FontInfo().FaceName('Source Code Pro'))
        print(self.font.GetFamily(),'ff')
        self.events = events
        self.frame = Example(None, title, events, width, height)
        self.textCtrl = self.frame.txtCtrl
        self.frame.Show()
        threading.Thread(target=events.update_loop,args=(self,)).start()
        # self.app.MainLoop()

class Example(wx.Frame):
    def __init__(self, parent, title, events, width=350, height=250):
        super(Example, self).__init__(parent, title=title,
            size=(width, height))
        # self.pnl = wx.Panel(self)
        # self.pnl.Bind(wx.EVT_PAINT, self.OnPaint)
        tc = self.txtCtrl = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_RICH2)
        # self.txtCtrl.AppendText('hello world')
        # tc.Replace(20,50,'bye') 
        # guifont = events.option['guifont'].split(':')
        # pt = guifont[0]
        # face = guifont[1]
        # print('ft',face,pt)
        tc.SetFont(wx.Font(wx.FontInfo().FaceName('Source Code Pro')))
        # tc.AppendText('\n'*50)
        tc.AppendText(((' '*50) + '\n')*50)
    def OnPaint(self, e):
        dc = wx.PaintDC(self.pnl)
        dc.SetPen(wx.Pen('RED'))
        dc.DrawText('hello' , 5,5)
        dc.DrawText('hello' , 5,6)
        dc.DrawLine(50, 60, 190, 60)
    def temp(self):
        print('hello')
        dc = wx.ClientDC(self)
        # dc.SetPen(wx.Pen('RED'))
        dc.DrawLine(50, 60, 190, 60)
        # dc.DrawText('hello world', 50,50)
        # dc.DrawCircle(50,50,200)


def main():
    pass

    # app = wx.App()
    # ex = Example(None, title='Sizing')
    # ex.Show()
    # threading.Thread(target=app.MainLoop).start()
    # app.MainLoop()

if __name__ == '__main__':
    main()
