from django.db import models

class addcourse(models.Model):
    subject = models.CharField(max_length=30)
    courseid = models.CharField(max_length=10)
    prof = models.CharField(max_length=20)
    grade = models.CharField(max_length=10)

    def publish(self):
        self.save()

    def _str_(self):
        return courseid
