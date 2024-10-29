from pom_generator.view import POMView
from pom_generator.model import SelectorModel
from pom_generator.utils import get_priority_selector

class POMController:
    def __init__(self):
        self.view = POMView(self)
        self.model = SelectorModel()

    def run(self):
        self.view.root.mainloop()

    def fetch_selectors(self):
        try:
            priorities = self.view.get_priorities()
            if not priorities:
                self.view.show_error_popup("Please specify at least one priority.")
                return
            self.view.update_status("Fetching selectors...")
            selectors = self.model.fetch_selectors(priorities, get_priority_selector)
            self.view.display_selectors(selectors)
            self.view.update_status("Selectors fetched successfully.")
        except Exception as e:
            self.view.show_error_popup(f"Error fetching selectors: {str(e)}")
            self.view.update_status("Fetch failed.")

    def move_selected_lines(self):
        selected_text = self.view.get_selected_text()
        if selected_text:
            self.view.move_text(selected_text)

    def generate_pom(self):
        # Check if Text Area 2 contains generated POM code
        if self.view.is_pom_code_present_in_text_area_2():
            # Clear only if generated POM code is present, then show an alert
            self.view.clear_text_area_2()
            self.view.show_move_lines_alert()
            return

        # Proceed with generating POM if Text Area 2 doesn't contain generated POM code
        class_name = self.view.get_class_name()
        if not class_name:
            self.view.show_error_popup("Class name cannot be empty.")
            return
        selectors = self.view.get_moved_text().strip().splitlines()

        # Generate POM code
        pom_code = self.model.generate_pom(class_name, selectors)
        # pom_code_with_identifier = f"# POM_START\n{pom_code}\n# POM_END"  # Identifier tags

        self.view.display_pom_code(pom_code)

    def save_to_file(self):
        pom_code = self.view.get_moved_text()
        if not pom_code.strip():
            self.view.show_error_popup("No content available to save.")
            return
        self.view.show_save_dialog(pom_code)
