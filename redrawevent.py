import wx
from config import Config

class Events:
    def __init__(self, nbr, title='Title', width=350, height=250):
        self.nbr = nbr
        self.option = {}
        self.default_colors = {}
        self.hl_attr = {}
        self.hl_attr[0] = {}
        self.hl_group = {}
        self.grid = {}
        self.lasthl = 0
        
    def option_set(self,ui,options):
        for opt in options:
            self.option[opt[0]] = opt[1]
            if opt[0] == 'guifont':
                guifont = opt[1].split(':')
                print(guifont,'gf')
                ui.textCtrl.SetFont(wx.Font(wx.FontInfo(int(guifont[1][1:])).FaceName(guifont[0])))

    def gui_default_colors(self, ui, fg, bg):
        tc = ui.textCtrl
        tc.SetForegroundColour(wx.Colour(fg))
        tc.SetBackgroundColour(wx.Colour(bg))

    def default_colors_set(self,ui,colors):
        fg = self.default_colors['foreground'] = colors[0][0]
        bg = self.default_colors['background'] = colors[0][1]
        sc = self.default_colors['special'] = colors[0][2]
        wx.CallAfter(self.gui_default_colors,ui,fg,bg)

    def hl_attr_define(self,ui,attrs):
        for att in attrs:
            self.hl_attr[att[0]] = att[1]

    def hl_group_set(self,ui,*args):
        pass

    def resize_ui(self,ui,width,height):
        ui.textCtrl.Clear()
        font = ui.textCtrl.GetFont()
        dc = wx.ClientDC(ui.textCtrl)
        dc.SetFont(font)
        font_size = dc.GetTextExtent('A')
        # ui.textCtrl.SetSize(width * font_size.GetWidth(), height * font_size.GetHeight())
        # ui.frame.SetClientSize((width+0) * font_size.GetWidth(), (height+0) * font_size.GetHeight())
        ui.textCtrl.AppendText(((' '*(width+0))+'\n')*(height+0-1))
        ui.textCtrl.AppendText(' '*width)
        s = dc.GetMultiLineTextExtent(ui.textCtrl.GetValue())
        ui.frame.SetClientSize(s.GetWidth()+Config.width_offset,s.GetHeight()+Config.height_offset)
        # ui.textCtrl.AppendText(((' '*(50))+'\n')*(50))
        print(font_size)
        print(width * font_size.GetWidth(), height * font_size.GetHeight())
        print('te', ui.textCtrl.GetFullTextExtent(ui.textCtrl.GetLineText(0)))
        print('bs', ui.textCtrl.GetBestSize())
        print('ds', dc.GetMultiLineTextExtent(ui.textCtrl.GetValue()))
        # ui.frame.Fit()

    def grid_resize(self,ui,e):
        print('size',e)
        self.grid['no'] = e[0][0]
        width = self.grid['width'] = e[0][1]
        height = self.grid['height'] = e[0][2]
        wx.CallAfter(self.resize_ui,ui,width,height)


    def clear_grid(self,ui,g):
        # wx.CallAfter(ui.textCtrl.Clear)
        pass

    def grid_clear(self,ui,grids):
        for g in grids:
            self.clear_grid(ui,g)

    def grid_line(self,ui,lines):
        for line in lines:
            # print('line', line)
            grid_no = line[0]
            row = line[1]
            col_start = line[2]
            cells = line[3]
            tc = ui.textCtrl
            pos = tc.XYToPosition(col_start, row)
            i = 0
            hl_id = 0
            for cell in cells:
                # print('cell',cell)
                repeat = 1
                try:
                    text = cell[0]
                    hl_id = cell[1]
                    repeat = cell[2]
                except IndexError:
                    pass
                    # print(text)
                    # wx.CallAfter(ui.textCtrl.AppendText,text)
                wx.CallAfter(self.do_gui_update,ui,row,col_start+i,text,hl_id,repeat)
                i += repeat
                    # print('w',text, pos, row, col_start)
        pass
    def do_gui_update(self,ui, row,col, text,hl_id, repeat=1):
        tc = ui.textCtrl
        pos = tc.XYToPosition(col, row)
        if self.lasthl != hl_id:
            hl = self.hl_attr[hl_id]
            # print('h',hl_id,text * repeat)
            # print(hl)
            # print('a', text, pos, row, col)
            # print('t',text,pos)
            # tc.Remove(pos,pos+repeat)
            # tc.SetInsertionPoint(pos)
            # tc.WriteText(text)
            fg_df = self.default_colors['foreground']
            bg_df = self.default_colors['background']
            sc_df = self.default_colors['special']
            foreground = hl.get('foreground',fg_df)
            background = hl.get('background',bg_df)
            special = hl.get('special',sc_df)
            reverse = hl.get('reverse', False)
            italic = hl.get('italic', False)
            bold = hl.get('bold', False)
            strikethrough = hl.get('strikethrough', False)
            underline = hl.get('underline', False)
            undercurl = hl.get('undercurl', False)
            blend = hl.get('blend', False)
            if reverse:
                foreground, background = background, foreground
            font = wx.Font(tc.GetFont())
            # font = wx.Font()#todo
            if bold: font.MakeBold()
            if italic: font.MakeItalic()
            if strikethrough: font.MakeStrikethrough()
            style = wx.TextAttr(wx.Colour(foreground), wx.Colour(background), font)
            # style = wx.TextAttr(wx.Colour(background), wx.Colour(foreground), font)
            if underline:
                style.SetFontUnderlineType(wx.TEXT_ATTR_UNDERLINE_SOLID, wx.Colour(special))
            if undercurl:
                style.SetFontUnderlineType(wx.TEXT_ATTR_UNDERLINE_SPECIAL, wx.Colour(special))
            # tc = wx.TextCtrl() #todo
            tc.SetDefaultStyle(style)
        tc.Remove(pos, pos+repeat)
        tc.SetInsertionPoint(pos)
        tc.WriteText(text*repeat)
        self.lasthl = hl_id
        # tc.Replace(pos, pos+repeat, text*repeat)
        # tc.SetStyle(pos, pos+repeat,
        

        # print('written',text,'at', pos, 'to', pos+repeat)
        # tc.Delete(rtr(pos+1,pos+2))
        
    def update_loop(self, ui):
        while True:
            self.do_update(ui)

    def do_update(self, ui):
        nm = self.nbr.next_message()
        for m in nm[2]:
            # print('m',m)
            func = getattr(self,m[0])
            func(ui,m[1:])
        pass

    def grid_cursor_goto(self,ui,position):
        pass

    def grid_destroy(self,ui,e):
        pass
    def grid_scroll(self,ui,e):
        pass
    def mode_info_set(self,ui,e):
        pass
    def mode_change(self,ui,e):
        pass
    def busy_start(self,ui,e):
        pass
    def busy_stop(self,ui,e):
        pass
    def flush(self,ui,e):
        pass




