import PIL
import customtkinter
from base import BaseFrame
from login import LoginFrame
import customtkinter as ctk
from profile import ProfileFrame
from PIL import Image


class BuildingInformationFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()

    def create_widgets(self):
        # Add background image
        dashboard_bg_image = PIL.Image.open("images/buildinginfobg.jpg")
        dashboard_bg = customtkinter.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = customtkinter.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0,)

        # Add dashboard container image
        container_image = PIL.Image.open("images/dashcontainer.png")
        container_img = customtkinter.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = customtkinter.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        # Building Information Label
        BuildingInfoLabel = ctk.CTkLabel(master=self, text="Building Information", fg_color="White",
                                      text_color="#3D291F", font=("Century Gothic", 45, "bold"))
        BuildingInfoLabel.place(relx=0.23, rely=0.18)

        # Ensure the sidebar is setup after the background images
        self.setup_sidebar()

        # Admin Toool Button

        # Profile Button
        self.add_profile_button()

        # Logout Button
        self.add_logout_button()


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
