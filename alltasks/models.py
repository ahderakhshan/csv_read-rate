from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    phone = models.CharField(unique=True, max_length=11)

    def __str__(self):
        return self.first_name + self.last_name + self.phone + f"user id : {self.id}"

class TakeExam(models.Model):
    exam_number = models.PositiveIntegerField()
    rate = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return  "userid:"+ str(self.user.id) + " rate:" +str(self.rate)