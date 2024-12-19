import tkinter as tk
from Player.Player import Player


class RoundControlFrame:
    def __init__(self,parent_frame: tk.Frame):
        self.frame = tk.Frame(
            master=parent_frame,
            bg="grey",
            width=500,
            height=300
        )
        self.frame.pack_propagate(0)
        self.frame.pack(anchor="nw")

    def refresh(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def create_setup(self, controller):
        self.refresh()
        label = tk.Label(
            self.frame,
            text="How many players will play?")
        label.pack()
        entry = tk.Entry(
            self.frame,
            width=20
        )
        entry.pack()
        submit_button = tk.Button(
            self.frame,
            text="Submit",
            command=lambda: self.create_setup_next(entry, controller)
        )
        submit_button.pack()

    def create_setup_next(self, entry, controller):
        player_nb = entry.get()
        try:
            player_nb = int(player_nb)
        except ValueError:
            controller.logger.add_line(f"DEBUG: invalid number: {player_nb}")
            self.create_setup(self, controller)
            return
        self.refresh()

        input_frame = tk.Frame(self.frame)
        submit_frame = tk.Frame(self.frame)

        input_frame.pack(padx=20, pady=10)
        submit_frame.pack(pady=10)

        candidate_entries = []
        for i in range(player_nb):
            label = tk.Label(input_frame, text=f"Player {i + 1} Name:")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

            entry = tk.Entry(input_frame, width=20)
            entry.grid(row=i, column=1, padx=5, pady=5)
            candidate_entries.append(entry)

        submit_button = tk.Button(
            submit_frame,
            text="Submit",
            command=lambda: controller.setup_players([name.get() for name in candidate_entries]))
        submit_button.pack()

    def create_debug(self, controller, player_names: list, selected_player: Player = None):
        self.refresh()
        left_frame = tk.Frame(master=self.frame)
        left_frame.pack(side="left")
        select_frame = tk.Frame(master=left_frame)
        select_frame.pack(anchor="nw")
        button_frame = tk.Frame(master=left_frame)
        button_frame.pack(anchor="w")
        right_frame = tk.Frame(master=self.frame)
        right_frame.pack(side="right")
        player_info_frame = tk.Frame(master=right_frame)
        player_info_frame.pack(anchor="ne")

        clicked = tk.StringVar()
        if selected_player is None:
            clicked.set("select player")
        else:
            clicked.set(selected_player.get_name())

        drop = tk.OptionMenu (
            select_frame,
            clicked,
            *player_names
        )
        drop.configure(width=25)
        drop.pack(anchor="w")

        button = tk.Button(
            select_frame,
            text="select",
            command=lambda: controller.debug_player(clicked.get()),
            width=25
        )
        button.pack(anchor="w")

        text = "-"
        if selected_player is not None:
            text = f"selected: {selected_player.get_name()}\nscore: {selected_player.get_score()}"
        tk.Label(
            player_info_frame,
            text=text,
            font=("Arial", 18, "bold"),
            fg="black",
            bg="lightgrey",
            width=10
        ).pack(anchor="e")

        buttons = [5, 10, 20, 30, 40, 50]
        for i, button_option in enumerate(buttons):
            button = tk.Button(
                button_frame,
                text=button_option,
                command=lambda x=button_option: self.add_time(controller, clicked.get(), x),
                width=10
            )
            button.grid(row=i % 3, column=int(i/3))
        buttons = ["start", "stop"]
        for i, button_option in enumerate(buttons):
            button = tk.Button(
                button_frame,
                text=button_option,
                command=lambda x=button_option: self.control_timer(controller, clicked.get(), x),
                width=10
            )
            button.grid(row=3, column=i)

    def add_time(self, controller, player_name, time_added):
        controller.add_time(player_name, time_added)
        controller.debug_player(player_name)

    def control_timer(self, controller, player_name, timer_state):
        if timer_state == "start":
            controller.start_playing(player_name)
        elif timer_state == "stop":
            controller.stop_playing(player_name)
        controller.debug_player(player_name)

    def r2_create_questions(self, controller, questions, next_player):
        self.refresh()
        for i, question in enumerate(questions):
            if not question[1]:
                button = tk.Button(
                    self.frame,
                    text=question[0],
                    command=lambda r=question[0]: controller.r2_question(r),
                    bg="white",
                    fg="black",
                    font=("Helvetica", 8, "bold"),
                    width=75,
                    height=2
                )
                button.pack(anchor="nw")
            else:
                label = tk.Label(
                    self.frame,
                    text=question[0],
                    bg="white",
                    fg="red",
                    font=("Helvetica", 8),
                    width=75,
                    height=2
                )
                label.pack(anchor="nw")
        label = tk.Label(
            self.frame,
            text=f"Next up: {next_player}",
            bg="white",
            fg="red",
            font=("Helvetica", 8),
            width=75,
            height=2
        )
        label.pack(anchor="nw")

    def r2_create_answer(self, controller, answer_info):
        self.refresh()
        for i, answer in enumerate(answer_info):
            if not answer[1]:
                button = tk.Button(
                    self.frame,
                    text=answer[0],
                    command=lambda r=answer[0]: controller.r2_answer(r),
                    bg="white",
                    fg="black",
                    font=("Helvetica", 8, "bold"),
                    width=75,
                    height=2
                )
                button.pack(anchor="nw")
            else:
                label = tk.Label(
                    self.frame,
                    text=answer[0],
                    bg="white",
                    fg="red",
                    font=("Helvetica", 8),
                    width=75,
                    height=2
                )
                label.pack(anchor="nw")
        button = tk.Button(
            self.frame,
            text="pass",
            command=lambda: controller.r2_pass_question(),
            bg="grey",
            fg="black",
            font=("Helvetica", 10, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r2_create_pass(self, controller, next_player):
        self.refresh()
        button = tk.Button(
            self.frame,
            text=f"Next up: {next_player}",
            command=lambda: controller.r2_continue(),
            bg="white",
            fg="black",
            font=("Helvetica", 8, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r3_create_next(self, controller, next_player):
        self.refresh()
        button = tk.Button(
            self.frame,
            text=f"Next up: {next_player}",
            command=lambda: controller.r3_question(),
            bg="white",
            fg="black",
            font=("Helvetica", 8, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r3_create_answer(self, controller, answer_info):
        self.refresh()
        for i, answer in enumerate(answer_info):
            if not answer[1]:
                button = tk.Button(
                    self.frame,
                    text=answer[0],
                    command=lambda r=answer[0]: controller.r3_answer(r),
                    bg="white",
                    fg="black",
                    font=("Helvetica", 8, "bold"),
                    width=75,
                    height=2
                )
                button.pack(anchor="nw")
            else:
                label = tk.Label(
                    self.frame,
                    text=answer[0],
                    bg="white",
                    fg="red",
                    font=("Helvetica", 8),
                    width=75,
                    height=2
                )
                label.pack(anchor="nw")
        button = tk.Button(
            self.frame,
            text="pass",
            command=lambda: controller.r3_pass_question(),
            bg="grey",
            fg="black",
            font=("Helvetica", 10, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r3_create_pass(self, controller, next_player):
        self.refresh()
        button = tk.Button(
            self.frame,
            text=f"Next up: {next_player}",
            command=lambda: controller.r3_continue(),
            bg="white",
            fg="black",
            font=("Helvetica", 8, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r4_create_next(self, controller, next_player):
        self.refresh()
        button = tk.Button(
            self.frame,
            text=f"Next up: {next_player}",
            command=lambda: controller.r4_question(),
            bg="white",
            fg="black",
            font=("Helvetica", 8, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r4_create_answer(self, controller, answer_info):
        self.refresh()
        for i, answer in enumerate(answer_info):
            if not answer[1]:
                button = tk.Button(
                    self.frame,
                    text=answer[0],
                    command=lambda r=answer[0]: controller.r4_answer(r),
                    bg="white",
                    fg="black",
                    font=("Helvetica", 8, "bold"),
                    width=75,
                    height=2
                )
                button.pack(anchor="nw")
            else:
                label = tk.Label(
                    self.frame,
                    text=answer[0],
                    bg="white",
                    fg="red",
                    font=("Helvetica", 8),
                    width=75,
                    height=2
                )
                label.pack(anchor="nw")
        button = tk.Button(
            self.frame,
            text="pass",
            command=lambda: controller.r4_pass_question(),
            bg="grey",
            fg="black",
            font=("Helvetica", 10, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r4_create_pass(self, controller, next_player):
        self.refresh()
        button = tk.Button(
            self.frame,
            text=f"Next up: {next_player}",
            command=lambda: controller.r4_continue(),
            bg="white",
            fg="black",
            font=("Helvetica", 8, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r5_create_next(self, controller, next_player):
        self.refresh()
        button = tk.Button(
            self.frame,
            text=f"Next up: {next_player}",
            command=lambda: controller.r5_question(),
            bg="white",
            fg="black",
            font=("Helvetica", 8, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r5_create_answer(self, controller, answer_info):
        self.refresh()
        for i, answer in enumerate(answer_info):
            if not answer[1]:
                button = tk.Button(
                    self.frame,
                    text=answer[0],
                    command=lambda r=answer[0]: controller.r5_answer(r),
                    bg="white",
                    fg="black",
                    font=("Helvetica", 8, "bold"),
                    width=75,
                    height=2
                )
                button.pack(anchor="nw")
            else:
                label = tk.Label(
                    self.frame,
                    text=answer[0],
                    bg="white",
                    fg="red",
                    font=("Helvetica", 8),
                    width=75,
                    height=2
                )
                label.pack(anchor="nw")
        button = tk.Button(
            self.frame,
            text="pass",
            command=lambda: controller.r5_pass_question(),
            bg="grey",
            fg="black",
            font=("Helvetica", 10, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")

    def r5_create_pass(self, controller, next_player):
        self.refresh()
        button = tk.Button(
            self.frame,
            text=f"Next up: {next_player}",
            command=lambda: controller.r5_continue(),
            bg="white",
            fg="black",
            font=("Helvetica", 8, "bold"),
            width=75,
            height=2
        )
        button.pack(anchor="nw")
