# Copyright (c) 2025, sourav and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum


def execute(filters=None):
    airline = DocType("Airline")
    airplane = DocType("Airplane")
    airplane_flight = DocType("Airplane Flight")
    airplane_ticket = DocType("Airplane Ticket")

    query = (
        frappe.qb
        .from_(airline)
        .left_join(airplane).on(airplane.airline == airline.name)
        .left_join(airplane_flight).on(airplane_flight.airplane == airplane.name)
        .left_join(airplane_ticket).on(airplane_ticket.flight == airplane_flight.name)
        .groupby(airline.name)
        .select(
            airline.name.as_('airline'),
            Sum(airplane_ticket.total_amount).as_('revenue')
        )
    )

    result = query.run()

    data = []
    total = 0
    for row in result:
        airline_name, revenue = row
        revenue = revenue or 0
        total += revenue
        data.append([airline_name, revenue])

    columns = [
        {
            "label": "Airline",
            "fieldname": "airline",
            "fieldtype": "Link",
            "options": "Airline",
            "width": "120px"
        },
        {
            "label": "Revenue",
            "fieldname": "revenue",
            "fieldtype": "Currency",
            "width": "120px"
        },
    ]

    chart = {
        "data": {
            "labels": [row[0] for row in data],
            "datasets": [{"values": [row[1] for row in data]}]
        },
        "type": "donut"
    }

    summary = [{"label": "Total Revenue",
                "value": total, "indicator": "green"}]

    return columns, data, None, chart, summary
