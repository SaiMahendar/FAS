import tkinter as tk
import subprocess

# Define the function to run searchbyname.py
def search_by_name():
    subprocess.run(["python", "searchbyname.py"])

# Define the function to run searchbyclass.py
def search_by_class():
    subprocess.run(["python", "searchbyclass.py"])

# Create the main window
root = tk.Tk()
root.title("Search")
root.configure(bg="#e6f3ff")  # Set the background color of the window
root.geometry("400x300")  # Set the size of the window
root.resizable(False,False)
icon_path = "UI/details.ico"  # Replace with the path to your icon file (.ico format)
root.iconbitmap(icon_path)

# Create the button to search by name
button1 = tk.Button(root, text="Search by Name", bg="#99ccff", fg="white", command=search_by_name,
                    font=("Arial", 16), width=15, height=2,
                    highlightbackground="#b3d9ff", highlightcolor="#e6f3ff", highlightthickness=2, anchor="center")
button1.pack(pady=20)

# Create the button to search by class
button2 = tk.Button(root, text="Search by Class", bg="#336699", fg="white", command=search_by_class,
                    font=("Arial", 16), width=15, height=2,
                    highlightbackground="#4d87c7", highlightcolor="#99ccff", highlightthickness=2, anchor="center")
button2.pack(pady=20)

# Run the main loop
root.mainloop()
