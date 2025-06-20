# Copyright (c) 2025, administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ShopContract(Document):
    def before_save(self):
        self.validate_contract()

    def validate_contract(self):
        if frappe.db.exists('Contract', {'status': 'Active', 'shop': self.shop}):
            frappe.throw(
                f"An active contract already exists for the shop {self.shop}.")

    def validate(self):
        self.validate_contract_dates()

    def on_submit(self):
        self.update_airport_shop_on_submit()

    def on_cancel(self):
        self.reset_airport_shop_on_cancel()

    def validate_contract_dates(self):
        if self.contract_start_date and self.contract_end_date and self.contract_start_date > self.contract_end_date:
            frappe.throw("Start date cannot be after end date.")

    def update_airport_shop_on_submit(self):
        if self.status == "Active" and self.shop:
            frappe.db.set_value("Airport Shop", self.shop, {
                "is_occupied": 1,
                "rent_amount": self.rent_amount,
                "active_contract":self.name,
                "deposit_amount":self.deposit_amount
            })

    def reset_airport_shop_on_cancel(self):
        if self.shop:
            frappe.db.set_value("Airport Shop", self.shop, {
                "is_occupied": 0,
                "current_contract": None,
                "rent_amount": 0,
                "deposit_amount":0
            })
