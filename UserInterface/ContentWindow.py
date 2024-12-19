import tkinter as tk


class ContentWindow:
    def __init__(self, parent_window):
        self.window = tk.Toplevel(parent_window)
        self.window.transient(parent_window)
        self.window.title("De Slimste Weet-Ik-Veel")

        self.window.geometry("1500x700")
        self.window.resizable(0, 0)

        # Set up frame structure
        upper_frame = tk.Frame(
            master=self.window,
            bg="grey", width=1500, height=600)
        upper_frame.pack_propagate(0)
        lower_frame = tk.Frame(
            master=self.window,
            bg="red", width=1500, height=100)
        lower_frame.pack_propagate(0)

        upper_frame.pack(side="top", fill="x")
        lower_frame.pack(side="bottom", fill="x")

        self.upper_frame = upper_frame
        self.lower_frame = lower_frame

    def get_upper_frame(self) -> tk.Frame:
        return self.upper_frame

    def get_lower_frame(self) -> tk.Frame:
        return self.lower_frame
