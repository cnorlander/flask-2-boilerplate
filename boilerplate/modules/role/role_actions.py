actions = []

def register_action(action: str, feature: str, description: str, required_actions: tuple = tuple(), system_only: bool = False):
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

class NonExistentActionError(Exception):
    def __init__(self, action, existing_actions, *args):
        super().__init__(args)
        self.action = action
        self.existing_actions = existing_actions

    def __str__(self):
        return f'The {self.action} is not in a valid system action. Please verify the correct action name is being called and the action is registered. \r\n ' \
               f'The list of all existing actions includes: \r\n {self.existing_actions}'

