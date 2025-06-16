frappe.ui.form.on("Airplane Ticket", {
    refresh(frm) {
            if(frm.doc.docstatus==0){
                frm.add_custom_button('Assign Seat', () => {
                    const d = new frappe.ui.Dialog({
                        title: 'Assign Seat',
                        fields: [
                            {
                                label: 'Seat Number',
                                fieldname: 'seat',
                                fieldtype: 'Data',
                                reqd: 1
                            }
                        ],
                        primary_action_label: 'Assign',
                        primary_action(values) {
                            frm.set_value('seat', values.seat);
                            frm.save()
                            d.hide();
                        }
                    });
                    d.show();
                }, 'Actions'); 
            }
        
    }
});