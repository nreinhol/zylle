from django.contrib.auth.models import User
from datetime import timezone
import json

from .models import Post


def get_all_user(request):
    return User.objects.all()