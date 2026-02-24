from __future__ import annotations

import random
import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox

from pet.config import load_config, save_config
from pet.logic import PetState, advance_motion, choose_next_mood, feed


MESSAGES = {
    "happy": ["I love hanging out with you!", "What a great day!", "Tail wiggles!"],
    "curious": ["What's that over there?", "Hmm... interesting.", "I heard a noise!"],
    "sleepy": ["Yaaawn...", "Need a tiny nap.", "Snuggle time?"],
    "playful": ["Let's play!", "Zoom zoom!", "Catch me if you can!"],
}


class DesktopPetApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Desktop Pet")
        self.root.geometry("260x260+100+100")
        self.root.attributes("-topmost", True)

        self.config = load_config()
        self.rng = random.Random()

        self.canvas = tk.Canvas(root, width=260, height=260, bg="#fffef8", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.state = PetState(x=120, y=120, vx=self.config.speed, vy=self.config.speed)

        self.pet = self.canvas.create_oval(95, 95, 165, 165, fill=self.config.color, outline="#333", width=2)
        self.eyes_left = self.canvas.create_oval(115, 120, 125, 130, fill="#222")
        self.eyes_right = self.canvas.create_oval(135, 120, 145, 130, fill="#222")
        self.mouth = self.canvas.create_arc(118, 132, 142, 150, start=200, extent=140, style=tk.ARC, width=2)

        self.name_label = self.canvas.create_text(130, 68, text=self.config.pet_name, font=("Arial", 11, "bold"))
        self.speech = self.canvas.create_text(130, 36, text="", font=("Arial", 10), width=220)

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<Button-3>", self.show_menu)

        self.drag_offset = (0, 0)
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Feed", command=self.feed_pet)
        self.menu.add_command(label="Rename", command=self.rename_pet)
        self.menu.add_command(label="Change Color", command=self.change_color)
        self.menu.add_separator()
        self.menu.add_command(label="About", command=self.show_about)
        self.menu.add_command(label="Quit", command=self.quit)

        self.animate()
        self.talk_loop()

    def move_pet(self, dx: int, dy: int) -> None:
        for item in (self.pet, self.eyes_left, self.eyes_right, self.mouth, self.name_label, self.speech):
            self.canvas.move(item, dx, dy)

    def animate(self) -> None:
        width = self.canvas.winfo_width() - 70
        height = self.canvas.winfo_height() - 70
        old_x, old_y = self.state.x, self.state.y
        self.state = advance_motion(self.state, width, height)
        dx, dy = self.state.x - old_x, self.state.y - old_y
        self.move_pet(dx, dy)

        if self.state.energy <= 0:
            self.state.vx = 0
            self.state.vy = 0
            self.state.mood = "sleepy"
            self.canvas.itemconfig(self.speech, text=f"{self.config.pet_name} is sleeping 😴")
        else:
            if self.rng.random() < 0.1:
                self.state.mood = choose_next_mood(self.rng, self.state.energy)

            if self.state.mood == "playful":
                self.state.vx = 8 if self.state.vx >= 0 else -8
                self.state.vy = 8 if self.state.vy >= 0 else -8
            elif self.state.mood == "sleepy":
                self.state.vx = 3 if self.state.vx >= 0 else -3
                self.state.vy = 3 if self.state.vy >= 0 else -3
            else:
                base = max(3, self.config.speed)
                self.state.vx = base if self.state.vx >= 0 else -base
                self.state.vy = base if self.state.vy >= 0 else -base

        self.root.after(70, self.animate)

    def talk_loop(self) -> None:
        mood = self.state.mood
        if mood in MESSAGES:
            self.canvas.itemconfig(self.speech, text=self.rng.choice(MESSAGES[mood]))
        self.root.after(self.config.speech_frequency_ms, self.talk_loop)

    def on_click(self, event: tk.Event) -> None:
        self.drag_offset = (event.x - self.state.x, event.y - self.state.y)
        self.canvas.itemconfig(self.speech, text=f"*{self.config.pet_name} chirps happily*")

    def on_drag(self, event: tk.Event) -> None:
        target_x = event.x - self.drag_offset[0]
        target_y = event.y - self.drag_offset[1]
        dx, dy = target_x - self.state.x, target_y - self.state.y
        self.move_pet(dx, dy)
        self.state.x = target_x
        self.state.y = target_y

    def show_menu(self, event: tk.Event) -> None:
        self.menu.tk_popup(event.x_root, event.y_root)

    def feed_pet(self) -> None:
        self.state = feed(self.state)
        self.canvas.itemconfig(self.speech, text=f"Yum! Thanks for the snack 🍪")

    def rename_pet(self) -> None:
        new_name = simpledialog.askstring("Rename pet", "Enter a new name:", initialvalue=self.config.pet_name)
        if new_name:
            self.config.pet_name = new_name.strip()
            self.canvas.itemconfig(self.name_label, text=self.config.pet_name)
            save_config(self.config)

    def change_color(self) -> None:
        color = colorchooser.askcolor(title="Pick pet color", initialcolor=self.config.color)[1]
        if color:
            self.config.color = color
            self.canvas.itemconfig(self.pet, fill=color)
            save_config(self.config)

    def show_about(self) -> None:
        messagebox.showinfo("About Desktop Pet", "Desktop Pet\nA tiny animated buddy for your screen.")

    def quit(self) -> None:
        save_config(self.config)
        self.root.destroy()


if __name__ == "__main__":
    app_root = tk.Tk()
    DesktopPetApp(app_root)
    app_root.mainloop()
