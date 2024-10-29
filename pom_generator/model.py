from playwright.sync_api import sync_playwright


class SelectorModel:
    def fetch_selectors(self, priorities, selector_function):
        selectors_by_priority = {
            "ID": set(),
            "Name": set(),
            "ClassName": set(),
            "LinkText": set(),
            "PartialLinkText": set(),
            "TagName": set(),
        }

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp("http://localhost:9214")
            page = browser.contexts[0].pages[0]
            page.wait_for_load_state("load")

            elements = page.query_selector_all("*")
            for element in elements:
                selector = selector_function(element)
                if selector:
                    if "id=" in selector:
                        selectors_by_priority["ID"].add(selector)
                    elif "name=" in selector:
                        selectors_by_priority["Name"].add(selector)
                    elif "contains(@class," in selector:
                        selectors_by_priority["ClassName"].add(selector)
                    elif "text()=" in selector:
                        selectors_by_priority["LinkText"].add(selector)
                    elif "contains(text()," in selector:
                        selectors_by_priority["PartialLinkText"].add(selector)
                    elif selector.startswith("//"):
                        selectors_by_priority["TagName"].add(selector)

            browser.close()
        return selectors_by_priority

    def generate_pom(self, class_name, selectors):
        """Generates the POM structure for the class name and given selectors."""
        # Handle case where class_name is empty or invalid
        class_name = class_name.strip() or "Test"

        # Build each element's name, type, and locator based on selector type
        elements = []
        for selector in selectors:
            name = self.extract_name(selector)
            elements.append({
                'name': name,
                'type': 'xpath',
                'locator': selector
            })

        # Generate the POM class structure
        pom_code = f"""import logging
import time
import utilities.custom_logger as cl
from base.selenium_driver import Selenium_Driver

class {class_name.capitalize()}Page(Selenium_Driver):

    log = cl.customLogger(logging.DEBUG)

    \"\"\"Page Object for {class_name}\"\"\"

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
"""
        for element in elements:
            locator_name = f"__{element['name']}"
            pom_code += f"    {locator_name} = \"{element['locator']}\"\n"

        pom_code += "\n    # Functions\n"

        for element in elements:
            function_name = element['name']
            pom_code += f"\n    def {function_name}(self):\n"
            pom_code += f"        self.element(self.__{function_name}, locatorType='xpath')\n"

        return pom_code

    @staticmethod
    def extract_name(selector):
        """Extracts a meaningful name from the selector for use as a variable or function name."""
        if "@id='" in selector:
            return selector.split("@id='")[1].split("']")[0]
        elif "@name='" in selector:
            return selector.split("@name='")[1].split("']")[0]
        elif "contains(@class," in selector:
            return "_".join(cls.split("')")[0] for cls in selector.split("contains(@class, '")[1:])
        elif "text()=" in selector:
            return selector.split("text()='")[1].split("']")[0]
        elif "contains(text()," in selector:
            return selector.split("contains(text(), '")[1].split("')")[0]
        else:
            return "custom_selector"

