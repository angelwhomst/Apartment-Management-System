from CTkMessagebox import CTkMessagebox
from PIL import Image
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkEntry, CTkLabel
import draft_backend


class AddBuildingComponent:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets(parent)

    def create_widgets(self, parent):
        # Example widgets for adding building components
        label = tk.Label(parent, text="Editing Building Information", font=('Century Gothic', 20, 'bold'))
        label.pack(pady=20)

        # Example entry field
        entry = tk.Entry(parent, font=('Century Gothic', 15))
        entry.pack(pady=10)

        # Example button
        button = tk.Button(parent, text="Save", command=self.save_building_info, font=('Century Gothic', 15, 'bold'))
        button.pack(pady=20)

    def save_building_info(self):
        # Example function to save building information
        pass


class DisplayBuildingInformation:
    def __init__(self, parent, building_id=None):
        self.parent = parent
        self.building_id = building_id
        self.add_building_window = None  # Initialize top-level window attribute for Add Building
        self.display_building_info_window = None  # Initialize top-level window attribute for Display Building Info
        self.create_widgets(parent)
        self.populate_building_info()  # Populate building information on initialization

    def create_widgets(self, parent):
        # Add background image
        building_bg_image = Image.open("images/bgBuildinginformation.png")
        building_bg = ctk.CTkImage(building_bg_image, size=(900, 600))
        building_bg_lbl = ctk.CTkLabel(parent, text="", image=building_bg)
        building_bg_lbl.place(x=0, y=0)

        # StringVars for labels
        self.label_building_name_var = tk.StringVar()
        self.label_country_var = tk.StringVar()
        self.label_province_var = tk.StringVar()
        self.label_city_var = tk.StringVar()
        self.label_street_var = tk.StringVar()
        self.label_lot_var = tk.StringVar()
        self.label_zipcode_var = tk.StringVar()
        self.label_amenities_var = tk.StringVar()

        # Entry fields with placeholders and StringVars
        self.entry_building_name = CTkEntry(parent, textvariable=self.label_building_name_var, width=181, height=30,
                                            border_color="#937A69", font=('Century Gothic', 15))
        self.entry_building_name.place(relx=0.336, rely=0.535, anchor="center")

        self.entry_country = CTkEntry(parent, textvariable=self.label_country_var,
                                      width=240, height=30, border_color="#937A69", font=('Century Gothic', 15))
        self.entry_country.place(relx=0.305, rely=0.605, anchor="center")

        self.entry_province = CTkEntry(parent, textvariable=self.label_province_var,
                                       width=240, height=30, border_color="#937A69", font=('Century Gothic', 15))
        self.entry_province.place(relx=0.305, rely=0.675, anchor="center")

        self.entry_city = CTkEntry(parent, textvariable=self.label_city_var, width=240, height=30,
                                   border_color="#937A69", font=('Century Gothic', 15))
        self.entry_city.place(relx=0.305, rely=0.745, anchor="center")

        self.entry_street = CTkEntry(parent, textvariable=self.label_street_var,
                                     width=240, height=30, border_color="#937A69", font=('Century Gothic', 15))
        self.entry_street.place(relx=0.795, rely=0.535, anchor="center")

        self.entry_lot = CTkEntry(parent, textvariable=self.label_lot_var,
                                  width=240, height=30, border_color="#937A69", font=('Century Gothic', 15))
        self.entry_lot.place(relx=0.795, rely=0.605, anchor="center")

        self.entry_zipcode = CTkEntry(parent, textvariable=self.label_zipcode_var,
                                      width=240, height=30, border_color="#937A69", font=('Century Gothic', 15))
        self.entry_zipcode.place(relx=0.795, rely=0.675, anchor="center")

        self.entry_amenities = CTkEntry(parent, textvariable=self.label_amenities_var, width=240, height=30,
                                        border_color="#937A69", font=('Century Gothic', 15))
        self.entry_amenities.place(relx=0.795, rely=0.745, anchor="center")

        # Buttons
        button_style = {
            "fg_color": "#CFB9A3",
            "hover_color": "#D6BC9D",
            "text_color": "#5C483F",
            "bg_color": "#f1f1f1",
            "font": ('Century Gothic', 20, "bold")
        }

        edit_button = ctk.CTkButton(parent, text="Edit", command=self.edit_building_info, **button_style)

        # Place the button
        edit_button.place(relx=0.85, rely=0.90, anchor='center')

    def populate_building_info(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            return

        try:
            building_info = draft_backend.fetch_new_building_info(conn, self.building_id)
            if building_info:
                # Populate entry fields with retrieved building information
                self.label_building_name_var.set(building_info[2])
                self.label_country_var.set(building_info[3])
                self.label_province_var.set(building_info[4])
                self.label_city_var.set(building_info[5])
                self.label_street_var.set(building_info[6])
                self.label_lot_var.set(building_info[7])
                self.label_zipcode_var.set(building_info[8])
                self.label_amenities_var.set(building_info[9])

                # Disable entry fields after populating them
                self.entry_building_name.configure(state="disabled")
                self.entry_country.configure(state="disabled")
                self.entry_province.configure(state="disabled")
                self.entry_city.configure(state="disabled")
                self.entry_street.configure(state="disabled")
                self.entry_lot.configure(state="disabled")
                self.entry_zipcode.configure(state="disabled")
                self.entry_amenities.configure(state="disabled")

            else:
                # Handle case where building information is not found
                CTkMessagebox(title="Error", message=f"Building information not found for ID: {self.building_id}")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def edit_building_info(self):
        # Close the Display Building Info window
        if self.display_building_info_window:
            self.display_building_info_window.destroy()

        # Create a new top-level window for Add Building
        self.add_building_window = ctk.CTkToplevel(self.parent)
        self.add_building_window.title("Edit Building")
        self.add_building_window.geometry("900x600")
        self.add_building_window.resizable(False, False)

        # Ensure the new window is always on top
        self.add_building_window.attributes('-topmost', True)

        # Center the new window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        self.add_building_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Create an instance of AddBuildingComponent and pass the new window as its parent
        AddBuildingComponent(self.add_building_window)

        # Close the current DisplayBuildingInformation window
        self.parent.destroy()

#
# def main():
#     root = tk.Tk()
#     root.geometry("950x600")
#     app = DisplayBuildingInformation(root)
#     root.mainloop()
#
#
# if __name__ == "__main__":
#     main()
