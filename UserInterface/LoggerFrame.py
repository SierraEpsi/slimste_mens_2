import tkinter as tk


class LoggerFrame:
    def __init__(self, parent_frame: tk.Frame):
        self.lines = []
        self.frame = tk.Frame(
            master=parent_frame,
            bg="white",
            width=500,
            height=200
        )
        self.frame.pack_propagate(0)
        self.frame.pack(anchor="sw")
        self.refresh()

    def add_line(self, line: str):
        if len(self.lines) > 10:
            self.lines.pop(0)
        self.lines.append(line)
        self.refresh()

    def generate_text(self) -> str:
        return "\n".join(self.lines)

    def refresh(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        label = tk.Label(
            self.frame,
            text=self.generate_text(),
            font=("Arial", 8),
            fg="black",
            bg="white",
            padx=10,
            pady=10
        )
        label.pack(anchor="w")

