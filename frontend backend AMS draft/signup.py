import PIL
import customtkinter as ctk
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import draft_backend

class SignupFrame(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        image = PIL.Image.open("images/bglogin.png")
        background_image = ctk.CTkImage(image, size=(1550, 800))
        bg_lbl = CTkLabel(self, text="", image=background_image)
        bg_lbl.place(x=0, y=0)

        smaller_image = PIL.Image.open("images/beigebg.png")
        smaller_img = ctk.CTkImage(smaller_image, size=(650, 675))
        smaller_img_lbl = CTkLabel(self, text="", image=smaller_img, fg_color="white")
        smaller_img_lbl.place(x=860, y=60)

        SignupUsernlabel = CTkLabel(self, text="Username", font=("century gothic", 27.5),
                                    text_color="#3D291F", fg_color="#e6e1dd")
        SignupUsernlabel.place(relx=0.665, rely=0.395, anchor="center")

        Signuppasslabel = CTkLabel(self, text="Password", font=("century gothic", 27.5),
                                   text_color="#3D291F", fg_color="#e6e1dd")
        Signuppasslabel.place(relx=0.665, rely=0.530, anchor="center")

        ConfirmUserpasslabel = CTkLabel(self, text="Confirm Password", font=("century gothic", 27.5),
                                        text_color="#3D291F", fg_color="#e6e1dd")
        ConfirmUserpasslabel.place(relx=0.700, rely=0.660, anchor="center")

        self.entry_username_signup = CTkEntry(self, placeholder_text="Type your username", width=450, height=55,
                                              font=('Century Gothic', 20))
        self.entry_username_signup.place(relx=0.770, rely=0.450, anchor="center")

        self.entry_password_signup = CTkEntry(self, placeholder_text="Type your password", width=450, height=55,
                                              font=('Century Gothic', 20), show='*')
        self.entry_password_signup.place(relx=0.770, rely=0.585, anchor="center")

        self.ConfimUserpass = CTkEntry(self, placeholder_text="Confirm password", width=450, height=55,
                                       font=('Century Gothic', 20), show='*')
        self.ConfimUserpass.place(relx=0.770, rely=0.710, anchor="center")

        signuploginicon = PIL.Image.open("images/signUpIcon.png")
        button_register = CTkButton(self, text="Sign up", corner_radius=5, fg_color="#5c483f",
                                    hover_color="#D6BC9D", image=CTkImage(light_image=signuploginicon),
                                    font=('Century Gothic', 27.5), width=250, height=50,
                                    command=self.register)
        button_register.place(relx=0.77, rely=0.790, anchor="center")

        image = PIL.Image.open("images/logoblack.png")
        logo1 = ctk.CTkImage(image, size=(180, 180))
        blklogo = ctk.CTkLabel(self, text="", image=logo1)
        blklogo.place(x=1100, y=100)

        backicon = PIL.Image.open("images/backbtn.png")
        back = CTkButton(self, text="Go back", corner_radius=5, fg_color="#e6e1dd", text_color="#3D291F",
                         font=('Century Gothic', 20), width=19, height=20, hover_color="#e6e1dd", border_color="#e6e1dd",
                         command=self.back_to_login, image=CTkImage(light_image=backicon))
        back.place(relx=.84, rely=0.89, anchor="center")

    def register(self):
        usernameSignup = self.entry_username_signup.get()
        passwordSignup = self.entry_password_signup.get()
        confirm_password = self.ConfimUserpass.get()

        if not usernameSignup or not passwordSignup or not confirm_password:
            CTkMessagebox(title="Error", message="All fields are required.")
            return

        if passwordSignup != confirm_password:
            CTkMessagebox(title="Error", message="Passwords do not match.")
            return

        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            if draft_backend.check_username_exists(conn, usernameSignup):
                CTkMessagebox(title="Error", message="User already exists.")
            else:
                draft_backend.insert_admin(conn, usernameSignup, passwordSignup)
                CTkMessagebox(title="Success", message="User registered successfully!")
                self.entry_username_signup.delete(0, END)
                self.entry_password_signup.delete(0, END)
                self.ConfimUserpass.delete(0, END)
                self.back_to_login()
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e))
        finally:
            conn.close()

    def back_to_login(self):
        # IMports LoginFrame here to avoid circular import
        from login import LoginFrame
        self.controller.show_frame(LoginFrame)

