import tkinter as tk
import customtkinter as ctk
from PIL import Image

class MonthlyRatesComponent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x600")
        self.parent.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):

        # Add background image
        admin_bg_image = Image.open("images/bgMonthlyRates.png")
        admin_bg = ctk.CTkImage(admin_bg_image, size=(900, 600))
        admin_bg_lbl = ctk.CTkLabel(self, text="", image=admin_bg)
        admin_bg_lbl.place(x=0, y=0)

        # Define StringVars for labels
        self.label_average_var = tk.StringVar()
        self.label_average_var.set("₱5,000")

        self.label_minimum_var = tk.StringVar()
        self.label_minimum_var.set("₱50,000")

        self.label_maximum_var = tk.StringVar()
        self.label_maximum_var.set("₱500,000")

        # Create labels
        self.label_average_var = ctk.CTkLabel(self, textvariable=self.label_average_var, font=('Century Gothic', 25), text_color="#3D291F",fg_color="#DCD7D4")
        self.label_average_var.place(relx=0.065, rely=0.55)

        self.label_minimun_var = ctk.CTkLabel(self, textvariable=self.label_minimum_var, font=('Century Gothic', 25), text_color="#3D291F", fg_color="#DCD7D4")
        self.label_minimun_var.place(relx=0.370, rely=0.55)

        self.label_maximum_var = ctk.CTkLabel(self, textvariable=self.label_maximum_var, font=('Century Gothic', 25), text_color="#3D291F", fg_color="#DCD7D4")
        self.label_maximum_var.place(relx=0.670, rely=0.55)

    def open_total_units(self):
        self.create_widgets()

if __name__ == "__main__":
    root = ctk.CTk()
    admin_tool = MonthlyRatesComponent(root)
    admin_tool.pack(fill="both", expand=True)
    root.mainloop()
