from django.db import models
# Create your models here.


class Customer(models.Model):
    customer_name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=15)  # Adjust the max length according to your needs
    email = models.EmailField(unique=True)  # Ensure uniqueness for email addresses
    password = models.CharField(max_length=50)  # Use a longer field to store hashed passwords

    def __str__(self):
        return self.customer_name
    

    
class Food_Item(models.Model):
    name=models.CharField(max_length=50)
    picture=models.ImageField()
    description=models.TextField()

    def __str__(self):
        return self.name


class Food(models.Model):
    item = models.ForeignKey(Food_Item, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    picture=models.ImageField()
    price =models.IntegerField()
    description=models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    date = models.DateTimeField()
    quantity = models.IntegerField()
    total = models.IntegerField()
    def __str__(self):
        return f"{self.customer.customer_name}-{self.food.name}"
    
class Reservations(models.Model):
    name= models.CharField(max_length=50)
    email=models.EmailField()
    date=models.DateField()
    time=models.TimeField()
    number_of_guest=models.IntegerField()
    def __str__(self):
        return self.name




