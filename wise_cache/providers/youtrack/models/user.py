

class User(object):
    def __init__(self,
                 name: str,
                 email: str = None):
        self.name = name
        self.email = email if email is not None else None

    def __str__(self):
        return (
            f"User(name='{self.name}', "
            f"email='{self.email}', )"
        )
