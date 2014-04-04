from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager

class Profile(models.Model):
    user = models.OneToOneField(User)
    tagline = models.CharField(max_length=100)

class BaseTshirt(models.Model):
    type = models.CharField(max_length=30, choices=(('tshirt', 'tshirt'),))
    name = models.CharField(max_length=100)
    url = models.URLField()
    description = models.CharField(max_length=200)
    white_price = models.DecimalField(max_digits=4, decimal_places=2)

class Color(models.Model):
    basetshirt = models.ForeignKey(BaseTshirt, related_name='colors')
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=7)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    url_code = models.CharField(max_length=10)

class PrintCost(models.Model):
    color = models.CharField(max_length=5)
    quantity_range_low = models.PositiveSmallIntegerField()
    quantity_range_high = models.PositiveSmallIntegerField()
    #costs are in cents
    color_1_cost = models.DecimalField(max_digits=3, decimal_places=2)
    color_2_cost = models.DecimalField(max_digits=3, decimal_places=2)
    color_3_cost = models.DecimalField(max_digits=3, decimal_places=2)
    color_4_cost = models.DecimalField(max_digits=3, decimal_places=2)
    color_5_cost = models.DecimalField(max_digits=3, decimal_places=2)
    color_6_cost = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    color_additional_cost = models.DecimalField(max_digits=3, decimal_places=2, null=True)

class Tshirt(models.Model):
    user = models.ForeignKey(User)

    #the basetshirt can be gotten from the foreign key of the Color
    color = models.ForeignKey(Color, related_name='tshirts')
    image = models.ImageField(upload_to='tshirt-images')
    image_back = models.ImageField(upload_to='tshirt-images')

    title = models.CharField(max_length=60)
    description = models.CharField(max_length=360)
    slug = models.SlugField(max_length=60) #same max length as title for now
    tags = TaggableManager(help_text=None)

    selling_price = models.DecimalField(max_digits=5, decimal_places=2)
    base_price = models.DecimalField(max_digits=5, decimal_places=2)

    min_orders = models.PositiveSmallIntegerField()
    days_left = models.PositiveSmallIntegerField()

    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # For automatic slug generation.
        if not self.slug:
            self.slug = slugify(self.title)[:60]

        return super(Tshirt, self).save(*args, **kwargs)

class Payment(models.Model):
    tshirt = models.ForeignKey(Tshirt, related_name='payments')
    customer_id = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    shipping_name = models.CharField(max_length=100)
    shipping_country = models.CharField(max_length=50)
    shipping_city = models.CharField(max_length=60)
    shipping_street = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=2)
    shipping_zip = models.CharField(max_length=9)

    TSHIRT_SIZE_CHOICES = (
        ('sm', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
        ('xl', 'Extra Large'),
    )
    tshirt_size = models.CharField(max_length=2, choices=TSHIRT_SIZE_CHOICES, default='sm')

