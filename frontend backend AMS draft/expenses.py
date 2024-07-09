import PIL
import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from base import BaseFrame
from login import LoginFrame
from profile import ProfileFrame
from PIL import Image
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
import draft_backend


class ExpenseFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.populate_treeview()

    def create_widgets(self):
        # Add background image
        dashboard_bg_image = PIL.Image.open("images/expensedashbg.png")
        dashboard_bg = ctk.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = ctk.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0)

        # Add dashboard container image
        container_image = PIL.Image.open("images/BgExpense.png")
        container_img = ctk.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = ctk.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        # Payment Management Label
        Expense_Label = ctk.CTkLabel(master=self, text="Expenses", fg_color="White",
                                     text_color="#3D291F", font=("Century Gothic", 45, "bold"))
        Expense_Label.place(relx=0.23, rely=0.18)

        # Ensure the sidebar is setup after the background images
        self.setup_sidebar()

        # Add Treeview with Scrollbar
        self.add_treeview()

        # Profile Button
        profile_btn = ctk.CTkButton(master=self, text="Profile", corner_radius=0, fg_color="#CFB9A3",
                                    hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                    font=('Century Gothic', 20, "bold"), width=90, height=30,
                                    command=lambda: self.controller.show_frame(ProfileFrame))
        profile_btn.place(relx=0.855, rely=0.105)

        # Logout Button
        logout_btn = ctk.CTkButton(master=self, text="Log out", corner_radius=0, fg_color="#CFB9A3",
                                   hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                   font=('Century Gothic', 20, "bold"), width=90, height=30,
                                   command=lambda: self.controller.show_frame(LoginFrame))
        logout_btn.place(relx=0.920, rely=0.105)

        # Add To: DateEntry
        to_date_entry = DateEntry(self, font=('Century Gothic', 16), width=12)
        to_date_entry.place(relx=0.710, rely=0.300)

        # Add From: DateEntry
        from_date_entry = DateEntry(self, font=('Century Gothic', 16), width=12)
        from_date_entry.place(relx=0.610, rely=0.300)

        # # Add Search Entry with Placeholder Text
        # def on_entry_click(event):
        #     if search_entry.get() == "Search Name...":
        #         search_entry.delete(0, tk.END)
        #         search_entry.config(fg="black")
        #
        # def on_focus_out(event):
        #     if search_entry.get() == "":
        #         search_entry.insert(0, "Search Name...")
        #         search_entry.config(fg="#5c483f")

        # search_entry = tk.Entry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=30)
        # search_entry.insert(0, "Search Name...")
        # search_entry.bind('<FocusIn>', on_entry_click)
        # search_entry.bind('<FocusOut>', on_focus_out)
        # search_entry.place(relx=0.400, rely=0.300)

        # Add Search Button
        search_button = ctk.CTkButton(master=self, text="Search", corner_radius=5, fg_color="#BDA588",
                                      hover_color="#D6BC9D", text_color="black", bg_color="White",
                                      font=('Century Gothic', 16), width=100, height=30,
                                      command=self.perform_search)
        search_button.place(relx=0.820, rely=0.295)

        # Add Clear Filter Button
        clear_filter_button = ctk.CTkButton(master=self, text="Clear Filter", corner_radius=5, fg_color="#B8C8D3",
                                            hover_color="#9EA3AC", text_color="black", bg_color="White",
                                            font=('Century Gothic', 16), width=100, height=30,
                                            command=self.clear_filters)
        clear_filter_button.place(relx=0.895, rely=0.295)

        # Add Treeview with Scrollbar
        self.add_treeview()

    def add_treeview(self):
        # Create Treeview
        columns = ("Expense Date", "Expense Amount", "Expense Type", "Description")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # Define headings with adjusted styles
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, anchor='w', width=100)  # Align data to the left

        # Style Treeview
        style = ttk.Style(self)
        style.theme_use("clam")  # Use a specific theme that can be customized
        style.configure("Treeview", background="#e6e1dd", foreground="#3D291F", rowheight=25,
                        font=('Century Gothic', 12))
        style.map('Treeview', background=[('selected', '#d6cec8')])
        style.configure("Treeview.Heading", background="#d6cec8", foreground="#3D291F",
                        font=('Century Gothic', 14, 'bold'))

        # Create Scrollbar
        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.place(x=1830, y=348, height=590)

        # Configure Treeview to use Scrollbar
        self.tree.configure(yscrollcommand=vsb.set)

        # Place Treeview inside the container
        self.tree.place(x=1130, y=348, width=700, height=590)

    def populate_treeview(self):
        conn = draft_backend.get_db_connection()
        if conn:
            expenses = draft_backend.fetch_expense_treeview(conn)
            conn.close()

            # insert data into the treeview
            for row in expenses:
                self.tree.insert("", 'end', values=row)

    def perform_search(self):
        # Placeholder for search functionality
        pass

    def clear_filters(self):
        # Placeholder for clear filters functionality
        pass
