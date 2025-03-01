import tkinter as tk
import json
from PIL import Image, ImageTk
from tkinter import filedialog
import csv
from collections import defaultdict
import tkinter.ttk as ttk
import base64
import io

def load_info():
    with open("students.json", "r") as f:
        contents = f.read()
        student_info_list = contents.strip().split("\n")
        student_info_list = [json.loads(info) for info in student_info_list]
        return student_info_list

def search_info():
    student_info_list = load_info()
    display_info(info_frame, student_info_list)

def delete_class():
    result = tk.messagebox.askquestion("Confirmation", "Are you sure you want to delete the selected class?")

    if result == 'yes':
        # Delete class from student_info.json
        search_class = search_entry.get()
        with open("students.json", "r") as f:
            contents = f.read()
            student_info_list = contents.strip().split("\n")
            updated_student_info_list = []
            for info in student_info_list:
                student_info = json.loads(info)
                if not student_info["class"].lower().startswith(search_class.lower()):
                    updated_student_info_list.append(student_info)

        with open("students.json", "w") as f:
            for info in updated_student_info_list:
                f.write(json.dumps(info) + "\n")

        # Delete class from attendance.csv
        with open("attendance.csv", "r") as f:
            csv_reader = csv.reader(f)
            rows = [row for row in csv_reader if not row[3].lower().startswith(search_class.lower())]

        with open("attendance.csv", "w") as f:
            csv_writer = csv.writer(f)
            for row in rows:
                csv_writer.writerow(row)

        # Update display
        search_info()

def show_attendance(student_info):
    attendance_list = []
    with open("attendance.csv") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row[0] == student_info["name"]:
                for date_time in row[1:]:
                    attendance_list.append(date_time)

    # Create a new window for attendance display
    attendance_window = tk.Toplevel()
    attendance_window.title("Attendance")
    attendance_window.geometry("600x400")

    # Create a table to display the attendance
    table = ttk.Treeview(attendance_window)
    table['columns'] = ('Date', 'Time')
    table.column('#0', width=0, stretch='no')
    table.column('Date', anchor='center', width=200)
    table.column('Time', anchor='center', width=200)

    table.heading('Date', text='Date')
    table.heading('Time', text='Time')

    for attendance in attendance_list:
        date, time = attendance.split()
        table.insert('', 'end', text='', values=(date, time))

    table.pack(padx=10, pady=10)

    # Create a back button to return to the previous window
    back_button = tk.Button(attendance_window, text="Back", command=attendance_window.destroy, font=("Arial", 14), bg='#3498DB', fg='#FFF')
    back_button.pack(pady=10)

def display_info(info_frame, student_info_list):
    for widget in info_frame.winfo_children():
        widget.destroy()

    search_class = search_entry.get()
    for student_info in student_info_list:
        if student_info["class"].lower().startswith(search_class.lower()):
            student_frame = tk.Frame(info_frame, bg='#2C3E50')
            student_frame.pack(fill='x', padx=10, pady=5)

            image_base64 = student_info["image_base64"]
            image_bytes = base64.b64decode(image_base64)
            image_stream = io.BytesIO(image_bytes)
            img = Image.open(image_stream)
            img = img.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            image_label = tk.Label(student_frame, image=photo)
            image_label.image = photo
            image_label.pack(side='left', padx=10, pady=10)

            info_label = tk.Label(student_frame, text="Name: " + student_info["name"] + "\n" +
                                                        "ID: " + student_info["id_no"] + "\n" +
                                                        "Class: " + student_info["class"] + "\n",
                                  font=("Arial", 16), bg='#2C3E50', fg='#FFF')
            info_label.pack(side='right', padx=10, pady=10)

            # Count the number of days present
            attendance_list = []
            with open("attendance.csv") as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if row[0] == student_info["name"]:
                        attendance_list.extend(row[1:])

            num_days_present = len(attendance_list)
            days_present_label = tk.Label(student_frame, text="Days Present: " + str(num_days_present),
                                          font=("Arial", 14), bg='#2C3E50', fg='#FFF')
            days_present_label.pack(side='top', padx=10, pady=10)

            attendance_button = tk.Button(student_frame, text="Show Attendance",
                                          command=lambda info=student_info: show_attendance(info),
                                          font=("Arial", 14), bg='#3498DB', fg='#FFF')
            attendance_button.pack(pady=5)

            separator = ttk.Separator(info_frame, orient="horizontal")
            separator.pack(fill="x", pady=10)


# Create GUI window
window = tk.Tk()
window.title("Students Information By Class")
window.geometry("700x600")
window.resizable(False, False)
window.configure(bg='#F5F5F5')

icon_path = "UI/details.ico"  # Replace with the path to your icon file (.ico format)
window.iconbitmap(icon_path)

# Create "Search" button and search input field
search_frame = tk.Frame(window, bg='#F5F5F5')
search_frame.pack(pady=20)

search_label = tk.Label(search_frame, text="Search Class:", font=("Arial", 16), bg='#F5F5F5')
search_label.pack(side='left', padx=10)

search_entry = tk.Entry(search_frame, font=("Arial", 16), width=15)
search_entry.pack(side='left', padx=10)

search_button = tk.Button(search_frame, text="Search", command=search_info, font=("Arial", 16), bg='#3498DB', fg='#FFF')
search_button.pack(side='left', padx=10)

delete_button = tk.Button(search_frame, text="delete", command=delete_class, font=("Arial", 16), bg='#3498DB', fg='#FFF')
delete_button.pack(side='right', padx=10)


# Create scrollable frame to display student information
canvas = tk.Canvas(window, bg='#2C3E50')
canvas.pack(side='left', fill='both', expand=True, padx=20, pady=10)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.pack(side='right', fill='y', pady=10)
canvas.configure(yscrollcommand=scrollbar.set)
info_frame = tk.Frame(canvas, bg='#2C3E50')
info_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=info_frame, anchor='nw')

# Start GUI event loop
window.mainloop()
