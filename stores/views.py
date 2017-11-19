from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from stores.models import Store
from uuid import uuid4

import json


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class StoreDetail(View):
    """
    This view shows store details.
    """
    
    def get(self, request, pk, *args, **kwargs):

        store = None
        try:
            store = Store.objects.get(pk=pk.__str__())
        except Exception as e:
            pass

        if store is not None:
            return JsonResponse({
                'id': store.pk.__str__(),
                'name': store.name,
                'products': store.products
            })
        else:
            return JsonResponse({
                'error': 'Store not exist.'
            })

    def dispatch(self, *args, **kwargs):
        return super(StoreDetail, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UserStores(View):
    """
    This view shows user stores.
    """
    
    def get(self, request, *args, **kwargs):

        stores = None
        try:
            stores = Store.objects.filter(owner=self.request.user)
        except Exception as e:
            pass

        if stores is not None:
            return JsonResponse([{'id': store.pk.__str__(), 'name': store.name} for store in stores], safe=False)
        else:
            return JsonResponse({
                'error': 'User has not stores.'
            })

    def dispatch(self, *args, **kwargs):
        return super(UserStores, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class CreateStore(View):

    request_data = None

    def post(self, request, *args, **kwargs):

        self.request_data = json.loads(self.request.body)

        name = self.request_data['name']
        products = self.request_data['products'] if 'products' in self.request_data else None
        owner = self.request.user
        
        try:
            Store.objects.get(name=name)
            return JsonResponse({
                'msg': 'Name taken.'
            })

        except:
            pass
        
        try:
            json.loads(product)
            return JsonResponse({
                'msg': 'json malformed.'
            })

        except:
            pass

        store = Store(name=name, products=products, owner=owner)
        store.save()
        return JsonResponse({
            'id': store.pk.__str__()
        }, safe=False)

    def dispatch(self, *args, **kwargs):
        return super(CreateStore, self).dispatch(*args, **kwargs)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class AddProducts(View):

    request_data = None

    def post(self, request, *args, **kwargs):

        try:
            self.request_data = json.loads(self.request.body)

        except:
            return JsonResponse({
                'msg': 'json product malformed.'
            })

        store_id = self.request_data['store_id']
        products_json = self.request_data['products'] if 'products' in self.request_data else None
        
        store = None
        products = None

        try:
            store = Store.objects.get(pk=store_id)

        except:
            return JsonResponse({
                'msg': 'Store not found.'
            })

        for obj in products_json:
            obj['id'] = uuid4().__str__()

        if store.products is None:
            store.products = products_json
        else:
            store.products += products_json

        store.save()
        return JsonResponse({
            'products_added': products_json,
            'msg': 'ok'
        })

    def dispatch(self, *args, **kwargs):
        return super(AddProducts, self).dispatch(*args, **kwargs)


