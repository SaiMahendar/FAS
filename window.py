import tkinter as tk
import subprocess

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.is_running = False
        
        # Create the start and stop buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_recognition, font=("Arial", 14))
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_recognition, state=tk.DISABLED, font=("Arial", 14))
        
        # Add the buttons to the window
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Bind hover events to the buttons
        self.start_button.bind("<Enter>", lambda event: self.start_button.config(bg="#007acc", fg="white", cursor="hand2"))
        self.start_button.bind("<Leave>", lambda event: self.start_button.config(bg="SystemButtonFace", fg="black", cursor="arrow"))
        self.stop_button.bind("<Enter>", lambda event: self.stop_button.config(bg="#cc0000", fg="white", cursor="hand2"))
        self.stop_button.bind("<Leave>", lambda event: self.stop_button.config(bg="SystemButtonFace", fg="black", cursor="arrow"))
        
    def start_recognition(self):
        if not self.is_running:
            # Enable the stop button and disable the start button
            self.stop_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.DISABLED)
            
            # Start the face recognition process
            self.process = subprocess.Popen(['python', 'attendance.py'])
            self.is_running = True
        
    def stop_recognition(self):
        if self.is_running:
            # Disable the stop button and enable the start button
            self.stop_button.config(state=tk.DISABLED)
            self.start_button.config(state=tk.NORMAL)
            
            # Stop the face recognition process
            self.process.terminate()
            self.is_running = False

# Create the main window
root = tk.Tk()
root.title("Attendance")
root.geometry("300x100")

# Set the window to be transparent
root.attributes("-alpha", 0.8)

# Set window icon
icon_path = "UI/index.ico"  # Replace with the path to your icon file (.ico format)
root.iconbitmap(icon_path)

# Create the FaceRecognitionApp object and run the main loop
app = FaceRecognitionApp(root)
root.mainloop()
