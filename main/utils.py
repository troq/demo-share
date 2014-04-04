"""    !!!!!!!!!!!!!!!"""
"""    there are todos"""
"""    !!!!!!!!!!!!!!!"""
from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image
import os
import cStringIO

from main.models import Color, PrintCost

def base_price(num_orders, num_colors, base_tshirt_id, base_tshirt_color):
    """caculates the base price (the sum of the base tshirt cost and the printing cost) in dollars
    @todo: raise exception when num_colors is too great,
    @todo: calculate garment_color somehow,

    :num_orders: the number of tshirt orders
    :num_colors: the number of colors in the design
    :base_tshirt_id: the id of the base tshirt used
    :base_tshirt_color: the hex code/color of the base tshirt
    :returns: base price in dollars

    """

    #this section gets the base tshirt cost
    color = Color.objects.get(basetshirt__id=base_tshirt_id, code=base_tshirt_color)
    base_tshirt_cost = color.price

    #this section gets the printing cost
    if num_colors > 0:
        #todo: add garment color to db
        #garment_color is just set to light for now
        garment_color = 'light' 
        print_cost_object = PrintCost.objects.get(color=garment_color, 
                                           quantity_range_low__lte=num_orders,
                                           quantity_range_high__gte=num_orders)
        #the color cost attribute of PrintCost corresponding to the number of colors
        color_attr = 'color_'+str(num_colors)+'_cost' if num_colors <= 6 else 'color_additional_cost'
        print_cost = getattr(print_cost_object, color_attr)
    else:
        print_cost = 0

    return base_tshirt_cost + print_cost + 2 #2 is our margin

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def new_tshirt_image(base_tshirt, base_tshirt_color, design):
    """creates the image for a new Tshirt by pasting a design onto the base tshirt

    :base_tshirt: type of base tshirt
    :base_tshirt_color: hex color of the base tshirt
    :design: design of size (215, 350) as a pillow.Image object
    :returns: the combined image as a pillow.Image object

    """
    tshirt = Image.open(os.path.join(__location__, 'extra/'+base_tshirt+'.png'))
    background = Image.new('RGB', tshirt.size, base_tshirt_color)

    colored_tshirt = Image.composite(tshirt, background, tshirt)
    colored_tshirt.paste(design, ((tshirt.size[0]-design.size[0])/2, 130), mask=design)

    colored_tshirt_io = cStringIO.StringIO()
    colored_tshirt.save(colored_tshirt_io, format='PNG')

    #returns the tshirt image as a django ContentFile
    return ContentFile(colored_tshirt_io.getvalue())
