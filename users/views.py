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
	"""
	This view handles user login
	"""

	request_data = None

	def post(self, request, *args, **kwargs):
		"""This method handles requests made by POST method"""

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
		"""
		This method handles requests made by GET method
		"""

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
	"""
	This view lists users. Because this is a MVP pagination
	is not supported... yet :)
	"""

	def get(self, request, *args, **kwargs):
		"""
		This method handles requests made by GET method
		"""

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
	"""
	This view creates users. It is done by the JSON object it receives
	with the correct parameters.
	"""
	
	request_data = None

	def post(self, request, *args, **kwargs):
		"""
		This method handles post methods, as the other above :)
		"""

		# Maybe you are interested in the line below and you're wondering
		# why this is showed in this way. The answer is simple.
		# self.request.body is the raw body stream, but we want it as JSON
		# so, json.loads parses it to a python dict type to handle it easier.

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