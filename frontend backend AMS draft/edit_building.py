from CTkMessagebox import CTkMessagebox
from PIL import Image
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry
import draft_backend

class EditBuildingComponent:
    def __init__(self, parent, building_id=None):
        self.parent = parent
        self.building_id = building_id
        self.create_widgets(parent)
        self.populate_building_info()  # Populate building information if editing existing building

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

        # Save button
        button_style = {
            "fg_color": "#CFB9A3",
            "hover_color": "#D6BC9D",
            "text_color": "#5C483F",
            "bg_color": "#f1f1f1",
            "font": ('Century Gothic', 20, "bold")
        }
        save_button = ctk.CTkButton(parent, text="Save", command=self.save_building_info, **button_style)
        save_button.place(relx=0.85, rely=0.90, anchor='center')

    def populate_building_info(self):
        if not self.building_id:
            return

        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        try:
            building_info = draft_backend.fetch_building_info(conn, self.building_id)
            if building_info:
                self.entry_building_name.set(building_info['building_name'])
                self.entry_country.set(building_info['country'])
                self.entry_province.set(building_info['province'])
                self.entry_city.set(building_info['city'])
                self.entry_street.set(building_info['street'])
                self.entry_lot.set(building_info['lot_number'])
                self.entry_zipcode.set(building_info['zip_code'])
                self.entry_amenities.set(building_info['amenities'])
            else:
                CTkMessagebox(title="Error", message=f"Building information not found for ID: {self.building_id}")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def save_building_info(self):
        building_name = self.entry_building_name.get()
        country = self.entry_country.get()
        province = self.entry_province.get()
        city = self.entry_city.get()
        street = self.entry_street.get()
        lot_number = self.entry_lot.get()
        zip_code = self.entry_zipcode.get()
        amenities = self.entry_amenities.get()

        if not building_name:
            CTkMessagebox(title="Error", message="Building name is required.")
            return

        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        try:
            draft_backend.update_building(conn, self.building_id, building_name, country, province, city, street,
                                          lot_number, zip_code, amenities)
            CTkMessagebox(title="Success", message="Building information updated successfully!")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

        # Close the Edit Building window after saving
        self.parent.destroy()

# Corrected indentation for main function
def main():
    root = tk.Tk()
    root.geometry("950x600")
    app = EditBuildingComponent(root)
    root.mainloop()

if __name__ == "__main__":
    main()
