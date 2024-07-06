from customtkinter import CTkButton, CTkFrame, CTkLabel, CTkImage
import PIL

class BaseFrame(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_sidebar()

    def setup_sidebar(self):
        from dashboard import DashboardFrame
        from units_info import UnitsInfoFrame
        from tenant_information import TenantInformationFrame
        from payment_management import PaymentManagementFrame
        from report import ReportFrame
        from building_information import BuildingInformationFrame
        from expenses import ExpenseFrame

        buttons_info = [
            ("   Owner Dashboard       ", 0.4, DashboardFrame),
            ("  Units Information          ", 0.52, UnitsInfoFrame),
            ("  Tenants Information    ", 0.58, TenantInformationFrame),
            ("     Payment Management", 0.64, PaymentManagementFrame),
            (" Expenses                     ", 0.70, ExpenseFrame),
            ("Building Information  ", 0.46, BuildingInformationFrame),
            ("   Report                           ", 0.76, ReportFrame),
        ]

        # Add sidebar background image
        smaller_image = PIL.Image.open("images/sideBar.png")
        smaller_img = CTkImage(smaller_image, size=(300, 800))
        smaller_img_lbl = CTkLabel(self, text="", image=smaller_img, fg_color="white")
        smaller_img_lbl.place(x=0, y=0)

        # Logo
        logo_3 = PIL.Image.open("images/whiteLogo.jpg")
        logos = CTkImage(logo_3, size=(180, 180))
        whitelogos = CTkLabel(self, text="", image=logos)
        whitelogos.place(x=50, y=55)

        # Menu Label
        MenuLabel = CTkLabel(master=self, text="MENU", fg_color="#5D4940",
                             text_color="#D9D9D8", font=("Garet", 32.7, "bold"))
        MenuLabel.place(relx=0.060, rely=0.3)

        for text, rel_y, frame_class in buttons_info:
            button = CTkButton(
                master=self,
                text=text,
                corner_radius=0,
                fg_color="#5c483f",
                hover_color="#D6BC9D",
                font=('Century Gothic', 20),
                width=300,
                height=50,
                command=lambda f=frame_class: self.show_frame(f)
            )
            button.place(relx=0, rely=rel_y)

    def show_frame(self, frame_class):
        frame = self.controller.frames[frame_class]
        frame.tkraise()
