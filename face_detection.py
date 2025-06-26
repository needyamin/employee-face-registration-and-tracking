import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import cv2
from PIL import Image, ImageTk
from retinaface import RetinaFace
import numpy as np
import os
import datetime
import threading
import queue
import data

# Global dictionary to store registered faces
known_faces = {}

# --- Utility Functions ---
def detect_and_register(image_path, name):
    try:
        faces = RetinaFace.extract_faces(img_path=image_path, align=True)
        if not faces:
            return None
        face_img = faces[0]  # Take the first detected face
        encoding = np.mean(face_img, axis=(0, 1))  # Simple encoding
        known_faces[name] = {
            'encoding': encoding,
            'image': face_img
        }
        return face_img
    except Exception as e:
        print(f"[ERROR] Face detection failed: {e}")
        return None

def log_movement(name):
    with open("movement_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {name} moved in front of camera\n")

# --- GUI Functions ---
def update_face_list():
    face_listbox.delete(*face_listbox.get_children())
    for name, data in known_faces.items():
        img = Image.fromarray(data['image'])
        img = img.resize((40, 40))
        photo = ImageTk.PhotoImage(img)
        face_thumbnails[name] = photo  # Keep reference
        face_listbox.insert('', 'end', iid=name, text=name, image=photo)

def show_status(msg, color=None):
    status_var.set(msg)
    if color:
        status_bar.config(foreground=color)
    else:
        status_bar.config(foreground='black')

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not file_path:
        show_status("No file selected.", 'red')
        return
    try:
        img = Image.open(file_path)
        img.thumbnail((180, 180))
        photo = ImageTk.PhotoImage(img)
        preview_label.configure(image=photo)
        preview_label.image = photo
        preview_label.file_path = file_path
        show_status("Image loaded. Enter name and register.", 'blue')
    except Exception as e:
        show_status(f"Error loading image: {e}", 'red')

registration_queue = queue.Queue()

# --- Progress Indicator ---
def show_progress():
    progress_bar.grid(row=7, column=0, columnspan=2, pady=5, sticky='ew')
    progress_bar.start(10)
    root.update_idletasks()

def hide_progress():
    progress_bar.stop()
    progress_bar.grid_remove()
    root.update_idletasks()

# --- Threaded Registration ---
def threaded_register_face():
    name = name_entry.get().strip()
    file_path = getattr(preview_label, 'file_path', None)
    if not name:
        messagebox.showerror("Error", "Please enter employee name.")
        return
    if not file_path:
        messagebox.showerror("Error", "Please upload an image.")
        return
    show_status("Registering face, please wait...", 'blue')
    show_progress()
    def worker():
        face = detect_and_register(file_path, name)
        registration_queue.put((face, name))
    threading.Thread(target=worker, daemon=True).start()
    root.after(100, check_registration_result)

def check_registration_result():
    try:
        face, name = registration_queue.get_nowait()
        hide_progress()
        if face is None:
            messagebox.showerror("Error", "No face detected.")
            show_status("No face detected.", 'red')
            return
        img = Image.fromarray(face)
        img = img.resize((150, 150))
        photo = ImageTk.PhotoImage(img)
        face_display_label.configure(image=photo)
        face_display_label.image = photo
        show_status(f"Face registered for {name}.", 'green')
        refresh_all_lists()
        messagebox.showinfo("Success", f"Face registered for {name}.")
    except queue.Empty:
        root.after(100, check_registration_result)

def start_tracking():
    def track():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Unable to access the camera.")
            return
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            try:
                detections = RetinaFace.detect_faces(frame)
                if isinstance(detections, dict):
                    for face_key in detections:
                        facial_area = detections[face_key]['facial_area']
                        x1, y1, x2, y2 = facial_area
                        x1, y1 = max(0, x1), max(0, y1)
                        x2, y2 = min(frame.shape[1], x2), min(frame.shape[0], y2)
                        face_crop = frame[y1:y2, x1:x2]
                        if face_crop.size == 0:
                            continue
                        encoding = np.mean(face_crop, axis=(0, 1))
                        for name, data in known_faces.items():
                            known_enc = data['encoding']
                            distance = np.linalg.norm(encoding - known_enc)
                            if distance < 30:
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.putText(frame, name, (x1, y1 - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                                log_movement(name)
                                break
            except Exception as e:
                print(f"[WARN] Detection error: {e}")
            cv2.imshow("Face Tracking", frame)
            if cv2.waitKey(1) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    threading.Thread(target=track, daemon=True).start()
    show_status("Tracking started. Press ESC in camera window to stop.", 'blue')

# --- Modern GUI Setup ---
root = tk.Tk()
root.title("Employee Face Registration & Tracking")
root.geometry("600x500")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Segoe UI', 11), padding=6)
style.configure('TLabel', font=('Segoe UI', 11))
style.configure('TEntry', font=('Segoe UI', 11))

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# --- Register Tab ---
register_frame = ttk.Frame(notebook)
notebook.add(register_frame, text='Register Face')

# Name entry
ttk.Label(register_frame, text="Employee Name:").grid(row=0, column=0, sticky='e', pady=8, padx=5)
name_entry = ttk.Entry(register_frame, width=25)
name_entry.grid(row=0, column=1, sticky='w', pady=8, padx=5)

# Upload button
upload_btn = ttk.Button(register_frame, text="Upload Image", command=upload_image)
upload_btn.grid(row=1, column=0, columnspan=2, pady=5)

# Image preview
preview_label = ttk.Label(register_frame)
preview_label.grid(row=2, column=0, columnspan=2, pady=5)

# Register button
register_btn = ttk.Button(register_frame, text="Register Face", command=threaded_register_face)
register_btn.grid(row=3, column=0, columnspan=2, pady=5)

# Registered face display
face_display_label = ttk.Label(register_frame)
face_display_label.grid(row=4, column=0, columnspan=2, pady=5)

# Progress bar for registration
progress_bar = ttk.Progressbar(register_frame, mode='indeterminate')
progress_bar.grid(row=5, column=0, columnspan=2, pady=5, sticky='ew')
progress_bar.grid_remove()

# --- Employee List Tab ---
employee_frame = ttk.Frame(notebook)
notebook.add(employee_frame, text='Employee List')

# Search bar
search_var = tk.StringVar()
def update_employee_list(search_text=None):
    for row in employee_listbox.get_children():
        employee_listbox.delete(row)
    users = data.get_all_users()
    for i, user in enumerate(users):
        if search_text and search_text.lower() not in user['name'].lower():
            continue
        img = Image.fromarray(user['image'])
        img = img.resize((40, 40))
        photo = ImageTk.PhotoImage(img)
        employee_thumbnails[user['name']] = photo
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        employee_listbox.insert('', 'end', iid=user['name'], text='', values=(user['name'],), image=photo, tags=(tag,))
    employee_listbox.tag_configure('evenrow', background='#f0f0ff')
    employee_listbox.tag_configure('oddrow', background='#ffffff')

search_entry = ttk.Entry(employee_frame, textvariable=search_var, width=30)
search_entry.grid(row=0, column=0, padx=5, pady=8, sticky='w')
search_label = ttk.Label(employee_frame, text="Search Employee:")
search_label.grid(row=0, column=1, padx=5, pady=8, sticky='w')

def on_search(*args):
    update_employee_list(search_var.get())
search_var.trace_add('write', on_search)

# Employee listbox (modern)
employee_listbox = ttk.Treeview(employee_frame, columns=("Name",), show='headings', height=12)
employee_listbox.heading("Name", text="Employee Name")
employee_listbox.column("Name", width=200, anchor='center')
employee_listbox.grid(row=1, column=0, columnspan=3, sticky='nsew', pady=5)
employee_thumbnails = {}
employee_frame.grid_rowconfigure(1, weight=1)
employee_frame.grid_columnconfigure(0, weight=1)

# Details popup
def show_employee_details(event=None):
    selected = employee_listbox.selection()
    if not selected:
        return
    name = selected[0]
    user = data.get_user(name)
    if not user:
        messagebox.showerror("Error", "Employee not found.")
        return
    top = tk.Toplevel(root)
    top.title(f"Details for {name}")
    img = Image.fromarray(user['image'])
    img = img.resize((120, 120))
    photo = ImageTk.PhotoImage(img)
    img_label = ttk.Label(top, image=photo)
    img_label.image = photo
    img_label.pack(pady=10)
    ttk.Label(top, text=f"Name: {name}", font=("Segoe UI", 12)).pack(pady=5)
    ttk.Button(top, text="Close", command=top.destroy).pack(pady=10)

employee_listbox.bind('<Double-1>', show_employee_details)

# Add Employee button
add_btn = ttk.Button(employee_frame, text="Add Employee", command=lambda: notebook.select(register_frame))
add_btn.grid(row=2, column=0, pady=10, sticky='w')

# Delete Employee logic
def delete_employee():
    selected = employee_listbox.selection()
    if not selected:
        messagebox.showerror("Error", "No employee selected.")
        return
    name = selected[0]
    if messagebox.askyesno("Confirm", f"Delete employee '{name}'?"):
        with data.get_connection() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM users WHERE name=?', (name,))
            conn.commit()
        if name in known_faces:
            del known_faces[name]
        show_status(f"Employee '{name}' deleted.", 'red')
        refresh_all_lists()

delete_btn = ttk.Button(employee_frame, text="Delete Employee", command=delete_employee)
delete_btn.grid(row=2, column=1, pady=10, sticky='e')

# Refresh button
refresh_btn = ttk.Button(employee_frame, text="Refresh List", command=lambda: update_employee_list(search_var.get()))
refresh_btn.grid(row=2, column=2, pady=10, sticky='e')

# --- Tracking Tab ---
track_frame = ttk.Frame(notebook)
notebook.add(track_frame, text='Tracking')

track_btn = ttk.Button(track_frame, text="Start Tracking", command=start_tracking)
track_btn.pack(pady=30)

# --- Tooltips (simple) ---
def add_tooltip(widget, text):
    def on_enter(e):
        show_status(text, 'gray')
    def on_leave(e):
        show_status("Ready.")
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

add_tooltip(upload_btn, "Upload an employee's face image.")
add_tooltip(register_btn, "Register the uploaded face with the entered name.")
add_tooltip(track_btn, "Start real-time face tracking using the camera.")
add_tooltip(add_btn, "Go to registration tab to add a new employee.")
add_tooltip(delete_btn, "Delete the selected employee.")
add_tooltip(refresh_btn, "Refresh the employee list.")
add_tooltip(employee_listbox, "Double-click to view employee details.")

# --- Update all lists on startup and after changes ---
def refresh_all_lists():
    update_employee_list(search_var.get())
    # Optionally update face_list for tracking if needed

refresh_all_lists()

# --- Status Bar ---
status_var = tk.StringVar()
status_bar = ttk.Label(root, textvariable=status_var, anchor='w', relief='sunken', font=('Segoe UI', 10))
status_bar.pack(side='bottom', fill='x')
show_status("Ready.")

# --- Company Name ---
company_name = "ANSNEW TECH."
company_label = ttk.Label(root, text=company_name, font=("Segoe UI", 16, "bold"), anchor='center')
company_label.pack(side='top', pady=(10, 0))

root.mainloop()
