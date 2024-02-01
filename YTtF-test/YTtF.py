import tkinter as tk
from tkinter import ttk

Amethyst_Violet = "#7506c5"
Midnight_Purple = "#22013a"
Cursed_Black = "#131313"
Young_Night = "#232323"
Raven_Black = "#3d3d3d"
Pure_White = "#ffffff"

L0_window = tk.Tk()
L0_window_height_width_multiplier = 100   # Ratio is 16:9 for the screen; multiplier of "1" gives a screen of 16 pixels wide by 9 pixels tall.
L0_window_width = 16*L0_window_height_width_multiplier
L0_window_height = 9*L0_window_height_width_multiplier
width_height_ratio = int(L0_window_height) / int(L0_window_width)
L0_window_resizable_boolean = False
L0_window.geometry(f"{L0_window_width}x{L0_window_height}")
L0_window.resizable(L0_window_resizable_boolean, L0_window_resizable_boolean)

L1_toolbar_ribbon_frame = tk.Frame(L0_window, bg=Amethyst_Violet, height=23, width=L0_window_width)
L1_toolbar_ribbon_frame.grid_propagate(0)
L1_toolbar_ribbon_frame.grid(row=0, column=0)



L2_toolbar_ribbon_dropdown_one_options = [
    '', 
    "Simple", 
    "Advanced"
] 
L2_toolbar_ribbon_dropdown_one_selected = tk.StringVar()
L2_toolbar_ribbon_dropdown_one_selected.set(L2_toolbar_ribbon_dropdown_one_options[1]) 
L2_toolbar_ribbon_dropdown_one_style = ttk.Style()
L2_toolbar_ribbon_dropdown_one_style.configure("style1.TMenubutton", foreground=Pure_White, background=Midnight_Purple, relief="raised", width=round(0.011*L0_window_width), borderwidth=round(L0_window_height_width_multiplier/16), sticky=tk.NS)
L2_toolbar_ribbon_dropdown_one = ttk.OptionMenu(L1_toolbar_ribbon_frame , L2_toolbar_ribbon_dropdown_one_selected , *L2_toolbar_ribbon_dropdown_one_options, style="style1.TMenubutton") 
L2_toolbar_ribbon_dropdown_one.grid()



L1_contents_frame = tk.Frame(L0_window, height=L0_window_height-23, width=L0_window_width)
L1_contents_frame.grid_propagate(0)
L1_contents_frame.grid(row=1, column=0)



L2_settings_frame = tk.Frame(L1_contents_frame, bg=Cursed_Black, height=L0_window_height-23, width=round(0.23*L0_window_width))
L2_settings_frame.grid_propagate(0)
L2_settings_frame.grid(row=0, column=0)
L3_settings_contents_frame = tk.Frame(L2_settings_frame, bg=Young_Night, relief="ridge", borderwidth=3, height=round(0.935763888888889*L0_window_height), width=round(0.21484375*L0_window_width))
L3_settings_contents_frame.grid(row=0, column=0)


# Calculate the center coordinates of L2_settings_frame
x_center = L2_settings_frame.winfo_reqwidth() / 2
y_center = L2_settings_frame.winfo_reqheight() / 2

# Calculate the coordinates for placing L3_settings_contents_frame in the center of L2_settings_frame
x_offset = (L3_settings_contents_frame.winfo_reqwidth() / 2)
y_offset = (L3_settings_contents_frame.winfo_reqheight() / 2)

# Place L3_settings_contents_frame in the center of L2_settings_frame
L3_settings_contents_frame.place(x=x_center - x_offset, y=y_center - y_offset)






L2_contents_frame = tk.Frame(L1_contents_frame, bg=Raven_Black, height=L0_window_height-23, width=round(0.77*L0_window_width))
L2_contents_frame.grid_propagate(0)
L2_contents_frame.grid(row=0, column=1)




L0_window.mainloop()





















































































































































































































































































"""
class Robot:
    class_variable = 0  # Class variable shared among all instances

    def __init__(self, num):
        self.number = num  # Instance variable unique to each instance

    @classmethod
    def set_class_variable(cls, value):  # Corrected: Added cls parameter
        cls.class_variable = value

    def set_instance_variable(self, value):
        self.number = value

    # Define class method to allow access to class variable
    @classmethod
    def get_class_variable(cls):
        return cls.class_variable
    
    def get_instance_variable(self):
        return self.number

# Create an instance of the Robot class
robot1 = Robot(1)

# Use the mutator methods to change class and instance variables
Robot.set_class_variable(5)  # Change class variable
robot1.set_instance_variable(10)  # Change instance variable

# Access the variables
print(Robot.get_class_variable())  # Output: 5
print(robot1.get_instance_variable())  # Output: 10


for x in range(40):
    globals()[f"robo{x}"] = Robot(3)

print(robo2.get_instance_variable())
"""