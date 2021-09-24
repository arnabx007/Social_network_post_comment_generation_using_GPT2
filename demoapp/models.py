from django.db import models
from .generate import generate_comment


def autocomment(text):
    comment = generate_comment(text)
    return comment

class postandcomment(models.Model):
    # id = models.AutoField(primary_key=True)
    post = models.CharField(max_length=2000, blank=False, default='')
    comment = models.CharField(max_length=1000,blank=True, default='')

    # When using PUT request or updating through admin dashboard, 
    # the comment field automatically populates itself and saves the entry.
    def save(self, *args, **kwargs):
        if self.comment == '':
            self.comment =  autocomment(self.post)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)