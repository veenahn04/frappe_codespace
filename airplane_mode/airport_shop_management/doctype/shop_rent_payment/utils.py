import frappe


@frappe.whitelist()
def send_rent_due_reminders():
    settings = frappe.get_single("Shop Settings")
    
    if not settings.enabledisable_rent_reminders:
        return
    
    contracts = frappe.get_all(
        "Shop Contract", 
        filters={"status": "Active"}, 
        fields=["name", "tenant", "shop"]
    )

    for contract in contracts:
        tenant_email = frappe.db.get_value("Tenant", contract.tenant, "email")
        shop_name = frappe.db.get_value("Airport Shop", contract.shop, "shop_name")

        if tenant_email:
            frappe.sendmail(
                recipients=[tenant_email],
                subject=f"Monthly Rent Reminder for {shop_name}",
                message=f"""
                    <p>Dear {contract.tenant},</p>
                    <p>This is a friendly reminder that your monthly rent for the shop <b>{shop_name}</b> is due by the <b>5th of this month</b>.</p>
                    <p>Please ensure the payment is made on time to avoid any penalties.</p>
                    <p>Thank you for your cooperation.</p>
                """
            )

def update_payment_statuses():
    today = frappe.utils.nowdate()
    payments = frappe.get_all("Shop Rent Payment", filters={"status": "Pending", "due_date": ["<", today]})
    for p in payments:
        frappe.db.set_value("SHop Rent Payment", p.name, "status", "Overdue")