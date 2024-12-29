import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json



# File to save event data
EVENT_FILE = "events.json"

# Load events from file
def load_events():
    try:
        with open(EVENT_FILE, "r") as file:
            content= file.read().strip()
            if not content:
                return []
            return json.loads(content)
         
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save events to file
def save_events():
    with open(EVENT_FILE, "w") as file:
        json.dump(events, file)

# Add new event
def add_event():
    name = event_name.get()
    date = event_date.get()
    time = event_time.get()
    desc = event_desc.get("1.0", tk.END).strip()

    if not name or not date or not time:
        messagebox.showerror("Error", "All fields are required!")
        return

    # Check for date-time conflicts
    for event in events:
        if event['date'] == date and event['time'] == time:
            messagebox.showwarning("Error", "Event already scheduled at this time!")
            return

    # Add event
    events.append({"name": name, "date": date, "time": time, "desc": desc})
    save_events()
    display_events()
    clear_fields()
    messagebox.showinfo("Success", "Event Added Successfully!")

# Display events
def display_events():
    event_list.delete(0, tk.END)
    sorted_events = sorted(events, key=lambda x: (x['date'], x['time']))
    for event in sorted_events:
        event_list.insert(tk.END, f"{event['date']} {event['time']} - {event['name']}")

# Clear input fields
def clear_fields():
    event_name.delete(0, tk.END)
    event_date.delete(0, tk.END)
    event_time.delete(0, tk.END)
    event_desc.delete("1.0", tk.END)

# Delete selected event
def delete_event():
    try:
        index = event_list.curselection()[0]
        events.pop(index)
        save_events()
        display_events()
        messagebox.showinfo("Success", "Event Deleted Successfully!")
    except IndexError:
        messagebox.showerror("Error", "No event selected!")

# GUI Setup
app = tk.Tk()
app.title("Event Planning and Scheduling")
app.geometry("600x500")
app.config(bg='#f2f2f2')


# Input Fields
tk.Label(app, text="Event Name:", font="Helvatica 18 bold",relief="sunken").grid(row=0, column=0, padx=10, pady=10)
event_name = tk.Entry(app, width=30)
event_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(app, text="Date (DD-MM-YYYY) :",font="Helvatica 18 bold",relief="sunken").grid(row=1, column=0, padx=10, pady=10)
event_date = tk.Entry(app, width=30)
event_date.grid(row=1, column=1, padx=10, pady=10)

tk.Label(app, text="Time (HH:MM):",font="Helvatica 18 bold",relief="sunken").grid(row=2, column=0, padx=10, pady=10)
event_time = tk.Entry(app, width=30)
event_time.grid(row=2, column=1, padx=10, pady=10)

tk.Label(app, text="Description:",font="Helvatica 18 bold",relief="sunken").grid(row=3, column=0, padx=10, pady=10)
event_desc = tk.Text(app, width=30, height=5)
event_desc.grid(row=3, column=1, padx=10, pady=10)

# Buttons
tk.Button(app, text="Add Event", command=add_event,font="Helvatica 18 bold",activebackground="green",relief="sunken").grid(row=4, column=0, padx=10, pady=10)
tk.Button(app, text="Delete Event", command=delete_event,font="Helvatica 18 bold",activebackground="red",relief="sunken").grid(row=4, column=1, padx=10, pady=10)

# Event List
event_list = tk.Listbox(app, width=70, height=15,font="Helvatica 18 bold")
event_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Load saved events
events = load_events()
display_events()

app.mainloop()
