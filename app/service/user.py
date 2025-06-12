from app.model.user import User


def get_sample_user() -> User:
    return User(id=1, name="Alice", email="alice@example.com")
