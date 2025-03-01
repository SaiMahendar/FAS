import tkinter as tk
import subprocess
from PIL import Image, ImageTk

# Create the root window
root = tk.Tk()

# Set the window size to match the desktop
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

root.title("Face Recognition Attendance System")

# Set the window state to maximized
root.state('zoomed')

root.resizable(False,False)
icon_path = "UI/index.ico"  # Replace with the path to your icon file (.ico format)
root.iconbitmap(icon_path)
# Load the background image
background_image = Image.open("background/index.jpg")
background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))  # Resize the image to fit the window

# Create a PhotoImage object from the loaded image
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to hold the background image and place it on the window
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set the window color to light blue
root.configure(background='light blue')

def show_options():
    # Remove the existing widgets
    welcome_label.pack_forget()
    enter_button.pack_forget()
    enter_button.place_forget()

    # Place the options buttons in a list-style format
    options_frame.pack(pady=60)
    attendance_button.pack(pady=10)
    details_button.pack(pady=10)
    entry_button.pack(pady=10)
    end_button.pack(pady=10)

    # Bind the "END" button to terminate the program
    end_button.configure(command=root.destroy)

welcome_label = tk.Label(root, text="Face Recognition Attendance System", font=("Arial", 25), bg="light blue")
welcome_label.pack(pady=50)

# Create enter button
enter_button = tk.Button(root, text="Enter", bg="violet", font=("Arial", 20), height=3, width=15, command=show_options)
enter_button.pack(pady=20)

def execute_atten():
    subprocess.run(['python', 'window.py'])  # launch attendance.py

def execute_details():
    subprocess.run(['python', 'details.py'])  # launch data.py

def execute_info():
    subprocess.run(['python', 'create info.py'])  # launch attendance.py


# Create options frame
options_frame = tk.Frame(root, bg="light blue")

# Define the ToolTip class for creating tooltips
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="light yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# Create the options buttons with big size
attendance_button = tk.Button(options_frame, text="Attendance", font=("Arial", int(root.winfo_screenwidth()/50)), bg="light green", width=20, height=2)
details_button = tk.Button(options_frame, text="Details", font=("Arial", int(root.winfo_screenwidth()/50)), bg="yellow", width=20, height=2)
entry_button = tk.Button(options_frame, text="Entry", font=("Arial", int(root.winfo_screenwidth()/50)), bg="orange", width=20, height=2)
end_button = tk.Button(options_frame, text="END", font=("Arial", int(root.winfo_screenwidth()/50)), bg="red", width=20, height=2)

# Create tooltips for the options buttons
attendance_tooltip = ToolTip(attendance_button, "Hello")
details_tooltip = ToolTip(details_button, "Hello")
entry_tooltip = ToolTip(entry_button, "Hello")
end_tooltip = ToolTip(end_button, "Hello")

# Create the options buttons with big size
attendance_button = tk.Button(options_frame, text="Attendance", command=execute_atten, font=("Arial", int(root.winfo_screenwidth()/50)), bg="light green", width=20, height=2)
details_button = tk.Button(options_frame, command=execute_details, text="Details", font=("Arial", int(root.winfo_screenwidth()/50)), bg="yellow", width=20, height=2)
entry_button = tk.Button(options_frame, text="Entry", command=execute_info, font=("Arial", int(root.winfo_screenwidth()/50)), bg="orange", width=20, height=2)
end_button = tk.Button(options_frame, text="END", font=("Arial", int(root.winfo_screenwidth()/50)), bg="red", width=20, height=2)

# Create tooltips for the options buttons
attendance_tooltip = ToolTip(attendance_button, "START TAKING ATTENDANCE")
details_tooltip = ToolTip(details_button, "CHECK STUDENT DEATILS")
entry_tooltip = ToolTip(entry_button, "CREATE STUDENTS DETAILS TO DATABASE")
end_tooltip = ToolTip(end_button, "EXIT/CLOSE THE APPLICATION")

# ... Rest of your code ...

# Bind the "Enter" button to the show_options() function
enter_button.configure(command=show_options)

# Center the "Enter" button vertically in the window
enter_button.pack(pady=(root.winfo_screenheight()//2, 0))

# Center the "Enter" button in the window
enter_button.place(relx=0.5, rely=0.5, anchor="center")

# Run the main loop of the application
root.mainloop()
