from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def verbose_name(self):
        return self.name
    
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'
