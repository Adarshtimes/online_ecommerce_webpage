from django.db import models

STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

PAYMENT_STATUS = (
    ('PENDING', 'Pending'),
    ('SUCCESS', 'Success'),
    ('FAILED', 'Failed'),
)


class OrderDetail(models.Model):
    user = models.IntegerField(default=True)
    product_name = models.CharField(max_length=250)
    image = models.ImageField(null=True,blank=True)
    qty = models.PositiveIntegerField(default=1)
    price = models.FloatField()
    ordered_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50,default='Accepted',choices=STATUS_CHOICE)
    payment_method = models.CharField(max_length=20, default='UPI')
    payment_status = models.CharField(max_length=20,choices=PAYMENT_STATUS,default='PENDING')
    upi_id = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} - {self.payment_status}"