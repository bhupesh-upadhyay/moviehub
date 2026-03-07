moviehub/
│
├── config/
├── apps/
│   └── users/
├── manage.py


user model:
The default Django user uses:
USERNAME_FIELD = "username"
But modern applications use:
    Email-based login
    Phone number login
    No username at all

TODO:
Send welcome email
Create user profile
Log activity

user verification link.
    User registers
    ↓
    UserService.create_user()
    ↓
    Signal triggers
    ↓
    Generate verification token
    ↓
    Send verification email
    ↓
    User clicks link
    ↓
    VerifyEmailView
    ↓
    user.is_verified = True


GET /verify-email/<uid>/<token>/

decode uid
↓
get user
↓
validate token
↓
verify account