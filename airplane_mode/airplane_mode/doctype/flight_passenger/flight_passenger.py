# Copyright (c) 2025, administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class FlightPassenger(Document):
    def before_save(self):
        self.set_full_name()

    def set_full_name(self):
        """Set the passenger full name"""
        self.full_name = " ".join(
            filter(lambda x: x, [self.first_name, self.last_name])
        )
