from django.contrib import admin

from refresh_tokens.models import RefreshToken
from users.models import User
from verification.models import VerificationCode


admin.site.register(User)
admin.site.register(VerificationCode)
admin.site.register(RefreshToken)
