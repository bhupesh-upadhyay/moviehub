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


simple jwt life cycle:

Step-by-Step: How request.user Is Determined
1️⃣ Client Sends Request

Example request:

GET /api/profile
Authorization: Bearer <access_token>
2️⃣ DRF Authentication Middleware Runs

Because in settings.py you configured:

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

DRF will use Simple JWT.

3️⃣ DRF Extracts the Token

From this header:

Authorization: Bearer <token>

It extracts:

<token>
4️⃣ Token Signature Verification

The library verifies the token using your Django SECRET_KEY.

It checks:

signature valid?
token expired?
token type correct?

If any of these fail → 401 Unauthorized.

5️⃣ Payload Is Decoded

If the token is valid, the payload is decoded:

{
  "user_id": "9"
}
6️⃣ DRF Fetches the User From Database

The authentication class runs something like:

User.objects.get(id=payload["user_id"])

Now DRF has the actual user object.

7️⃣ request.user Is Assigned

DRF sets:

request.user = user
request.auth = token

Now inside your view you can access:

request.user

Example:

def get(self, request):
    print(request.user.email)
🧠 Important Security Detail

Even though the token contains:

"user_id": 9

DRF still queries the database to load the user.

This ensures:

user still exists

user not disabled

user permissions still valid





Your backend now supports:

User Registration
Email Verification
Login (JWT)
Profile Retrieval
Profile Update
Service Layer Architecture
Signals
Transactions



Next Feature (Day 3 Advanced)
Next we should implement Password Reset Flow, which includes:
Forgot password
Email reset link
Token validation
Set new password

This will teach you:

token-based security

time-limited links

email flows

safe password handling


POST /forgot-password
↓
generate reset token
↓
send email with reset link

POST /reset-password/<uid>/<token>
↓
verify token
↓
set new password


🧠 Why Stateless Tokens Are Better

When we use Django’s token generator (like PasswordResetTokenGenerator), the system does not store tokens in the database.

Instead the token is generated using:

user_id
password hash
timestamp
secret key

So every time we verify a token, Django recomputes the expected token and compares it.


🧠 Why This Is Secure

Because the token depends on the user’s password hash.

If the user resets their password:

password hash changes

Old tokens automatically become invalid.

No manual cleanup required.



New workflow using background task
Client request
↓
Create user
↓
Queue email task
↓
Return response immediately
↓
Worker sends email in background


Client
  │
  ▼
Django API (handles HTTP)
  │
  │ enqueue task
  ▼
Redis (message queue) (stores tasks)
  │
  ▼
Celery Worker (executes tasks)
  │
  ▼
Send Email

Importantance of background worker.
    emails
    notifications
    image processing
    video encoding
    AI jobs
    analytics
    report generation

Important Architecture Concept
    Your system now has two processes.
    Web Server
    Handles API requests.
        Django
        Gunicorn
        Uvicorn

    Worker Server
    Handles background jobs.
        Celery worker

Instead of this:
    register → wait for email → respond
you get:
    register → queue email → respond immediately


Message Queue (Celery Broker)
    This is what we discussed earlier.
    Django pushes task
    ↓
    Redis stores task
    ↓
    Celery worker processes task

    Example tasks:

    send email
    generate embeddings
    process uploaded files



Use of Redis:
1. Caching (Most CommoN)
    User requests movie list
    ↓
    Check Redis cache
    ↓
    If exists → return instantly
    If not → query database
    Example:
        cache.set("movie_list", data, timeout=300)

2. Message Queue (Celery Broker)
This is what we discussed earlier.
    Django pushes task
    ↓
    Redis stores task
    ↓
    Celery worker processes task
    Example tasks:
        send email
        generate embeddings
        process uploaded files

3. Rate Limiting / Throttling
Redis is often used to store counters like:
    user:123:request_count
Example:
    10 requests per minute
Because Redis operations are extremely fast.

4. Session Storage
Instead of storing sessions in the database:
    user session
    ↓
    stored in Redis

Benefits:
    faster login systems
    better scaling for large apps
    Django supports this with:
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"

5. Real-Time Features
Redis can also power:
    live notifications
    chat systems
    websocket events
Especially with Django Channels.

Client
   │
   ▼
Django API
   │
   ├── PostgreSQL (database)
   │
   ├── Redis (cache + queue)
   │
   └── Celery Workers (background jobs)