import re


class PasswordValidation:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def validate(self):

        username = self.user.cleaned_data.get('username')
        email = self.user.cleaned_data.get('email')

        lower = re.findall('[a-z]', self.password)
        upper = re.findall('[A-Z]', self.password)
        num = re.findall('[0-9]', self.password)
        specialChar = re.findall('[!@#$%^&*()]', self.password)

        if len(self.password) > 8 and \
                lower and upper and num and len(specialChar) > 1 and \
                self.password != username and self.password != email:
            print(specialChar)

            return True

        return False
