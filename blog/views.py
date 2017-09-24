from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .serializers import UserSerializer
from .serializers import UserDetailSerializer
from .serializers import UserUpdateSerializer

from .models import Board
from .util import UserService
# Create your views here.

class Users(APIView):
    #회원 list
    def get(self,request,format=None):
        print(request.data)

        userList = []

        userList = User.objects.all()
        #다수의 데이터 query set을 serialize하려고 할때 many=True를 사용
        serializer = UserSerializer(userList,many=True)

        result = {
            'msg' : 'success',
            'userList' : serializer.data
        }

        return Response({'result':result})

    #회원 등록
    def post(self,request,format=None):
        print(request.data)
        params = request.data

        user = User.objects.create(
            username=params["username"],
            password=make_password(params["password"])
        )
        user.save()

        result = {
            'username': user.username,
            'msg': 'success'
        }
        return Response({'result' : result})

class UserDetail(APIView):
    #특정 회원 조회
    def get(self,request,pk,format=None):
        print(pk)

        user = User.objects.get(pk=pk)

        serializer = UserDetailSerializer(user);

        result = {
            'msg' : 'success',
            'user' : serializer.data
        }
        return Response({'result' : result})

    #특정 회원 데이터 수정
    def put(self,request,pk,format=None):
        print(request.data)
        params = request.data
        user = User.objects.get(pk=pk)
        params['password'] = make_password(params.get('password'))
        serializer = UserUpdateSerializer(data=params)

        result = {
            'msg':'false'
        }

        if serializer.is_valid():
            serializer.save()
            result['msg'] = 'success'

        return Response({'result' : result})


    def delete(self,request,pk,format=None):
        print('pk='+pk)
        params = request.data

        user = User.objects.get(pk=pk)
        user.delete()

        result = {
            'msg' : 'success'
        }

        return Response({'result':result})

#로그인요청에는 토큰을 발급받지 않은 상태이므로 토큰 검사를 행하지 않게 데코레이터를 사용하여 제외 시킴
#AllowAny : 어떤 사용자든 접근 가능
@permission_classes((AllowAny,))
class UserSign(APIView):
    def post(self,request,format=None):
        print(request.data)

        if request.data.get('username') == "" or request.data.get('password') == "":
            result = {
                'msg' : 'false'
            }
            return Response({'result' : result})

        userService = UserService()

        result = userService.authentication(request.data)

        result['msg'] = 'success'

        return Response({'result':result})

class UserSignout(APIView):
    def post(self,request,format=None):
        print(request.data)

        userService = UserService()

        result = userService.logout(request.data,request.META['HTTP_AUTHORIZATION'])

        result['msg'] = 'success'

        return Response({'result':result})

@permission_classes((AllowAny,))
class TokenRefresh(APIView):

    def post(self,request,format=None):
        print(request.data)

        userService = UserService()

        result = userService.token_refresh(request.data)

        result['msg'] = 'success'

        return Response({'result':result})

class Test(APIView):
    def post(self,request,format=None):
        print(request.data)
        raise Exception('error발생')

@permission_classes((AllowAny,))
class BoardView(APIView):
    def get(self,request,format=None):
        print(request.data)
        print('boardview.get')
        items = Board.objects.all()
        item_list = []
        for i in items:
            item_list.append(i.as_json())

        result ={
            'msg' : 'success',
            'items' : item_list
        }
        return Response({'result':result})

    def get_object(self,request,pk,format=None):
        print(request.data)

        item = Board.Objects.get(pk=pk)

        result = {
            'msg' : 'success',
            'item' : item.as_json()
        }

        return Response({'result':result})

    def post(self,request,format=None):
        print(request.data)
        params = request.data
        board = Board.objects.create(
            title=params["title"],
            content=params["content"]
        )
        board.save()
        result = {
            'msg' : 'success',
        }
        return Response({'result':result})
    def put(self,request,format=None):
        print(request.data)
        print('BoardDetailView.put')
        params = request.data
        result = {
            'msg' : 'success'
        }

        board = Board.objects.get(pk=params.get('pk'))

        board.title = params.get('title')
        board.content = params.get('content')

        board.save()

        return Response({'result' : result})

@permission_classes((AllowAny,))
class BoardDetailView(APIView):
    def get(self,request,pk,format=None):
        print(request.data)
        print('BoardDetailView.get')
        item = Board.objects.get(pk=pk)

        result ={
            'msg' : 'success',
            'item' : item.as_json()
        }
        return Response({'result':result})

    def delete(self,request,pk,format=None):
        print(request.data)
        print('BoardDetailView.delete')

        result = {
            'msg' : 'success'
        }

        item = {}

        try:
            item = Board.objects.get(pk=pk)
        except Exception as e:
            result['msg'] = '선택한 게시글이 존재하지 않습니다.'

        try:
            item.delete()
        except Exception as e:
            result['msg'] = '삭제에 실패하였습니다.'

        return Response({'result':result})
