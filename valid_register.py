def valid_form(orm_user, username: str, password: str):
    if not username or not password or len(password)<5:
        return False, "El username y la password son obligatorias y la password debe contener mas de 5 caracteres"
    
    user_exist = orm_user.get_user_by_username(username=username)
    if user_exist:
        return False, "El username ya existe"
    
    return True, "Formulario valido"