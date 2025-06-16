# Copyright (c) 2025, administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import random
from frappe.utils import flt


class AirplaneTicket(Document):
    def before_insert(self):
        self.allocate_seat()
        self.validate_flight_capacity()

    def allocate_seat(self):
        if not self.seat:
            random_number = random.randint(1, 99)
            random_letter = random.choice(
                ['A', 'B', 'C', 'D', 'E'])
            self.seat = f"{random_number}{random_letter}"

    def validate(self):
        self.remove_duplicate_entries_add_ons()

    def before_save(self):
        self.calculate_total_amount()

    def before_submit(self):
        self.validate_status()

    def remove_duplicate_entries_add_ons(self):
        unique_items = set()
        add_ons_list = []

        for row in self.add_ons:
            if row.item not in unique_items:
                unique_items.add(row.item)
                add_ons_list.append(row)

            self.add_ons = add_ons_list

    def calculate_total_amount(self):
        self.total_amount = flt(self.flight_price) + \
            sum(row.amount for row in self.add_ons)

    def validate_status(self):
        if self.status != "Boarded":
            frappe.throw(
                _("The ticket can only be submitted when the status is 'Boarded'."))

    def validate_flight_capacity(self):
        airplane = frappe.get_value("Airplane Flight", self.flight, 'airplane')
        airplane_capacity = frappe.get_value("Airplane", airplane, 'capacity')
        ticket_count = frappe.db.count(
            "Airplane Ticket", filters={"flight": self.flight})

        if ticket_count >= airplane_capacity:
            frappe.throw(
                _("Cannot create ticket. The airplane flight has reached its full capacity of {airplane_capacity} passengers."))
