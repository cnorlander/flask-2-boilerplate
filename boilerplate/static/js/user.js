function submitUserForm() {
    if (document.forms["create-user-form"].reportValidity()) {
        if (document.getElementById("passed-validity").value === "true") {
            document.forms["create-user-form"].submit();
        }
    }
}

function submitUserUpdate() {
    if (document.forms["update-user-form"].reportValidity()) {
        const passwordElement = document.getElementById("password");
        const passwordConfirmElement = document.getElementById("confirm-password");
        let isPasswordFieldEmpty = true;
        let isPasswordConfirmFieldEmpty = true;
        if ( passwordConfirmElement !== null && passwordConfirmElement.value > 0 ) {
            isPasswordConfirmFieldEmpty = false;
        }
        if ( passwordElement !== null && passwordElement.value > 0 ) {
            isPasswordFieldEmpty = false;
        }

        if ((document.getElementById("passed-validity").value === "true") || (isPasswordFieldEmpty && isPasswordConfirmFieldEmpty)){
            document.forms["update-user-form"].submit();
        }
    }
}