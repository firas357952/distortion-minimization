import tkinter as tk

from animation import Animation

root = tk.Tk()

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set your boundary and number of prototypes here
boundary = [[100, 100], [700, 100], [700, 500], [100, 500]]
num_prototypes = 10

animation = Animation(root, screen_width, screen_height, boundary, num_prototypes)
root.after(50, animation.update)
root.mainloop()
