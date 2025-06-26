# Copyright (c) 2025, administrator and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.naming import make_autoname
from frappe.utils import get_datetime


class AirplaneFlight(WebsiteGenerator):
    def autoname(self):
        month_year = get_datetime(self.date_of_departure).strftime("%m-%Y")
        prefix = f"{self.airplane}-{month_year}-"
        self.name = make_autoname(prefix + ".#####")

    def on_submit(self):
        self.status = "Completed"

    def validate(self):
        self.check_crew_conflicts()

    # validate Utils
    def check_crew_conflicts(self):
        # to check crew member already active or not by date of departure date
        if not self.date_of_departure or not self.airplane_crew_member:
            return

        assigned_crew = [
            row.crew_member for row in self.airplane_crew_member if row.crew_member]
        if not assigned_crew:
            return

        other_flights = frappe.get_all(
            "Airplane Flight",
            filters={
                "date_of_departure": self.date_of_departure,
                "name": ["!=", self.name]
            },
            pluck="name"
        )

        if not other_flights:
            return

        conflicting_assignments = frappe.get_all(
            "Crew Member Assignment",
            filters={
                "parent": ["in", other_flights],
                "crew_member": ["in", assigned_crew]
            },
            fields=["crew_member", "parent"]
        )

        if conflicting_assignments:
            conflict_details = "\n".join(
                f"- {row.crew_member} (already in flight: {row.parent})" for row in conflicting_assignments
            )
            frappe.throw(
                f"The following crew members are already assigned to another flight on {self.date_of_departure}:\n{conflict_details}"
            )

    def on_update(self):
        if self.has_value_changed("gate_number"):
            frappe.enqueue(
                "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_in_tickets",
                doc=self,
                queue='short',  # or 'default' or 'long'
                now=False,
                timeout=300
            )

    def before_update_after_submit(self):
        if self.has_value_changed("gate_number"):
            frappe.enqueue(
                "airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_gate_number_in_tickets",
                doc=self,
                queue='short',  # or 'default' or 'long'
                now=False,
                timeout=300
            )

# on_update utils


def update_gate_number_in_tickets(doc):
    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={"flight": doc.name},
        fields=["name"]
    )

    for ticket in tickets:
        frappe.db.set_value('Airplane Ticket', ticket.name,
                            'gate_number', doc.gate_number)
