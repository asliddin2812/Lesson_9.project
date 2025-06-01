from django.db import models

# Create your models here.

class Construction(models.Model):
    rus_tili = models.CharField(max_length=150)
    uzbek_kiril = models.CharField(max_length=150)
    uzbek_lotin = models.CharField(max_length=150)
    ingliz_tili = models.CharField(max_length=150)
    turk_tili = models.CharField(max_length=150)

    def __str__(self):
        return self.uzbek_lotin

    class Meta:
        db_table = 'construction'
        ordering = ['uzbek_lotin']

