import tkinter as tk
from tkinter import ttk
import csv
from PIL import Image, ImageTk
import subprocess
import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Function to open account creation window
def open_create_account_window():
    create_window = tk.Toplevel(root)
    create_window.title("Create Account")
    create_window.geometry("550x400")
    create_window.resizable(False, False)
    
    # Set window icon
    icon_path = "UI/login.ico"  # Replace with the path to your icon file (.ico format)
    create_window.iconbitmap(icon_path)

    # Create labels and entry fields for name, username, password, and confirm password
    name_label = ttk.Label(create_window, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = ttk.Entry(create_window, font=("Arial", 16))
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    username_label = ttk.Label(create_window, text="Username:")
    username_label.grid(row=1, column=0, padx=10, pady=10)
    username_entry = ttk.Entry(create_window, font=("Arial", 16))
    username_entry.grid(row=1, column=1, padx=10, pady=10)

    password_label = ttk.Label(create_window, text="Password:")
    password_label.grid(row=2, column=0, padx=10, pady=10)
    password_entry = ttk.Entry(create_window, show="*", font=("Arial", 16))
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    confirm_password_label = ttk.Label(create_window, text="Confirm Password:")
    confirm_password_label.grid(row=3, column=0, padx=10, pady=10)
    confirm_password_entry = ttk.Entry(create_window, show="*", font=("Arial", 16))
    confirm_password_entry.grid(row=3, column=1, padx=10, pady=10)

    # Create submit button
    submit_button = ttk.Button(create_window, text="Submit", command=lambda: create_account(create_window, name_entry.get(), username_entry.get(), password_entry.get(), confirm_password_entry.get()))
    submit_button.grid(row=4, columnspan=2, padx=10, pady=10)


# Rest of the code...

# Function to create account
def create_account(window, name, username, password, confirm_password):
    if not name or not username or not password or not confirm_password:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Password and Confirm Password do not match.")
        return

    # Open CSV file for appending
    with open('accounts.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, username, password])


    # Clear input fields
    window.destroy()
    messagebox.showinfo("Account Created", "Account created successfully.")

# Function to login
def login():
    # Get input values
    username = username_entry.get()
    password = password_entry.get()

    # Open CSV file for reading
    with open('accounts.csv', mode='r') as file:
        reader = csv.reader(file)
        found = False
        for row in reader:
            # Check if username and password match
            if row[1] == username and row[2] == password:
                found = True
                break

        # Show success message if match found, otherwise show error message
        if found:
            success_label.config(text="Login successful.")
            enter_button.config(state='normal')  # enable Enter button
        else:
            success_label.config(text="Invalid username or password.")
            enter_button.config(state='disabled')  # disable Enter button

        # Clear input fields
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)


# ... Rest of the code ...

# Function to show/hide password
def show_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        show_button.config(text='Hide')
    else:
        password_entry.config(show='*')
        show_button.config(text='Show')


# Function to launch index.py
def launch_index():
    subprocess.run(['python', 'index.py'])


# Create main window
root = tk.Tk()
root.title("FRAS Login")
root.resizable(False, False)

# Set window size and position
root.geometry("440x490")

# Set window icon
icon_path = "UI/login.ico"  # Replace with the path to your icon file (.ico format)
root.iconbitmap(icon_path)

# Load the background image
background_image = Image.open("background/login.png")
background_image = background_image.resize((440, 490))  # Resize the image to fit the window

# Create a PhotoImage object from the loaded image
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to hold the background image and place it on the window
background_label = ttk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create ttk style
style = ttk.Style()
style.configure("TLabel", font=('Helvetica', 16), heigth=50, foreground="#333", background="#F5F5F5")
style.configure("TEntry", font=('Helvetica', 16), heigth=50, fieldbackground="#FFF")

# Create input fields
username_label = ttk.Label(root, text="Username:")
username_label.place(x=190, y=50)
username_entry = ttk.Entry(root, font=("Arial", 16), width=20)
username_entry.place(x=115, y=80)

password_label = ttk.Label(root, text="Password:")
password_label.place(x=190, y=120)
password_entry = ttk.Entry(root, show="*", font=("Arial", 16), width=20)
password_entry.place(x=115, y=150)

# Create show password button
show_button = ttk.Button(root, text='Show', command=show_password)
show_button.place(x=190, y=183)

# Create "Create Account" button
create_account_button = ttk.Button(root, text="Create Account", command=open_create_account_window, width=15, style="Color.TButton")
create_account_button.place(x=140, y=310)


login_button = ttk.Button(root, text="Login", command=login, width=10, style="Color.TButton")
login_button.place(x=160, y=240)

# Create label for success/error messages
success_label = ttk.Label(root)
success_label.place(x=90, y=375)

# Create ENTER button to execute index.py
def execute_index():
    root.destroy()  # terminate current program
    subprocess.run(['python', 'index.py'])  # launch index.py

enter_button = ttk.Button(root, text="Enter", command=execute_index, state='disabled', width=10, style="Color.TButton")
enter_button.place(x=170, y=420)

# Configure style for colored buttons
style.configure("Color.TButton", font=('Helvetica', 14), background="yellow", foreground="blue", padding=8)

# Start main loop
root.mainloop()

