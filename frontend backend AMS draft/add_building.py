from CTkMessagebox import CTkMessagebox
from PIL import Image
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry
import draft_backend
from add_unit import AddUnitComponent


class AddBuildingComponent:
    def __init__(self, parent):
        self.parent = parent
        self.add_building_window = None  # Initialize top-level window attribute for Add Building
        self.add_unit_window = None  # Initialize top-level window attribute for Add Unit
        self.display_building_id = None
        self.create_widgets(parent)

    def create_widgets(self, parent):
        # Add background image
        building_bg_image = Image.open("images/bgBuildinginformation.png")
        building_bg = ctk.CTkImage(building_bg_image, size=(900, 600))
        building_bg_lbl = ctk.CTkLabel(parent, text="", image=building_bg)
        building_bg_lbl.place(x=0, y=0)

        # Entry fields
        self.entry_building_name = CTkEntry(parent, placeholder_text="Enter building name", width=181, height=30,
                                            border_color="#937A69",
                                            font=('Century Gothic', 15))
        self.entry_building_name.place(relx=0.336, rely=0.535, anchor="center")

        self.entry_country = CTkEntry(parent, placeholder_text="Enter country", width=240, height=30,
                                      border_color="#937A69",
                                      font=('Century Gothic', 15))
        self.entry_country.place(relx=0.305, rely=0.605, anchor="center")

        self.entry_province = CTkEntry(parent, placeholder_text="Enter province", width=240, height=30,
                                       border_color="#937A69",
                                       font=('Century Gothic', 15))
        self.entry_province.place(relx=0.305, rely=0.675, anchor="center")

        self.entry_city = CTkEntry(parent, placeholder_text="Enter city", width=240, height=30, border_color="#937A69",
                                   font=('Century Gothic', 15))
        self.entry_city.place(relx=0.305, rely=0.745, anchor="center")

        self.entry_street = CTkEntry(parent, placeholder_text="Enter street", width=240, height=30,
                                     border_color="#937A69",
                                     font=('Century Gothic', 15))
        self.entry_street.place(relx=0.795, rely=0.535, anchor="center")

        self.entry_lot = CTkEntry(parent, placeholder_text="Enter lot number", width=240, height=30,
                                  border_color="#937A69",
                                  font=('Century Gothic', 15))
        self.entry_lot.place(relx=0.795, rely=0.605, anchor="center")

        self.entry_zipcode = CTkEntry(parent, placeholder_text="Enter zip code", width=240, height=30,
                                      border_color="#937A69",
                                      font=('Century Gothic', 15))
        self.entry_zipcode.place(relx=0.795, rely=0.675, anchor="center")

        self.entry_amenities = CTkEntry(parent, placeholder_text="Enter amenities", width=240, height=30,
                                        border_color="#937A69",
                                        font=('Century Gothic', 15))
        self.entry_amenities.place(relx=0.795, rely=0.745, anchor="center")

        # Buttons
        button_style = {
            "fg_color": "#CFB9A3",
            "hover_color": "#D6BC9D",
            "text_color": "#5C483F",
            "bg_color": "#f1f1f1",
            "font": ('Century Gothic', 20, "bold")
        }

        save_button = ctk.CTkButton(parent, text="Save", command=self.save_building_info, **button_style)
        add_unit_button = ctk.CTkButton(parent, text="Add Unit", command=self.open_add_unit, **button_style)

        # Place the buttons
        save_button.place(relx=0.85, rely=0.90, anchor='center')
        add_unit_button.place(relx=0.68, rely=0.90, anchor='center')

    def save_building_info(self):
        # Collect data from the entry fields
        building_name = self.entry_building_name.get()
        country = self.entry_country.get()
        province = self.entry_province.get()
        city = self.entry_city.get()
        street = self.entry_street.get()
        lot_number = self.entry_lot.get()
        zip_code = self.entry_zipcode.get()
        amenities = self.entry_amenities.get()

        # Validate required fields
        if not building_name:
            CTkMessagebox(title="Error", message="Building name is required.")
            return

        # Insert the building information into the database
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        try:
            draft_backend.insert_building(conn, building_name, country, province, city, street, lot_number, zip_code,
                                          amenities)
            CTkMessagebox(title="Success", message="Building information saved successfully!")

            # fetch the building_id of the newly inserted building
            self.display_building_id = draft_backend.fetch_latest_building_id(conn)

            self.clear_entry_fields()
            self.open_display_building_info()  # Open display building info window
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

        # Close the Add Building window if it exists
        if self.add_building_window:
            self.add_building_window.destroy()

        # Create a new CTkToplevel window for displaying building information

    def open_display_building_info(self):
        # Create a new CTkToplevel window for displaying building information
        self.display_building_info_window = ctk.CTkToplevel(self.parent)
        self.display_building_info_window.title("Display Building Information")
        self.display_building_info_window.geometry("900x600")

        # Ensure the new window is always on top
        self.display_building_info_window.attributes('-topmost', True)

        self.display_building_info_window.resizable(False, False)

        # Center the new window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        self.display_building_info_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Import DisplayBuildingInformation class here to avoid circular import
        from display_building_info import DisplayBuildingInformation
        # Create an instance of DisplayBuildingInformation and pass the new window as its parent
        DisplayBuildingInformation(self.display_building_info_window, self.display_building_id)

    def clear_entry_fields(self):
        self.entry_building_name.delete(0, tk.END)
        self.entry_country.delete(0, tk.END)
        self.entry_province.delete(0, tk.END)
        self.entry_city.delete(0, tk.END)
        self.entry_street.delete(0, tk.END)
        self.entry_lot.delete(0, tk.END)
        self.entry_zipcode.delete(0, tk.END)
        self.entry_amenities.delete(0, tk.END)

    def open_add_unit(self):
        # Close the Add Building window if it exists
        if self.add_building_window:
            self.add_building_window.destroy()

        # Create a new CTkToplevel window for the Add Unit component
        self.add_unit_window = ctk.CTkToplevel(self.parent)
        self.add_unit_window.title("Add Unit")
        self.add_unit_window.geometry("900x600")

        self.add_unit_window.resizable(False, False)

        # Ensure the new window is always on top
        self.add_unit_window.attributes('-topmost', True)

        # Center the new window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        self.add_unit_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Create an instance of AddUnitComponent and pass the new window as its parent
        AddUnitComponent(self.add_unit_window)

# def main():
#     root = tk.Tk()
#     root.geometry("950x600")
#     app = AddBuildingComponent(root)
#     root.mainloop()
#
# if __name__ == "__main__":
#     main()
