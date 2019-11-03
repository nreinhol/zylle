from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Post(models.Model):
    fish_choices = (
        ('BARSCH', 'Barsch'),
        ('HECHT', 'Hecht'),
        ('ZANDER', 'Zander'),
    )

    fish_type = models.CharField(max_length=10, choices=fish_choices)
    fish_length = models.FloatField()
    img = models.ImageField(default='default.jpg', upload_to='post_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}, {}cm'.format(self.author, self.fish_type, self.fish_length)
