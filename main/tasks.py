"""    !!!!!!!!!!!!!!!"""
"""    there are todos"""
"""    !!!!!!!!!!!!!!!"""

from django.conf import settings

from celery import shared_task
from PIL import Image
from firebase import Firebase
from firebase_token_generator import create_token
import cStringIO
import stripe

from main.utils import new_tshirt_image
from main.models import Tshirt, Payment

@shared_task
def complete_campaign(tshirt_pk):
    #todo: get shipping cost w/ easypost and charge customer, complete campaign
    return

@shared_task
def create_customer(payment_pk, stripe_token):
    """creates a customer using stripe_token and saves the customer id into the payment

    :payment_pk: pk of Payment
    :stripe_token: stripe token
    :returns: nothing

    """
    payment = Payment.objects.get(pk=payment_pk)

    try:
        customer = stripe.Customer.create(
            card        =  stripe_token,
            description =  'Custom shirt',
            email       =  payment.email,
            api_key     =  settings.STRIPE_SECRET_KEY,
        )
    except:
        # customer creation failed
        payment.delete()
    else:
        # customer creation succeeded
        payment.customer_id = customer.id
        payment.save()

@shared_task
def set_tshirt_image(new_tshirt_image_front_args, new_tshirt_image_back_args, new_tshirt_pk):
    #converts the base64 image string into a pil Image
    #for front
    tempimg = cStringIO.StringIO(new_tshirt_image_front_args[2].decode('base64'))
    new_tshirt_image_front_args[2] = Image.open(tempimg)
    #for back
    tempimg_back = cStringIO.StringIO(new_tshirt_image_back_args[2].decode('base64'))
    new_tshirt_image_back_args[2] = Image.open(tempimg_back)

    #creates the new tshirt image as a django ContentFile
    #for front
    tshirt_image = new_tshirt_image(*new_tshirt_image_front_args)
    #for back
    tshirt_image_back = new_tshirt_image(*new_tshirt_image_back_args)

    #sets the new tshirt image to the tshirt image with the user id + a uuid as filename
    new_tshirt = Tshirt.objects.get(pk=new_tshirt_pk)
    new_tshirt_pk_str = str(new_tshirt_pk)
    new_tshirt.image.save(new_tshirt_pk_str, tshirt_image)
    new_tshirt.image_back.save(new_tshirt_pk_str+'b', tshirt_image_back)

    firebase_token = create_token(settings.FIREBASE_SECRET, None, {'admin': True})
    tshirtRef = Firebase(settings.FIREBASE_URL+str(new_tshirt_pk), auth_token=firebase_token)
    tshirtRef.set(new_tshirt.image.url)
