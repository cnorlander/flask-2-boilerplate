from user_controller import user_model


# Assure the hash_password and check_passwords functions are working.
def bcrypt_test():
    output = user_model.hash_password("iloveflask!")
    assert user_model.check_password("iloveflask!", output) == True
    assert user_model.check_password("ilovedjango!", output) == False