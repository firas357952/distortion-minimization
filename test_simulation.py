import tkinter as tk

from animation import Animation

root = tk.Tk()

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_point = [screen_width // 2, screen_height // 2]

# Set your boundary and number of prototypes here
boundary = [[200, 200], [800, 200], [800, 500], [200, 500]]
num_prototypes = 5

animation = Animation(root, screen_width, screen_height, boundary, num_prototypes)
root.after(50, animation.update)
root.mainloop()
