actions = []

def register_action(action: str, feature: str, description: str, required_actions: tuple = tuple(), system_only: bool = False):
    actions.append({'action': action, 'feature': feature, 'description': description, 'required_actions': required_actions, 'system_only':system_only})

def get_actions():
    return sorted(actions, key=lambda action: action['feature'])

def get_action_names():
    return [item['action'] for item in actions]

