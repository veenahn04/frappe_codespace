# Copyright (c) 2025, administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class FlightPassenger(Document):
	def before_save(self):
		self.set_full_name()
	
	def validate(self):
		self.check_duplicate_add_ons()

	def set_full_name(self):
		"""Set the passenger full name"""
		self.full_name = " ".join(
			filter(lambda x: x, [self.first_name, self.last_name])
		)

	def check_duplicate_add_ons(self):
		seen = set()
		for row in self.add_ons:
			if row.add_on_type in seen:
				frappe.throw(
					_("Duplicate add-on type '{0}' is not allowed. Each add-on must be unique.").format(
						row.add_on_type),
					frappe.ValidationError
				)
			seen.add(row.add_on_type)
