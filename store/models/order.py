from django.db import models

STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderDetail(models.Model):
    user = models.IntegerField(default=True)
    product_name = models.CharField(max_length=250)
    image = models.ImageField(null=True,blank=True)
    qty = models.PositiveIntegerField(default=1)
    price = models.FloatField()
    ordered_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50,default='pending',choices=STATUS_CHOICE)