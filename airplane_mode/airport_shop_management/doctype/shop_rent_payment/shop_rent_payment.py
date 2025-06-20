# Copyright (c) 2025, administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopRentPayment(Document):
	def validate(self):
		self.validate_paid_amount()
		self.set_status()

	def validate_paid_amount(self):
		if not self.amount_paid or self.amount_paid <= 0:
			frappe.throw(("Paid Amount must be greater than 0"))

	def set_status(self):
		if not self.shop_contract:
			return

		rent_amount = frappe.db.get_value("Shop Contract", self.shop_contract, "rent_amount") or 0

		if self.amount_paid >= rent_amount:
			self.status = "Paid"
		elif 0 < self.amount_paid < rent_amount:
			self.status = "Partially Paid"
		else:
			self.status = "Unpaid"
