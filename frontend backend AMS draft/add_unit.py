import tkinter as tk
from tkinter import END
from CTkMessagebox import CTkMessagebox
from PIL import Image
import customtkinter as ctk
from customtkinter import CTkEntry, CTkButton, CTkLabel, CTkComboBox
import draft_backend

# mapping from the combobox values to their respective integer values for availability_status
availability_status_mapping = {
    "Available": 1,
    "Occupied": 2,
    "Under Maintenance": 3
}


class AddUnitComponent:
    def __init__(self, parent):
        self.parent = parent
        self.display_unit_id = None
        self.create_widgets(parent)

    def create_widgets(self, parent):
        # Add background image
        building_bg_image = Image.open("images/bgAddUnitInformation.png")
        building_bg = ctk.CTkImage(building_bg_image, size=(900, 600))
        building_bg_lbl = ctk.CTkLabel(parent, text="", image=building_bg)
        building_bg_lbl.place(x=0, y=0)

        # Fetch building names from the database
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return
        building_names = draft_backend.fetch_building_names(conn)
        conn.close()

        self.combo_box_building_name = ctk.CTkComboBox(parent, values=building_names, width=200, height=30,
                                                       font=('Century Gothic', 15), border_color="#937A69")
        self.combo_box_building_name.place(relx=0.340, rely=0.535, anchor="center")

        self.combo_box_availability_status = ctk.CTkComboBox(parent,
                                                             values=['Available', 'Occupied', 'Under Maintenance'],
                                                             width=200, height=30, font=('Century Gothic', 15),
                                                             border_color="#937A69")
        self.combo_box_availability_status.place(relx=0.340, rely=0.745, anchor="center")

        # Add Entries
        self.entry_unit_number = CTkEntry(parent, placeholder_text="Enter unit number", width=200, height=30,
                                            border_color="#937A69",
                                            font=('Century Gothic', 15))
        self.entry_unit_number.place(relx=0.340, rely=0.605, anchor="center")

        self.entry_rental_rate = CTkEntry(parent, placeholder_text="Enter rental rate", width=200, height=30,
                                            border_color="#937A69",
                                            font=('Century Gothic', 15))
        self.entry_rental_rate.place(relx=0.340, rely=0.675, anchor="center")

        self.entry_number_of_bedrooms = CTkEntry(parent, placeholder_text="Enter number of bedrooms", width=230, height=30,
                                            border_color="#937A69",
                                            font=('Century Gothic', 15))
        self.entry_number_of_bedrooms.place(relx=0.840, rely=0.535, anchor="center")

        self.entry_number_of_bathrooms = CTkEntry(parent, placeholder_text="Enter number of bathrooms", width=230, height=30,
                                            border_color="#937A69",
                                            font=('Century Gothic', 15))
        self.entry_number_of_bathrooms.place(relx=0.840, rely=0.605, anchor="center")

        self.entry_unit_size = CTkEntry(parent, placeholder_text="Enter unit size", width=230, height=30,
                                            border_color="#937A69",
                                            font=('Century Gothic', 15))
        self.entry_unit_size.place(relx=0.840, rely=0.675, anchor="center")

        self.entry_maintenance_request = CTkEntry(parent, placeholder_text="Enter maintenance request", width=230, height=30,
                                        border_color="#937A69",
                                        font=('Century Gothic', 15))
        self.entry_maintenance_request.place(relx=0.840, rely=0.745, anchor="center")

        # Buttons
        button_style = {
            "fg_color": "#CFB9A3",
            "hover_color": "#D6BC9D",
            "text_color": "#5C483F",
            "bg_color": "#f1f1f1",
            "font": ('Century Gothic', 20, "bold")
        }

        save_button = ctk.CTkButton(parent, text="Save", command=self.save_unit_info, **button_style)
        add_tenant_button = ctk.CTkButton(parent, text="Add Tenant", command=self.open_add_unit, **button_style)

        # Place the buttons on the same line with closer margins
        save_button.place(relx=0.85, rely=0.90, anchor='center')
        add_tenant_button.place(relx=0.68, rely=0.90, anchor='center')

    def save_unit_info(self):
        # Collect data from the entry fields
        unit_number = self.entry_unit_number.get()
        rental_rate = self.entry_rental_rate.get()
        number_of_bedrooms = self.entry_number_of_bedrooms.get()
        number_of_bathrooms = self.entry_number_of_bathrooms.get()
        unit_size = self.entry_unit_size.get()
        maintenance_request = self.entry_maintenance_request.get()
        availability_status = self.combo_box_availability_status.get()

        # Map the selected availability status to its integer value
        availability_status_int = availability_status_mapping.get(availability_status)

        # Fetch the selected building name from the combo box
        building_name = self.combo_box_building_name.get()

        # Proceed to save the data to the database
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return
        try:
            building_id = draft_backend.fetch_building_id_by_name(conn, building_name)
            if not building_id:
                CTkMessagebox(title="Error", message=f"No building found with the name {building_name}")
                return

            draft_backend.insert_unit(conn, building_id, unit_number, rental_rate, number_of_bedrooms,
                                      number_of_bathrooms, unit_size, maintenance_request, availability_status_int)
            CTkMessagebox(title="Success", message="Unit information saved successfully!")

            # fetch the unit_id of the newly inserted building
            self.display_unit_id = draft_backend.fetch_latest_unit_id(conn)

            # fetches the unit_id of the newly inserted unit to immediately display
            self.display_unit_id = draft_backend.fetch_latest_unit_id(conn)
            self.clear_entry_fields()
            self.show_unit_info()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def clear_entry_fields(self):
        self.entry_unit_number.delete(0, END)
        self.entry_rental_rate.delete(0, END)
        self.entry_number_of_bedrooms.delete(0, END)
        self.entry_number_of_bathrooms.delete(0, END)
        self.entry_unit_size.delete(0, END)
        self.entry_maintenance_request.delete(0, END)

    def show_unit_info(self):
        # Display the unit information using the DisplayUnitInformation class
        from display_unit_info import DisplayUnitInformation
        DisplayUnitInformation(self.parent, self.display_unit_id)

    def open_add_unit(self):
        # Create a new top-level window for adding a unit
        top_level_window = ctk.CTkToplevel(self.parent)
        top_level_window.title("Add Unit")
        top_level_window.geometry("950x600")
        top_level_window.attributes('-topmost', True)  # Keep the window on top

        # Disable window resizing
        top_level_window.resizable(False, False)

        # Center the window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        top_level_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Create widgets in the top-level window
        self.create_widgets(top_level_window)


