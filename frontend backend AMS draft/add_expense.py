from CTkMessagebox import CTkMessagebox
from PIL import Image
import tkinter as tk
from tkinter import ttk, END
import customtkinter as ctk
from add_unit import AddUnitComponent
from tkcalendar import DateEntry  # Assuming you have tkcalendar installed for DateEntry
from tkinter import StringVar
import draft_backend


# mapping from combobox values to database int values for expense_type
expense_type_mapping = {
    'Utilities': 1,
    'Maintenance and Repairs': 2,
    'Advertising': 3,
    'Insurance': 4,
    'Administrative Costs': 5,
    'Property Management Costs': 6
}

class AddExpenseComponent:
    def __init__(self, parent):
        self.parent = parent
        self.add_building_window = None  # Initialize top-level window attribute for Add Building
        self.add_unit_window = None  # Initialize top-level window attribute for Add Unit
        self.create_widgets(parent)

    def create_widgets(self, parent):
        # Add background image
        building_bg_image = Image.open("images/bgAddExpense.png")
        building_bg = ctk.CTkImage(building_bg_image, size=(900, 600))
        building_bg_lbl = ctk.CTkLabel(parent, text="", image=building_bg)
        building_bg_lbl.place(x=0, y=0)

        # Date Entry field using tkcalendar DateEntry
        self.entry_expense_date = DateEntry(parent, width=26, background='#937A69', foreground='white', borderwidth=2,
                                            font=('Century Gothic', 15))
        self.entry_expense_date.place(relx=0.395, rely=0.535, anchor="center")

        # Expense Amount Entry
        self.entry_expense_amount = ctk.CTkEntry(parent, placeholder_text="Enter expense amount", width=250, height=25,
                                                 border_color="#937A69", font=('Century Gothic', 15))
        self.entry_expense_amount.place(relx=0.395, rely=0.605, anchor="center")

        # Expense Type ComboBox
        expense_types = ['Utilities', 'Maintenance and Repairs', 'Advertising', 'Insurance' 'Administrative Costs',
                         'Property Management Costs']
        self.expense_type_var = StringVar(parent)
        self.expense_type_var.set(expense_types[0])  # Default selection
        self.entry_expense_type = ctk.CTkComboBox(parent, values=expense_types, width=250, height=25, border_color="#937A69",
                                                  font=('Century Gothic', 15))
        # self.entry_expense_type['values'] = expense_types
        self.entry_expense_type.place(relx=0.395, rely=0.675, anchor="center")

        # Description Entry as CTkEntry
        self.entry_description = ctk.CTkEntry(parent, placeholder_text="Enter description", width= 250, height=25,
                                              border_color="#937A69", font=('Century Gothic', 15))
        self.entry_description.place(relx=0.395, rely=0.745, anchor="center")

        # Buttons
        button_style = {
            "fg_color": "#CFB9A3",
            "hover_color": "#D6BC9D",
            "text_color": "#5C483F",
            "bg_color": "#f1f1f1",
            "font": ('Century Gothic', 20, "bold")
        }

        save_button = ctk.CTkButton(parent, text="Save", command=self.save_expense, **button_style)

        # Place the buttons
        save_button.place(relx=0.85, rely=0.90, anchor='center')

    def save_expense(self):
        # Collect data from the entry fields
        expense_date = self.entry_expense_date.get_date()
        expense_amount = self.entry_expense_amount.get()
        expense_type = self.entry_expense_type.get()
        description = self.entry_description.get()

        # map the selected expense type to its integer value
        expense_type_int = expense_type_mapping.get(expense_type)

        # proceed to save data to the database
        conn = draft_backend.get_db_connection()
        if not conn:
            CTkMessagebox(title="Error", message="Error connecting to database.")
            return
        try:
            draft_backend.insert_expense(conn, expense_date, expense_amount, expense_type_int, description)
            CTkMessagebox(title="Success", message="Expense information saved successfully!")
            self.clear_entry_fields()
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def clear_entry_fields(self):
        self.entry_expense_date.delete(0, END)
        self.entry_expense_amount.delete(0, END)
        self.entry_description.delete(0, END)

    def save_building_info(self):
        # Close the Add Building window if it exists
        if self.add_building_window:
            self.add_building_window.destroy()

        # Create a new CTkToplevel window for displaying building information
        self.display_add_expense_window = ctk.CTkToplevel(self.parent)
        self.display_add_expense_window.title("Display Building Information")
        self.display_add_expense_window.geometry("900x600")

        # Ensure the new window is always on top
        self.display_add_expense_window.attributes('-topmost', True)

        self.display_add_expense_window.resizable(False, False)

        # Center the new window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        self.display_add_expense_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Import DisplayBuildingInformation class here to avoid circular import
        from display_building_info import DisplayBuildingInformation
        # Create an instance of DisplayBuildingInformation and pass the new window as its parent
        DisplayBuildingInformation(self.display_building_info_window)

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
#     app = AddExpenseComponent(root)
#     root.mainloop()
#
# if __name__ == "__main__":
#     main()
