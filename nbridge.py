
class NBridge:
    """as it turns out pretty useless class, all the functions are already implemented in nvim class. Well I'll just delegate to it from this one. Now removing it is too much trouble."""
    def __init__(self, nvim):
        self.nvim = nvim
    def next_message(self):
        return self.nvim.next_message()
    #just adding delegater methods after this line
    def input(self, *args, **kwargs):
        return self.nvim.input(*args, **kwargs)
    def ui_attach(self, *args, **kwargs):
        return self.nvim.ui_attach(*args, **kwargs)
    def ui_detach(self, *args, **kwargs):
        return self.nvim.ui_detach(*args, **kwargs)
    def close(self, *args, **kwargs):
        return self.nvim.close(*args, **kwargs)
    def request(self, *args, **kwargs):
        return self.nvim.request(*args, **kwargs)
