# Copyright (c) 2025, administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class Tenant(Document):
    def autoname(self):
        self.full_name = self.name = " ".join(
            filter(lambda x: x, [self.first_name, self.last_name])
        )
        self.name = self.full_name
