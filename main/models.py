import random
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from pathlib import Path

from decouple import config
import os
from supabase import create_client, Client
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.files.storage import default_storage


url: str = config('SUPABASE_URL')
key: str = config('SUPABASE_KEY')

supabase: Client = create_client(url, key)

# BASE_DIR = Path(__file__).resolve().parent.parent

# file_path = os.path.join(BASE_DIR, 'static', 'images', 'cover.jpg')
# path_on_supastorage = 'image.jpg'
# with open(file_path, 'rb') as f:
#     image_data = f.read()

# content_type = 'image/jpeg'  

# bucket_name = 'dzecko_image_bucket'  # Replace with your Supabase bucket name
# bucket = supabase.storage.from_(bucket_name)

# file_options = {"content-type": content_type}
# upload_response = bucket.upload(file=image_data, path=path_on_supastorage, file_options=file_options)


def upload_image_to_supabase(image, path_on_supastorage, bucket_name='dzeko_server_images'):
    with open(image.path, 'rb') as f:
        image_data = f.read()
    bucket = supabase.storage.from_(bucket_name)
    upload_response = bucket.upload(file=image_data, path=path_on_supastorage, file_options={"content-type": 'image/jpeg'})
    return f"{url}/storage/v1/object/public/{bucket_name}/{path_on_supastorage}" if upload_response else None





# with open(filepath, 'rb') as f:
#     supabase.storage.from_("dzeko_image_bucket").upload(file=f,path=path_on_supastorage, file_options={"content-type": "audio/mpeg"})


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


IMAGE_PLACEHOLDER = 'https://dlomnkdfvdzwzajbgpxu.supabase.co/storage/v1/object/public/dzeko_server_images/images.jpg'

class Media(models.Model):
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER) 
    description = models.TextField(null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Media - {self.id}"

    
class Color(models.Model):
    name = models.CharField(max_length=50)
    hex_value = models.CharField(max_length=7)
    image = models.ImageField(null= True , blank=True) 

    def __str__(self):
        return self.name
    
class UserImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    image = models.ImageField(null= True , blank=True,max_length=300) 
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER) 

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.user.name)[:50]  

        super().save(*args, **kwargs)
        
        if self.image:
            path_on_supastorage = f'{self.ref}_image{random.randint(100, 999)}.jpg'
            public_url = upload_image_to_supabase(self.image, path_on_supastorage)
            if public_url:
                self.image_url = public_url
                super().save(*args, **kwargs)
                print(f'Image uploaded successfully to Supabase. Public URL: {public_url}')


    def __str__(self):
        return self.name

   
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(null= True , blank=True,max_length=300) 
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER) 

    
    
    
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]  

        super().save(*args, **kwargs)
        
        if self.image:
            path_on_supastorage = f'{self.ref}_image{random.randint(100, 999)}.jpg'
            public_url = upload_image_to_supabase(self.image, path_on_supastorage)
            if public_url:
                self.image_url = public_url
                super().save(*args, **kwargs)
                print(f'Image uploaded successfully to Supabase. Public URL: {public_url}')


    def __str__(self):
        return self.name



class Type(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    images = models.ManyToManyField(Media, related_name='type_images', blank=True)
    image = models.ImageField(null= True , blank=True) 
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER)
    

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)
        
        if self.image:
            path_on_supastorage = f'{self.ref}_image{random.randint(1, 99)}.jpg'
            public_url = upload_image_to_supabase(self.image, path_on_supastorage)
            if public_url:
                self.image_url = public_url
                super().save(*args, **kwargs)
                print(f'Image uploaded successfully to Supabase. Public URL: {public_url}')


    def __str__(self):
        return self.name
    
class Palette(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(null= True , blank=True) 
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER)
    
    
    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)
        
        if self.image:
            path_on_supastorage = f'{self.ref}_image{random.randint(1, 99)}.jpg'
            public_url = upload_image_to_supabase(self.image, path_on_supastorage)
            if public_url:
                self.image_url = public_url
                super().save(*args, **kwargs)
                print(f'Image uploaded successfully to Supabase. Public URL: {public_url}')


    def __str__(self):
        return self.name
    
    
    
class Ambiance(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True)
    images = models.ManyToManyField(Media, related_name='ambiance_images', blank=True)
    image = models.ImageField(null= True , blank=True)
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER) 
    

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)
        
        if self.image:
            path_on_supastorage = f'{self.ref}_image{random.randint(1, 99)}.jpg'
            public_url = upload_image_to_supabase(self.image, path_on_supastorage)
            if public_url:
                self.image_url = public_url
                super().save(*args, **kwargs)
                print(f'Image uploaded successfully to Supabase. Public URL: {public_url}')

    def __str__(self):
        return self.name
    
    
    
class Revetement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    description = models.TextField()
    images = models.ManyToManyField(Media, related_name='revetment_images', blank=True)
    image = models.ImageField(null= True , blank=True)
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER) 
    

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)
        if self.image:
            path_on_supastorage = f'{self.ref}_image{random.randint(1, 99)}.jpg'
            public_url = upload_image_to_supabase(self.image, path_on_supastorage)
            if public_url:
                self.image_url = public_url
                super().save(*args, **kwargs)
                print(f'Image uploaded successfully to Supabase. Public URL: {public_url}')

    def __str__(self):
        return self.name


class FurnitureType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True)
    images = models.ManyToManyField(Media, related_name='furniture_type_images', blank=True)
    image = models.ImageField(null= True , blank=True) 
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER)
    

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)
        if self.image:
            path_on_supastorage = f'{self.ref}_image{random.randint(1, 99)}.jpg'
            public_url = upload_image_to_supabase(self.image, path_on_supastorage)
            if public_url:
                self.image_url = public_url
                super().save(*args, **kwargs)
                print(f'Image uploaded successfully to Supabase. Public URL: {public_url}')

    def __str__(self):
        return self.name




class Furniture(models.Model):
    name = models.CharField(max_length=100)
    ref = models.CharField(max_length=50, blank=True)
    furniture_type = models.ForeignKey(FurnitureType, on_delete=models.CASCADE)
    images = models.ManyToManyField('Media', related_name='furniture_images', blank=True)
    image = models.ImageField(null= True , blank=True)
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER) 
    
    color = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)
        if self.image:
            path_on_supastorage = f'{self.ref}_image{random.randint(1, 99)}.jpg'
            public_url = upload_image_to_supabase(self.image, path_on_supastorage)
            if public_url:
                self.image_url = public_url
                super().save(*args, **kwargs)
                print(f'Image uploaded successfully to Supabase. Public URL: {public_url}')

    def __str__(self):
        return self.name



class Option(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ref = models.CharField(max_length=50, unique=True, blank=True)
    images = models.ManyToManyField(Media, related_name='option_images', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    image = models.ImageField(null= True , blank=True)
    image_url = models.URLField(max_length=500,null=True, blank=True, default=IMAGE_PLACEHOLDER) 
    

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = slugify(self.name)[:50]

        super().save(*args, **kwargs)
        if self.image:
            path_on_supastorage = f'{self.ref}_image{random.randint(1, 99)}.jpg'
            public_url = upload_image_to_supabase(self.image, path_on_supastorage)
            if public_url:
                self.image_url = public_url
                super().save(*args, **kwargs)
                print(f'Image uploaded successfully to Supabase. Public URL: {public_url}')

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

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, blank=True)
    ambiance = models.ForeignKey(Ambiance, on_delete=models.CASCADE, blank=True)
    revetment = models.ForeignKey(Revetement, on_delete=models.CASCADE, blank=True)
    furnitures = models.ManyToManyField(Furniture, related_name='orders', blank=True)
    options = models.ManyToManyField(Option, related_name='orders', blank=True)
    questions = models.ManyToManyField(Question, related_name='orders', blank=True)

    def save(self, *args, **kwargs):
        if not self.ref:
            self.ref = f"{slugify(self.user.username)}_{slugify(self.type.name)}_{self.pk}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.user.username} - {self.pk}"