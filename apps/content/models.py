from django.db import models

# Create your models here.

class Content(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('show', 'TV Show'),
        ('episode', 'Episode'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    content_type = models.CharField(choices=CONTENT_TYPE_CHOICES, max_length=20)
    release_year = models.IntegerField()
    duration = models.IntegerField(help_text="Druation in Seconds")
    genre = models.CharField(max_length=100)
    thumbnail = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    