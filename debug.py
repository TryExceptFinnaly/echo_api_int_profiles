import requests

# data = {
#     "study": 'A06.23.008',
#     "purpose": 3,
#     "cito": False,
#     "patient": {
#         "fio": "Ульяна Фомина Ивановна",
#         "birth": "1985-07-04",
#         "polis_number": "1234567890000000",
#         "snils": "112-233-445 95"
#     }
# }

data = {
    "study": 7000011,
    "purpose": 104,
    "cito": False,
    "patient": {
        "fio": "Крошкина Марина Сергеевна",
        "birth": "1980-01-08",
        "polis_number": "0102030405",
        "snils": "156-332-679 72"
    }
}

# url = r'http://77.73.27.195:5002/api-external/add-visit-image-to-mediafile/'
url = r'https://test.ris-x.com:8000/api-external/validity/order/'

headers = {'Content-type': 'application/json',
           'Authorization': 'Token szq5hnfk4Hw3yhjlxYgp'}
           #'Authorization': 'Token 4y2DYuHpZdAAMz2VxJK5'}

post_study = requests.post(url, verify=False, headers=headers, json=data)
print(f'STATUS_CODE: {post_study.status_code}')
print(f'RESPONSE: {post_study.text}')
