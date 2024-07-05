import PIL
import customtkinter
from customtkinter import *
from login import LoginFrame
class WelcomeFrame(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        image = PIL.Image.open("images/welcomePage.png")
        background_image = customtkinter.CTkImage(image, size=(1550, 800))
        bg_lbl = CTkLabel(self, text="", image=background_image)
        bg_lbl.place(x=0, y=0)

        welcome = CTkButton(master=self, text="Get Started", corner_radius=30, fg_color="#5c483f",
                            hover_color="#D6BC9D", bg_color=("#a1988b"),
                            font=('Century Gothic', 27.5), width=250, height=50,
                            command=lambda: self.controller.show_frame(LoginFrame))
        welcome.place(relx=0.50, rely=0.879, anchor="center")
