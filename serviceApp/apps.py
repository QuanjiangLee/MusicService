#from django.apps import AppConfig


def is_logined(request):
    login_user=request.session.get('login_user',None)
    user_grant=request.session.get('user_grant',None)
    #print('login_user is',login_user)
    print('user_grant is',user_grant)
    if login_user is None:
        return False
    if user_grant == 1:
        return 'admin'
    elif user_grant == 0:
        return 'user' 
    return False

def get_user_grant(request):
    user_grant = {}
    if is_logined(request) is False:
        user_grant = "custom"
    elif is_logined(request) == 'user':
        user_grant = "user"
    elif is_logined(request) == 'admin':
        user_grant = "admin"
    else:
        user_grant = "custom"
    return user_grant
