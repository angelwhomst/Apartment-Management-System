import tkinter as tk
import tkinter.ttk as ttk
import PIL.Image
from tkinter import Scrollbar, Toplevel
import customtkinter as ctk
from tkcalendar import Calendar
from base import BaseFrame
from login import LoginFrame
from profile import ProfileFrame

class TenantInformationFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()

    def create_widgets(self):
        # Add background image
        dashboard_bg_image = PIL.Image.open("images/tenantInformationbg.jpg")
        dashboard_bg = ctk.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = ctk.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0)

        # Add dashboard container image
        container_image = PIL.Image.open("images/dashcontainer.png")
        container_img = ctk.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = ctk.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        # Tenant information Label
        TenantInfoLabel = ctk.CTkLabel(master=self, text="Tenants Information", fg_color="White",
                                       text_color="#3D291F", font=("Century Gothic", 45, "bold"))
        TenantInfoLabel.place(relx=0.23, rely=0.18)

        # Ensure the sidebar is setup after the background images
        self.setup_sidebar()

        # Add Treeview with Scrollbar
        self.add_treeview()

        # Profile Button
        self.add_profile_button()

        # Logout Button
        self.add_logout_button()

        # Add To: Calendar Entry with Calendar Button
        self.add_to_calendar_entry()

        # Add From: Calendar Entry with Calendar Button
        self.add_from_calendar_entry()

        # Add Search Entry with Placeholder Text
        self.add_search_entry()

        # Add Search Button
        self.add_search_button()

        # Add Clear Filter Button
        self.add_clear_filter_button()

    def add_treeview(self):
        # Create Treeview
        columns = ("Building Name", "Unit Number", "Name", "Contact Number", "Status", "Start Date")
        tree = ttk.Treeview(self, columns=columns, show='headings')

        # Define headings with adjusted styles
        for col in columns:
            tree.heading(col, text=col, anchor='w')
            tree.column(col, anchor='w', width=190)  # Align data to the left

        # Style Treeview
        style = ttk.Style(self)
        style.theme_use("clam")  # Use a specific theme that can be customized
        style.configure("Treeview", background="#e6e1dd", foreground="#3D291F", rowheight=25,
                        font=('Century Gothic', 12))
        style.map('Treeview', background=[('selected', '#d6cec8')])
        style.configure("Treeview.Heading", background="#d6cec8", foreground="#3D291F",
                        font=('Century Gothic', 14, 'bold'))

        # Create Scrollbar
        vsb = Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        vsb.place(x=1835, y=370, height=537)

        # Configure Treeview to use Scrollbar
        tree.configure(yscrollcommand=vsb.set)

        # Place Treeview inside the container
        tree.place(x=440, y=370, width=1415, height=538)

        # Example data (adjust as needed)
        data = [
            ("Building A", "101", "John Doe", "1234567890", "Paid", "2023-01-01"),
            ("Building B", "202", "Jane Smith", "0987654321", "Not Paid", "2023-02-15"),
            # Add more data if needed
        ]

        # Insert example data multiple times for more rows
        for _ in range(5):
            data.extend(data)

        # Insert example data into Treeview
        for item in data:
            tree.insert('', 'end', values=item)

    def add_profile_button(self):
        profile_btn = ctk.CTkButton(master=self, text="Profile", corner_radius=0, fg_color="#CFB9A3",
                                    hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                    font=('Century Gothic', 20, "bold"), width=90, height=30,
                                    command=lambda: self.controller.show_frame(ProfileFrame))
        profile_btn.place(relx=0.855, rely=0.105)

    def add_logout_button(self):
        logout_btn = ctk.CTkButton(master=self, text="Log out", corner_radius=0, fg_color="#CFB9A3",
                                   hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                   font=('Century Gothic', 20, "bold"), width=90, height=30,
                                   command=lambda: self.controller.show_frame(LoginFrame))
        logout_btn.place(relx=0.920, rely=0.105)

    def add_to_calendar_entry(self):
        # Create Entry for manual input
        self.to_calendar_entry = tk.Entry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=10)
        self.to_calendar_entry.insert(0, "To:")
        self.to_calendar_entry.bind('<FocusIn>', self.on_to_entry_click)
        self.to_calendar_entry.bind('<FocusOut>', self.on_to_focus_out)
        self.to_calendar_entry.place(relx=0.710, rely=0.300)

        # Create Calendar Button
        calendar_icon_image = PIL.Image.open("images/CalendarIcon.png")
        calendar_icon = ctk.CTkImage(calendar_icon_image, size=(20, 20))

        calendar_btn = ctk.CTkButton(master=self, text="", corner_radius=0, fg_color="white",
                                     hover_color="white", text_color="#5c483f", bg_color="white", compound="right",
                                     font=('Century Gothic', 20, "bold"), width=30, height=30, image=calendar_icon,
                                     command=self.open_to_calendar)
        calendar_btn.place(relx=0.775, rely=0.295)

    def on_to_entry_click(self, event):
        if self.to_calendar_entry.get() == "To:":
            self.to_calendar_entry.delete(0, tk.END)
            self.to_calendar_entry.config(fg="#5c483f")  # Set text color to normal

    def on_to_focus_out(self, event):
        if self.to_calendar_entry.get() == "":
            self.to_calendar_entry.insert(0, "To:")
            self.to_calendar_entry.config(fg="#5c483f")  # Set text color to placeholder color

    def add_from_calendar_entry(self):
        # Create Entry for manual input
        self.from_calendar_entry = tk.Entry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=10)
        self.from_calendar_entry.insert(0, "From:")
        self.from_calendar_entry.bind('<FocusIn>', self.on_from_entry_click)
        self.from_calendar_entry.bind('<FocusOut>', self.on_from_focus_out)
        self.from_calendar_entry.place(relx=0.610, rely=0.300)

        # Create Calendar Button
        calendar_icon_image = PIL.Image.open("images/CalendarIcon.png")
        calendar_icon = ctk.CTkImage(calendar_icon_image, size=(20, 20))

        calendar_btn = ctk.CTkButton(master=self, text="", corner_radius=0, fg_color="white",
                                     hover_color="white", text_color="#5c483f", bg_color="white", compound="right",
                                     font=('Century Gothic', 20, "bold"), width=30, height=30, image=calendar_icon,
                                     command=self.open_from_calendar)
        calendar_btn.place(relx=0.675, rely=0.295)

    def on_from_entry_click(self, event):
        if self.from_calendar_entry.get() == "From:":
            self.from_calendar_entry.delete(0, tk.END)
            self.from_calendar_entry.config(fg="#5c483f")  # Set text color to normal

    def on_from_focus_out(self, event):
        if self.from_calendar_entry.get() == "":
            self.from_calendar_entry.insert(0, "From:")
            self.from_calendar_entry.config(fg="#5c483f")  # Set text color to placeholder color

    def add_search_entry(self):
        def on_entry_click(event):
            if search_entry.get() == "Search Name...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="black")

        def on_focus_out(event):
            if search_entry.get() == "":
                search_entry.insert(0, "Search Name...")
                search_entry.config(fg="#5c483f")

        search_entry = tk.Entry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=30)
        search_entry.insert(0, "Search Name...")
        search_entry.bind('<FocusIn>', on_entry_click)
        search_entry.bind('<FocusOut>', on_focus_out)
        search_entry.place(relx=0.400, rely=0.300)

    def add_search_button(self):
        search_button = ctk.CTkButton(master=self, text="Search", corner_radius=5, fg_color="#BDA588",
                                      hover_color="#D6BC9D", text_color="black", bg_color="White",
                                      font=('Century Gothic', 16,), width=100, height=30,
                                      command=self.perform_search)
        search_button.place(relx=0.820, rely=0.295)

    def add_clear_filter_button(self):
        clear_filter_button = ctk.CTkButton(master=self, text="Clear Filter", corner_radius=5, fg_color="#B8C8D3",
                                            hover_color="#9EA3AC", text_color="black", bg_color="White",
                                            font=('Century Gothic', 16,), width=100, height=30,
                                            command=self.clear_filters)
        clear_filter_button.place(relx=0.890, rely=0.295)

    def perform_search(self):
        # Placeholder for search functionality
        pass

    def clear_filters(self):
        self.to_calendar_entry.delete(0, tk.END)
        self.to_calendar_entry.insert(0, "To:")
        self.from_calendar_entry.delete(0, tk.END)
        self.from_calendar_entry.insert(0, "From:")
        # Additional clearing operations if any

    def open_to_calendar(self):
        top = Toplevel(self)
        top.geometry("400x300")
        top.attributes('-topmost', 'true')  # Ensure calendar is on top
        cal = Calendar(top, selectmode='day')
        cal.pack(fill="both", expand=True)

        def on_select():
            self.display_to_selected_date(cal, top)

        ok_button = ttk.Button(top, text="OK", command=on_select)
        ok_button.pack(pady=10)

        # Calculate position relative to to_calendar_entry
        x = self.to_calendar_entry.winfo_rootx()
        y = self.to_calendar_entry.winfo_rooty() + self.to_calendar_entry.winfo_height()
        top.geometry(f"+{x}+{y}")

    def display_to_selected_date(self, cal, top):
        selected_date = cal.get_date()
        self.to_calendar_entry.delete(0, tk.END)
        self.to_calendar_entry.insert(0, selected_date)
        top.destroy()

    def open_from_calendar(self):
        top = Toplevel(self)
        top.geometry("400x300")
        top.attributes('-topmost', 'true')  # Ensure calendar is on top
        cal = Calendar(top, selectmode='day')
        cal.pack(fill="both", expand=True)

        def on_select():
            self.display_from_selected_date(cal, top)

        ok_button = ttk.Button(top, text="OK", command=on_select)
        ok_button.pack(pady=10)

        # Calculate position relative to from_calendar_entry
        x = self.from_calendar_entry.winfo_rootx()
        y = self.from_calendar_entry.winfo_rooty() + self.from_calendar_entry.winfo_height()
        top.geometry(f"+{x}+{y}")

    def display_from_selected_date(self, cal, top):
        selected_date = cal.get_date()
        self.from_calendar_entry.delete(0, tk.END)
        self.from_calendar_entry.insert(0, selected_date)
        top.destroy()
