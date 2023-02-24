actions = []

def register_action(action: str, feature: str, description: str, required_actions: tuple = tuple()):
    actions.append({'action': action, 'feature': feature, 'description': description, 'required_actions': required_actions})

def get_actions():
    return actions