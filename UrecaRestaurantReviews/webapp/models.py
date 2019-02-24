from django.db import models
from django.core import serializers

# 1. Instructions for developmental phase
    ## To reset migrations, remove all files EXCEPT __init__.py & __pycache 
    ## in webapp/migrations
# 2. Instructions for database setup
    ## Navigate to settings.py
    ## Change attributes of 'default' to suitable user, password, host & port
# 3. Creating models
    ## django automatically creates a PRIMARY KEY
    ## Unless required a customized PRIMARY KEY, consult django documentation

# Relation : DiningSubArea
# Purpose : Each dining area may belong to a region of campus
class DiningSubArea(models.Model):
    # mandatory (to ease queries)
    manager = models.Manager()

    # attributes
    loc = models.CharField(max_length=255)

# Relation : DiningArea
# Purpose : Relation for information of a DiningArea
class DiningArea(models.Model):
    # mandatory (to ease queries)
    manager = models.Manager()

    # attributes
    name = models.CharField(max_length=255)
    addr = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    operating_hour = models.CharField(max_length=255)
    capacity = models.IntegerField()
    dining_type = models.CharField(max_length=20) 
    imgurl = models.TextField()

    # foreign key constraints
    sub_loc = models.ForeignKey(DiningSubArea, on_delete=models.CASCADE)

    # constraint(s) required
        ## capacity needs to be > 0
        ## dining_type needs to be 'Restaurant' or 'Food Court'

# Relation : DiningAreaAssets
# Purpose : Relation for assets (i.e. images) of a DiningArea 
class DiningAreaAssets(models.Model):
    # mandatory (to ease queries)
    manager = models.Manager()

    # attributes
    url = models.TextField()

    # foreign key constraints
    dining_area = models.ForeignKey(DiningArea, on_delete=models.CASCADE)

# Relation : Menu
# Purpose : Relation for menu item of a dining area
class Menu(models.Model):
    # mandatory (to ease queries)
    manager = models.Manager()

    # attributes
    name = models.CharField(max_length=255)
    price = models.FloatField()

    # foreign key constraints
    dining_area = models.ForeignKey(DiningArea, on_delete=models.CASCADE)

# Relation : Tag
# Purpose : Relation for search tags of a dining area
class Tag(models.Model):
    # mandatory (to ease queries)
    manager = models.Manager()

    # attributes
    name = models.CharField(max_length=255)

    # foreign key constraints
    dining_area = models.ForeignKey(DiningArea, on_delete=models.CASCADE)

# Relation : Review
# Purpose : Relation for reviews of a dining area
class Review(models.Model):
    # mandatory (to ease queries)
    manager = models.Manager()

    # attributes
    reviewer = models.CharField(max_length=255)
    comment = models.TextField()
    date = models.DateTimeField()
    score = models.IntegerField()

    # foreign key constraints
    dining_area = models.ForeignKey(DiningArea, on_delete=models.CASCADE)



    

