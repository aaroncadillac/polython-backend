from django.views import View
from django.http import JsonResponse
from django.core import serializers
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import login, authenticate, logout

from users.models import User
import json


@method_decorator(csrf_exempt, name='dispatch')
class LoginUser(View):

	request_data = None

	def post(self, request, *args, **kwargs):

		self.request_data = json.loads(self.request.body)
		
		username = self.request_data['username']
		password = self.request_data['password']
		user = authenticate(request, username=username, password=password)

		response = None

		if user is not None:
			login(request, user)
			response = JsonResponse({'msg': 'ok'})
			response['Access-Control-Allow-Origin'] = '*'
			return response
		else:
			response = JsonResponse({'msg': 'error'})
			response['Access-Control-Allow-Origin'] = '*'
			return response
		return super(LoginUser, self).get(request, *args, **kwargs)

	def dispatch(self, *args, **kwargs):
		return super(LoginUser, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UserDetail(View):
	def get(self, request, pk, *args, **kwargs):		

		user = None
		try:
			user = User.objects.get(pk=pk.__str__())
		except Exception as e:
			pass

		if user is not None:
			return JsonResponse({
				'id': user.pk.__str__(),
				'username': user.username,
				'email': user.email
			})
		else:
			return JsonResponse({
				'error': 'User not exist.'
			})

	def dispatch(self, *args, **kwargs):
		return super(UserDetail, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ListUsers(View):
	def get(self, request, *args, **kwargs):

		users = [{
			'id': user.pk.__str__(),
			'username': user.username,
			'email': user.email
		} for user in User.objects.filter()]
		print(users)

		return JsonResponse(users, safe=False)

	def dispatch(self, *args, **kwargs):
		return super(ListUsers, self).dispatch(*args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class CreateUser(View):
	
	request_data = None

	def post(self, request, *args, **kwargs):

		self.request_data = json.loads(self.request.body)

		username = self.request_data['username']
		password = self.request_data['password']
		email = self.request_data['email']

		try:
			User.objects.get(username=username)
			return JsonResponse({
				'msg': 'username taken.'
			})

		except:
			pass
		
		try:
			User.objects.get(email=email)
			return JsonResponse({
				'msg': 'email taken.'
			})

		except:
			pass

		user = User.objects.create_user(username, password=password)
		user.email = email
		user.is_superuser= False
		user.save()
		return JsonResponse({
			'id': user.pk.__str__()
		})

	def dispatch(self, *args, **kwargs):
		return super(CreateUser, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
class LogoutUser(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({
			'msg': 'See ya !'
		})