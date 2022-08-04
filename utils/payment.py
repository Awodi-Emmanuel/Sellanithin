from email import header
# from random import random
from urllib import response
from Ecom import settings
import math, requests
import random


def process_payment(name, email, amount, phone):
    auth_token = (settings.SECRET_KEY2)
    hed = {'Authorization': 'Bearer' + auth_token}
    data = {
        "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
        "amount":amount,
        "currency":"KES",
        "redirect_url":"http://localhost:8000/callback",
        "payment_options":"card",
        "meta":{
            "consumer_id":23,
            "consumer_mac":"92a3-912ba-1192a",
        },
        "customer":{
            "email":email,
            "phonenumber":phone,
            "name":name,
            "amount":amount
        },
        "customizations":{
            "title":"Supa Electronics Store",
            "description":"Best store in town",
            "logo":"https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
        }
    }
    
    url = 'https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    link=response['data']['link']
    return link
    