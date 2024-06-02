import json

from .models import User

def login_validation(request, pk):
    error_list =[]
    data = json.loads(request.body)
    username = data[username]
    if not username:
        error_list.append("Username should not be blank")
    
    if len(username)<3:
        error_list.append("Name should be greater than 3 character")
    
    email =