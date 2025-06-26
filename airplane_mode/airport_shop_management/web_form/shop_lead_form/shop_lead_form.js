frappe.ready(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const shopName = urlParams.get('shop');
	const rentAmount = urlParams.get('rent_amount')

    if (shopName) {
        frappe.web_form.set_value('shop', shopName);
    }
	  if (rentAmount) {
        frappe.web_form.set_value('rent_amount', rentAmount);
    }
});