import tkinter as tk


class ui_box:
    root = tk.Tk()
    widthpixels=130
    heightpixels=25
    root.geometry('{}x{}'.format(widthpixels, heightpixels))
    root.configure(background="green")
    label = tk.Label(root,text='Listening',width=10,anchor=tk.W,bg='green', fg = "white",font='Mincho 10')
    label.pack()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    _running = True

    def _update_ready(self):
        """Internal method to update UI on main thread"""
        try:
            self.root.lift()
            self.root.configure(background = "green")
            self.label.config(text='Listening!')
            self.label.config(bg = "green")
            self.root.attributes("-topmost", True)
        except:
            pass  # Ignore errors if main loop has exited

    def _update_busy(self):
        """Internal method to update UI on main thread"""
        try:
            self.root.configure(background = "red")
            self.label.config(text='analysing...')
            self.label.config(bg = "red")
            self.root.lift()
            self.root.attributes("-topmost", True)
        except:
            pass  # Ignore errors if main loop has exited

    def ready(self):
        """Thread-safe method to set UI to ready state"""
        if self._running:
            try:
                self.root.after(0, self._update_ready)
            except:
                pass  # Ignore errors if main loop has exited

    def busy(self):
        """Thread-safe method to set UI to busy state"""
        if self._running:
            try:
                self.root.after(0, self._update_busy)
            except:
                pass  # Ignore errors if main loop has exited

    def stop(self):
        """Mark UI as stopped"""
        self._running = False

