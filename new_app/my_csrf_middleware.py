from django.middleware.csrf import CsrfViewMiddleware

class MyCsrfViewMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('MyCsrfViewMiddleware process_view request', request.COOKIES)
        csrf_secret = self._get_secret(request)
        request_csrf_token = request.POST.get("csrfmiddlewaretoken", "")
        print('MyCsrfViewMiddleware process_view request_csrf_token', request_csrf_token)
        request_csrf_token = request.META
        print('MyCsrfViewMiddleware process_view META', request_csrf_token)
        return super().process_view(request, callback, callback_args, callback_kwargs)

    def process_response(self, request, response):
        print('MyCsrfViewMiddleware process_response request', request)
        return super().process_response(request, response)
