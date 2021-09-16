from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,BasePermission
from functools import partial
from .models import PermissionsS,Roles,RoleUser,PermissionRole,User
from django.db.models import Q




def user_list(request):
    user_list = {"name":"akshay","email":"akshay@gmail.com"}
    return JsonResponse(user_list, safe=False)

class genericPermissionCheck(BasePermission):
    
    def __init__(self, action, entity):
        self.action = action
        self.entity = entity
    
    def has_permission(self, request, view):
        
        permission = PermissionsS.objects.filter(name = self.action).first()
        role_user = RoleUser.objects.filter(user_id=request.user).first()
        role = Roles.objects.filter(id=role_user.id).first()
        if not role_user and not permission:
            return False
        check_perm = PermissionRole.objects.filter(Q(permission_id = permission) & Q(role_id = role))
        
        if check_perm:
            print('permission granted')            
            return True
        else:
            return False

class DemoView(APIView):
    permission_classes = (IsAuthenticated,partial(genericPermissionCheck,'fetch','Categories'))

    def get(self, request):
        content = {'message': 'Hello,!'}
        return Response(content)


class PersonalInfoView(APIView):
    permission_classes = (IsAuthenticated,partial(genericPermissionCheck,'fetch_personal_info','Categories'))

    def get(self, request):
        content = {'name': 'Akshay'}
        return Response(content)