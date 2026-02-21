from django.db import models
from django.contrib.auth.models import AbstractUser

class Login(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('user', 'User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    view_password = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username

class Seller(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    status = models.CharField(max_length=20, default='pending') # approve, reject, block
    image = models.ImageField(upload_to='seller_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class User(models.Model):
    login = models.OneToOneField(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Design(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='design_images/', null=True, blank=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='ordered')
    payment_status = models.CharField(max_length=20, default='pending')
    
    # Customization selections
    custom_text = models.CharField(max_length=255, null=True, blank=True)
    custom_image = models.ImageField(upload_to='custom_images/', null=True, blank=True)
    custom_color = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.design.title}"

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    design = models.ForeignKey(Design, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    rating = models.IntegerField(default=5)
    date = models.DateField(auto_now_add=True)

class Chat(models.Model):
    sender = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Login, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
