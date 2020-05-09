import threading

class NBridge:
    def __init__(self, nvim, incoming_callback=None):
        """self: instance
            nvim: connection channel with neovim
            incoming_callback: function to call when event from neovim arrives
        """
        self.nvim = nvim
        self.incoming_callback = incoming_callback
    def next_message_async(self):
        self.next_message_async(self.incoming_callback)
    def next_message_async(self, incoming_callback):
        threading.Thread(target=self.next_message, args=(incoming_callback,))

    def next_message(self, incoming_callback):
        incoming_callback(self.nvim.next_message())
    #just adding delegater methods after this line
    def next_message(self):
        return self.nvim.next_message()
    def input(self, *args, **kwargs):
        return self.nvim.input(*args, **kwargs)
    def ui_attach(self, *args, **kwargs):
        return self.nvim.ui_attach(*args, **kwargs)
    def ui_detach(self, *args, **kwargs):
        return self.nvim.ui_detach(*args, **kwargs)
    def close(self, *args, **kwargs):
        return self.nvim.close(*args, **kwargs)
