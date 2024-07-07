import tkinter as tk
from tkinter import ttk
from tkinter import Scrollbar
from PIL import Image
import customtkinter as ctk

class RecentTenantComponent:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Create TopLevel window
        self.top_level = tk.Toplevel(self.parent)
        self.top_level.title("Recent Tenants")
        self.top_level.geometry("900x600")  # Set initial size of the window
        self.top_level.resizable(False, False)  # Disable resizing

        # Add background image
        admin_bg_image = Image.open("images/bgRecentTenants.png")
        admin_bg = ctk.CTkImage(admin_bg_image, size=(900, 600))
        admin_bg_lbl = ctk.CTkLabel(self.top_level, text="", image=admin_bg)
        admin_bg_lbl.place(x=0, y=0)

        # Create Frame to hold Treeview and Scrollbar
        self.frame = tk.Frame(self.top_level)
        self.frame.place(relx=0.015, rely=0.20  , relwidth=0.99, relheight=0.8)  # Adjust placement and size

        # Create Treeview
        columns = ("Building Name", "Unit Number", "Name", "Contact Number", "Move in Date")
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

        # Example data (adjust as needed)
        data = [
            ("Building A", "101", "John Doe", "1234567890","2023-01-01"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building A", "101", "John Doe", "1234567890", "2023-01-01"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building A", "101", "John Doe", "1234567890", "2023-01-01"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building A", "101", "John Doe", "1234567890", "2023-01-01"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building A", "101", "John Doe", "1234567890", "2023-01-01"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building A", "101", "John Doe", "1234567890", "2023-01-01"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),
            ("Building B", "202", "Jane Smith", "0987654321", "2023-02-15"),

            # Add more data if needed
        ]

        # Insert example data into Treeview
        for item in data:
            self.tree.insert('', 'end', values=item)

# Entry point for running the LeaseExpirationAlertComponent directly
if __name__ == "__main__":
    root = tk.Tk()
    admin_tool = RecentTenantComponent(root)
    root.mainloop()
