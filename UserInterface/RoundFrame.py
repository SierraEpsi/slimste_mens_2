import tkinter as tk
import random

from PIL import Image, ImageTk


class RoundFrame:
    def __init__(self, parent_frame: tk.Frame):
        self.frame = tk.Frame(
            master=parent_frame,
            bg="red",
            width=1000,
            height=600
        )
        self.frame.pack()

        image_path = "images/intro.jpg"
        image = Image.open(image_path)
        image = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.frame, image=image)
        image_label.pack()

    def refresh(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def r2_draw(self, answers_info):
        self.refresh()
        for i, answer in enumerate(answers_info):
            color = "red"
            if answer[1]:
                color = "white"
            label = tk.Label(
                master=self.frame,
                text=answer[0],
                font=("Arial", 40, "bold"),
                fg=color,
                bg="red",
                padx=10,
                pady=5,
            )
            label.grid(row=i, column=0, padx=5, pady=5)

    def r3_draw(self, question_hints, answers_info):
        self.refresh()

        upper_frame = tk.Frame(
            master=self.frame,
            bg="red", width=1000, height=400)
        upper_frame.pack_propagate(0)
        lower_frame = tk.Frame(
            master=self.frame,
            bg="grey", width=1000, height=200)
        upper_frame.pack_propagate(0)
        upper_frame.pack(anchor="nw")
        lower_frame.pack(anchor="nw")

        for i, hint in enumerate(question_hints):
            color = "white"
            if hint[1]:
                color = hint[2]
            label = tk.Label(
                master=upper_frame,
                text=hint[0],
                font=("Arial", 22, "bold"),
                fg=color,
                bg="red",
                padx=10,
                pady=5,
            )
            label.grid(row=int(i/3), column=i % 3, padx=5, pady=5)

        for i, answer in enumerate(answers_info):
            color = "red"
            if answer[1]:
                color = answer[2]
            label = tk.Label(
                master=lower_frame,
                text=answer[0],
                font=("Arial", 20, "bold"),
                fg=color,
                bg="red",
                padx=10,
                pady=5,
            )
            label.grid(row=0, column=i, padx=5, pady=5)

    def r4_draw(self, answers_info):
        self.refresh()
        for i, answer in enumerate(answers_info):
            color = "red"
            if answer[1]:
                color = "white"
            label = tk.Label(
                master=self.frame,
                text=answer[0],
                font=("Arial", 40, "bold"),
                fg=color,
                bg="red",
                padx=10,
                pady=5,
            )
            label.grid(row=i, column=0, padx=5, pady=5)

    def r5_draw(self, answers_info):
        self.refresh()
        for i, answer in enumerate(answers_info):
            color = "red"
            if answer[1]:
                color = "white"
            label = tk.Label(
                master=self.frame,
                text=answer[0],
                font=("Arial", 40, "bold"),
                fg=color,
                bg="red",
                padx=10,
                pady=5,
            )
            label.grid(row=i, column=0, padx=5, pady=5)



