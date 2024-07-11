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
        self.populate_treeview()

    def create_widgets(self):
        # Add background image
        admin_bg_image = Image.open("images/BgPaymentManagement.png")
        admin_bg = ctk.CTkImage(admin_bg_image, size=(900, 600))
        admin_bg_lbl = ctk.CTkLabel(self, text="", image=admin_bg)
        admin_bg_lbl.place(x=0, y=0)

        # Create Frame to hold Treeview and Scrollbar
        self.frame = tk.Frame(self)
        self.frame.place(relx=0.015, rely=0.20, relwidth=0.99, relheight=0.8)  # Adjust placement and size

        # Create Treeview
        columns = ("Tenant Name", "Building Name", "Unit Number", "Rental Rate", "Payment Date", "Mode of Payment",
                   "Amount Received")
        self.tree = ttk.Treeview(self.frame, columns=(*columns, "hidden_id"), show='headings')

        # Hide the ID column
        self.tree.column("hidden_id", width=0, stretch=False)
        self.tree.heading("hidden_id", text="")

        # Define headings with adjusted styles
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, anchor='w', width=120)

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

    def populate_treeview(self):
        conn = draft_backend.get_db_connection()
        if conn:
            transactions = draft_backend.fetch_transaction_history(conn)
            conn.close()
            for row in transactions:
                # Insert the row with the hidden ID column
                self.tree.insert("", "end",
                                 values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[0]))
        else:
            print("Error: Failed to connect to the database.")

    def start_refresh(self):
        # Periodically refresh data
        self.refresh_data()
        self.after(5000, self.start_refresh)  # Refresh every 5 seconds

    def refresh_data(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            # Fetch the transaction history
            transaction_history = draft_backend.fetch_transaction_history(conn)

            # Clear existing items from the Treeview
            self.tree.delete(*self.tree.get_children())

            # Iterate over fetched units and update or insert into Treeview
            for transaction in transaction_history:
                tenant_name = self.replace_none(transaction[1])
                building_name = self.replace_none(transaction[2])
                unit_number = self.replace_none(transaction[3])
                rental_rate = self.replace_none(transaction[4])
                payment_date = self.replace_none(transaction[5])
                payment_method = self.replace_none(transaction[6])
                amount = self.replace_none(transaction[7])
                payment_id = self.replace_none(transaction[0])
        except Exception as e:
            print(f"Error fetching data: {str(e)}")

        finally:
            conn.close()

        # Resume refreshing after processing
        self.after(5000, self.start_refresh)  # Refresh every 5 seconds

    def replace_none(self, value):
        return value if value is not None else ""


