import wx
from wx.richtext import RichTextCtrl
import threading

class NGUI:
    def __init__(self, nbr, events, title='Title', width=350, height=250):
        self.app = wx.App()
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
        self.events = events
        self.pnl = wx.Panel(self)
        # self.pnl.SetFont(wx.Font(wx.FontInfo().FaceName('Source Code Pro')))
        self.pnl.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, e):
        dc = wx.PaintDC(self.pnl)
        dc.SetBackgroundMode(wx.SOLID)
        font = self.pnl.GetFont()
        # font = wx.Font()#todo
        font_style = font.GetStyle()
        dc.SetFont(font)
        text_size = dc.GetTextExtent('_')
        def_fg = self.events.default_colors['foreground']
        def_bg = self.events.default_colors['background']
        def_sc = self.events.default_colors['special']
        for i,row in enumerate(self.events.grid.content):
            for j,col in enumerate(row):
                hl_id = col[1]
                hl = self.events.hl_attr[hl_id]
                fg = hl['foreground'] if 'foreground' in hl else def_fg
                bg = hl['background'] if 'background' in hl else def_bg
                sc = hl['special'] if 'special' in hl else def_sc
                underline = hl['underline'] if 'underline' in hl else False
                undercurl = hl['undercurl'] if 'undercurl' in hl else False
                italic = hl['italic'] if 'italic' in hl else False
                strikethrough = hl['strikethrough'] if 'strikethrough' in hl else False
                bold = hl['bold'] if 'bold' in hl else False
                reverse = hl['reverse'] if 'reverse' in hl else False
                blend = hl['blend'] if 'blend' in hl else False
                #todo I dont know what blend meand. make underline same as undercurl for now.
                if reverse:
                    temp = fg
                    fg = bg
                    bg = temp
                dc.SetTextForeground(wx.Colour(fg))
                dc.SetTextBackground(wx.Colour(bg))
                if underline or undercurl:
                    font.MakeUnderlined()
                if italic:
                    font.MakeItalic()
                if strikethrough:
                    font.MakeStrikethrough()
                if bold:
                    font.MakeBold()
                dc.DrawText(col[0], j*text_size.GetWidth(), i*text_size.GetHeight())
        font.SetStyle(font_style)
        # dc.SetPen(wx.Pen('RED'))
        # dc.DrawText('hello{}'.format(self.counter) , 5,5)
        # self.counter += 1
        # dc.DrawLine(50, 60, 190, 60)
    def temp(self):
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
