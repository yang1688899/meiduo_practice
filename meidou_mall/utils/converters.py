from django.urls import converters


class UsernameValidator:
    regex = "[A-Za-z0-9_-]{5,20}"

    def to_python(self, value):
        return value
