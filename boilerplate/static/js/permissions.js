

function flash(textElement) {
  textElement.classList.add("flashed");
  setTimeout(function() {
      textElement.classList.remove("flashed");
  }, 100);
}

function createBackRequirements(item) {
    const itemID = item.id;
    const requires = item.getAttribute("data-requires");
    if (requires != null) {
        for (const id of requires.replace(/ /g,'').split(",")) {
            requiredElement = document.getElementById(id);
            existingValues = requiredElement.getAttribute("data-required-by");
            if (existingValues == null || existingValues == "") {
                requiredElement.setAttribute("data-required-by", itemID);
            } else {
                requiredElement.setAttribute("data-required-by", existingValues + ", " + itemID);
            }
        }
    }
}


function setChecked(id) {
    checkbox = document.getElementById(id);
    checkbox.checked = true;
}

function checkboxClicked(target, seen) {
    let requiredIDs = [];
    let requiredByIDs = [];
    const requiredByString = target.getAttribute("data-required-by");
    const requiredString = target.getAttribute("data-requires");
    if (requiredString != null && requiredString != "") {
        requiredIDs = requiredString.replace(/ /g,'').split(",");
    }
    if (requiredByString != null && requiredString != "") {
        requiredByIDs = requiredByString.replace(/ /g,'').split(",");
    }

    if (!target.checked && requiredByIDs.length > 0) {
        for (const requiredByElementID of requiredByIDs) {
            if (document.getElementById(requiredByElementID).checked) {
                flash(document.getElementById(requiredByElementID).parentNode.parentNode.parentNode);
                setChecked(target.id);
            }
        }
    }

    for (const requiredElementID of requiredIDs) {
        if (target.checked && !seen.includes(requiredElementID)) {
            setChecked(requiredElementID);
            seen.push(requiredElementID);
            checkboxClicked(document.getElementById(requiredElementID), seen);
        }
    }
}

function createListeners(item, index) {
    item.addEventListener("click", (event) => {
        checkboxClicked(event.target, []);
    });
}

function resetAllCheckboxes(){
  for (const checkbox of checkboxes) {
    checkbox.checked = false;
  }
}

function selectAllCheckboxes(){
  for (const checkbox of checkboxes) {
    checkbox.checked = true;
  }
}

function submitPermissionsForm(){
    const checkboxes = document.querySelectorAll("input[type=checkbox]");
    if (document.forms["permissions-form"].reportValidity()) {
        for (const checkbox of checkboxes){
            if (checkbox.checked){ checkbox.value = "true"; }
            else {checkbox.value = "false"; }
        document.forms["permissions-form"].submit();
        }
    }
}

function clearModal(){
    document.getElementById("create-edit-role-modal-header").innerHTML = "Create New Role";
    document.getElementById("role-id").value = "new";
    const checkboxes = document.querySelectorAll("input[type=checkbox]");
    const textboxes = document.querySelectorAll("input[type=text]");
    for (const checkbox of checkboxes){
        checkbox.checked = false;
    }
    for (const textbox of textboxes){
        textbox.value = "";
    }
}

function editRole(role){
    clearModal();
    document.getElementById("create-edit-role-modal-header").innerHTML = 'Editing Role "' + role.name + '"';
    document.getElementById("role-id").value = role.uuid;
    document.getElementById("role-name").value = role.name;
    document.getElementById("role-description").value = role.description;
    roleHiddenCheckbox = document.getElementById("role-hidden")
    if (roleHiddenCheckbox != null){
        roleHiddenCheckbox.checked = role.hidden
    }
    roleSystemCheckbox = document.getElementById("role-system")
    if (roleSystemCheckbox != null){
        roleSystemCheckbox.checked = role.system
    }

    for (const action of role.actions){
        actionCheckbox = document.getElementById(action);
        if (actionCheckbox != null){
            actionCheckbox.checked = true
        }
    }
}

function deleteRole(roleId, roleName, roleCount){
    document.getElementById("delete-role-confirm").value = ""
    document.getElementById("delete-role-confirm").classList.remove("is-invalid")
    document.getElementById("replacement-info").style.display = "block";
    if (roleCount == 0) {
        document.getElementById("replacement-info").style.display = "none";
    }
    const replacementRoleElements = document.getElementById("replacement-role-id").querySelectorAll("option");
    let setDefault = false;
    for (const roleElement of replacementRoleElements) {
        roleElement.disabled = false;
        if (roleElement.value == roleId) {
            console.log(roleElement.value, "==", roleId)
            roleElement.disabled = true
        }
        else if (!setDefault) {
            setDefault = true;
            document.getElementById("replacement-role-id").value = roleElement.value;
        }
    }
    document.getElementById("delete-role-modal-header").innerHTML = 'Delete Role "' + roleName + '"?';
    document.getElementById("disabled-role-name").value = roleName;
    document.getElementById("delete-role-id").value = roleId;
    document.getElementById("delete-role-count").value = roleCount;
}

function confirmDeleteRole(){
    if (document.getElementById("delete-role-confirm").value != document.getElementById("disabled-role-name").value) {
        document.getElementById("delete-role-confirm").classList.add("is-invalid")
    }
    else {
        document.getElementById("delete-role-form").submit();
    }
}


document.addEventListener("DOMContentLoaded", function(event){
    const checkboxes = document.querySelectorAll(".dependent-checkboxes input[type=checkbox]");
    checkboxes.forEach(createListeners);
    checkboxes.forEach(createBackRequirements);
});


