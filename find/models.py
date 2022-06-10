from django.db import models

class Element(models.Model):
    image_name=models.CharField(primary_key=True,max_length=150)
    objects_detected=models.CharField(max_length=200)
    timestamp=models.DateField()
class File(models.Model):
    file_name=models.FileField(upload_to='')
    def __str__(self):
        return f"File id: {self.id}"