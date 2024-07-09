import PIL
import customtkinter
import customtkinter as ctk
import tkinter as tk
import tkinter.ttk as ttk
from CTkMessagebox import CTkMessagebox
from customtkinter import CTkComboBox
from tkcalendar import DateEntry
from base import BaseFrame
from login import LoginFrame
from profile import ProfileFrame
from PIL import Image
import draft_backend

# mapping from combobox values to database int values for payment_method
payment_method_mapping = {
    'Cash': 1,
    'E-wallet': 2,
    'Bank Transfer': 3,
    'Credit Card': 4
}


class PaymentManagementFrame(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_widgets()
        self.populate_treeview()
        self.start_refresh()

    def create_widgets(self):
        # Add background image
        dashboard_bg_image = PIL.Image.open("images/paymentmanagementbg.png")
        dashboard_bg = customtkinter.CTkImage(dashboard_bg_image, size=(1550, 800))
        dashboard_bg_lbl = customtkinter.CTkLabel(self, text="", image=dashboard_bg)
        dashboard_bg_lbl.place(x=0, y=0, )

        # Add dashboard container image
        container_image = PIL.Image.open("images/BgPaymentManagement.png")
        container_img = customtkinter.CTkImage(container_image, size=(1170, 650))
        container_img_lbl = customtkinter.CTkLabel(self, text="", image=container_img, fg_color="white")
        container_img_lbl.place(x=333, y=120)

        # Payment Management Label
        PaymentManagementLabel = ctk.CTkLabel(master=self, text="Payment Management", fg_color="White",
                                              text_color="#3D291F", font=("Century Gothic", 45, "bold"))
        PaymentManagementLabel.place(relx=0.23, rely=0.18)
        # Combo box and entries
        self.entry_first_name = ctk.CTkEntry(self, width=200, height=30,
                                             font=('Century Gothic', 15), border_color="#937A69")

        self.entry_first_name.place(relx=0.325, rely=0.465, anchor="center")

        self.entry_middle_name = ctk.CTkEntry(self, width=200, height=30,
                                              font=('Century Gothic', 15), border_color="#937A69")

        self.entry_middle_name.place(relx=0.325, rely=0.545, anchor="center")

        self.entry_last_name = ctk.CTkEntry(self, width=200, height=30,
                                            font=('Century Gothic', 15), border_color="#937A69")

        self.entry_last_name.place(relx=0.325, rely=0.625, anchor="center")

        self.entry_bill = ctk.CTkEntry(self, width=200, height=30,
                                       font=('Century Gothic', 15), border_color="#937A69")

        self.entry_bill.place(relx=0.490, rely=0.545, anchor="center")

        # Fetch building names from the database
        conn = draft_backend.get_db_connection()
        if not conn:
            return
        building_names = draft_backend.fetch_building_names(conn)
        conn.close()

        self.combo_box_building_name = CTkComboBox(self, values=building_names, width=240, height=25,
                                                   font=('Century Gothic', 12))
        self.combo_box_building_name.place(relx=0.490, rely=0.625, anchor="center")

        self.combo_box_unit_number = ctk.CTkComboBox(self, values=[], width=200, height=30,
                                                     font=('Century Gothic', 15), border_color="#937A69")

        self.combo_box_unit_number.place(relx=0.490, rely=0.465, anchor="center")

        # Bind the command to update unit numbers based on building selection
        self.combo_box_building_name.configure(command=self.update_unit_numbers)

        self.payment_date = DateEntry(self, width=21, height=30,
                                      font=('Century Gothic', 15), border_color="#937A69")

        self.payment_date.place(relx=0.490, rely=0.775, anchor="center")

        payment_methods = ['Cash', 'E-wallet', 'Bank Transfer', 'Credit Card']
        self.combo_box_MOP = ctk.CTkComboBox(self, values=payment_methods, width=200, height=30,
                                             font=('Century Gothic', 15), border_color="#937A69")

        self.combo_box_MOP.place(relx=0.325, rely=0.780, anchor="center")

        self.entry_amount = ctk.CTkEntry(self, width=200, height=30,
                                         font=('Century Gothic', 15), border_color="#937A69")

        self.entry_amount.place(relx=0.325, rely=0.860, anchor="center")

        # Transaction history

        transaction_button = ctk.CTkButton(master=self, text="Transaction History", corner_radius=5, fg_color="#BDA588",
                                           hover_color="#D6BC9D", text_color="black", bg_color="White",
                                           font=('Century Gothic', 16,), width=205, height=30)
        transaction_button.place(relx=0.825, rely=0.250)
        # Add Search Button
        search_button = ctk.CTkButton(master=self, text="Search", corner_radius=5, fg_color="#BDA588",
                                      hover_color="#D6BC9D", text_color="black", bg_color="White",
                                      font=('Century Gothic', 16,), width=100, height=25)
        search_button.place(relx=0.625, rely=0.300)

        # Add Clear Filter Button
        clear_filter_button = ctk.CTkButton(master=self, text="Clear Filter", corner_radius=5, fg_color="#B8C8D3",
                                            hover_color="#9EA3AC", text_color="black", bg_color="White",
                                            font=('Century Gothic', 16,), width=100, height=30)
        clear_filter_button.place(relx=0.895, rely=0.295)

        # Add Delete Button

        delete_button = ctk.CTkButton(master=self, text="Delete", corner_radius=5, fg_color="#B8C8D3",
                                      hover_color="#9EA3AC", text_color="black", bg_color="White",
                                      font=('Century Gothic', 16,), width=100, height=30)
        delete_button.place(relx=0.825, rely=0.295)

        save_button = ctk.CTkButton(master=self, text="Save", corner_radius=5, fg_color="#BDA588",
                                    hover_color="#D6BC9D", text_color="black", bg_color="#D8CCC4",
                                    font=('Century Gothic', 16,), width=100, height=30, command=self.save_payment)
        save_button.place(relx=0.458, rely=0.860, anchor="center")

        # Add To: DateEntry
        self.to_date_entry = DateEntry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=12)
        self.to_date_entry.place(relx=0.430, rely=0.300)

        # Add From: DateEntry
        self.from_date_entry = DateEntry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=12)
        self.from_date_entry.place(relx=0.520, rely=0.300)

        # Add Search Entry with Placeholder Text
        def on_entry_click(event):
            if self.search_entry.get() == "Search Name...":
                self.search_entry.delete(0, tk.END)
                self.search_entry.config(fg="black")

        def on_focus_out(event):
            if self.search_entry.get() == "":
                self.search_entry.insert(0, "Search Name...")
                self.search_entry.config(fg="#5c483f")

        self.search_entry = tk.Entry(self, font=('Century Gothic', 16), bg="white", fg="#5c483f", width=30)
        self.search_entry.insert(0, "Search Name...")
        self.search_entry.bind('<FocusIn>', on_entry_click)
        self.search_entry.bind('<FocusOut>', on_focus_out)
        self.search_entry.place(relx=0.235, rely=0.300)

        # Ensure the sidebar is setup after the background images
        self.setup_sidebar()

        # Profile Button
        self.add_profile_button()

        # Logout Button
        self.add_logout_button()

        # Add Treeview with Scrollbar
        self.add_treeview()

    def update_unit_numbers(self, selected_building):
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        unit_numbers = draft_backend.fetch_unit_numbers_by_building(conn, selected_building)
        conn.close()

        print(f"Fetched unit numbers: {unit_numbers}")  # Debug statement

        # Clear existing values and update with fetched unit numbers
        self.combo_box_unit_number.configure(values=unit_numbers)

    def add_treeview(self):
        # Create Treeview
        columns = ("Building Name", "Unit Number", "Tenant Name", "Due Date", "Bill")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # Define headings with adjusted styles
        for col in columns:
            self.tree.heading(col, text=col, anchor='w')
            self.tree.column(col, anchor='w', width=100)  # Align data to the left

        # Style Treeview
        style = ttk.Style(self)
        style.theme_use("clam")  # Use a specific theme that can be customized
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

    def populate_treeview(self):
        conn = draft_backend.get_db_connection()
        if conn:
            payment = draft_backend.fetch_payment_treeview(conn)
            conn.close()

            # insert data into the treeview
            for row in payment:
                self.tree.insert("", 'end', values=row)

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
            payments = draft_backend.fetch_payment_treeview(conn)

            # Clear existing items from the Treeview
            self.tree.delete(*self.tree.get_children())

            # Iterate over fetched expenses and update or insert into Treeview
            for payment in payments:
                # Extract relevant values
                building_name = payment[0]
                unit_number = payment[1]
                tenant_name = payment[2]
                due_date = payment[3]
                bill = payment[4]

                # Insert or update Treeview item
                self.tree.insert("", "end", values=(building_name, unit_number, tenant_name, due_date,
                                                    bill))

        except Exception as e:
            print(f"Error fetching data: {str(e)}")

        finally:
            conn.close()

    def save_payment(self):

        amount = self.entry_amount.get()
        date = self.payment_date.get_date()
        mode_of_payment = self.combo_box_MOP.get()
        first_name = self.entry_first_name.get()
        middle_name = self.entry_middle_name.get()
        last_name = self.entry_last_name.get()
        unit_number = self.combo_box_unit_number.get()
        building_name = self.combo_box_building_name.get()

        # map the selected mode of payment to its integer value
        payment_method_int = payment_method_mapping.get(mode_of_payment)

        # validate user inputs
        if not amount and not date and not building_name and not unit_number:
            CTkMessagebox(title="Error", message="All fields are required.")
            return

        if not amount.isdigit():
            CTkMessagebox(title="Error", message="Please input only digits on payment amount.")
            return

        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        tenant_id = draft_backend.fetch_tenant_id_by_name_and_unit_details(conn, first_name, last_name, unit_number,
                                                                           building_name)
        if tenant_id is None:
            CTkMessagebox(title="Error",
                          message=f"Tenant '{first_name} {last_name}' in unit '{unit_number}' of '{building_name}' "
                                  f"not found.")
            return

        # Fetch unit_id based on unit number and building name
        unit_id = draft_backend.fetch_unit_id_by_number_and_building(conn, unit_number, building_name)
        if unit_id is None:
            CTkMessagebox(title="Error", message=f"Unit '{unit_number}' in '{building_name}' not found.")
            return

        # Proceed to save data to the database
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        try:
            success = draft_backend.insert_payment(conn, float(amount), date, payment_method_int, tenant_id, unit_id)
            if success:
                CTkMessagebox(title="Success", message="Payment saved successfully.")
                # Clear input fields after successful save
                self.entry_amount.delete(0, tk.END)
                self.payment_date.set_date("")
                self.combo_box_MOP.set("")
                self.entry_first_name.delete(0, tk.END)
                self.entry_middle_name.delete(0, tk.END)
                self.entry_last_name.delete(0, tk.END)
                self.combo_box_unit_number.set("")
                self.combo_box_building_name.set("")

                # Refresh the Treeview to display updated data
                self.populate_treeview()
            else:
                CTkMessagebox(title="Error", message="Failed to save payment.")
        except Exception as e:
            print(f"Error saving payment: {str(e)}")
        finally:
            conn.close()

    def add_profile_button(self):
        profile_btn = ctk.CTkButton(master=self, text="Profile", corner_radius=0, fg_color="#CFB9A3",
                                    hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                    font=('Century Gothic', 20, "bold"), width=90, height=30,
                                    command=lambda: self.controller.show_frame(ProfileFrame))
        profile_btn.place(relx=0.855, rely=0.105)

    def add_logout_button(self):
        logout_btn = ctk.CTkButton(master=self, text="Log out", corner_radius=0, fg_color="#CFB9A3",
                                   hover_color="#D6BC9D", text_color="#5c483f", bg_color="#5D646E",
                                   font=('Century Gothic', 20, "bold"), width=90, height=30,
                                   command=lambda: self.controller.show_frame(LoginFrame))
        logout_btn.place(relx=0.920, rely=0.105)
