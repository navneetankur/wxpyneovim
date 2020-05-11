import wx
import threading
import itertools

class NGUI:
    def __init__(self, nbr, events, title='Title', width=350, height=250):
        self.app = wx.App()
        self.events = events
        self.frame = Example(None, title, events, width, height)
        self.pnl = self.frame
        threading.Thread(target=events.update_loop,args=(self,)).start()
        self.frame.Show()

class Example(wx.Frame):
    def __init__(self, parent, title, events, width=350, height=250):
        super(Example, self).__init__(parent, title=title,
            size=(width, height))
        self.linespace = 0
        self.resize_timer = wx.Timer(self)
        self.charspace = 0
        self.counter = 0
        self.events = events
        self.pnl = self
        self.pnl.Bind(wx.EVT_PAINT, self.OnPaint)
        self.pnl.Bind(wx.EVT_CHAR, self.OnKey)
        self.pnl.Bind(wx.EVT_SIZE, self.OnResize)
        self.pnl.Bind(wx.EVT_TIMER, self.resize_timer_expired)
    def resize_timer_expired(self,e):
        dc = wx.ClientDC(self)
        dc.SetFont(self.GetFont())
        text_size = dc.GetTextExtent('_')
        size = self.GetClientSize()
        grid_width = size.GetWidth()/text_size.GetWidth()
        grid_height = size.GetHeight()/text_size.GetHeight()
        self.events.nbr.request('nvim_ui_try_resize_grid',1,int(grid_width),int(grid_height),async_=True)
        

    def OnResize(self,e):
        self.resize_timer.StartOnce(200)
    def OnKey(self,e):
        unicodekey = e.GetUnicodeKey()
        keycode = e.GetKeyCode()
        if unicodekey in self.events.config.keymap:
            self.events.nbr.request('nvim_input',self.events.config.keymap[unicodekey],async_=True)
        elif keycode in self.events.config.keycodemap:
            self.events.nbr.request('nvim_input',self.events.config.keycodemap[keycode],async_=True)

    def OnPaint(self, e):
        self.draw(wx.PaintDC(self.pnl),True)

    def draw(self,dc,redraw=False):
        dc.SetBackgroundMode(wx.SOLID)
        font = self.pnl.GetFont()
        font_style = font.GetStyle()
        dc.SetFont(font)
        text_size = dc.GetTextExtent('_')
        def_fg = self.events.default_colors['foreground']
        def_bg = self.events.default_colors['background']
        def_sc = self.events.default_colors['special']
        for i,row in enumerate(itertools.chain(self.events.grid.content.copy(), [self.events.grid.status_line,self.events.grid.cmd_line])):
            for j,col in enumerate(row):
                if col[2] or redraw:
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
                    #I dont know what blend means. make underline same as undercurl for now.
                    #also need to draw the underline manually to make it of different color
                    if reverse:
                        fg,bg = bg,fg
                    dc.SetTextForeground(wx.Colour(fg))
                    dc.SetTextBackground(wx.Colour(bg))
                    if italic:
                        font.MakeItalic()
                    if strikethrough:
                        font.MakeStrikethrough()
                    if bold:
                        font.MakeBold()
                    dc.DrawText(col[0], j*text_size.GetWidth(), i*text_size.GetHeight())
                    if underline or undercurl:
                        if underline:
                            dc.SetPen(wx.Pen(wx.Colour(sc),1,wx.PENSTYLE_SOLID))
                        else:
                            dc.SetPen(wx.Pen(wx.Colour(sc),1,wx.PENSTYLE_DOT))
                        x1 = j*text_size.GetWidth() - 1
                        y1 = (i+1)*text_size.GetHeight() - 2
                        x2 = x1 + text_size.GetWidth() + 0
                        dc.DrawLine(x1,y1,x2,y1)
                    col[2] = False #grid dirty bit unset
        #start drawing cursor
        cursor_position = self.events.grid.cursor_position
        mode_idx = self.events.mode_idx
        mode_info = self.events.mode_infos[mode_idx]
        cursor_shape = mode_info['cursor_shape']
        cell_percentage = mode_info['cell_percentage']/100
        attr_id = mode_info['attr_id']
        hl = self.events.hl_attr[attr_id]
        fg = hl['foreground'] if 'foreground' in hl else def_fg
        bg = hl['background'] if 'background' in hl else def_bg
        if attr_id == 0: fg,bg = bg,fg
        if cursor_position[0] >= self.events.grid.status_line_no:
            #cursor in cmd_line hopefully
            text = self.events.grid.cmd_line[cursor_position[1]][0]
            self.events.grid.cmd_line[cursor_position[1]][2] = True #set dirty bit at cursor position
        else:
            #cursor in grid
            text = self.events.grid.content[cursor_position[0]][cursor_position[1]][0]
            self.events.grid.content[cursor_position[0]][cursor_position[1]][2] = True #set dirty bit at cursor position
        if cursor_shape == 'block':
            dc.SetTextForeground(wx.Colour(fg))
            dc.SetTextBackground(wx.Colour(bg))
            dc.DrawText(text, cursor_position[1]*text_size.GetWidth(), cursor_position[0]*text_size.GetHeight())
        else:
            dc.SetBrush(wx.Brush(wx.Colour(bg)))
            dc.SetPen(wx.Pen(None,1,style=wx.TRANSPARENT))
            dc.DrawRectangle(cursor_position[1]*text_size.GetWidth(), cursor_position[0]*text_size.GetHeight(),text_size.GetWidth()*cell_percentage,text_size.GetHeight())
        font.SetStyle(font_style)# is this needed?
