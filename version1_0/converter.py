class signedInteger():
    regex = '-*\d'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return int(value)
