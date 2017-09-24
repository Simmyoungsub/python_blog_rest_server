import requests
import json
from django.conf import settings

class UserService():
    def authentication(self,params):
        url = settings.BASE_URL + 'auth/token'
        headers = {'Content-Type' : 'application/json'}
        username = params.get('username')
        params['client_id'] = settings.BLOG_AUTH_CLIENT_ID
        params['client_secret'] = settings.BLOG_AUTH_CLIENT_SECRET
        params['grant_type'] = settings.BLOG_AUTH_GRANT_TYPE

        print('url : ' + url)
        params = json.dumps(params)
        print('params : ' + params)

        try:
            result = requests.post(url,params,headers=headers).json()
            print(result)

            if result.get('error') != None :
                returnValue = {
                    'isUser' : False
                }
            else :
                #refresh token은 별도 db에 저장할 예정이므로 저장후 사용자에게 리턴해줄때 삭제가 필요함(자동으로 갱신되는것인지, 수동으로 갱신해줘야되는지 조사 필요)
                #access_token은 클라이언트에서 웹 storage에 저장
                returnValue = {
                    'access_token' : result.get("access_token"),
                    'refresh_token' : result.get("refresh_token"),
                    'username' : username,
                    'isUser' : True
                }

        except:
            print('util.UserService.authentication() : Error')

            #예외 발생시 리턴되는 데이터 폼
            returnValue = {
                'isUser' : False
            }

        return returnValue

    def logout(self,params,http_authorization):
        url = settings.BASE_URL + 'auth/revoke-token'
        headers = {'Content-Type' : 'application/json'}
        # username = params.get('username')
        params['client_id'] = settings.BLOG_AUTH_CLIENT_ID
        params['client_secret'] = settings.BLOG_AUTH_CLIENT_SECRET
        params['token'] = http_authorization.split()[1]
        # params['grant_type'] = settings.BLOG_AUTH_GRANT_TYPE
        print('url : ' + url)
        params = json.dumps(params)
        print('params : ' + params)

        try:
            result = requests.post(url,params,headers=headers)

            if result.status_code is 204:
                returnValue = {
                    # 'username' : username,
                    'isUser' : True
                }
            else :
                returnValue = {
                    'isUser' : False
                }
        except:
            print('util.UserService.authentication() : Error')

            #예외 발생시 리턴되는 데이터 폼
            returnValue = {
                'isUser' : False
            }

        return returnValue

    def token_refresh(self,params):
        url = settings.BASE_URL + 'auth/token'
        headers = {'Content-Type' : 'application/json'}

        params['client_id'] = settings.BLOG_AUTH_CLIENT_ID
        params['client_secret'] = settings.BLOG_AUTH_CLIENT_SECRET
        params['grant_type'] = settings.BLOG_AUTH_GRANT_REFRESH_TOKEN

        params = json.dumps(params);
        # try:
        print(url)
        print(params)
        result = requests.post(url,params,headers=headers).json()
        print(result)

        if result.get('error') != None :
            returnValue = {
                'isUser' : False
            }
        else :
            #refresh token은 별도 db에 저장할 예정이므로 저장후 사용자에게 리턴해줄때 삭제가 필요함(자동으로 갱신되는것인지, 수동으로 갱신해줘야되는지 조사 필요)
            #access_token은 클라이언트에서 웹 storage에 저장
            returnValue = {
                'isUser' : True,
                'username' : 'user1',
                'access_token': result.get('access_token'),
                'refresh_token' : result.get('refresh_token')
            }

        # except:
        #     print('util.UserService.token_refresh() : Error')
        #
        #     #예외 발생시 리턴되는 데이터 폼
        #     returnValue = {
        #         'isUser' : False
        #     }

        return returnValue
