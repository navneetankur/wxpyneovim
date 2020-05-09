import ngui
import wx
from wx.richtext import RichTextRange as rtr
import copy
from collections import deque
class Grid:
    def __init__(self):
        self.width = 400
        self.height = 200
        self.content = deque([[[]]])

class Events:
    def __init__(self, nbr, title='Title', width=350, height=250):
        self.nbr = nbr
        self.option = {}
        self.default_colors = {}
        self.hl_attr = {}
        self.hl_group = {}
        self.grid = Grid()
        
    def option_set(self,ui,options):
        for opt in options:
            self.option[opt[0]] = opt[1]
            if opt[0] == 'guifont':
                guifont = opt[1].split(':')
                ui.frame.pnl.SetFont(wx.Font(wx.FontInfo(int(guifont[1][1:])).FaceName(guifont[0])))

    def default_colors_set(self,ui,colors):
        fg = self.default_colors['foreground'] = colors[0][0]
        bg = self.default_colors['background'] = colors[0][1]
        sc = self.default_colors['special'] = colors[0][2]
        if 0 not in self.hl_attr:
            self.hl_attr[0] = {'foreground':fg, 'background':bg, 'special':sc}
        wx.CallAfter(self.set_default_gui_color,ui,fg,bg)
    def set_default_gui_color(self,ui, fg, bg):
        pnl = ui.frame.pnl
        pnl.SetForegroundColour(wx.Colour(fg))
        pnl.SetBackgroundColour(wx.Colour(bg))
    def hl_attr_define(self,ui,attrs):
        for att in attrs:
            self.hl_attr[att[0]] = att[1]

    def hl_group_set(self,ui,*args):
        pass

    def resize_ui(self,ui,width,height):
        # ui.textCtrl.Clear()
        font = ui.frame.pnl.GetFont()
        dc = wx.ClientDC(ui.frame.pnl)
        dc.SetFont(font)
        font_size = dc.GetTextExtent('_')
        # ui.textCtrl.SetSize(width * font_size.GetWidth(), height * font_size.GetHeight())
        ui.frame.SetClientSize((width) * font_size.GetWidth(), (height) * font_size.GetHeight())
        # ui.textCtrl.AppendText(((' '*(width+0))+'\n')*(height+1))
        # ui.textCtrl.AppendText(((' '*(50))+'\n')*(50))
        # ui.frame.Fit()

    def grid_resize(self,ui,e):
        col = self.grid.width = e[0][1]
        row = self.grid.height = e[0][2]
        c = [' ',1]
        d = [copy.deepcopy(c) for i in range(col)]
        e = deque(copy.deepcopy(d) for i in range(row))
        self.grid.content = e
        wx.CallAfter(self.resize_ui,ui,col,row)

    def clear_grid(self,ui,g):
        # wx.CallAfter(ui.textCtrl.Clear)
        pass

    def grid_clear(self,ui,grids):
        for g in grids:
            self.clear_grid(ui,g)

    def grid_line(self,ui,lines):
        for line in lines:
            grid_no = line[0]
            row = line[1]
            col_start = line[2]
            cells = line[3]
            i = 0
            hl_id = 1
            for cell in cells:
                repeat = 1
                try:
                    text = cell[0]
                    hl_id = cell[1]
                    repeat = cell[2]
                except IndexError:
                    continue
                finally:
                    # wx.CallAfter(ui.textCtrl.AppendText,text)
                    # tc = wx.richtext.RichTextCtrl()#todo
                    for r in range(repeat):
                        self.grid.content[row][col_start+i+r][0] = text
                        self.grid.content[row][col_start+i+r][1] = hl_id
                    i += repeat

    def do_gui_update(self,tc, row,col, text, repeat=1):
        pos = tc.XYToPosition(col, row)
        # tc.Remove(pos,pos+repeat)
        # tc.SetInsertionPoint(pos)
        # tc.WriteText(text)
        tc.Replace(pos, pos+repeat, text)
        # tc.Delete(rtr(pos+1,pos+2))
        
    def update_loop(self, ui):
        while True:
            self.do_update(ui)

    def do_update(self, ui):
        nm = self.nbr.next_message()
        for m in nm[2]:
            func = getattr(self,m[0])
            func(ui,m[1:])

    def update_gui(self,ui):
        ui.frame.pnl.Refresh()

    def grid_cursor_goto(self,ui,position):
        pass

    def grid_destroy(self,ui,e):
        pass
    def grid_scroll(self,ui,e):
        scroll = e[0][5]
        # wx.CallAfter(self.grid.content.rotate,-scroll)
        #doen't work because this causes status bar to scroll as well

        # self.grid.content.rotate(scroll)

        pass
    def mode_info_set(self,ui,e):
        pass
    def mode_change(self,ui,e):
        pass
    def flush(self,ui,e):
        self.update_gui(ui)
    def busy_start(self,ui,e):
        pass




