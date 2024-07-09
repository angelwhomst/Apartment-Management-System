import PIL
import customtkinter
import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from base import BaseFrame
from login import LoginFrame
from profile import ProfileFrame
from PIL import Image
import draft_backend


class PaymentManagementFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()

    def create_widgets(self):
        # Add background image
        dashboard_bg_image = PIL.Image.open("images/paymentmanagementbg.png")
        dashboard_bg = customtkinter.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = customtkinter.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0, )

        # Add dashboard container image
        container_image = PIL.Image.open("images/BgPaymentManagement.png")
        container_img = customtkinter.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = customtkinter.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        # Payment Management Label
        PaymentManagementLabel = ctk.CTkLabel(master=self, text="Payment Management", fg_color="White",
                                              text_color="#3D291F", font=("Century Gothic", 45, "bold"))
        PaymentManagementLabel.place(relx=0.23, rely=0.18)

        # Ensure the sidebar is setup after the background images
        self.setup_sidebar()

        # Profile Button
        self.add_profile_button()

        # Logout Button
        self.add_logout_button()

        # Add Treeview with Scrollbar
        self.add_treeview()

    def add_treeview(self):
        # Create Treeview
        columns = ("Building Number", "Unit Number", "Tenant Name", "Due Date")
        tree = ttk.Treeview(self, columns=columns, show='headings')

        # Define headings with adjusted styles
        for col in columns:
            tree.heading(col, text=col, anchor='w')
            tree.column(col, anchor='w', width=100)  # Align data to the left

        # Style Treeview
        style = ttk.Style(self)
        style.theme_use("clam")  # Use a specific theme that can be customized
        style.configure("Treeview", background="#e6e1dd", foreground="#3D291F", rowheight=25,
                        font=('Century Gothic', 12))
        style.map('Treeview', background=[('selected', '#d6cec8')])
        style.configure("Treeview.Heading", background="#d6cec8", foreground="#3D291F",
                        font=('Century Gothic', 14, 'bold'))

        # Create Scrollbar
        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        vsb.place(x=1830, y=348, height=590)

        # Configure Treeview to use Scrollbar
        tree.configure(yscrollcommand=vsb.set)

        # Place Treeview inside the container
        tree.place(x=1130, y=348, width=700, height=590)

        # Example data (adjust as needed)
        data = [
            ("June/22/2004", "101", "Utilities", "SalamAaaaa-- --"),
            ("August/10/2004", "202", "Advertising", "tHankyouUU so MuuUU"),
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
