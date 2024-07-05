import PIL
import customtkinter as ctk
from base import BaseFrame
from login import LoginFrame
from profile import ProfileFrame
from admin_tool import AdminToolComponent

class DashboardFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()

    def create_widgets(self):
        # Add background image
        dashboard_bg_image = PIL.Image.open("images/dashboardbg.jpg")
        dashboard_bg = ctk.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = ctk.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0)

        # Add dashboard container image
        container_image = PIL.Image.open("images/dashcontainer.png")
        container_img = ctk.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = ctk.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        # Dashboard Label
        DashboardLabel = ctk.CTkLabel(master=self, text="Dashboard", fg_color="White",
                                      text_color="#3D291F", font=("Century Gothic", 45, "bold"))
        DashboardLabel.place(relx=0.23, rely=0.18)

        # Sidebar setup
        self.setup_sidebar()

        # Admin Tool Button
        self.add_admin_tool_button()

        # Profile Button
        self.add_profile_button()

        # Logout Button
        self.add_logout_button()

    def add_admin_tool_button(self):
        admin_icon_image = PIL.Image.open("images/toolIcon.png")
        admin_icon = ctk.CTkImage(admin_icon_image, size=(20, 20))

        admin_tool_btn = ctk.CTkButton(master=self, text="Admin Tool", corner_radius=0, fg_color="#CFB9A3",
                                       hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                       font=('Century Gothic', 20, "bold"), width=190, height=30,
                                       image=admin_icon, compound="left",
                                       command=self.open_admin_tool)
        admin_tool_btn.place(relx=0.855, rely=0.055)

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

    def open_admin_tool(self):
        admin_tool = AdminToolComponent(self)
        admin_tool.open_admin_tool()
