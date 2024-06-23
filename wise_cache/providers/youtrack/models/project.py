
class Project(object):
    def __init__(self, name, shortName):
        self.name = name
        self.short_name = shortName

    def __str__(self):
        return (
            f"Project(name='{self.name}', "
            f"shortName='{self.short_name}')"
        )
