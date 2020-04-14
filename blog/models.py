from django.db import models

# Create your models here.


class Blog(models.Model):
    headline = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    summary = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="receipe_image")
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.headline
