import tkinter as tk
import customtkinter as ctk
from PIL import Image
import draft_backend


class TotalUnitsComponent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x600")
        self.parent.resizable(False, False)
        self.create_widgets()
        self.update_available_units()
        self.update_under_maintenance_units()
        self.update_occupied_units()

    def create_widgets(self):

        # Add background image
        admin_bg_image = Image.open("images/bgTotalunits.png")
        admin_bg = ctk.CTkImage(admin_bg_image, size=(900, 600))
        admin_bg_lbl = ctk.CTkLabel(self, text="", image=admin_bg)
        admin_bg_lbl.place(x=0, y=0)

        # Define StringVars for labels
        self.label_occupied_var = tk.StringVar()
        self.label_available_var = tk.StringVar()
        self.label_under_maintenance_var = tk.StringVar()


        # Create labels
        self.label_occupied = ctk.CTkLabel(self, textvariable=self.label_occupied_var, font=('Century Gothic', 50), text_color="#3D291F",fg_color="#DCD7D4")
        self.label_occupied.place(relx=0.060, rely=0.5)

        self.label_available = ctk.CTkLabel(self, textvariable=self.label_available_var, font=('Century Gothic', 50), text_color="#3D291F", fg_color="#DCD7D4")
        self.label_available.place(relx=0.365, rely=0.5)

        self.label_under_maintenance = ctk.CTkLabel(self, textvariable=self.label_under_maintenance_var, font=('Century Gothic', 50), text_color="#3D291F", fg_color="#DCD7D4")
        self.label_under_maintenance.place(relx=0.670, rely=0.5)

    def update_available_units(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        count = draft_backend.count_available_units(conn)
        self.label_available_var.set(f"{count}")
        conn.close()

    def update_occupied_units(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        count = draft_backend.count_occupied_units(conn)
        self.label_occupied_var.set(f"{count}")
        conn.close()

    def update_under_maintenance_units(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        count = draft_backend.count_under_maintenance_units(conn)
        self.label_under_maintenance_var.set(f"{count}")
        conn.close()

    def open_total_units(self):
        self.create_widgets()


# FOR TESTING
if __name__ == "__main__":
    root = ctk.CTk()
    admin_tool = TotalUnitsComponent(root)
    admin_tool.pack(fill="both", expand=True)
    root.mainloop()
