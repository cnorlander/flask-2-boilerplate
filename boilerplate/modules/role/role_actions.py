# ==============================================================================================================================================================
#                                                                   Variables
# ==============================================================================================================================================================
actions = []

# ==============================================================================================================================================================
#                                                                   Functions
# ==============================================================================================================================================================
def register_action(action: str, feature: str, description: str, required_actions: tuple = tuple(), system_only: bool = False):
    existing_actions = get_action_names()
    if action in existing_actions:
        raise DuplicateActionError(action)
    for required_action in required_actions:
        if not required_action in existing_actions:
            raise NonExistentRequiredActionError(existing_actions, required_action)

    actions.append({'action': action, 'feature': feature, 'description': description, 'required_actions': required_actions, 'system_only':system_only})

def get_actions():
    return sorted(actions, key=lambda action: action['feature'])

def get_action_names():
    return [item['action'] for item in actions]

def action_exists(action):
    all_action_names = get_action_names()
    if action in all_action_names:
        return True
    raise NonExistentActionError(action, all_action_names)


# ==============================================================================================================================================================
#                                                                   Exceptions
# ==============================================================================================================================================================
class NonExistentActionError(Exception):
    def __init__(self, action, existing_actions, *args):
        super().__init__(args)
        self.action = action
        self.existing_actions = existing_actions

    def __str__(self):
        return f'The action "{self.action}" is not in a valid system action. Please verify the correct action name is being called and the action is registered.' \
               f' \r\nThe list of all existing actions includes: \r\n {self.existing_actions}'

class NonExistentRequiredActionError(Exception):
    def __init__(self, action, existing_actions, *args):
        super().__init__(args)
        self.action = action
        self.existing_actions = existing_actions

    def __str__(self):
        return f'The action required action registered "{self.action}" is not in a valid system action. Please verify the correct action name is being called ' \
               f'and the action is registered. \r\nThe list of all existing actions includes: \r\n {self.existing_actions}'

class DuplicateActionError(Exception):
    def __init__(self, action, *args):
        super().__init__(args)
        self.action = action

    def __str__(self):
        return f'The action "{self.action}" is not in a is a duplicate of an already registered action.'


