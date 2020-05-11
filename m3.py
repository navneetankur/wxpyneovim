from pynvim import attach
import redrawevent
import nbridge
import ngui
# Create a python API session attached to unix domain socket created above:
print(r'\\.\pipe\nvim-15468-0')
# nvim = attach('socket', path=r'\\.\pipe\nvim-15468-0')
nvim = attach('tcp', address='127.0.0.1', port=8080)
nbr = nbridge.NBridge(nvim)
# Now do some work. 
buffer = nvim.current.buffer # Get the current buffer
buffer[0] = 'replace first line'
nbr.input('inew line')
nvim.vars['global_var'] = [1, 2, 3]
gv = nvim.eval('g:global_var')
nbr.ui_attach(400,200,True,ext_linegrid=True)
events = redrawevent.Events(nbr)
ui = ngui.NGUI(nbr, events, 'Title',800,500)
# threading.Thread(target=events.update_loop,args=(self,)).start()
# print(nm)

ui.app.MainLoop()

nbr.ui_detach()
nbr.close()
print('done')
