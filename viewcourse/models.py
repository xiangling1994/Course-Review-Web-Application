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

class comment(models.Model):
    course = models.ForeignKey(addcourse, related_name='comments')
    published_date = models.DateTimeField(
            blank=True, null=True)
    user = models.CharField(max_length=30)
    commenttext = models.TextField(max_length=200)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user
