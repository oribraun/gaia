from django.middleware.csrf import CsrfViewMiddleware, InvalidTokenFormat, RejectRequest, _check_token_format, _does_token_match
from django.conf import settings
import logging
import string
from collections import defaultdict
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import DisallowedHost, ImproperlyConfigured
from django.http import UnreadablePostError
from django.http.request import HttpHeaders
from django.urls import get_callable
from django.utils.cache import patch_vary_headers
from django.utils.crypto import constant_time_compare, get_random_string
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import cached_property
from django.utils.http import is_same_domain
from django.utils.log import log_response
from django.utils.regex_helper import _lazy_re_compile

REASON_BAD_ORIGIN = "Origin checking failed - %s does not match any trusted origins."
REASON_NO_REFERER = "Referer checking failed - no Referer."
REASON_BAD_REFERER = "Referer checking failed - %s does not match any trusted origins."
REASON_NO_CSRF_COOKIE = "CSRF cookie not set."
REASON_CSRF_TOKEN_MISSING = "CSRF token missing."
REASON_MALFORMED_REFERER = "Referer checking failed - Referer is malformed."
REASON_INSECURE_REFERER = (
    "Referer checking failed - Referer is insecure while host is secure."
)
# The reason strings below are for passing to InvalidTokenFormat. They are
# phrases without a subject because they can be in reference to either the CSRF
# cookie or non-cookie token.
REASON_INCORRECT_LENGTH = "has incorrect length"
REASON_INVALID_CHARACTERS = "has invalid characters"

class MyCsrfViewMiddleware(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('MyCsrfViewMiddleware process_view request', request.COOKIES)
        self._check_token(request)
        return super().process_view(request, callback, callback_args, callback_kwargs)

    def process_response(self, request, response):
        print('MyCsrfViewMiddleware process_response request', request)
        return super().process_response(request, response)

    def _check_token(self, request):
        # Access csrf_secret via self._get_secret() as rotate_token() may have
        # been called by an authentication middleware during the
        # process_request() phase.
        try:
            csrf_secret = self._get_secret(request)
            print('csrf_secret', csrf_secret)
        except InvalidTokenFormat as exc:
            raise RejectRequest(f"CSRF cookie {exc.reason}.")

        if csrf_secret is None:
            # No CSRF cookie. For POST requests, we insist on a CSRF cookie,
            # and in this way we can avoid all CSRF attacks, including login
            # CSRF.
            raise RejectRequest(REASON_NO_CSRF_COOKIE)

        # Check non-cookie token for match.
        request_csrf_token = ""
        if request.method == "POST":
            try:
                request_csrf_token = request.POST.get("csrfmiddlewaretoken", "")
                print('request_csrf_token', request_csrf_token)
            except UnreadablePostError:
                # Handle a broken connection before we've completed reading the
                # POST data. process_view shouldn't raise any exceptions, so
                # we'll ignore and serve the user a 403 (assuming they're still
                # listening, which they probably aren't because of the error).
                pass

        if request_csrf_token == "":
            # Fall back to X-CSRFToken, to make things easier for AJAX, and
            # possible for PUT/DELETE.
            try:
                # This can have length CSRF_SECRET_LENGTH or CSRF_TOKEN_LENGTH,
                # depending on whether the client obtained the token from
                # the DOM or the cookie (and if the cookie, whether the cookie
                # was masked or unmasked).
                request_csrf_token = request.META[settings.CSRF_HEADER_NAME]
                print('request_csrf_token 2', request_csrf_token)
            except KeyError:
                raise RejectRequest(REASON_CSRF_TOKEN_MISSING)
            token_source = settings.CSRF_HEADER_NAME
            print('token_source', token_source)
        else:
            token_source = "POST"

        try:
            _check_token_format(request_csrf_token)
        except InvalidTokenFormat as exc:
            print('InvalidTokenFormat', exc.reason)
            reason = self._bad_token_message(exc.reason, token_source)
            raise RejectRequest(reason)

        if not _does_token_match(request_csrf_token, csrf_secret):
            print('not _does_token_match', csrf_secret)
            reason = self._bad_token_message("incorrect", token_source)
            raise RejectRequest(reason)
