from django.db import models

# Create your models here.
class Movies(models.Model):
    name = models.CharField(max_length=255, null=False)
    actor = models.EmailField(max_length=255, null=False)
    director = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=500)
    release_date = models.DateField("Release_Date")
    image = models.URLField('Image', default='')

    def __str__(self):
        return self.name