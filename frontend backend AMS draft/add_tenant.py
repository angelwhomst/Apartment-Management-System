import tkinter as tk
from tkcalendar import DateEntry
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkEntry, CTkComboBox


class AddTenantComponent:
    def __init__(self, parent):
        self.parent = parent
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
        self.entry_tenant_name = CTkEntry(parent, placeholder_text="Enter tenant name", width=240, height=25,
                                          border_color="#937A69",
                                          font=('Century Gothic', 12))
        self.entry_tenant_name.place(relx=0.310, rely=0.425, anchor="center")

        self.entry_contactnum = CTkEntry(parent, placeholder_text="Enter contact number", width=240, height=25,
                                         border_color="#937A69",
                                         font=('Century Gothic', 12))
        self.entry_contactnum.place(relx=0.310, rely=0.482, anchor="center")

        self.entry_email = CTkEntry(parent, placeholder_text="Enter email", width=240, height=25,
                                    border_color="#937A69",
                                    font=('Century Gothic', 12))
        self.entry_email.place(relx=0.310, rely=0.539, anchor="center")

        self.entry_unit_number = CTkEntry(parent, placeholder_text="Enter unit number", width=240, height=25,
                                          border_color="#937A69",
                                          font=('Century Gothic', 12))
        self.entry_unit_number.place(relx=0.310, rely=0.596, anchor="center")

        self.combo_box_sex = CTkComboBox(parent, width=240, height=25,
                                         border_color="#937A69",
                                         font=('Century Gothic', 12))
        self.combo_box_sex.place(relx=0.310, rely=0.653, anchor="center")

        self.entry_birthdate = DateEntry(parent, width=30, background='#937A69', foreground='white', borderwidth=2,
                                         font=('Century Gothic', 12))
        self.entry_birthdate.place(relx=0.310, rely=0.710, anchor="center")

        self.entry_move_in = CTkEntry(parent, placeholder_text="Enter move in date", width=150, height=25,
                                      border_color="#937A69",
                                      font=('Century Gothic', 12))
        self.entry_move_in = DateEntry(parent, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                       selectbackground='#937A69',
                                       font=('Century Gothic', 12))
        self.entry_move_in.place(relx=0.840, rely=0.425, anchor="center")

        self.entry_lease_start = DateEntry(parent, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                           selectbackground='#937A69',
                                           font=('Century Gothic', 12))
        self.entry_lease_start.place(relx=0.840, rely=0.482, anchor="center")

        self.entry_lease_end = DateEntry(parent, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                         selectbackground='#937A69',
                                         font=('Century Gothic', 12))
        self.entry_lease_end.place(relx=0.840, rely=0.539, anchor="center")

        self.entry_last_payment = DateEntry(parent, width=20, background='#937A69', foreground='#937A69', borderwidth=2,
                                            selectbackground='#937A69',
                                            font=('Century Gothic', 12))
        self.entry_last_payment.place(relx=0.840, rely=0.596, anchor="center")

        self.entry_emergency_contact_number = CTkEntry(parent, placeholder_text="Enter emergency contact number",
                                                       width=250, height=25, border_color="#937A69",
                                                       font=('Century Gothic', 12))
        self.entry_emergency_contact_number.place(relx=0.420, rely=0.800, anchor="center")

        self.entry_emergency_contact_name = CTkEntry(parent, placeholder_text="Enter emergency contact name",
                                                     width=250, height=25, border_color="#937A69",
                                                     font=('Century Gothic', 12))
        self.entry_emergency_contact_name.place(relx=0.420, rely=0.857, anchor="center")

        self.entry_relationship = CTkEntry(parent, placeholder_text="Enter relationship",
                                           width=250, height=25, border_color="#937A69",
                                           font=('Century Gothic', 12))
        self.entry_relationship.place(relx=0.420, rely=0.914, anchor="center")

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

    def save_tenant_info(self):
        # collect data from the entry fields
        first_name = self.entry_tenant_name


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

        self.display_tenant_info_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Import DisplayTenantComponent class here to avoid circular import
        from display_tenant_details import DisplayTenantComponent
        # Create an instance of DisplayTenantComponent and pass the new window as its parent
        DisplayTenantComponent(self.display_tenant_info_window)


def main():
    root = tk.Tk()
    root.geometry("950x600")
    app = AddTenantComponent(root)
    root.mainloop()


if __name__ == "__main__":
    main()
