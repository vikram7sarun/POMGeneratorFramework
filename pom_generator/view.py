import tkinter as tk
from tkinter import scrolledtext, messagebox, END, filedialog


class POMView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Enhanced POM Generator")
        self.set_colors()
        self.create_widgets()
        self.configure_grid()
        self.configure_tags()  # Configure the highlight tag

    def set_colors(self):
        self.bg_color = "#f5f5f5"
        self.button_bg = "#dbe9f4"
        self.entry_bg = "#f0f8ff"
        self.text_bg = "#e8eff5"
        self.text_color = "#333333"
        self.highlight_color = "#d4edda"  # Light green for highlighting moved text
        self.placeholder_color = "grey"  # Color for placeholder text
        self.normal_text_color = "black"  # Standard color for entered text
        self.root.configure(bg=self.bg_color)

    def create_widgets(self):
        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w",
                                   bg=self.bg_color)
        self.status_bar.grid(row=6, column=0, columnspan=4, sticky="ew")

        # Priorities Entry
        self.label = tk.Label(self.root, text="Enter Selector Priorities:", bg=self.bg_color, fg=self.text_color)
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.entry = tk.Entry(self.root, bg=self.entry_bg, fg=self.text_color, relief="solid")
        self.entry.insert(0, "ID, Name, ClassName, LinkText, PartialLinkText, TagName")
        self.entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))

        # Fetch Button
        self.fetch_button = tk.Button(self.root, text="Fetch Selectors", command=self.controller.fetch_selectors,
                                      bg=self.button_bg, relief="groove")
        self.fetch_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Output Text Area
        self.output_text = scrolledtext.ScrolledText(self.root, bg=self.text_bg, fg=self.text_color, relief="solid")
        self.output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # Move Button
        self.move_button = tk.Button(self.root, text="Move Selected Lines", command=self.controller.move_selected_lines,
                                     bg=self.button_bg, relief="groove")
        self.move_button.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Class Name Entry with Placeholder
        self.class_name_entry = tk.Entry(self.root, fg=self.placeholder_color, bg=self.entry_bg, relief="solid")
        self.class_name_entry.insert(0, "Enter Class Name")
        self.class_name_entry.bind("<FocusIn>", self.on_class_name_focus_in)
        self.class_name_entry.bind("<FocusOut>", self.on_class_name_focus_out)
        self.class_name_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Generate POM Button
        self.generate_button = tk.Button(self.root, text="Generate POM", command=self.controller.generate_pom,
                                         bg=self.button_bg, relief="groove")
        self.generate_button.grid(row=3, column=2, sticky="ew", padx=10, pady=5)

        # Moved Text Area
        self.moved_text = scrolledtext.ScrolledText(self.root, bg=self.text_bg, fg=self.text_color, relief="solid")
        self.moved_text.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # Save Button
        self.save_button = tk.Button(self.root, text="Save to File", command=self.controller.save_to_file,
                                     bg=self.button_bg, relief="groove")
        self.save_button.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Text Area 1 (output_text)
        self.output_text = scrolledtext.ScrolledText(self.root, bg=self.text_bg, fg=self.text_color, relief="solid")
        self.output_text.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        # Move Button
        self.move_button = tk.Button(self.root, text="Move Selected Lines", command=self.controller.move_selected_lines,
                                     bg=self.button_bg, relief="groove")
        self.move_button.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        # Text Area 2 (moved_text) for moved text
        self.moved_text = scrolledtext.ScrolledText(self.root, bg=self.text_bg, fg=self.text_color, relief="solid")
        self.moved_text.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")


    def configure_grid(self):
        """Configure grid weights to ensure responsive layout."""
        for i in range(3):
            self.root.columnconfigure(i, weight=1)
        for i in range(7):
            self.root.rowconfigure(i, weight=1)

    def on_class_name_focus_in(self, event):
        """Clears placeholder text when the entry gains focus."""
        if self.class_name_entry.get() == "Enter Class Name":
            self.class_name_entry.delete(0, "end")
            self.class_name_entry.config(fg=self.normal_text_color)

    def on_class_name_focus_out(self, event):
        """Restores placeholder text if the entry is empty when it loses focus."""
        if self.class_name_entry.get() == "":
            self.class_name_entry.insert(0, "Enter Class Name")
            self.class_name_entry.config(fg=self.placeholder_color)

    def show_tooltip(self, message):
        tooltip = tk.Toplevel(self.root)
        tooltip.wm_overrideredirect(True)
        tooltip.geometry(f"+{self.root.winfo_pointerx()}+{self.root.winfo_pointery()}")
        label = tk.Label(tooltip, text=message, background="yellow", relief="solid", borderwidth=1, padx=2, pady=2)
        label.pack()
        self.root.after(2000, tooltip.destroy)

    def update_status(self, message):
        self.status_var.set(message)

    def show_error_popup(self, message):
        messagebox.showerror("Error", message)

    def show_save_dialog(self, code):
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(code)
            messagebox.showinfo("Saved", f"POM saved as {file_path}")

    def get_priorities(self):
        return [p.strip() for p in self.entry.get().split(",")]

    def display_selectors(self, selectors):
        self.output_text.delete(1.0, END)
        for priority, sel_list in selectors.items():
            self.output_text.insert(END, f"\n{priority} Selectors:\n")
            for selector in sel_list:
                self.output_text.insert(END, f"{selector}\n")

    def get_selected_text(self):
        try:
            return self.output_text.get("sel.first", "sel.last")
        except tk.TclError:
            self.show_error_popup("No text selected to move.")
            return None

    def move_text(self, text):
        self.moved_text.insert(END, text + "\n")

    def get_class_name(self):
        """Returns the entered class name or a default if the placeholder is still present."""
        class_name = self.class_name_entry.get()
        return class_name if class_name != "Enter Class Name" else "Test"

    def display_pom_code(self, code):
        self.moved_text.delete(1.0, END)
        self.moved_text.insert(END, code)

    def get_moved_text(self):
        return self.moved_text.get(1.0, END)

    def is_pom_code_present_in_text_area_2(self):
        """Check if Text Area 2 (moved_text) contains generated POM code."""
        text_content = self.moved_text.get("1.0", END)
        return "# Locators" in text_content and "# Functions" in text_content

    def clear_text_area_2(self):
        """Clear the content of Text Area 2 (moved_text)."""
        self.moved_text.delete("1.0", END)

    def show_move_lines_alert(self):
        """Show an alert prompting the user to use 'Move Selected Lines' again."""
        messagebox.showinfo("Generate POM", "Move the Selectors to generate the POM again.")

    def configure_tags(self):
        """Configure text tags for highlighting moved selectors."""
        self.output_text.tag_configure("green_highlight", background=self.highlight_color)

    def move_text(self, text):
        """Move the selected text to Text Area 2 and highlight it in green in Text Area 1."""
        # Insert the selected text into Text Area 2
        self.moved_text.insert(END, text + "\n")

        # Highlight the selected text in Text Area 1
        try:
            # Get the indices of the selected text in Text Area 1
            start_index = self.output_text.index("sel.first")
            end_index = self.output_text.index("sel.last")

            # Apply the green highlight tag to the selected text in Text Area 1
            self.output_text.tag_add("green_highlight", start_index, end_index)

        except tk.TclError:
            # If no text is selected, ignore
            messagebox.showinfo("No Selection", "Please select text to move.")