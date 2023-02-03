import requests

# url = r'http://77.73.27.195:5002/api-external/add-visit-image-to-mediafile/'
# url = r'https://test.ris-x.com:8000/api-external/validity/order/'
url = r'https://nt.ris-x.com:8000/api-admin/user/36/?expand=tz,_links,category,specialty,position,work_places.room.department.lpu,consults_place.lpu_source,consults_place.lpu_target,roles.role,available_roles,image_view_interfaces,eris_emias_code'

headers = {'Content-type': 'application/json',
           'Authorization': 'Token szq5hnfk4Hw3yhjlxYgp'}
           #'Authorization': 'Token 4y2DYuHpZdAAMz2VxJK5'}

# post_study = requests.post(url, verify=False, headers=headers, json=data)

get_requests = requests.get(url)

print(f'STATUS_CODE: {get_requests.status_code}')
print(f'RESPONSE: {get_requests.text}')
