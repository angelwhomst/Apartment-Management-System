import PIL
import customtkinter
from customtkinter import *
from CTkMessagebox import CTkMessagebox
import draft_backend


class testFrame(CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.total_unit_var = None
        self.under_maintenance_var = None
        self.rented_units_var = None
        self.available_units_var = None
        self.controller = controller
        self.create_widgets()
        self.update_all_counts()

    def create_widgets(self):
        welcome_label = CTkLabel(self, text="Welcome to the test page!", font=("Century Gothic", 40))
        welcome_label.grid(columnspan=3, row=0, pady=30, padx=30)

        # frames for units
        available_frame = CTkFrame(self)
        available_frame.grid(column=0, row=1, pady=20, padx=20, sticky=NSEW)
        rented_frame = CTkFrame(self)
        rented_frame.grid(column=1, row=1, pady=20, padx=20, sticky=NSEW)
        under_maintenance_frame = CTkFrame(self)
        under_maintenance_frame.grid(column=2, row=1, pady=20, padx=20, sticky=NSEW)
        total_units_frame = CTkFrame(self)
        total_units_frame.grid(column=3, row=1, pady=20, padx=20, sticky=NSEW)

        # Variable to hold the number of available/rented/under maintenance units
        self.available_units_var = StringVar()
        self.available_units_var.set("Available Units: 0")
        self.rented_units_var = StringVar()
        self.rented_units_var.set('Rented Units: 0')
        self.under_maintenance_var = StringVar()
        self.under_maintenance_var.set('Under Maintenance Units: 0')
        self.total_unit_var = StringVar()
        self.total_unit_var.set('Total Units: 0')

        # Label to display the number of available/rented/under maintenance units
        available_units_label = CTkLabel(master=available_frame, textvariable=self.available_units_var,
                                         font=("Century Gothic", 20), cursor="hand2")
        available_units_label.pack(pady=10)
        available_units_label.bind("<Button-1>", lambda event: self.dashboard())

        rented_units_label = CTkLabel(rented_frame, textvariable=self.rented_units_var,
                                      font=("Century Gothic", 20))
        rented_units_label.pack(pady=10)

        under_maintenance_label = CTkLabel(under_maintenance_frame, textvariable=self.under_maintenance_var,
                                           font=("Century Gothic", 20))
        under_maintenance_label.pack(pady=10)

        total_units_label = CTkLabel(total_units_frame, textvariable=self.total_unit_var,
                                     font=("Century Gothic", 20))
        total_units_label.pack(pady=10)

        # ============ for displaying field per label

        tenant_info_frame = CTkFrame(self)
        tenant_info_frame.grid(column=1, row=2, pady=20, padx=20, sticky=NSEW)

        # ============ for displaying field per label

        tenant_info_frame = CTkFrame(self)
        tenant_info_frame.grid(column=1, row=2, pady=20, padx=20, sticky=NSEW)

        # Get data from the record
        tenants = draft_backend.fetch_tenants_complete(draft_backend.get_db_connection())
        if tenants:
            tenant = tenants[0]  # Get the first tenant

            # Create labels for each field
            self.last_name_label = CTkLabel(tenant_info_frame, text=f"Last Name: {tenant[2]}")
            self.last_name_label.pack(pady=5)
            self.first_name_label = CTkLabel(tenant_info_frame, text=f"First Name: {tenant[3]}")
            self.first_name_label.pack(pady=5)
            self.middle_name_label = CTkLabel(tenant_info_frame, text=f"Middle Name: {tenant[5]}")
            self.middle_name_label.pack(pady=5)
            self.contactNumber = CTkLabel(tenant_info_frame, text=f'Contact Number: {tenant[6]}')
            self.contactNumber.pack(pady=5)
            self.move_in_date = CTkLabel(tenant_info_frame, text=f'Move In Date: {tenant[7]}')
            self.move_in_date.pack(pady=5)
            self.lease_start_date = CTkLabel(tenant_info_frame, text=f'Lease Start Date: {tenant[8]}')
            self.lease_start_date.pack(pady=5)
            self.tenant_dob_label = CTkLabel(tenant_info_frame, text=f"Date of Birth: {tenant[14]}")
            self.tenant_dob_label.pack(pady=5)


        # ================= UNIT
        self.unit_info_frame = CTkFrame(self)
        self.unit_info_frame.grid(column=0, row=2, columnspan=4, pady=20, padx=20, sticky=NSEW)
        self.display_unit_numbers()

    def display_unit_numbers(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("SELECT unit_id, unit_number FROM Apartment_Unit")
        units = cursor.fetchall()
        conn.close()

        for unit in units:
            unit_id, unit_number = unit
            unit_label = CTkLabel(self.unit_info_frame, text=f"Unit {unit_number}", font=("Century Gothic", 20), cursor='hand2')
            unit_label.pack(pady=5)
            unit_label.bind("<Button-1>", lambda e, uid=unit_id: self.show_unit_info(uid))

    def show_unit_info(self, unit_id):
        conn = draft_backend.get_db_connection()
        if not conn:
            return
        unit_info = draft_backend.fetch_one_unit(conn, unit_id)
        conn.close()

        if unit_info:
            # Clear existing labels
            for widget in self.unit_info_frame.winfo_children():
                widget.destroy()

            # Create and display labels for each field in unit_info
            fields = [
                ("Unit Number", unit_info[0]),
                ("Number of Bedrooms", unit_info[1]),
                ("Number of Bathrooms", unit_info[2]),
                ("Unit Size (sq m)", unit_info[3]),
                ("Rental Rate", unit_info[4]),
                ("Availability Status", unit_info[5])
            ]

            for field_name, value in fields:
                label = CTkLabel(self.unit_info_frame, text=f"{field_name}: {value}", font=("Century Gothic", 20))
                label.pack(pady=5)
        else:
            CTkMessagebox(title="Error", message= "Could not retrieve unit information")



    def update_available_units(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        count = draft_backend.count_available_units(conn)
        self.available_units_var.set(f"Available Units: {count}")
        conn.close()

    def update_rented_units(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        count = draft_backend.count_rented_units(conn)
        self.rented_units_var.set(f"Rented Units: {count}")
        conn.close()

    def update_under_maintenance(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        count = draft_backend.count_under_maintenance_units(conn)
        self.under_maintenance_var.set(f"Under Maintenance Units: {count}")
        conn.close()

    def update_total_units(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        count = draft_backend.count_total_units(conn)
        self.total_unit_var.set(f"Total Units: {count}")
        conn.close()

    def update_all_counts(self):
        # Updates the counts of all units.
        self.update_available_units()
        self.update_rented_units()
        self.update_under_maintenance()
        self.update_total_units()

    def dashboard(self):
        from dashboard import DashboardFrame
        self.controller.show_frame(DashboardFrame)
