import customtkinter as ctk
from customtkinter import *

class TenantViewFrame(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.configure(fg_color="white")

        title_label = CTkLabel(self, text="Tenant View", font=('Century Gothic', 27.5))
        title_label.pack(pady=20)

        back_button_tenant_view = CTkButton(self, text="Back", command=self.back_to_login)
        back_button_tenant_view.pack(pady=10)

    def back_to_login(self):
        # IMports LoginFrame here to avoid circular import
        from login import LoginFrame
        self.controller.show_frame(LoginFrame)
