import tkinter as tk

from CTkMessagebox import CTkMessagebox
from PIL import Image
import customtkinter as ctk
from customtkinter import *
import add_unit  # Import the AddUnitComponent class
import draft_backend


class DisplayUnitInformation:
    def __init__(self, parent, unit_id=None):
        self.building_name = None
        self.parent = parent
        self.unit_id = unit_id
        self.create_widgets(parent)
        self.populate_unit_info()

    def create_widgets(self, parent):
        # Add background image
        building_bg_image = Image.open("images/bgAddUnitInformation.png")
        building_bg = ctk.CTkImage(building_bg_image, size=(900, 600))
        building_bg_lbl = ctk.CTkLabel(parent, text="", image=building_bg)
        building_bg_lbl.place(x=0, y=0)

        # StringVars for labels
        self.label_building_name_var = tk.StringVar()
        self.label_availability_status_var = tk.StringVar()
        self.label_unit_number_var = tk.StringVar()
        self.label_rental_rate_var = tk.StringVar()
        self.label_number_of_bedrooms_var = tk.StringVar()
        self.label_number_of_bathrooms_var = tk.StringVar()
        self.label_unit_size_var = tk.StringVar()
        self.label_maintenance_request_var = tk.StringVar()

        # Entry fields with placeholders and StringVars
        self.entry_building_name = CTkEntry(parent, textvariable=self.label_building_name_var,
                                            placeholder_text="Enter building name", width=200, height=30,
                                            border_color="#937A69", font=('Century Gothic', 15))
        self.entry_building_name.place(relx=0.340, rely=0.535, anchor="center")

        self.entry_availability_status = CTkEntry(parent, textvariable=self.label_availability_status_var,
                                                  placeholder_text="Enter availability status", width=200, height=30,
                                                  border_color="#937A69", font=('Century Gothic', 15))
        self.entry_availability_status.place(relx=0.340, rely=0.745, anchor="center")

        self.entry_unit_number = CTkEntry(parent, textvariable=self.label_unit_number_var,
                                          placeholder_text="Enter unit number", width=200, height=30,
                                          border_color="#937A69", font=('Century Gothic', 15))
        self.entry_unit_number.place(relx=0.340, rely=0.605, anchor="center")

        self.entry_rental_rate = CTkEntry(parent, textvariable=self.label_rental_rate_var,
                                          placeholder_text="Enter rental rate", width=200, height=30,
                                          border_color="#937A69", font=('Century Gothic', 15))
        self.entry_rental_rate.place(relx=0.340, rely=0.675, anchor="center")

        self.entry_number_of_bedrooms = CTkEntry(parent, textvariable=self.label_number_of_bedrooms_var,
                                                 placeholder_text="Enter number of bedrooms", width=230, height=30,
                                                 border_color="#937A69", font=('Century Gothic', 15))
        self.entry_number_of_bedrooms.place(relx=0.840, rely=0.535, anchor="center")

        self.entry_number_of_bathrooms = CTkEntry(parent, textvariable=self.label_number_of_bathrooms_var,
                                                  placeholder_text="Enter number of bathrooms", width=230, height=30,
                                                  border_color="#937A69", font=('Century Gothic', 15))
        self.entry_number_of_bathrooms.place(relx=0.840, rely=0.605, anchor="center")

        self.entry_unit_size = CTkEntry(parent, textvariable=self.label_unit_size_var,
                                        placeholder_text="Enter unit size", width=230, height=30,
                                        border_color="#937A69", font=('Century Gothic', 15))
        self.entry_unit_size.place(relx=0.840, rely=0.675, anchor="center")

        self.entry_maintenance_request = CTkEntry(parent, textvariable=self.label_maintenance_request_var,
                                                  placeholder_text="Enter maintenance request", width=230, height=30,
                                                  border_color="#937A69", font=('Century Gothic', 15))
        self.entry_maintenance_request.place(relx=0.840, rely=0.745, anchor="center")

        # Buttons
        button_style = {
            "fg_color": "#CFB9A3",
            "hover_color": "#D6BC9D",
            "text_color": "#5C483F",
            "bg_color": "#f1f1f1",
            "font": ('Century Gothic', 20, "bold")
        }

        edit_button = ctk.CTkButton(parent, text="Edit", command=self.edit_unit_info, **button_style)
        tenant_details_button = ctk.CTkButton(parent, text="Tenant Details", **button_style)

        # Place the buttons on the same line with closer margins
        edit_button.place(relx=0.85, rely=0.90, anchor='center')
        tenant_details_button.place(relx=0.68, rely=0.90, anchor='center')

    def populate_unit_info(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            unit_info = draft_backend.fetch_unit_info(conn, self.unit_id)
            if unit_info:
                building_id = unit_info[1]
                building_info = draft_backend.fetch_new_building_info(conn, building_id)
                if building_info:
                    building_name = building_info[2]

                    # Populate entry fields with retrieved unit information
                    self.label_building_name_var.set(building_name)
                    self.label_unit_number_var.set(unit_info[2])  # unit_number
                    self.label_number_of_bedrooms_var.set(unit_info[3])  # num_bedrooms
                    self.label_number_of_bathrooms_var.set(unit_info[4])  # num_bathrooms
                    self.label_unit_size_var.set(unit_info[5])  # unit_size_square_m
                    self.label_rental_rate_var.set(unit_info[6])  # rental_rate
                    self.label_availability_status_var.set(unit_info[7])  # availability_status
                    self.label_maintenance_request_var.set(unit_info[8])  # maintenance_request

                    self.disable_fields()

                else:
                    # Handle case where building information is not found
                    CTkMessagebox(title="Error", message=f"Building information not found for ID: {building_id}")

            else:
                # Handle case where unit information is not found
                CTkMessagebox(title="Error", message=f"Unit information not found for ID: {self.unit_id}")

        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")

        finally:
            conn.close()

    def disable_fields(self):
        # Disable entry fields after populating them
        self.entry_building_name.configure(state="disabled")
        self.entry_unit_number.configure(state="disabled")
        self.entry_number_of_bedrooms.configure(state="disabled")
        self.entry_number_of_bathrooms.configure(state="disabled")
        self.entry_unit_size.configure(state="disabled")
        self.entry_rental_rate.configure(state="disabled")
        self.entry_availability_status.configure(state="disabled")
        self.entry_maintenance_request.configure(state="disabled")

    def edit_unit_info(self):
        # Close the Display Unit Info window
        if self.parent:
            self.parent.destroy()

        # Create a new top-level window for Add Unit
        self.add_unit_window = tk.Toplevel()
        self.add_unit_window.title("Edit Unit Information")
        self.add_unit_window.geometry("1125x750")
        self.add_unit_window.resizable(False, False)

        # Ensure the new window is always on top
        self.add_unit_window.attributes('-topmost', True)

        # Center the new window on the screen
        screen_width = self.add_unit_window.winfo_screenwidth()
        screen_height = self.add_unit_window.winfo_screenheight()
        window_width = 1125
        window_height = 750

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        self.add_unit_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Create an instance of AddUnitComponent and pass the new window as its parent
        add_unit_component = add_unit.AddUnitComponent(self.add_unit_window)
