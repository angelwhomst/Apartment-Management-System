import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from PIL import Image
import customtkinter as ctk
import draft_backend


class MonthlyEarningsComponent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x600")
        self.parent.resizable(False, False)
        self.create_widgets()
        self.update_monthly_earnings()

    def create_widgets(self):

        # Add background image
        admin_bg_image = Image.open("images/bgMonthlyEarnings.png")
        admin_bg = ctk.CTkImage(admin_bg_image, size=(900, 600))
        admin_bg_lbl = ctk.CTkLabel(self, text="", image=admin_bg)
        admin_bg_lbl.place(x=0, y=0)

        # Define StringVars for labels
        self.label_earnings_var = tk.StringVar()
        self.label_collection_var = tk.StringVar()
        self.label_expense_var = tk.StringVar()

        # Create labels
        self.label_earnings = ctk.CTkLabel(self, textvariable=self.label_earnings_var, font=('Century Gothic', 25),
                                           text_color="#3D291F", fg_color="#DCD7D4")
        self.label_earnings.place(relx=0.065, rely=0.55)

        self.label_collection = ctk.CTkLabel(self, textvariable=self.label_collection_var, font=('Century Gothic', 25),
                                             text_color="#3D291F", fg_color="#DCD7D4")
        self.label_collection.place(relx=0.370, rely=0.55)

        self.label_expense = ctk.CTkLabel(self, textvariable=self.label_expense_var, font=('Century Gothic', 25),
                                          text_color="#3D291F", fg_color="#DCD7D4")
        self.label_expense.place(relx=0.670, rely=0.55)

    def update_monthly_earnings(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            # Fetch monthly earnings
            monthly_earnings = draft_backend.monthly_earnings(conn)
            self.label_earnings_var.set(f"₱{monthly_earnings:.2f}")

            # Fetch month's rent collection
            monthly_rate = draft_backend.rent_collection(conn)
            self.label_collection_var.set(f"₱{monthly_rate :.2f}")

            # Fetch monthly expense
            monthly_expense = draft_backend.monthly_expense(conn)
            self.label_expense_var.set(f"₱{monthly_expense :.2f}")

        except Exception as e:
            print(f"Error fetching rental rates: {e}")
        finally:
            conn.close()

    def open_total_units(self):
        self.create_widgets()

# FOR TESTING ONLY
if __name__ == "__main__":
    root = ctk.CTk()
    admin_tool = MonthlyEarningsComponent(root)
    admin_tool.pack(fill="both", expand=True)
    root.mainloop()
