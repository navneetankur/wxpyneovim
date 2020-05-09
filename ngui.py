import wx
from wx.richtext import RichTextCtrl
import threading

class NGUI:
    def __init__(self, nbr, events, title='Title', width=350, height=250):
        self.app = wx.App()
        self.font = wx.Font(wx.FontInfo().FaceName('Source Code Pro'))
        self.events = events
        self.frame = Example(None, title, events, width, height)
        self.frame.Show()
        threading.Thread(target=events.update_loop,args=(self,)).start()

class Example(wx.Frame):
    def __init__(self, parent, title, events, width=350, height=250):
        super(Example, self).__init__(parent, title=title,
            size=(width, height))
        self.linespace = 0
        self.charspace = 0
        self.counter = 0
        self.SetFont(wx.Font(wx.FontInfo().FaceName('Source Code Pro')))
        self.events = events
        self.pnl = wx.Panel(self)
        self.pnl.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, e):
        dc = wx.PaintDC(self.pnl)
        dc.SetFont(self.GetFont())
        text_size = dc.GetTextExtent('A')
        # print(self.events.grid.content)
        for i,row in enumerate(self.events.grid.content):
            for j,col in enumerate(row):
                dc.DrawText(col[0], j*text_size.GetWidth(), i*text_size.GetHeight())
                    
        # dc.SetPen(wx.Pen('RED'))
        # dc.DrawText('hello{}'.format(self.counter) , 5,5)
        # self.counter += 1
        # dc.DrawLine(50, 60, 190, 60)
        print('painted')
    def temp(self):
        print('hello')
        dc = wx.ClientDC(self)
        # dc.SetPen(wx.Pen('RED'))
        dc.DrawLine(50, 60, 190, 60)
        # dc.DrawText('hello world', 50,50)
        # dc.DrawCircle(50,50,200)


def main():
    app = wx.App()
    ex = Example(None,'Sizing',None)
    ex.Show()
    # threading.Thread(target=app.MainLoop).start()
    app.MainLoop()

if __name__ == '__main__':
    main()
