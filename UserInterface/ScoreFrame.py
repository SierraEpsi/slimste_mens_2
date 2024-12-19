import tkinter as tk


class ScoreFrame:
    def __init__(self, parent_frame: tk.Frame):
        self.current_player = None
        self.frame = tk.Frame(
            master=parent_frame,
            bg="red",
            width=1000,
            height=100
        )
        self.frame.pack_propagate(0)
        self.frame.pack(anchor="sw")
        self.refresh()

    def refresh(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def draw_score(self, players: list):
        self.refresh()
        for i, player in enumerate(players):
            if player.get_name() == self.current_player:
                tk.Label(
                    self.frame,
                    text=f"{player.get_name()}\n{player.get_score()} seconds",
                    font=("Arial", 30, "bold"),
                    fg="orange",
                    bg="red",
                    padx=10,
                    pady=5,
                ).grid(row=0, column=i, padx=5, pady=5)
            else:
                tk.Label(
                    self.frame,
                    text=f"{player.get_name()}\n{player.get_score()} seconds",
                    font=("Arial", 30, "bold"),
                    fg="white",
                    bg="red",
                    padx=10,
                    pady=5,
                ).grid(row=0, column=i, padx=5, pady=5)

    def update_current_player(self, current_player):
        self.current_player = current_player

