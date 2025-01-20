import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
import calendar
from datetime import datetime
from logic import load_events, save_events, toggle_event, remove_event, add_event, get_events


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Assignment Tracker")
        self.geometry("1200x650")
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        load_events()
        self.create_widgets()

    def create_widgets(self):
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=5, side="top", anchor="n")
        prev_button = tk.Button(nav_frame, text="<<", command=self.prev_month)
        prev_button.pack(side="left")
        self.header = tk.Label(nav_frame, text=f"{calendar.month_name[self.current_month]} {self.current_year}",
                               font=("Helvetica", 16))
        self.header.pack(side="left", padx=10)
        next_button = tk.Button(nav_frame, text=">>", command=self.next_month)
        next_button.pack(side="left")
        self.calendar_frame = tk.Frame(self)
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)
        self.display_calendar(self.calendar_frame, self.current_year, self.current_month)
        self.calendar_frame.update_idletasks()

    def display_calendar(self, calendar_frame, year, month):
        for widget in calendar_frame.winfo_children():
            widget.destroy()

        cal = calendar.monthcalendar(year, month)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        #Weekday headers
        header_canvas = tk.Frame(calendar_frame)
        header_canvas.pack()
        for day in days:
            tk.Label(header_canvas, text=day, width=22, height=2, borderwidth=1, relief="solid").pack(side="left")

        #Calendar days
        for week in cal:
            week_frame = tk.Frame(calendar_frame)
            week_frame.pack()
            for day in week:
                frame_length = 152
                if day == 0:
                    tk.Canvas(week_frame, width=frame_length, height=90, borderwidth=1, relief="solid").pack(side="left")
                else:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    day_canvas = tk.Canvas(week_frame, width=frame_length, height=90, borderwidth=1, relief="solid")
                    day_canvas.pack(side="left", pady=5, padx=0)
                    day_label = tk.Label(day_canvas, text=str(day), font=("Helvetica", 12, "bold"), borderwidth=1, relief="solid")
                    day_canvas.create_window(78, 13, window=day_label)
                    events = get_events(date_str)
                    if events:
                        event_frame = tk.Frame(day_canvas)
                        event_frame.place(x=2, y=28, width=frame_length, height=36)
                        events_canvas = tk.Canvas(event_frame, height=34, width=frame_length)
                        day_canvas.pack(side="left", fill="both", expand=True)
                        scrollbar = tk.Scrollbar(event_frame, orient="vertical", command=events_canvas.yview)
                        scrollbar.pack(side="right", fill="y")
                        events_canvas.config(yscrollcommand=scrollbar.set)
                        event_holder = tk.Frame(events_canvas)
                        events_canvas.create_window(0, 0, window=event_holder, anchor="nw")
                        for event_idx, event in enumerate(events):
                            event = tk.Label(event_holder, text=event["task"], font=("Helvetica", 10))
                            event.grid(row=event_idx, column=0, sticky="w", padx=5, pady=5)
                        event_holder.update_idletasks()
                        events_canvas.config(scrollregion=events_canvas.bbox("all"))



                    add_event_button = tk.Button(day_canvas, text="Add Assignment",
                                             command=lambda date=date_str: self.open_event_dialog(date))
                    day_canvas.create_window(78, 80, window=add_event_button)



    def open_event_dialog(self, date):
        new_event = simpledialog.askstring("Add Event", f"Enter a task for {date}:")
        if new_event:
            add_event(date, new_event)
            messagebox.showinfo("Success", f"Task added for {date}!")
            self.refresh_calendar()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.refresh_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.refresh_calendar()

    def refresh_calendar(self):
        self.header.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        self.display_calendar(self.calendar_frame, self.current_year, self.current_month)