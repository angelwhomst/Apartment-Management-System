import tkinter as tk
import customtkinter as ctk


class AdminToolComponent:
    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self, parent):
        # Importing inside the method to avoid circular import
        from PIL import Image
        from add_building import AddBuildingComponent
        from add_unit import AddUnitComponent

        # Add background image
        admin_bg_image = Image.open("images/bgAdmintools.png")
        admin_bg = ctk.CTkImage(admin_bg_image, size=(900, 600))
        admin_bg_lbl = ctk.CTkLabel(parent, text="", image=admin_bg)
        admin_bg_lbl.place(x=0, y=0)

        # Create three buttons with "Add" text and specified styles
        button_style = {
            "fg_color": "#CFB9A3",
            "hover_color": "#D6BC9D",
            "text_color": "#5c483f",
            "bg_color": "#f1f1f1",
            "font": ('Century Gothic', 20, "bold")
        }

        button1 = ctk.CTkButton(parent, text="Add", width=175, command=self.open_add_building, **button_style)
        button2 = ctk.CTkButton(parent, text="Add", width=175, command=self.open_add_unit, **button_style)
        button3 = ctk.CTkButton(parent, text="Add", width=175, command=self.open_add_tenant, **button_style)
        button4 = ctk.CTkButton(parent, text="Add", width=175, command=self.open_add_expense, **button_style)

        # Place the buttons on the same line with closer margins
        button1.place(relx=0.16, rely=0.74, anchor='center')
        button2.place(relx=0.386, rely=0.74, anchor='center')
        button3.place(relx=0.613, rely=0.74, anchor='center')
        button4.place(relx=0.84, rely=0.74, anchor='center')

    def open_admin_tool(self):
        # Create a CTkToplevel window
        self.top_level_window = ctk.CTkToplevel(self.parent)
        self.top_level_window.title("Admin Tool")
        self.top_level_window.geometry("950x600")
        self.top_level_window.attributes('-topmost', True)  # Keep the window on top

        # Disable window resizing
        self.top_level_window.resizable(False, False)

        # Center the window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        self.top_level_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Create widgets in the top-level window
        self.create_widgets(self.top_level_window)

    def open_add_building(self):
        # Importing inside the method to avoid circular import
        from PIL import Image
        from add_building import AddBuildingComponent

        # Create a new CTkToplevel window for the Add Building component
        add_building_window = ctk.CTkToplevel(self.parent)
        add_building_window.title("Add Building")
        add_building_window.geometry("800x600")

        # Disable window resizing
        add_building_window.resizable(False, False)

        # Center the new window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        add_building_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Close the admin tool window
        self.top_level_window.destroy()

        # Create an instance of AddBuildingComponent and pass the new window as its parent
        AddBuildingComponent(add_building_window)

    def open_add_unit(self):
        # Importing inside the method to avoid circular import
        from PIL import Image
        from add_unit import AddUnitComponent

        # Create a new CTkToplevel window for the Add Unit component
        add_unit_window = ctk.CTkToplevel(self.parent)
        add_unit_window.title("Add Unit")
        add_unit_window.geometry("900x600")

        # Disable window resizing
        add_unit_window.resizable(False, False)

        # Center the new window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        add_unit_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Ensure the new window is always on top
        add_unit_window.attributes('-topmost', True)

        # Close the admin tool window
        self.top_level_window.destroy()

        # Create an instance of AddUnitComponent and pass the new window as its parent
        AddUnitComponent(add_unit_window)

    def open_add_tenant(self):
        # Importing inside the method to avoid circular import
        from PIL import Image
        from add_tenant import AddTenantComponent

        # Create a new CTkToplevel window for the Add Unit component
        add_tenant_window = ctk.CTkToplevel(self.parent)
        add_tenant_window.title("Add Tenant")
        add_tenant_window.geometry("900x600")

        # Disable window resizing
        add_tenant_window.resizable(False, False)

        # Center the new window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        add_tenant_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Ensure the new window is always on top
        add_tenant_window.attributes('-topmost', True)

        # Close the admin tool window
        self.top_level_window.destroy()

        # Create an instance of AddUnitComponent and pass the new window as its parent
        AddTenantComponent(add_tenant_window)

    def open_add_expense(self):
        # Importing inside the method to avoid circular import
        from PIL import Image
        from add_expense import AddExpenseComponent

        # Create a new CTkToplevel window for the Add Unit component
        add_tenant_window = ctk.CTkToplevel(self.parent)
        add_tenant_window.title("Add Expense")
        add_tenant_window.geometry("900x600")

        # Disable window resizing
        add_tenant_window.resizable(False, False)

        # Center the new window on the screen
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        window_width = 900
        window_height = 600

        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)

        add_tenant_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

        # Ensure the new window is always on top
        add_tenant_window.attributes('-topmost', True)

        # Close the admin tool window
        self.top_level_window.destroy()

        # Create an instance of AddUnitComponent and pass the new window as its parent
        AddExpenseComponent(add_tenant_window)


#
# Entry point for running the AdminToolComponent directly
if __name__ == "__main__":
    root = tk.Tk()
    admin_tool = AdminToolComponent(root)
    admin_tool.open_admin_tool()
    root.mainloop()
