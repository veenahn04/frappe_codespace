// Copyright (c) 2025, administrator and contributors
// For license information, please see license.txt

frappe.ui.form.on("Shop Rent Payment", {
	refresh(frm) {
        frappe.db.get_single_value('Airport Shop Settings', 'enable_rent_reminders')
            .then(value => {
                if (value === 1) {
                    frm.add_custom_button(__('Send Rent Reminders'), function() {
                        frappe.call({
                            method: "airplane_mode.airport_shop_management.doctype.shop_rent_payment.utils.send_rent_due_reminders",
                            callback: function(r) {
                                if (!r.exc) {
                                    frappe.msgprint(__('Rent reminders sent successfully.'));
                                } else {
                                    frappe.msgprint(__('Error sending reminders.'));
                                }
                            }
                        });
                    });
                }
            });
	},
});
