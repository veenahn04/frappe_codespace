import frappe
import random


def execute():
    def generate_random_seat():
        seat_number = random.randint(1, 100)
        seat_letter = random.choice(["A", "B", "C", "D", "E"])
        return f"{seat_number}{seat_letter}"

    tickets = frappe.get_all(
        "Airplane Ticket", filters={"seat": ["is", "not set"]}, fields=["name"]
    )
    updates = {ticket.name: {"seat": generate_random_seat()}
               for ticket in tickets}

    if updates:
        frappe.db.bulk_update("Airplane Ticket", updates)
