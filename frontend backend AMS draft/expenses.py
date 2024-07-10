import tkinter as tk
import tkinter.ttk as ttk
from tkinter import END

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from base import BaseFrame
from login import LoginFrame
from profile import ProfileFrame
from PIL import Image
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
import draft_backend

# mapping from combobox values to database int values for expense_type
expense_type_mapping = {
    'Utilities': 1,
    'Maintenance and Repairs': 2,
    'Advertising': 3,
    'Insurance': 4,
    'Administrative Costs': 5,
    'Property Management Costs': 6
}


class ExpenseFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.add_treeview()
        self.populate_treeview()
        self.start_refresh()

    def create_widgets(self):
        # Add background image
        dashboard_bg_image = Image.open("images/expensedashbg.png")
        dashboard_bg = ctk.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = ctk.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0)

        # Add dashboard container image
        container_image = Image.open("images/BgExpense.png")
        container_img = ctk.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = ctk.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        # Payment Management Label
        Expense_Label = ctk.CTkLabel(master=self, text="Expenses", fg_color="White",
                                     text_color="#3D291F", font=("Century Gothic", 45, "bold"))
        Expense_Label.place(relx=0.23, rely=0.18)

        # Ensure the sidebar is setup after the background images
        self.setup_sidebar()

        # Profile Button
        profile_btn = ctk.CTkButton(master=self, text="Profile", corner_radius=0, fg_color="#CFB9A3",
                                    hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                    font=('Century Gothic', 20, "bold"), width=90, height=30,
                                    command=lambda: self.controller.show_frame(ProfileFrame))
        profile_btn.place(relx=0.855, rely=0.105)

        # Logout Button
        logout_btn = ctk.CTkButton(master=self, text="Log out", corner_radius=0, fg_color="#CFB9A3",
                                   hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                   font=('Century Gothic', 20, "bold"), width=90, height=30,
                                   command=lambda: self.controller.show_frame(LoginFrame))
        logout_btn.place(relx=0.920, rely=0.105)

        # Add Search Button
        search_button = ctk.CTkButton(master=self, text="Search", corner_radius=5, fg_color="#BDA588",
                                      hover_color="#D6BC9D", text_color="black", bg_color="White",
                                      font=('Century Gothic', 16,), width=100, height=25)
        search_button.place(relx=0.515, rely=0.300)
        # Add Clear Filter Button
        clear_filter_button = ctk.CTkButton(master=self, text="Clear Filter", corner_radius=5, fg_color="#B8C8D3",
                                            hover_color="#9EA3AC", text_color="black", bg_color="White",
                                            font=('Century Gothic', 16,), width=100, height=30,
                                            command=self.clear_filters)
        clear_filter_button.place(relx=0.895, rely=0.295)

        # Add Delete Button
        delete_button = ctk.CTkButton(master=self, text="Delete", corner_radius=5, fg_color="#B8C8D3",
                                      hover_color="#9EA3AC", text_color="black", bg_color="White",
                                      font=('Century Gothic', 16,), width=100, height=30,
                                      command=self.delete_selected)
        delete_button.place(relx=0.825, rely=0.295)

        save_button = ctk.CTkButton(master=self, text="Save", corner_radius=5, fg_color="#BDA588",
                                    hover_color="#D6BC9D", text_color="black", bg_color="#D8CCC4",
                                    font=('Century Gothic', 16,), width=100, height=30, command=self.save_expense)
        save_button.place(relx=0.540, rely=0.900, anchor="center")

        self.entry_expense = ctk.CTkEntry(self, width=215, height=30,
                                          font=('Century Gothic', 15), border_color="#937A69")

        self.entry_expense.place(relx=0.327, rely=0.685, anchor="center")

        # Expense Type ComboBox
        expense_types = ['Utilities', 'Maintenance and Repairs', 'Advertising', 'Insurance', 'Administrative Costs',
                         'Property Management Costs']
        self.combo_box_expense_type = ctk.CTkComboBox(self, values=expense_types, width=215, height=30,
                                                      font=('Century Gothic', 15), border_color="#937A69")

        self.combo_box_expense_type.place(relx=0.327, rely=0.765, anchor="center")

        self.entry_description = ctk.CTkEntry(self, width=215, height=30,
                                              font=('Century Gothic', 15), border_color="#937A69")

        self.entry_description.place(relx=0.327, rely=0.845, anchor="center")

        # Add To: DateEntry
        self.to_date_entry = DateEntry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=12)
        self.to_date_entry.place(relx=0.320, rely=0.300)

        # Add From: DateEntry
        self.from_date_entry = DateEntry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=12)
        self.from_date_entry.place(relx=0.415, rely=0.300)

        # Expense DateEntry
        self.expense_date_entry = DateEntry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=21,
                                            height=30)
        self.expense_date_entry.place(relx=0.257, rely=0.585)

    def add_treeview(self):
        # Create Treeview
        columns = ("Date", "Amount", "Type", "Description")
        self.tree = ttk.Treeview(self, columns=(*columns, "hidden_id"), show='headings')

        # Hide the ID column
        self.tree.column("hidden_id", width=0, stretch=False)
        self.tree.heading("hidden_id", text="")

        # Define headings with adjusted styles
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, anchor='w', width=150)  # Adjusted width

        # Style Treeview
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background="#e6e1dd", foreground="#3D291F", rowheight=25,
                        font=('Century Gothic', 12))
        style.map('Treeview', background=[('selected', '#d6cec8')])
        style.configure("Treeview.Heading", background="#d6cec8", foreground="#3D291F",
                        font=('Century Gothic', 14, 'bold'))

        # Create Scrollbar
        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        vsb.place(x=1830, y=348, height=590)

        # Configure Treeview to use Scrollbar
        self.tree.configure(yscrollcommand=vsb.set)

        # Place Treeview inside the container
        self.tree.place(x=1130, y=348, width=700, height=590)

        # Bind double click to select
        self.tree.bind("<Double-1>", self.on_treeview_select)

    def save_expense(self):
        # Collect data from the entry fields
        expense_date = self.expense_date_entry.get_date()
        expense_amount = self.entry_expense.get()
        expense_type = self.combo_box_expense_type.get()
        description = self.entry_description.get()

        # map the selected expense type to its integer value
        expense_type_int = expense_type_mapping.get(expense_type)

        # validate user inputs
        if not expense_amount.isdigit():
            CTkMessagebox(title="Error", message="Please input only digits on expense amount.")
            return

        if not expense_amount or not expense_date:
            CTkMessagebox(title="Error", message="Expense date and amount required.")
            return

        # proceed to save data to the database
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return
        try:
            draft_backend.insert_expense(conn, expense_date, expense_amount, expense_type_int, description)
            CTkMessagebox(title="Success", message="Expense information saved successfully!")

            self.clear_entry_fields()

        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def clear_entry_fields(self):
        self.entry_expense.delete(0, END)
        self.expense_date_entry.delete(0, END)
        self.entry_description.delete(0, END)

    def populate_treeview(self):
        conn = draft_backend.get_db_connection()
        if conn:
            expenses = draft_backend.fetch_expense_treeview(conn)
            conn.close()

            # Insert data into the treeview
            for row in expenses:
                self.tree.insert("", 'end', values=(row[1], row[2], row[3], row[4], row[0]))

    def start_refresh(self):
        # Periodically refresh data
        self.refresh_data()
        self.after(5000, self.start_refresh)  # Refresh every 5 seconds

    def refresh_data(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            # Fetch all expenses
            expenses = draft_backend.fetch_expense_treeview(conn)

            # Clear existing items from the Treeview
            self.tree.delete(*self.tree.get_children())

            # Iterate over fetched expenses and update or insert into Treeview
            for expense in expenses:
                # Extract relevant values
                expense_date = expense[1]
                expense_amount = expense[2]
                expense_type = expense[3]
                description = expense[4]
                expense_id = expense[0]

                # Insert or update Treeview item
                self.tree.insert("", "end", values=(expense_date, expense_amount, expense_type,
                                                    description, expense_id))

        except Exception as e:
            print(f"Error fetching data: {str(e)}")

        finally:
            conn.close()

    def on_treeview_select(self, event):
        selected_item = self.tree.selection()[0]  # Get selected item ID
        print(f"Selected item: {selected_item}")

    def delete_selected(self):
        selected_item = self.tree.selection()  # Get selected item(s)
        if selected_item:
            response = CTkMessagebox(title="Delete Confirmation",
                                     message="Are you sure you want to delete the selected expense?",
                                     icon="warning",
                                     option_1="Yes",
                                     option_2="No").get()

            if response == "Yes":
                for item in selected_item:
                    # Get the expense_id from the hidden column
                    expense_id = self.tree.item(item, 'values')[4]

                    # Delete from Treeview
                    self.tree.delete(item)

                    # Delete from Database
                    conn = draft_backend.get_db_connection()
                    if conn:
                        try:
                            draft_backend.delete_expense(conn, expense_id)
                        except Exception as e:
                            CTkMessagebox(title="Error", message=f"Error deleting: {str(e)}")
                        finally:
                            conn.close()
        else:
            CTkMessagebox(title="Error", message="No item selected.")

    def perform_search(self):
        # Placeholder for search functionality
        pass

    def clear_filters(self):
        # Placeholder for clear filters functionality
        pass
