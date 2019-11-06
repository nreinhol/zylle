from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class Post(models.Model):
    fish_choices = (
        ('Barsch', 'Barsch'),
        ('Hecht', 'Hecht'),
        ('Zander', 'Zander'),
    )

    fish_type = models.CharField(max_length=10, choices=fish_choices, verbose_name='Fisch')
    fish_length = models.FloatField(verbose_name='Länge')
    img = models.ImageField(default='default.jpg', upload_to='post_pics/', verbose_name='Bild')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}, {}cm'.format(self.author, self.fish_type, self.fish_length)

    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

