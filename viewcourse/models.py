from django.db import models
import hashlib

class course(models.Model):
    subject = models.CharField(max_length=30)
    courseid = models.CharField(max_length=10)
    grade = models.CharField(max_length=10)

    def publish(self):
        self.save()

    def _str_(self):
        return courseid

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


class account(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, default='', unique=True)

    def __unicode__(self):
        return self.username

 '''def hashed_password(self,password=None):
        if not password:
            return self.password
        else:
            #生成password的md5码，hexdigest()即为取得哈希码的16进制字符串
            return hashlib.md5(password).hexdigest()

    def is_authenticated(self):
        return True

    def check_password(self,password):
        if self.hashed_password(password) == self.password:
            return True
        else:
            return False
'''
