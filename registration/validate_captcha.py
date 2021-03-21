import requests
import json

def validate_captcha(request):
    recaptcha_client_key = request.POST['g-recaptcha-response']

    recaptcha_api_url = 'https://www.google.com/recaptcha/api/siteverify'
    recaptcha_data = {
        'secret': '6Lca6PAZAAAAAAMMzLDQFZBUxjEr3oyhanRDrds8',
        'response': recaptcha_client_key
    }

    verify_recaptcha = requests.post(recaptcha_api_url, recaptcha_data)
    response_json = verify_recaptcha.text
    response_obj = json.loads(response_json)
    user_verify = response_obj['success']
    
    return True if user_verify else False