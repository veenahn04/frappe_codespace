# Copyright (c) 2025, administrator and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.naming import make_autoname
from frappe.utils import get_datetime


class AirplaneFlight(WebsiteGenerator):
    def autoname(self):
        month_year = get_datetime(self.date).strftime("%m-%Y")
        prefix = f"{self.airplane}-{month_year}-"
        self.name = make_autoname(prefix + ".#####")

    def on_submit(self):
        if self.docstatus == 1:
            self.status = "Completed"
