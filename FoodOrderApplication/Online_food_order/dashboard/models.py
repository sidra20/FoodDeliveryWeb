from django.db import models

# Create your models here.
class Role(models.Model):
    role = models.CharField(max_length=50, unique=True)

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=32)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

 #veg/non veg etc
class FoodType(models.Model):   #ADMIN
    foodtype = models.CharField(max_length=200, unique=True)


#italian/bbq/fast food etc
class Category(models.Model):  #ADMIN
    category = models.CharField(max_length=200, unique=True)

class Books(models.Model): #ADMIN
    book_name = models.CharField(max_length=200, unique=True)
    book_author = models.CharField(max_length=200)
    book_cover = models.ImageField
    book = models.CharField # book pdf field....?????????????

class Resturant(models.Model):  #RESTURANT OWNER
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=11)
    image = models.ImageField
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ResturantRatings(models.Model):
    resturant = models.ForeignKey(Resturant, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=255)
    person_email = models.CharField(max_length=255)
    review = models.CharField(max_length=255)
    ratings = models.IntegerField(max_length=1)
    date = models.DateTimeField



# pizza/drinks/sandwiches/burgers
class Menu(models.Model): # RESTURANT OWNER
    resturant = models.ForeignKey(Resturant, on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=200, unique=True)

class Dishes(models.Model): #RESTUTANT OWNER
    food_name = models.CharField(max_length=200)
    food_details = models.CharField(max_length=255)
    food_price = models.DecimalField(max_length=20)
    food_image = models.ImageField
    date = models.DateTimeField
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    foodtype = models.ForeignKey(FoodType, on_delete=models.CASCADE)
    resturant = models.ForeignKey(Resturant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class DishReview(models.Model):
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    person_name = models.CharField(max_length=255)
    person_email = models.CharField(max_length=255)
    date = models.DateTimeField
    review = models.CharField(max_length=255)
    ratings = models.IntegerField(max_length=1)


class MenuCards(models.Model): #RESTURANT OWNER
    resturant = models.ForeignKey(Resturant, on_delete=models.CASCADE)
    card = models.ImageField

class Videos(models.Model): #RESTURANT OWNER
    resturant = models.ForeignKey(Resturant, on_delete=models.CASCADE)
    videos = models.CharField   #field..........??????????????????


class Coupens(models.Model):  # RESTURANT OWNER
    resturant = models.ForeignKey(Resturant, on_delete=models.CASCADE)
    coupen = models.CharField(max_length=5)
    discount = models.IntegerField(max_length=2)
class Cart(models.Model): #Customer
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resturant = models.ForeignKey(Resturant, on_delete=models.CASCADE)
    quantity = models.IntegerField

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_address = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=11)
    address_type = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=11)


class Order(models.Model):
    pass

class CompletedOrders(models.Model):
    pass

class Feedback(models.Model):
    pass




