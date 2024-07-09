import tkinter as tk
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


class AddTenantComponent:
    def __init__(self, parent):
        self.parent = parent
        self.display_tenant_id = None
        self.add_building_window = None  # Initialize top-level window attribute for Add Building
        self.add_unit_window = None  # Initialize top-level window attribute for Add Unit
        self.create_widgets(parent)

    def create_widgets(self, parent):
        # Add background image
        building_bg_image = Image.open("images/addTenantBg.png")
        building_bg = ctk.CTkImage(building_bg_image, size=(900, 600))
        building_bg_lbl = ctk.CTkLabel(parent, text="", image=building_bg)
        building_bg_lbl.place(x=0, y=0)

        # Entry fields/Combo box
        self.entry_first_name = CTkEntry(parent, placeholder_text="First name", width=80, height=25,
                                         border_color="#937A69",
                                         font=('Century Gothic', 12))
        self.entry_first_name.place(relx=0.090, rely=0.368, anchor="center")

        self.entry_middle_name = CTkEntry(parent, placeholder_text="Middle name", width=80, height=25,
                                          border_color="#937A69",
                                          font=('Century Gothic', 12))
        self.entry_middle_name.place(relx=0.194, rely=0.368, anchor="center")

        self.entry_last_name = CTkEntry(parent, placeholder_text="Last name", width=80, height=25,
                                        border_color="#937A69",
                                        font=('Century Gothic', 12))
        self.entry_last_name.place(relx=0.296, rely=0.368, anchor="center")

        self.entry_suffix_name = CTkEntry(parent, placeholder_text="Suffix", width=80, height=25,
                                          font=('Century Gothic', 12))
        self.entry_suffix_name.place(relx=0.400, rely=0.368, anchor="center")

        self.entry_contactnum = CTkEntry(parent, placeholder_text="Enter contact number", width=240, height=25,
                                         border_color="#937A69",
                                         font=('Century Gothic', 12))
        self.entry_contactnum.place(relx=0.310, rely=0.425, anchor="center")

        self.entry_email = CTkEntry(parent, placeholder_text="Enter email", width=240, height=25,
                                    border_color="#937A69",
                                    font=('Century Gothic', 12))
        self.entry_email.place(relx=0.310, rely=0.482, anchor="center")

        # Fetch building names from the database
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return
        building_names = draft_backend.fetch_building_names(conn)
        conn.close()

        self.entry_building_name = CTkComboBox(parent, values=building_names, width=240, height=25,
                                                font=('Century Gothic', 12))
        self.entry_building_name.place(relx=0.310, rely=0.300, anchor="center")

        # # Bind event to update unit numbers when building is selected HINDI GUMAGANA SA CTK
        # self.entry_building_name.bind("<<ComboboxSelected>>", self.update_unit_numbers)

        # Fetch unit numbers from the database when building is selected
        self.entry_unit_number = CTkComboBox(parent, values=[], width=240, height=25,
                                              font=('Century Gothic', 12))
        self.entry_unit_number.place(relx=0.310, rely=0.539, anchor="center")

        # Bind the command to update unit numbers based on building selection
        self.entry_building_name.configure(command=self.update_unit_numbers)

        self.combo_box_sex = CTkComboBox(parent, values=['Male', 'Female', 'Prefer not to say'], width=240, height=25,
                                         border_color="#937A69",
                                         font=('Century Gothic', 12))
        self.combo_box_sex.place(relx=0.310, rely=0.596, anchor="center")

        self.entry_birthdate = DateEntry(parent, width=30, background='#937A69', foreground='white', borderwidth=2,
                                         font=('Century Gothic', 12))
        self.entry_birthdate.place(relx=0.310, rely=0.653, anchor="center")

        self.entry_income = CTkEntry(parent, placeholder_text="Enter income",
                                     width=240, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_income.place(relx=0.310, rely=0.710, anchor="center")

        self.entry_move_in = DateEntry(parent, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                       selectbackground='#937A69',
                                       font=('Century Gothic', 12))
        self.entry_move_in.place(relx=0.840, rely=0.311, anchor="center")

        self.entry_lease_start = DateEntry(parent, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                           selectbackground='#937A69',
                                           font=('Century Gothic', 12))
        self.entry_lease_start.place(relx=0.840, rely=0.368, anchor="center")

        self.entry_lease_end = DateEntry(parent, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                         selectbackground='#937A69',
                                         font=('Century Gothic', 12))
        self.entry_lease_end.place(relx=0.840, rely=0.425, anchor="center")

        self.entry_emergency_contact_number = CTkEntry(parent, placeholder_text="Enter emergency contact number",
                                                       width=250, height=25, border_color="#937A69",
                                                       font=('Century Gothic', 12))
        self.entry_emergency_contact_number.place(relx=0.420, rely=0.7955, anchor="center")

        self.entry_emergency_contact_name = CTkEntry(parent, placeholder_text="Enter emergency contact name",
                                                     width=250, height=25, border_color="#937A69",
                                                     font=('Century Gothic', 12))
        self.entry_emergency_contact_name.place(relx=0.420, rely=0.8525, anchor="center")

        self.entry_relationship = CTkEntry(parent, placeholder_text="Enter relationship",
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
            self.display_tenant_id = draft_backend.insert_tenant(
                conn, last_name, first_name, middle_name, suffix, email, contact_number,
                move_in_date, lease_start_date, lease_end_date,
                emergency_contact_name, emergency_contact_number, emergency_contact_relationship,
                birthdate, sex_int, income, unit_id)

            if self.display_tenant_id:
                CTkMessagebox(title="Success", message="Tenant information saved successfully!")

                # Close the Add Building window if it exists
                if self.add_building_window:
                    self.add_building_window.destroy()

                # Close the Add Unit window if it exists
                if self.add_unit_window:
                    self.add_unit_window.destroy()

                # Close the current Add Tenant window
                self.parent.destroy()

                # Create a new CTkToplevel window for displaying tenant information
                self.display_tenant_info_window = ctk.CTkToplevel()
                self.display_tenant_info_window.title("Display Tenant Information")
                self.display_tenant_info_window.geometry("900x600")

                # Ensure the new window is always on top
                self.display_tenant_info_window.attributes('-topmost', True)
                self.display_tenant_info_window.resizable(False, False)

                # Center the new window on the screen
                screen_width = self.display_tenant_info_window.winfo_screenwidth()
                screen_height = self.display_tenant_info_window.winfo_screenheight()
                window_width = 900
                window_height = 600

                position_right = int(screen_width / 2 - window_width / 2)
                position_down = int(screen_height / 2 - window_height / 2)

                self.display_tenant_info_window.geometry(
                    f"{window_width}x{window_height}+{position_right}+{position_down}")

                # Import DisplayTenantComponent class here to avoid circular import
                from display_tenant_details import DisplayTenantComponent

                # Create an instance of DisplayTenantComponent and pass the new window as its parent
                DisplayTenantComponent(self.display_tenant_info_window, self.display_tenant_id)

                # # Update Treeview with new tenant data
                # from tenant_information import TenantInformationFrame
                # new_tenant_data = (unit_number, last_name, first_name, contact_number, "Active", move_in_date)
                # self.controller.frames[TenantInformationFrame].add_tenant_to_treeview(new_tenant_data)

            else:
                CTkMessagebox(title="Error", message="Failed to save tenant information.")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")

        finally:
            conn.close()
