import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
from customtkinter import CTkEntry
from tkinter import StringVar
from tkcalendar import DateEntry
import draft_backend


class DisplayTenantComponent:
    def __init__(self, parent, tenant_id=None):
        self.parent = parent
        self.tenant_id = tenant_id
        self.add_building_window = None  # Initialize top-level window attribute for Add Building
        self.add_unit_window = None  # Initialize top-level window attribute for Add Unit

        # StringVars for entry fields
        self.tenant_name_var = StringVar()
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

        # Create widgets first
        self.create_widgets(parent)

        # Populate tenant info after widgets are created
        if self.tenant_id:
            self.populate_tenant_info()

    def create_widgets(self, parent):
        # Add background image
        building_bg_image = Image.open("images/addTenantBg.png")
        building_bg = ctk.CTkImage(building_bg_image, size=(900, 600))
        building_bg_lbl = ctk.CTkLabel(parent, text="", image=building_bg)
        building_bg_lbl.place(x=0, y=0)

        # Entry fields/Combo box
        self.entry_tenant_name = CTkEntry(parent, textvariable=self.tenant_name_var,
                                          placeholder_text="Enter tenant name",
                                          width=230, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_tenant_name.place(relx=0.310, rely=0.425, anchor="center")

        self.entry_contactnum = CTkEntry(parent, textvariable=self.contactnum_var,
                                         placeholder_text="Enter contact number",
                                         width=230, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_contactnum.place(relx=0.310, rely=0.482, anchor="center")

        self.entry_email = CTkEntry(parent, textvariable=self.email_var, placeholder_text="Enter email",
                                    width=230, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_email.place(relx=0.310, rely=0.539, anchor="center")

        self.entry_unit_number = CTkEntry(parent, textvariable=self.unit_number_var,
                                          placeholder_text="Enter unit number",
                                          width=230, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_unit_number.place(relx=0.310, rely=0.596, anchor="center")

        self.entry_sex = CTkEntry(parent, textvariable=self.sex_var, placeholder_text="Enter sex",
                                  width=230, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_sex.place(relx=0.310, rely=0.653, anchor="center")

        self.entry_birthdate = CTkEntry(parent, textvariable=self.birthdate_var, placeholder_text="Enter birthdate",
                                        width=230, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_birthdate.place(relx=0.310, rely=0.710, anchor="center")

        self.entry_move_in = CTkEntry(parent, textvariable=self.move_in_var, placeholder_text="Enter move in date",
                                      width=200, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_move_in.place(relx=0.840, rely=0.425, anchor="center")

        self.entry_lease_start = CTkEntry(parent, textvariable=self.lease_start_var,
                                          placeholder_text="Enter lease start date",
                                          width=200, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_lease_start.place(relx=0.840, rely=0.482, anchor="center")

        self.entry_lease_end = CTkEntry(parent, textvariable=self.lease_end_var,
                                        placeholder_text="Enter lease end date",
                                        width=200, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_lease_end.place(relx=0.840, rely=0.539, anchor="center")

        self.entry_last_payment = CTkEntry(parent, textvariable=self.last_payment_var,
                                           placeholder_text="Enter last payment date",
                                           width=200, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_last_payment.place(relx=0.840, rely=0.596, anchor="center")

        self.entry_emergency_contact_number = CTkEntry(parent, textvariable=self.emergency_contact_number_var,
                                                       placeholder_text="Enter emergency contact number",
                                                       width=250, height=25, border_color="#937A69",
                                                       font=('Century Gothic', 12))
        self.entry_emergency_contact_number.place(relx=0.420, rely=0.800, anchor="center")

        self.entry_emergency_contact_name = CTkEntry(parent, textvariable=self.emergency_contact_name_var,
                                                     placeholder_text="Enter emergency contact name",
                                                     width=250, height=25, border_color="#937A69",
                                                     font=('Century Gothic', 12))
        self.entry_emergency_contact_name.place(relx=0.420, rely=0.857, anchor="center")

        self.entry_relationship = CTkEntry(parent, textvariable=self.relationship_var,
                                           placeholder_text="Enter relationship",
                                           width=250, height=25, border_color="#937A69", font=('Century Gothic', 12))
        self.entry_relationship.place(relx=0.420, rely=0.914, anchor="center")

        # Buttons
        button_style = {
            "fg_color": "#CFB9A3",
            "hover_color": "#D6BC9D",
            "text_color": "#5C483F",
            "bg_color": "#f1f1f1",
            "font": ('Century Gothic', 20, "bold")
        }

        save_button = ctk.CTkButton(parent, text="Save", command=self.edit_tenant_info, **button_style)
        save_button.place(relx=0.85, rely=0.90, anchor='center')

    def populate_tenant_info(self):
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return

        try:
            print(f"Populating info for tenant_id: {self.tenant_id}")
            tenant_info = draft_backend.fetch_new_tenant_info(conn, self.tenant_id)
            if tenant_info:
                print(f"Fetched tenant info: {tenant_info}")
                self.tenant_name_var.set(tenant_info[0])
                self.contactnum_var.set(tenant_info[1])
                self.email_var.set(tenant_info[2])
                self.unit_number_var.set(tenant_info[3])
                self.sex_var.set(tenant_info[4])
                self.birthdate_var.set(tenant_info[5])
                self.move_in_var.set(tenant_info[6])
                self.lease_start_var.set(tenant_info[7])
                self.lease_end_var.set(tenant_info[8])
                self.last_payment_var.set(tenant_info[9])
                self.emergency_contact_name_var.set(tenant_info[10])
                self.emergency_contact_number_var.set(tenant_info[11])
                self.relationship_var.set(tenant_info[12])

                # Disable entry fields after populating them
                self.disable_fields()

            else:
                CTkMessagebox(title="Error", message="Tenant not found.")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def disable_fields(self):
        # Disable entry fields after populating them
        self.entry_tenant_name.configure(state="disabled")
        self.entry_contactnum.configure(state="disabled")
        self.entry_email.configure(state="disabled")
        self.entry_unit_number.configure(state="disabled")
        self.entry_sex.configure(state="disabled")
        self.entry_birthdate.configure(state="disabled")
        self.entry_move_in.configure(state="disabled")
        self.entry_lease_start.configure(state="disabled")
        self.entry_lease_end.configure(state="disabled")
        self.entry_last_payment.configure(state="disabled")
        self.entry_emergency_contact_number.configure(state="disabled")
        self.entry_emergency_contact_name.configure(state="disabled")
        self.entry_relationship.configure(state="disabled")


    def edit_tenant_info(self):
        # Close the Add Building window if it exists
        if self.add_building_window:
            self.add_building_window.destroy()

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
        DisplayBuildingInformation(self.display_building_info_window)


def main():
    root = tk.Tk()
    root.geometry("950x600")
    app = DisplayTenantComponent(root)
    root.mainloop()


if __name__ == "__main__":
    main()
