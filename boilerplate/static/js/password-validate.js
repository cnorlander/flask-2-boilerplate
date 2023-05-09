function validatePassword(passwordMinCharacters, passwordMaxCharacters, passwordRequireNumerals, passwordRequireUpperCase, passwordRequireLowerCase, passwordRequireSpecialCharacters, passwordListOfAllowedSpecialCharacters) {
    let passwordRulesBroken = [];
    let passwordRulesBrokenHTML = ""
    const newPassword = document.getElementById("password").value
    const confirmPassword = document.getElementById("confirm-password").value
    const passwordRequirementsList = document.getElementById("password-requirements")

    if (newPassword.length < passwordMinCharacters) {
        passwordRulesBroken.push(`Password is too short. Passwords should contain at least ${passwordMinCharacters} characters.`);
    }

    if (newPassword.length > passwordMaxCharacters) {
        passwordRulesBroken.push(`Password is too long. Passwords should contain at most ${passwordMaxCharacters} characters.`);
    }

    if (passwordRequireNumerals && (!/\d/.test(newPassword))) {
        passwordRulesBroken.push(`Password must contain at least one number.`);
    }

    if (passwordRequireUpperCase && (!/[A-Z]/.test(newPassword))) {
        passwordRulesBroken.push(`Password must contain at least one upper case letter.`);
    }

    if (passwordRequireLowerCase && (!/[a-z]/.test(newPassword))) {
        passwordRulesBroken.push(`Password must contain at least one lower case letter.`);
    }

    if (passwordRequireSpecialCharacters && (!newPassword.match(new RegExp(`[${passwordListOfAllowedSpecialCharacters}]`)))) {
        passwordRulesBroken.push(`Password must contain at least one special symbol of the following: ${passwordListOfAllowedSpecialCharacters}`);
    }

    if (newPassword !== confirmPassword) {
        passwordRulesBroken.push(`Password does not match the confirmed password.`);
    }

    for (const brokenRequirement of passwordRulesBroken) {
        passwordRulesBrokenHTML = passwordRulesBrokenHTML + `<li class="text-danger">${brokenRequirement}</li>`
    }
    passwordRequirementsList.innerHTML = passwordRulesBrokenHTML;

    if (passwordRulesBroken.length == 0) return true;
    return false
}
