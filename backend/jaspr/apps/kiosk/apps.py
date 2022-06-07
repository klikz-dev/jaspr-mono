from types import MethodType

from django.apps import AppConfig

_auth_token_original_get_queryset_ = None
_manager = None

def _get_queryset_with_jaspr_session_(self):
    qs = _auth_token_original_get_queryset_()
    qsr = qs.select_related("jaspr_session")
    return qsr


class KioskConfig(AppConfig):
    name = "jaspr.apps.kiosk"
    verbose_name = "Kiosk"

    def ready(self):
        # Make `_auth_token_original_get_queryset_` global. We will only populate it
        # once with the original `AuthToken.objects.get_queryset` method (whatever
        # manager instance method that resolves to). That way,
        # `_get_queryset_with_jaspr_session_` can have it available to call.
        global _auth_token_original_get_queryset_
        global _manager

        from knox.models import AuthToken, AuthTokenManager

        # Since `ready` can potentially be called more than once in some circumstances
        # (see Django docs), we want to be careful to make this section of code work
        # properly if that ever happens.
        #if (
        #    AuthToken.objects.get_queryset.__func__.__qualname__
        #    != _get_queryset_with_jaspr_session_.__qualname__
        #    and _auth_token_original_get_queryset_ is None
        #):
        #    _auth_token_original_get_queryset_ = AuthToken.objects.get_queryset
        #    AuthToken.objects.get_queryset = MethodType(
        #        _get_queryset_with_jaspr_session_, AuthToken.objects
        #    )
        #    print(AuthToken.objects.get_queryset)

        if AuthToken.objects != _manager:
            _manager = AuthTokenManager()
            _manager.model = AuthToken
            _auth_token_original_get_queryset_ = _manager.get_queryset
            _manager.get_queryset = MethodType(
                _get_queryset_with_jaspr_session_, _manager
            )
            AuthToken.objects = _manager
