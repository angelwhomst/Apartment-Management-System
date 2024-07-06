import customtkinter
from customtkinter import CTk, set_appearance_mode
from welcome import WelcomeFrame
from login import LoginFrame
from dashboard import DashboardFrame
from units_info import UnitsInfoFrame
from tenant_information import TenantInformationFrame
from payment_management import PaymentManagementFrame
from report import ReportFrame
from building_information import BuildingInformationFrame
from profile import ProfileFrame
from expenses import ExpenseFrame


class ApartmentManagementApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        set_appearance_mode("light")
        self.title("Apartment Management System")

        self.container = customtkinter.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.create_frames()
        self.show_frame(WelcomeFrame)

    def create_frames(self):
        for F in (LoginFrame, WelcomeFrame, DashboardFrame, UnitsInfoFrame, TenantInformationFrame, PaymentManagementFrame,
                  ReportFrame, BuildingInformationFrame, ProfileFrame, ExpenseFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = ApartmentManagementApp()
    app.mainloop()
