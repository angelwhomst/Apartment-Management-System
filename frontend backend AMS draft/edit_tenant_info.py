from tkinter import *
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkEntry, CTkComboBox
import draft_backend

sex_mapping = {
    'Male': 1,
    'Female': 2,
    'Prefer not to say': 3
}


class EditTenantInformation:
    def __init__(self, parent, tenant_id=None):
        self.parent = parent
        self.tenant_id = tenant_id
        self.display_tenant_id = None
        self.add_building_window = None  # Initialize top-level window attribute for Add Building
        self.add_unit_window = None  # Initialize top-level window attribute for Add Unit
        self.create_widgets(parent)
        self.populate_tenant_info()

    def create_widgets(self, parent):
        # Add background image
        building_bg_image = Image.open("images/addTenantBg.png")
        building_bg = ctk.CTkImage(building_bg_image, size=(900, 600))
        building_bg_lbl = ctk.CTkLabel(parent, text="", image=building_bg)
        building_bg_lbl.place(x=0, y=0)

        # StringVars for entry fields
        self.tenant_firt_name_var = StringVar()
        self.tenant_middle_name_var = StringVar()
        self.tenant_last_name_var = StringVar()
        self.suffix_var = StringVar()
        self.contactnum_var = StringVar()
        self.email_var = StringVar()
        self.unit_number_var = StringVar()
        self.sex_var = StringVar()
        self.birthdate_var = StringVar()
        self.move_in_var = StringVar()
        self.lease_start_var = StringVar()
        self.lease_end_var = StringVar()
        self.last_payment_var = StringVar()
        self.emergency_contact_number_var = StringVar()
        self.emergency_contact_name_var = StringVar()
        self.relationship_var = StringVar()
        self.income_var = StringVar()

        # Entry fields/Combo box
        self.entry_first_name = CTkEntry(parent, textvariable=self.tenant_firt_name_var, width=80, height=25,
                                         border_color="#937A69", bg_color="White",
                                         font=('Century Gothic', 12))
        self.entry_first_name.place(relx=0.090, rely=0.368, anchor="center")

        self.entry_middle_name = CTkEntry(parent, textvariable=self.tenant_middle_name_var, width=80, height=25,
                                          border_color="#937A69",bg_color="White",
                                          font=('Century Gothic', 12))
        self.entry_middle_name.place(relx=0.194, rely=0.368, anchor="center")

        self.entry_last_name = CTkEntry(parent, textvariable=self.tenant_last_name_var, width=80, height=25,
                                        border_color="#937A69",bg_color="White",
                                        font=('Century Gothic', 12))
        self.entry_last_name.place(relx=0.296, rely=0.368, anchor="center")

        self.entry_suffix_name = CTkEntry(parent, textvariable=self.suffix_var, width=80, height=25,bg_color="White",border_color="#937A69",
                                          font=('Century Gothic', 12))
        self.entry_suffix_name.place(relx=0.400, rely=0.368, anchor="center")

        self.entry_contactnum = CTkEntry(parent, textvariable=self.contactnum_var, width=240, height=25,
                                         border_color="#937A69",bg_color="White",
                                         font=('Century Gothic', 12))
        self.entry_contactnum.place(relx=0.310, rely=0.425, anchor="center")

        self.entry_email = CTkEntry(parent, textvariable=self.email_var, width=240, height=25,
                                    border_color="#937A69",bg_color="White",
                                    font=('Century Gothic', 12))
        self.entry_email.place(relx=0.310, rely=0.482, anchor="center")

        # Fetch building names from the database
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return
        building_names = draft_backend.fetch_building_names(conn)
        conn.close()

        self.entry_building_name = CTkComboBox(parent, values=building_names, width=160, height=25,
                                               font=('Century Gothic', 12), border_color="#937A69",bg_color="White",)
        self.entry_building_name.place(relx=0.840, rely=0.482, anchor="center")

        # Fetch unit numbers from the database when building is selected
        self.entry_unit_number = CTkComboBox(parent, values=[], width=240, height=25, border_color="#937A69",bg_color="White",
                                             font=('Century Gothic', 12))
        self.entry_unit_number.place(relx=0.310, rely=0.539, anchor="center")

        # Bind the command to update unit numbers based on building selection
        self.entry_building_name.configure(command=self.update_unit_numbers)

        self.combo_box_sex = CTkComboBox(parent, values=['Male', 'Female', 'Prefer not to say'], width=240, height=25,bg_color="White",
                                         border_color="#937A69",
                                         font=('Century Gothic', 12))
        self.combo_box_sex.place(relx=0.310, rely=0.596, anchor="center")

        self.entry_birthdate = DateEntry(parent, textvariable=self.birthdate_var, width=30, background='#937A69', foreground='white', borderwidth=2,
                                         font=('Century Gothic', 12))
        self.entry_birthdate.place(relx=0.310, rely=0.653, anchor="center")

        self.entry_income = CTkEntry(parent, textvariable=self.income_var,
                                     width=240, height=25, border_color="#937A69", font=('Century Gothic', 12),bg_color="White",)
        self.entry_income.place(relx=0.310, rely=0.710, anchor="center")

        self.entry_move_in = DateEntry(parent, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                       selectbackground='#937A69',
                                       font=('Century Gothic', 12))
        self.entry_move_in.place(relx=0.840, rely=0.311, anchor="center")

        self.entry_lease_start = DateEntry(parent, textvariable=self.lease_start_var, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                           selectbackground='#937A69',
                                           font=('Century Gothic', 12))
        self.entry_lease_start.place(relx=0.840, rely=0.368, anchor="center")

        self.entry_lease_end = DateEntry(parent, textvariable=self.lease_end_var, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                         selectbackground='#937A69',
                                         font=('Century Gothic', 12))
        self.entry_lease_end.place(relx=0.840, rely=0.425, anchor="center")

        self.entry_emergency_contact_number = CTkEntry(parent, textvariable=self.emergency_contact_number_var,
                                                       width=250, height=25, border_color="#937A69",bg_color="White",
                                                       font=('Century Gothic', 12))
        self.entry_emergency_contact_number.place(relx=0.420, rely=0.7955, anchor="center")

        self.entry_emergency_contact_name = CTkEntry(parent, textvariable=self.emergency_contact_name_var,
                                                     bg_color="White",
                                                     width=250, height=25, border_color="#937A69",
                                                     font=('Century Gothic', 12))
        self.entry_emergency_contact_name.place(relx=0.420, rely=0.8525, anchor="center")

        self.entry_relationship = CTkEntry(parent, textvariable=self.relationship_var, bg_color="White",
                                           width=250, height=25, border_color="#937A69",
                                           font=('Century Gothic', 12))
        self.entry_relationship.place(relx=0.420, rely=0.9095, anchor="center")

        # Buttons
        button_style = {
            "fg_color": "#CFB9A3",
            "hover_color": "#D6BC9D",
            "text_color": "#5C483F",
            "bg_color": "#f1f1f1",
            "font": ('Century Gothic', 20, "bold")
        }

        save_button = ctk.CTkButton(parent, text="Save", command=self.save_tenant_info, **button_style)

        # Place the buttons
        save_button.place(relx=0.85, rely=0.90, anchor='center')

    def update_unit_numbers(self, selected_building):
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        unit_numbers = draft_backend.fetch_unit_numbers_by_building(conn, selected_building)
        conn.close()

        print(f"Fetched unit numbers: {unit_numbers}")  # Debug statement

        # Clear existing values and update with fetched unit numbers
        self.entry_unit_number.configure(values=unit_numbers)

    def save_tenant_info(self):
        # Collect data from the entry fields/user input
        first_name = self.entry_first_name.get()
        middle_name = self.entry_middle_name.get()
        last_name = self.entry_last_name.get()
        suffix = self.entry_suffix_name.get()
        contact_number = self.entry_contactnum.get()
        email = self.entry_email.get()
        sex = self.combo_box_sex.get()
        birthdate = self.entry_birthdate.get_date()
        move_in_date = self.entry_move_in.get_date()
        lease_start_date = self.entry_lease_start.get_date()
        lease_end_date = self.entry_lease_end.get_date()
        emergency_contact_number = self.entry_emergency_contact_number.get()
        emergency_contact_name = self.entry_emergency_contact_name.get()
        emergency_contact_relationship = self.entry_relationship.get()
        income = self.entry_income.get()
        building_name = self.entry_building_name.get()
        unit_number = self.entry_unit_number.get()

        # Map the selected sex to its integer value
        sex_int = sex_mapping.get(sex)

        # Validate required fields
        if not building_name or not unit_number or not last_name or not first_name:
            CTkMessagebox(title="Error", message="All fields are required.")
            return

        if not income.isdigit():
            CTkMessagebox(title="Error", message="Please input only digits on tenant income.")
            return

        # Proceed to save data to the database
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        try:
            # Fetch the building_id based on building_name
            building_id = draft_backend.get_building_id(conn, building_name)
            if not building_id:
                CTkMessagebox(title="Error", message="Invalid building selected.")
                return

            # Fetch the unit_id based on unit_number and building_id
            unit_id = draft_backend.get_unit_id(conn, unit_number, building_id)
            if not unit_id:
                CTkMessagebox(title="Error", message="Invalid unit number selected.")
                return

            # Insert tenant information and fetch the tenant_id
            self.display_tenant_id = draft_backend.edit_tenant_info(
                conn, unit_id, last_name, first_name, middle_name, suffix, email, contact_number,
                move_in_date, lease_start_date, lease_end_date,
                emergency_contact_name, emergency_contact_number, emergency_contact_relationship,
                birthdate, sex_int, income, self.tenant_id)
            CTkMessagebox(title="Success", message="Tenant information updated successfully!")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

        # Close the Edit Building window after saving
        self.parent.destroy()

    def populate_tenant_info(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        try:
            print(f"Populating info for tenant_id: {self.tenant_id}")
            tenant_info = draft_backend.fetch_edit_tenant_info(conn, self.tenant_id)
            if tenant_info:
                print(f"Fetched tenant info: {tenant_info}")
                self.tenant_firt_name_var.set(tenant_info[0])
                self.tenant_middle_name_var.set(tenant_info[1])
                self.tenant_last_name_var.set(tenant_info[2])
                self.suffix_var.set(tenant_info[3])
                self.email_var.set(tenant_info[4])
                self.contactnum_var.set(tenant_info[5])
                self.birthdate_var.set(tenant_info[6])
                self.move_in_var.set(tenant_info[7])
                self.lease_start_var.set(tenant_info[8])
                self.lease_end_var.set(tenant_info[9])
                self.emergency_contact_name_var.set(tenant_info[10])
                self.emergency_contact_number_var.set(tenant_info[11])
                self.relationship_var.set(tenant_info[12])
                self.income_var.set(tenant_info[13])

                # Fetch building name and unit number for the tenant
                building_name = draft_backend.get_building_name_by_unit_id(conn, tenant_info[14])
                unit_number = draft_backend.get_unit_number_by_unit_id(conn, tenant_info[14])

                sex_str = list(sex_mapping.keys())[list(sex_mapping.values()).index(tenant_info[15])]
                self.combo_box_sex.set(sex_str)
            else:
                CTkMessagebox(title="Error", message="Tenant not found.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

