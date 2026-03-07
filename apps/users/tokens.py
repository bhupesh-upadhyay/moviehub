from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):

    # Overide this method and make custom verification
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) +
            str(timestamp) +
            str(user.is_verified) # invalid token if alrady verified.
        )

email_verification_token = EmailVerificationTokenGenerator()

# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# uid = urlsafe_base64_encode(force_bytes(user.pk))