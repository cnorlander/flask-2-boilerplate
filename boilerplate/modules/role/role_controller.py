from boilerplate.app import app
from boilerplate.db import save
from boilerplate.modules.role.role_model import Role, get_role_by_name, get_role_by_uuid, create_if_not_exists
from boilerplate.modules.role.role_actions import get_actions, get_action_names, register_action
from boilerplate.modules.role.role_decorators import require_action
from boilerplate.modules.user.user_model import replace_all_instances_of_role
from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user

# ==============================================================================================================================================================
#                                                                      View Routes
# ==============================================================================================================================================================
@app.get('/roles')
@login_required
@require_action("read_roles_list")
def get_roles_list():
    roles = Role.query.all()
    actions = get_actions()
    return render_template("role/role_list.html", actions=actions, roles=roles)

@app.post('/roles')
@login_required
@require_action("create_or_edit_role")
def post_create_or_edit_role():

    role_id = request.form.get("role-id")
    role_description = request.form.get("role-description")
    role_name = request.form.get("role-name").title()
    role_hidden = False
    role_system = False
    actions = []
    if (not role_id) or (not role_description) or (not role_name):
        return abort(400)

    if request.form.get("role-hidden") and request.form.get("role-hidden") == "true" and current_user.role.system:
        role_hidden = True

    if request.form.get("role-system") and request.form.get("role-system") == "true" and current_user.role.system:
        role_system = True

    if role_id == "new":
        existing_role = get_role_by_name(role_name)
        if existing_role:
            flash("A role with that name already exists. Please use a unique name when creating roles.", "error")
            return redirect(url_for("get_roles_list"))
        for key in request.form:
            value = request.form.get(key)
            if ("action-flag-" in key) and (value == "true"):
                actions.append(key.replace("action-flag-", ""))
        create_if_not_exists(Role(role_name, role_description, actions, system=role_system, hidden=role_hidden))
        flash(f"Role {role_name} created successfully!", "success")
        return redirect(url_for("get_roles_list"))


    existing_role = get_role_by_uuid(role_id)
    if not existing_role:
        flash("Something happened while updating the role. Please Try again and if you continue to experience issues contact an administrator", "error")
        return redirect(url_for("get_roles_list"))
    all_actions = get_action_names()
    existing_actions = existing_role.actions
    new_actions = []
    for action in all_actions:
        form_action = request.form.get("action-flag-" + action)
        if form_action == "false":
            continue
        elif form_action == "true":
            new_actions.append(action)
        elif (form_action is None) and (action in existing_actions):
            new_actions.append(action)
        else:
            return abort(400)
    existing_role.actions = new_actions
    existing_role.name = role_name
    existing_role.description = role_description
    existing_role.system = role_system
    existing_role.hidden = role_hidden
    if save():
        flash(f"Role {role_name} has been edited!", "success")
    return redirect(url_for("get_roles_list"))

@app.post('/roles/delete')
@login_required
@require_action("delete_role")
def delete_role():

    role_id = request.form.get("delete-role-id")
    replacement_role_id = request.form.get("replacement-role-id")
    delete_role_count = request.form.get("delete-role-count")

    if (not role_id) or (not replacement_role_id) or (not delete_role_count):
        flash(
            "An error occured while getting the information to delete the role. Please try again and if you continue to "
            "experience issues contact an administrator",
            "error")
        return redirect(url_for("get_roles_list"))

    # Get the role to delete and confirm it still exists
    existing_role = get_role_by_uuid(role_id)
    if not existing_role:
        flash("An error occured while retreiving the role to delete. The role may have already been deleted.", "error")
        return redirect(url_for("get_roles_list"))

    # See if the role is in use
    if len(existing_role.users) > 0:
        # A user was added to the role being deleted while they were deleting the role, better we have them try again.
        if delete_role_count == 0:
            flash(
                "An error occured while preparing to delete the role. Please try again and if you continue to experience"
                " issues contact an administrator",
                "error")
            return redirect(url_for("get_roles_list"))

        # Get the role to replace and confirm it exists.
        replacement_role = get_role_by_uuid(replacement_role_id)
        if not replacement_role:
            flash(
                "An error occured while getting the replacement role. Please try again and if you continue to experience"
                " issues contact an administrator",
                "error")
            return redirect(url_for("get_roles_list"))

        # Replace the role
        replace_all_instances_of_role(existing_role, replacement_role)

    existing_role.delete()
    flash("Role deleted successfully.","success")

    return redirect(url_for("get_roles_list"))

# ==============================================================================================================================================================
#                                                                  Context Processors
# ==============================================================================================================================================================
@app.context_processor
def context_processor_role_has_action():
    def role_has_action(role: Role, action: str):
        return role.has_action(action)
    return dict(role_has_action=role_has_action)


# ==============================================================================================================================================================
#                                                                 Action Registrations
# ==============================================================================================================================================================
register_action("read_roles_list", "roles", "Allows a user to see the list of roles in the system.")
register_action("create_or_edit_role", "roles", "Allows a user create or edit a user role.", ("read_roles_list",))
register_action("delete_role", "roles", "Allows a user to delete roles.", ("read_roles_list",))