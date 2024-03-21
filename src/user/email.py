from djoser import email


class CustomPasswordResetEmail(email.PasswordResetEmail):
    template_name = 'email/custom_reset_password_email.html'


