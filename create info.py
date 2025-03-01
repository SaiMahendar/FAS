import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox
import json
from PIL import Image, ImageTk
import base64
import io

def save_info():
    # Get input values from the GUI
    name = name_entry.get()
    id_no = id_no_entry.get()
    student_class = class_entry.get()

    # Check if any input field is empty
    if name == "" or id_no == "" or student_class == "":
        # Display error message and return
        error_label.configure(text="Please fill out all fields")
        error_label.grid()
        return
    else:
        error_label.grid_remove()

    # Check if ID No. is already in use
    with open("students.json", "r") as f:
        for line in f:
            if id_no == json.loads(line)["id_no"]:
                error_label.config(text="ID No. already in use")
                error_label.grid()
                return
            else:
                id_no_error_label.grid_remove()

    # Load existing student data from JSON file
    try:
        with open("students.json", "r") as f:
            student_list = json.load(f)
    except json.decoder.JSONDecodeError:
        student_list = []

    # Convert the image to base64 format
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Store new student information in dictionary
    student_info = {
        "name": name,
        "id_no": id_no,
        "class": student_class,
        "image_base64": encoded_image,
    }

    # Show confirmation message box
    confirm = messagebox.askokcancel(
        "Confirmation",
        f"Are you sure you want to save the following information?\n\nName: {name}\nID: {id_no}\nClass: {student_class}"
    )

    if confirm:
        # Save student information to JSON file
        with open("students.json", "a") as f:
            json.dump(student_info, f)
            f.write("\n")

        # Clear input fields and reset image label
        name_entry.delete(0, tk.END)
        id_no_entry.delete(0, tk.END)
        class_entry.delete(0, tk.END)
        clear_image_label()
        error_label.configure(text="")
        error_label.grid_remove()

def clear_image_label():
    # Reset the image label to an empty placeholder image
    placeholder_image = Image.open("UI/placeholder.jpg")
    placeholder_image = placeholder_image.resize((100, 100), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(placeholder_image)
    image_label.configure(image=photo)
    image_label.image = photo

def browse_image():
    # Open file dialog box to select image file
    file_path = filedialog.askopenfilename()
    if file_path:
        # Load selected image file and display it in the GUI
        global image_path
        image_path = file_path
        img = Image.open(image_path)
        img = img.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        image_label.configure(image=photo)
        image_label.image = photo
        image_label.grid()
    else:
        image_label.grid_remove()

def validate_name(input_str):
    # Check if input string contains alphabets, spaces, and dots
    if all(char.isalpha() or char.isspace() or char == '.' for char in input_str):
        return True
    else:
        return False

def validate_id(input_str):
    # Check if input string only contains digits
    if input_str.isdigit():
        return True
    else:
        return False

# Create GUI window
window = tk.Tk()
window.title("Create Student Information")
window.geometry("430x450")
window.resizable(False,False)

icon_path = "UI/create info.ico"  # Replace with the path to your icon file (.ico format)
window.iconbitmap(icon_path)

# Load the background image
background_image = Image.open("background/info.jpg")
background_image = background_image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))  # Resize the image to fit the window

# Create a PhotoImage object from the loaded image
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to hold the background image and place it on the window
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a label to hold the background image and place it on the window
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create "Browse" button to select image file
browse_button = tk.Button(window, text="Browse", command=browse_image, font=("Arial", 16))
browse_button.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Create label to display selected image
image_label = tk.Label(window)
image_label.grid(row=1, column=0, columnspan=2)
image_label.grid_remove()

# Create input fields and labels
name_label = tk.Label(window, text="Name:", font=("Arial", 16))
name_label.grid(row=2, column=0, padx=10, pady=10)
name_entry = tk.Entry(window, font=("Arial", 16), width=25, validate="key")
name_entry.grid(row=2, column=1, padx=10, pady=10)
name_entry.configure(validatecommand=(name_entry.register(validate_name), "%S"))

# Create label to display error message for name field
name_error_label = tk.Label(window, text="", font=("Arial", 12), fg="red")
name_error_label.grid(row=3, column=1, pady=5)
name_error_label.grid_remove()

# Create input fields and labels
id_no_label = tk.Label(window, text="ID No.:", font=("Arial", 16))
id_no_label.grid(row=3, column=0, padx=10, pady=10)
id_no_entry = tk.Entry(window, font=("Arial", 16), width=25, validate="key")
id_no_entry.grid(row=3, column=1, padx=10, pady=10)
id_no_entry.configure(validatecommand=(id_no_entry.register(validate_id), "%S"))

# Create label to display error message for id_no field
id_no_error_label = tk.Label(window, text="", font=("Arial", 12), fg="red")
id_no_error_label.grid(row=5, column=1, pady=5)
id_no_error_label.grid_remove()

class_label = tk.Label(window, text="Class:", font=("Arial", 16))
class_label.grid(row=4, column=0, padx=10, pady=10)
class_entry = tk.Entry(window, font=("Arial", 16), width=25)
class_entry.grid(row=4, column=1, padx=10, pady=10)

# Create "Save" button
save_button = tk.Button(window, text="Save", command=save_info, font=("Arial", 16))
save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Create label to display error message
error_label = tk.Label(window, text="", font=("Arial", 12), fg="red")
error_label.grid(row=6, column=0, columnspan=2, pady=10)
error_label.grid_remove()

# Start GUI event loop
window.mainloop()
