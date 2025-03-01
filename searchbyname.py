import tkinter as tk
import json
from PIL import Image, ImageTk
from tkinter import filedialog
import csv
from collections import defaultdict
import base64
import io

def load_info():
    with open("students.json", "r") as f:
        contents = f.read()
        student_info_list = contents.strip().split("\n")
        student_info_list = [json.loads(info) for info in student_info_list]
        return student_info_list

def delete_info():
    result = tk.messagebox.askquestion("Confirmation", "Are you sure you want to delete the selected student?")
    if result == 'yes':
        # Delete student from students.json
        search_name = search_entry.get()
        with open("students.json", "r") as f:
            contents = f.read()
            student_info_list = contents.strip().split("\n")
            updated_student_info_list = []
            for info in student_info_list:
                student_info = json.loads(info)
                if not student_info["name"].lower().startswith(search_name.lower()):
                    updated_student_info_list.append(student_info)

        with open("students.json", "w") as f:
            for info in updated_student_info_list:
                f.write(json.dumps(info) + "\n")

        # Delete student from attendance.csv
        with open("attendance.csv", "r") as f:
            csv_reader = csv.reader(f)
            rows = [row for row in csv_reader if not row[0].lower().startswith(search_name.lower())]

        with open("attendance.csv", "w") as f:
            csv_writer = csv.writer(f)
            for row in rows:
                csv_writer.writerow(row)

        # Update display
        search_info()
        delete_button.config(state=tk.DISABLED)

def display_info(info_frame, student_info_list):
    for widget in info_frame.winfo_children():
        widget.destroy()

    search_name = search_entry.get()
    for student_info in student_info_list:
        if student_info["name"].lower().startswith(search_name.lower()):
            name_label = tk.Label(info_frame, text="Name: " + student_info["name"], font=("Arial", 16))
            name_label.grid(row=0, column=0, pady=5)

            age_label = tk.Label(info_frame, text="ID: " + student_info["id_no"], font=("Arial", 16))
            age_label.grid(row=1, column=0, pady=5)

            class_label = tk.Label(info_frame, text="Class: " + student_info["class"], font=("Arial", 16))
            class_label.grid(row=2, column=0, pady=5)

            image_data = base64.b64decode(student_info["image_base64"])
            img = Image.open(io.BytesIO(image_data))
            img = img.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            image_label = tk.Label(info_frame, image=photo)
            image_label.image = photo
            image_label.grid(row=3, column=0, pady=5)

            # Count number of days present for student
            attendance_dict = defaultdict(int)
            with open("attendance.csv") as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if row[0] == student_info["name"]:
                        for date_time in row[1:]:
                            attendance_dict[date_time.split()[0]] += 1

            # Display number of days present for student
            attendance_label = tk.Label(info_frame, text="Days Present: " + str(len(attendance_dict)), font=("Arial", 16))
            attendance_label.grid(row=4, column=0, pady=5)

            # Enable the "Delete" button
            delete_button.config(state=tk.NORMAL)

def search_info():
    student_info_list = load_info()
    display_info(info_frame, student_info_list)

# Create GUI window
window = tk.Tk()
window.title("Student Information By Name")
window.geometry("400x520")
window.configure(bg='#2C3E50')

icon_path = "UI/details.ico"  # Replace with the path to your icon file (.ico format)
window.iconbitmap(icon_path)

# Create "Search" button and search input field
search_button = tk.Button(window, text="Search", command=search_info, font=("Arial", 16), bg='#3498DB', fg='#FFF')
search_button.grid(row=0, column=0, padx=10, pady=10)

search_entry = tk.Entry(window, font=("Arial", 16))
search_entry.grid(row=0, column=1, padx=10, pady=10)
search_entry.bind("<Return>", search_info)  # Bind Enter key to search_info function

# Create frame to display student information
info_frame = tk.Frame(window)
info_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

# Create "Delete" button
delete_button = tk.Button(window, text="Delete", command=delete_info, font=("Arial", 16), bg='#E74C3C', fg='#FFF')
delete_button.config(state=tk.DISABLED)  # Disable the button initially
delete_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

# Start GUI event loop
window.mainloop()
