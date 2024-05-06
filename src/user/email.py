from djoser import email


class CustomPasswordResetEmail(email.PasswordResetEmail):
    template_name = 'reset_password.html'
