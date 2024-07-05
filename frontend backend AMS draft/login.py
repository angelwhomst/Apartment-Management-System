import PIL
import customtkinter
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from tkinter import *
import draft_backend

class LoginFrame(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        image = PIL.Image.open("images/bglogin.png")
        background_image = customtkinter.CTkImage(image, size=(1550, 800))
        bg_lbl = CTkLabel(self, text="", image=background_image)
        bg_lbl.place(x=0, y=0)

        smaller_image = PIL.Image.open("images/beigebg.png")
        smaller_img = customtkinter.CTkImage(smaller_image, size=(650, 675))
        smaller_img_lbl = CTkLabel(self, text="", image=smaller_img, fg_color="white")
        smaller_img_lbl.place(x=860, y=60)
#LABELS
        LoginUsernlabel = CTkLabel(self, text="Username", font=("century gothic", 27.5),
                                   text_color="#3D291F", fg_color="#e6e1dd")
        LoginUsernlabel.place(relx=0.665, rely=0.395, anchor="center")

        Loginpasslabel = CTkLabel(self, text="Password", font=("century gothic", 27.5),
                                  text_color="#3D291F", fg_color="#e6e1dd")
        Loginpasslabel.place(relx=0.665, rely=0.530, anchor="center")

#ENTRY
        self.entry_username_login = CTkEntry(self, placeholder_text="Type your username", width=450, height=55,
                                             font=('Century Gothic', 20))
        self.entry_username_login.place(relx=0.770, rely=0.450, anchor="center")

        self.entry_password_login = CTkEntry(self, placeholder_text="Type your password", width=450, height=55,
                                             font=('Century Gothic', 20), show='*')
        self.entry_password_login.place(relx=0.771, rely=0.585, anchor="center")
#BUTTONS
        loginicon = PIL.Image.open("images/loginIcon.png")
        self.button_login = CTkButton(self, text="Log in", corner_radius=5, fg_color="#5c483f",
                                      hover_color="#D6BC9D", image=CTkImage(light_image=loginicon),
                                      font=('Century Gothic', 27.5), width=250, height=50,
                                      command=self.login)
        self.button_login.place(relx=0.77, rely=0.710, anchor="center")

        viewicon = PIL.Image.open("images/viewIcon.png")
        self.button_tenant_view = CTkButton(self, text="Tenant View", corner_radius=5, fg_color="#937A69",
                                            hover_color="#D6BC9D", image=CTkImage(light_image=viewicon),
                                            font=('Century Gothic', 27.5), width=250, height=50,
                                            command=lambda: self.tenant_view)
        self.button_tenant_view.place(relx=.77, rely=0.790, anchor="center")



        image = PIL.Image.open("images/logoblack.png")
        logo = customtkinter.CTkImage(image, size=(180, 180))
        blklogo = CTkLabel(self, text="", image=logo)
        blklogo.place(x=1100, y=100)

        self.update_tenant_view_button()

    def login(self):
        usernameLogin = self.entry_username_login.get()
        passwordLogin = self.entry_password_login.get()

        if not usernameLogin or not passwordLogin:
            CTkMessagebox(title="Error", message="Username and Password are required.")
            return

        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            if draft_backend.verify_login(conn, usernameLogin, passwordLogin):
                CTkMessagebox(title="Success", message="Admin login successfully!")
                self.entry_username_login.delete(0, END)
                self.entry_password_login.delete(0, END)
                # ========    self.dashboard()
                self.dashboard()
            else:
                CTkMessagebox(title="Error", message="Invalid username or password.")
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e))
        finally:
            conn.close()

    def update_tenant_view_button(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        units_exist = draft_backend.check_apartment_units_exist(conn)
        if units_exist:
            self.button_tenant_view.configure(state=NORMAL)
        else:
            self.button_tenant_view.configure(state=DISABLED)
        conn.close()

    def tenant_view(self):
        from tenant_view import TenantViewFrame
        self.controller.show_frame(TenantViewFrame)

    def dashboard(self):
        from dashboard import DashboardFrame
        self.controller.show_frame(DashboardFrame)

    #def test_frame(self):
        #from test_frame import testFrame
       #self.controller.show_frame(testFrame)
