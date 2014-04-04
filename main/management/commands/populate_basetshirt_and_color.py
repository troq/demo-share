from django.core.management.base import BaseCommand
from main.models import BaseTshirt, Color
basetshirts = [
    {
        'basetshirt': {
            "type": "tshirt", 
            "name": "Anvil 4.5 oz. Ringspun T-Shirt", 
            "url": "https://www.nesclothing.com/cgi-bin/online/webshr/prod-detail.w?sr=980&currentColor=00", 
            "description": "Ringspun tshirts are the highest quality tshirts available. They're light and extremely comfortable.", 
            "white_price": 2.57, 
        },
        "colors": [
            {
                "name": "white", 
                "code": "#ffffff", 
                "price": 2.57, 
                "url_code": "00"
            }, 
            {
                "name": "heather blue", 
                "code": "#3d4e86", 
                "price": 3.58, 
                "url_code": "98"
            }, 
            {
                "name": "light blue", 
                "code": "#82aace", 
                "price": 3.58, 
                "url_code": "62"
            }, 
            {
                "name": "storm grey", 
                "code": "#838185", 
                "price": 3.58, 
                "url_code": "07"
            }, 
            {
                "name": "caribbean blue", 
                "code": "#03a0c6", 
                "price": 3.58, 
                "url_code": "21"
            }, 
            {
                "name": "lake", 
                "code": "#434a5d", 
                "price": 3.58, 
                "url_code": "08"
            }, 
            {
                "name": "green apple", 
                "code": "#058e4b", 
                "price": 3.58, 
                "url_code": "AC"
            }, 
            {
                "name": "royal blue", 
                "code": "#17468c", 
                "price": 3.58, 
                "url_code": "53"
            }, 
            {
                "name": "heather purple", 
                "code": "#644684", 
                "price": 3.58, 
                "url_code": "AS"
            }, 
            {
                "name": "purple", 
                "code": "#482c5d", 
                "price": 3.58, 
                "url_code": "63"
            }, 
            {
                "name": "hot pink", 
                "code": "#e23e7a", 
                "price": 3.58, 
                "url_code": "16"
            }, 
            {
                "name": "independence red", 
                "code": "#8c1d2e", 
                "price": 3.58, 
                "url_code": "52"
            }, 
            {
                "name": "mandarin orange", 
                "code": "#f08833", 
                "price": 3.58, 
                "url_code": "09"
            }, 
            {
                "name": "orange", 
                "code": "#e44b22", 
                "price": 3.58, 
                "url_code": "59"
            }, 
            {
                "name": "spring yellow", 
                "code": "#fdf895", 
                "price": 3.58, 
                "url_code": "AD"
            }, 
            {
                "name": "chocolate", 
                "code": "#2e1a1b", 
                "price": 3.58, 
                "url_code": "68"
            }, 
            {
                "name": "silver", 
                "code": "#c0bcbd", 
                "price": 3.58, 
                "url_code": "19"
            }, 
            {
                "name": "charcoal", 
                "code": "#58575d", 
                "price": 3.58, 
                "url_code": "43"
            }, 
            {
                "name": "black", 
                "code": "#000000", 
                "price": 3.58, 
                "url_code": "51"
            }, 
            {
                "name": "key lime", 
                "code": "#acca42", 
                "price": 3.58, 
                "url_code": "14"
            }, 
            {
                "name": "heather green", 
                "code": "#017d58", 
                "price": 3.58, 
                "url_code": "44"
            }, 
            {
                "name": "khaki", 
                "code": "#ae9e86", 
                "price": 3.58, 
                "url_code": "22"
            }, 
            {
                "name": "mocha", 
                "code": "#6c5243", 
                "price": 3.58, 
                "url_code": "48"
            }, 
            {
                "name": "moss", 
                "code": "#91907d", 
                "price": 3.58, 
                "url_code": "AT"
            }, 
            {
                "name": "ocean blue", 
                "code": "#33435f", 
                "price": 3.58, 
                "url_code": "AX"
            }
        ]
    }, 
    {
        'basetshirt': {
            "type": "tshirt", 
            "name": "Gildan 6 oz. UltraCotton T-Shirt", 
            "url": "https://www.nesclothing.com/cgi-bin/online/webshr/prod-detail.w?sr=G200&currentColor=00", 
            "description": "The combination of low cost and comfort makes the Gildan UltraCotton the most popular t-shirt.",
            "white_price": 1.83, 
        },
        "colors": [
            {
                "name": "old gold", 
                "code": "#b79a72", 
                "price": 2.83, 
                "url_code": "29"
            }, 
            {
                "name": "citrus yellow", 
                "code": "#fff2ae", 
                "price": 2.83, 
                "url_code": "AK"
            }, 
            {
                "name": "blue dusk", 
                "code": "#223544", 
                "price": 2.83, 
                "url_code": "57"
            }, 
            {
                "name": "safety pink", 
                "code": "#f86994", 
                "price": 2.83, 
                "url_code": "AN"
            }, 
            {
                "name": "safety green", 
                "code": "#c6d61e", 
                "price": 2.83, 
                "url_code": "38"
            }, 
            {
                "name": "white", 
                "code": "#ffffff", 
                "price": 1.83, 
                "url_code": "00"
            }, 
            {
                "name": "forest green", 
                "code": "#223d38", 
                "price": 2.83, 
                "url_code": "44"
            }, 
            {
                "name": "olive", 
                "code": "#473e21", 
                "price": 2.83, 
                "url_code": "13"
            }, 
            {
                "name": "military green", 
                "code": "#4b504a", 
                "price": 2.83, 
                "url_code": "75"
            }, 
            {
                "name": "irish green", 
                "code": "#02a266", 
                "price": 2.83, 
                "url_code": "83"
            }, 
            {
                "name": "kelly green", 
                "code": "#01855e", 
                "price": 2.83, 
                "url_code": "26"
            }, 
            {
                "name": "lime", 
                "code": "#83c259", 
                "price": 2.83, 
                "url_code": "41"
            }, 
            {
                "name": "jade dome", 
                "code": "#01948c", 
                "price": 2.83, 
                "url_code": "17"
            }, 
            {
                "name": "serene green", 
                "code": "#c0caa7", 
                "price": 2.83, 
                "url_code": "04"
            }, 
            {
                "name": "black", 
                "code": "#000000", 
                "price": 2.83, 
                "url_code": "51"
            }, 
            {
                "name": "charcoal", 
                "code": "#4d515a", 
                "price": 2.83, 
                "url_code": "43"
            }, 
            {
                "name": "sport grey", 
                "code": "#c3bec4", 
                "price": 2.83, 
                "url_code": "95"
            }, 
            {
                "name": "ice grey", 
                "code": "#d3ceca", 
                "price": 2.83, 
                "url_code": "23"
            }, 
            {
                "name": "ash grey", 
                "code": "#d4d3d9", 
                "price": 2.52, 
                "url_code": "50"
            }, 
            {
                "name": "dark chocolate", 
                "code": "#2f1322", 
                "price": 2.83, 
                "url_code": "78"
            }, 
            {
                "name": "chestnut", 
                "code": "#846563", 
                "price": 2.83, 
                "url_code": "48"
            }, 
            {
                "name": "tan", 
                "code": "#b9a46d", 
                "price": 2.83, 
                "url_code": "24"
            }, 
            {
                "name": "sand", 
                "code": "#d6cabe", 
                "price": 2.83, 
                "url_code": "18"
            }, 
            {
                "name": "prairie dust", 
                "code": "#80776e", 
                "price": 2.83, 
                "url_code": "22"
            }, 
            {
                "name": "camel", 
                "code": "#c2a07b", 
                "price": 2.83, 
                "url_code": "82"
            }, 
            {
                "name": "natural", 
                "code": "#eeebd8", 
                "price": 1.83, 
                "url_code": "20"
            }, 
            {
                "name": "tangerine", 
                "code": "#f48939", 
                "price": 2.83, 
                "url_code": "12"
            }, 
            {
                "name": "honey", 
                "code": "#fab152", 
                "price": 2.83, 
                "url_code": "68"
            }, 
            {
                "name": "gold", 
                "code": "#f9b514", 
                "price": 2.83, 
                "url_code": "56"
            }, 
            {
                "name": "daisy", 
                "code": "#ffd701", 
                "price": 2.83, 
                "url_code": "21"
            }, 
            {
                "name": "vegas gold", 
                "code": "#fde1b1", 
                "price": 2.83, 
                "url_code": "19"
            }, 
            {
                "name": "yellow haze", 
                "code": "#f5d98f", 
                "price": 2.83, 
                "url_code": "05"
            }, 
            {
                "name": "texas orange", 
                "code": "#cc643d", 
                "price": 2.83, 
                "url_code": "25"
            }, 
            {
                "name": "rusty bronze", 
                "code": "#882c31", 
                "price": 2.83, 
                "url_code": "AM"
            }, 
            {
                "name": "paprika", 
                "code": "#b82724", 
                "price": 2.83, 
                "url_code": "37"
            }, 
            {
                "name": "orange", 
                "code": "#e65a1d", 
                "price": 2.83, 
                "url_code": "59"
            }, 
            {
                "name": "safety orange", 
                "code": "#e97c13", 
                "price": 2.83, 
                "url_code": "92"
            }, 
            {
                "name": "maroon", 
                "code": "#4f0230", 
                "price": 2.83, 
                "url_code": "66"
            }, 
            {
                "name": "cherry red", 
                "code": "#c21d2e", 
                "price": 2.83, 
                "url_code": "16"
            }, 
            {
                "name": "red", 
                "code": "#b61827", 
                "price": 2.83, 
                "url_code": "52"
            }, 
            {
                "name": "heather cardinal", 
                "code": "#9e3846", 
                "price": 2.83, 
                "url_code": "96"
            }, 
            {
                "name": "cedar", 
                "code": "#b85750", 
                "price": 2.83, 
                "url_code": "03"
            }, 
            {
                "name": "cardinal red", 
                "code": "#901d3a", 
                "price": 2.83, 
                "url_code": "67"
            }, 
            {
                "name": "antique cherry red", 
                "code": "#831d35", 
                "price": 2.83, 
                "url_code": "71"
            }, 
            {
                "name": "heliconia", 
                "code": "#f43c84", 
                "price": 2.83, 
                "url_code": "30"
            }, 
            {
                "name": "azalea", 
                "code": "#ed72a9", 
                "price": 2.83, 
                "url_code": "01"
            }, 
            {
                "name": "light pink", 
                "code": "#f1bbd3", 
                "price": 2.83, 
                "url_code": "11"
            }, 
            {
                "name": "purple", 
                "code": "#5d3476", 
                "price": 2.83, 
                "url_code": "62"
            }, 
            {
                "name": "violet", 
                "code": "#9998c2", 
                "price": 2.83, 
                "url_code": "63"
            }, 
            {
                "name": "iris", 
                "code": "#287bbd", 
                "price": 2.83, 
                "url_code": "80"
            }, 
            {
                "name": "orchid", 
                "code": "#c9a6c7", 
                "price": 2.83, 
                "url_code": "34"
            }, 
            {
                "name": "navy", 
                "code": "#1f2a4a", 
                "price": 2.83, 
                "url_code": "54"
            }, 
            {
                "name": "royal", 
                "code": "#084d9a", 
                "price": 2.83, 
                "url_code": "53"
            }, 
            {
                "name": "heather navy", 
                "code": "#424558", 
                "price": 2.83, 
                "url_code": "93"
            }, 
            {
                "name": "stone blue", 
                "code": "#7a929e", 
                "price": 2.83, 
                "url_code": "47"
            }, 
            {
                "name": "indigo blue", 
                "code": "#4a6c88", 
                "price": 2.83, 
                "url_code": "08"
            }, 
            {
                "name": "heather indigo", 
                "code": "#4f698a", 
                "price": 2.83, 
                "url_code": "94"
            }, 
            {
                "name": "sapphire", 
                "code": "#0182bc", 
                "price": 2.83, 
                "url_code": "49"
            }, 
            {
                "name": "heather sapphire", 
                "code": "#299dd8", 
                "price": 2.83, 
                "url_code": "39"
            }, 
            {
                "name": "sky", 
                "code": "#74c5d8", 
                "price": 2.83, 
                "url_code": "74"
            }, 
            {
                "name": "metro blue", 
                "code": "#0d418c", 
                "price": 2.83, 
                "url_code": "55"
            }, 
            {
                "name": "galapagos blue", 
                "code": "#005c71", 
                "price": 2.83, 
                "url_code": "AL"
            }, 
            {
                "name": "carolina blue", 
                "code": "#71a8cf", 
                "price": 2.83, 
                "url_code": "77"
            }, 
            {
                "name": "light blue", 
                "code": "#a0c2de", 
                "price": 2.83, 
                "url_code": "64"
            }, 
            {
                "name": "antique royal", 
                "code": "#034895", 
                "price": 2.83, 
                "url_code": "AJ"
            }
        ]
    }, 
]

class Command(BaseCommand):
    help = 'populates the database BaseTshirt model with basetshirts and their colors'

    def handle(self, *args, **options):
        BaseTshirt.objects.all().delete()
        Color.objects.all().delete()

        for basetshirt in basetshirts:
            new_basetshirt = BaseTshirt.objects.create(**basetshirt['basetshirt'])
            for color in basetshirt['colors']:
                new_basetshirt.colors.create(**color)
        self.stdout.write('Successfully populated the database BaseTshirt model with basetshirt and their colors.')
