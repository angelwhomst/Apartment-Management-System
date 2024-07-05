from customtkinter import *

class ProfileFrame(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(master=parent)
        self.controller = controller

        logout_btn = CTkButton(master=self, text="Log out", corner_radius=0, fg_color="#CFB9A3",
                               hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                               font=('Century Gothic', 20, "bold"), width=90, height=30, 
                               command=lambda: self.controller.show_frame("LoginFrame"))
        logout_btn.place(relx=0.920, rely=0.095)

        # Add other profile-related widgets here
