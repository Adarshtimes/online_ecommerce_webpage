from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12, blank=True, null=True)


    def register(self):
        self.save()

    def isExists(self):
        if Customer.objects.filter(phone=self.phone):
            return True
        else:
            return False