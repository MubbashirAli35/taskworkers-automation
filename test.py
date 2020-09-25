import requests

dict = {'sameSite': 'Strict', 
        'auth': 'Mubbashir Ali',
        'expiresIn': 123456789,
        'secure': True}

if 'sameSite' in dict:
    print('Good hogaya')
else:
    print('Shughal Maila lagaye rakho')