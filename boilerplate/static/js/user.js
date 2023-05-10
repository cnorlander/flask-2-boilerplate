function submitUserForm() {
    if (document.forms["create-user-form"].reportValidity()) {
        if (document.getElementById("passed-validity").value === "true") {
            document.forms["create-user-form"].submit();
        }
    }
}