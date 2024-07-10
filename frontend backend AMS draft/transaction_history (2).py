import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from PIL import Image
import customtkinter as ctk
import draft_backend


class TransactionHistory(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.parent.geometry("900x600")
        self.parent.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Add background image
        admin_bg_image = Image.open("images/bgTransactionHistory.png")
        admin_bg = ctk.CTkImage(admin_bg_image, size=(900, 600))
        admin_bg_lbl = ctk.CTkLabel(self, text="", image=admin_bg)
        admin_bg_lbl.place(x=0, y=0)

        # Create Frame to hold Treeview and Scrollbar
        self.frame = tk.Frame(self)
        self.frame.place(relx=0.015, rely=0.20, relwidth=0.99, relheight=0.8)  # Adjust placement and size

        # Create Treeview
        columns = ("Tenant Name", "Unit Number", "Building Number", "Rental Rate", "Bill","Payment Date", "Mode of Payment","Amount Received")
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')

        # Define headings with adjusted styles
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, anchor='w', width=120)  # Adjust column widths as needed

        # Style Treeview
        style = ttk.Style()
        style.theme_use("clam")  # Use a specific theme that can be customized
        style.configure("Treeview", background="#e6e1dd", fieldbackground="#e6e1dd", foreground="#3D291F", rowheight=25,
                        font=('Century Gothic', 12), padding=0)  # Adjust padding and border properties
        style.map('Treeview', background=[('selected', '#d6cec8')])
        style.configure("Treeview.Heading", background="#d6cec8", foreground="#3D291F",
                        font=('Century Gothic', 11, 'bold'))

        # Create Scrollbar
        vsb = Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure Treeview to use Scrollbar
        self.tree.configure(yscrollcommand=vsb.set)

        # Place Treeview inside the Frame
        self.tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)


# FOR TESTING Entry point for running the RecentTenantComponent directly
if __name__ == "__main__":
    root = ctk.CTk()
    admin_tool = TransactionHistory(root)
    admin_tool.pack(fill="both", expand=True)
    root.mainloop()