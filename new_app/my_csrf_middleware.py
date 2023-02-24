from django.middleware.csrf import CsrfViewMiddleware

class MyCsrfViewMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('MyCsrfViewMiddleware process_view request', request.COOKIES)
        return super().process_view(request, callback, callback_args, callback_kwargs)

    def process_response(self, request, response):
        print('MyCsrfViewMiddleware process_response request', request)
        return super().process_response(request, response)
