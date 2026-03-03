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

