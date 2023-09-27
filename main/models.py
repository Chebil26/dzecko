from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User



# Media: A model to store media-related information, including image URLs, description, and tags.

# Category: Represents furniture categories.

# Type: Represents types of furniture.

# Ambiance: Represents different ambiance related to furniture.

# Revetement: Represents different types of revetement.

# FurnitureType: Represents different types of furniture with associated category and type.

# Furniture: Represents furniture with associated category, type, furniture type, images, color, and dimensions.

# Option: Represents options for furniture with associated images and price.

# Question: Represents different questions.

# Order: Represents an order, including a reference, description, images, and associations with user, category, type, ambiance, revetment, furnitures, options, and questions.

# The usage of slugify to generate unique references is a good approach, and the relationships between the models seem appropriate based on the information provided.


IMAGE_PLACEHOLDER = 'https://dlomnkdfvdzwzajbgpxu.supabase.co/storage/v1/object/sign/dzecko_image_bucket/gato.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJkemVja29faW1hZ2VfYnVja2V0L2dhdG8uanBnIiwiaWF0IjoxNjk1ODI0MzkzLCJleHAiOjE3MjczNjAzOTN9.IIMx1Zg5Vbfniiecnx6SuXAK9UjnonxQcr9LENSEhRM&t=2023-09-27T14%3A19%3A48.828Z'

class Media(models.Model):
    image_url = models.URLField(null=True, blank=True, default=IMAGE_PLACEHOLDER) 
    description = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Media - {self.id}"

    
class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_value = models.CharField(max_length=7)  # Assuming you'll store color hex values

    def __str__(self):
        return self.name
   
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]  

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    images = models.ManyToManyField(Media, related_name='type_images', blank=True)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
class Ambiance(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    images = models.ManyToManyField(Media, related_name='ambiance_images', blank=True)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
    
class Revetement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    images = models.ManyToManyField(Media, related_name='revetment_images', blank=True)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FurnitureType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    images = models.ManyToManyField(Media, related_name='furniture_type_images', blank=True)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name




class Furniture(models.Model):
    name = models.CharField(max_length=100)
    ref = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    furniture_type = models.ForeignKey(FurnitureType, on_delete=models.CASCADE)
    images = models.ManyToManyField('Media', related_name='furniture_images', blank=True)
    color = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Option(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    images = models.ManyToManyField(Media, related_name='option_images', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
    
    
    
    
class Question(models.Model):
    question = models.CharField(max_length=500)
    ref = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.question)[:50]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    
    



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref = models.CharField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    images = models.ManyToManyField(Media, related_name='order_images', blank=True)
    colors = models.ManyToManyField(Color, related_name='orders', blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    ambiance = models.ForeignKey(Ambiance, on_delete=models.CASCADE)
    revetment = models.ForeignKey(Revetement, on_delete=models.CASCADE)
    furnitures = models.ManyToManyField(Furniture, related_name='orders')
    options = models.ManyToManyField(Option, related_name='orders')
    questions = models.ManyToManyField(Question, related_name='orders')

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = f"{slugify(self.user.username)}_{slugify(self.type.name)}_{self.pk}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.user.username} - {self.pk}"