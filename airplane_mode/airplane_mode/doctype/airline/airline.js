frappe.ui.form.on("Airline", {
    // Standard Events
    refresh(frm) {
        if (frm.doc.website) {
            frm.add_web_link(frm.doc.website, 'Visit Website');
        }
    }
});