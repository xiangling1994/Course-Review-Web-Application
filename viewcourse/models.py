from django.db import models

class course(models.Model):
    university = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    courseid = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)

    def publish(self):
        self.save()

    def _str_(self):
        return courseid


class professor(models.Model):
    course = models.ForeignKey(course, related_name='professors')
    full_name = models.CharField(max_length=20)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    helpfulness = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    clarity = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    easiness = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    textbook = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ratetimes = models.IntegerField(default=0)

    def publish(self):
        self.save()

    def __str__(self):
        return self.full_name


class comment(models.Model):
    course = models.ForeignKey(course, related_name='comments')
    published_date = models.DateTimeField(blank=True, null=True)
    user = models.CharField(max_length=30)
    commenttext = models.TextField(max_length=200)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.user


class account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=30, unique=True)

    def __str__(self):
        return self.username


class vote(models.Model):
    account = models.ForeignKey(account, related_name='votes')
    prof = models.CharField(max_length=20)
    cid = models.CharField(max_length=10)

    def publish(self):
        self.save()

    def __str__(self):
        return self.prof
