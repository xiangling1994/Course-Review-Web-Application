from django.db import models

class addcourse(models.Model):
    subject = models.CharField(max_length=30)
    courseid = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)

    def publish(self):
        self.save()

    def _str_(self):
        return courseid

class comment(models.Model):
    course = models.ForeignKey(addcourse, related_name='comments')
    published_date = models.DateTimeField(blank=True, null=True)
    user = models.CharField(max_length=30)
    commenttext = models.TextField(max_length=200)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user


class professor(models.Model):
    course = models.ForeignKey(addcourse, related_name='professors')
    full_name = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    def publish(self):
        self.save()
    def __str__(self):
        return self.full_name


class user(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, default='')

    def __str__(self):
        return self.username


class ratingCriteria(models.Model):
    course = models.ForeignKey(addcourse,null=True, related_name='criterias')
    prof = models.ForeignKey(professor, related_name='Criteria_Professor')
    helpfulness = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    clarity = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    easiness = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    textbook = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ratetimes = models.IntegerField(default=0)

    def publish(self):
        self.save()
