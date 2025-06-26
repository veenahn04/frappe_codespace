# Copyright (c) 2025, administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import calendar
from datetime import date, datetime


class ShopRentPayment(Document):
    def validate(self):
        self.get_last_day_of_month()
        self.set_status()


    def get_last_day_of_month(self):
        month = datetime.strptime(self.month, "%b").month
        year = int(self.year)
        last_day = calendar.monthrange(year, month)[1]
        self.due_date = date(year, month, last_day)

    def on_submit(self):
        self.set_status()

    def set_status(self):
        today = date.today()
        if not self.shop_contract:
              return
        rent_amount = frappe.db.get_value(
			"Shop Contract", self.shop_contract, "rent_amount") or 0
        if self.amount_paid >= rent_amount:
               self.status = "Paid"
        elif self.amount_paid < rent_amount and self.amount_paid>0 and self.due_date >= today :
            self.status = "Partially Paid"
        elif self.due_date <= today and self.amount_paid != rent_amount:
            self.status = "Overdue"
        else:
            self.status = "Pending"
