import tkinter as tk
from UserInterface.LoggerFrame import LoggerFrame


class ControlWindow:
    def __init__(self, controller):
        self.window = tk.Tk()
        self.window.title("Control")

        self.window.geometry("700x500")
        self.window.resizable(0, 0)

        left_frame = tk.Frame(
            master=self.window,
            bg="red", width=200, height=500)
        left_frame.pack_propagate(0)
        right_frame = tk.Frame(
            master=self.window,
            bg="grey", width=500, height=500)
        right_frame.pack_propagate(0)
        left_frame.pack(side="left", fill="y")
        right_frame.pack(side="right", fill="y")
        self.create_menu(left_frame, controller)
        self.right_frame = right_frame

    def create_menu(self, frame: tk.Frame, controller):
        pages = ["Setup","Debug","Porte Ouverte","Tour de Puzzle","Galerie","Mémoire collective","Final"]
        menu_buttons = [
            tk.Button(
                frame,
                text=page_name,
                command=lambda r=page_name: controller.menu_click(r),
                bg="red",
                fg="black",
                font=("Helvetica", 12, "bold"),
                width=20,
                height=1
            ) for page_name in pages
        ]
        for i, button in enumerate(menu_buttons):
            button.pack(anchor='nw')

    def start(self):
        self.window.mainloop()

    def plan_refresh(self, controller):
        self.window.after(1000, lambda: controller.refresh_score())

    def get_window(self):
        return self.window

    def get_right_frame(self) -> tk.Frame:
        return self.right_frame
