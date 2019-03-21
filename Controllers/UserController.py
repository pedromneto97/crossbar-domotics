from mongoengine import DoesNotExist

from Models.User import User


def get_user(id: str) -> User or None:
    user = User.objects(id=id).first()
    if user is None:
        return None
    return user.to_json()


def get_user_by_cpf(cpf: str) -> User or None:
    user = User.objects(cpf=cpf).first()
    if user is None:
        return None
    return user.to_json()


def get_user_by_username(username: str) -> User or None:
    user = User.objects(username=username).first()
    if user is None:
        return None
    return user.to_json()


def get_user_by_email(email: str) -> User or None:
    user = User.objects(email=email).first()
    if user is None:
        return None
    return user.to_json()


def insert(username: str, name: str, password: str, cpf: str, email: str) -> bool:
    password = User.encrypt(password, username)
    user = User(username=username, name=name, password=password, cpf=cpf, email=email)
    user.save()
    return True


def insert_json(json: str) -> bool:
    user = User.from_json(json)
    user.password = User.encrypt(user.password, user.username)
    user.save()
    return True


def update(id: str = None, username: str = None, name: str = None, password: str = None, cpf: str = None,
           email: str = None) -> bool:
    user: User = User.objects(id=id).first()
    if user is None:
        raise DoesNotExist('User does not exist')
    if username is not None:
        user.username = username
        if password is not None:
            user.password = User.encrypt(password, username)
    if name is not None:
        user.name = name
    if cpf is not None:
        user.cpf = cpf
    if email is not None:
        user.email = email
    user.save()
    return True
