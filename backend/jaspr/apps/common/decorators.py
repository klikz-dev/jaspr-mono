import functools

from django.http import HttpRequest
from rest_framework.request import Request


class classproperty(property):
    """
    Similar to `property`, but allows class-level properties.  That is,
    a property whose getter is like a `classmethod`.
    The wrapped method may explicitly use the `classmethod` decorator (which
    must become before this decorator), or the `classmethod` may be omitted
    (it is implicit through use of this decorator).
    .. note::
        classproperty only works for *read-only* properties.  It does not
        currently allow writeable/deletable properties, due to subtleties of how
        Python descriptors work.  In order to implement such properties on a class
        a metaclass for that class must be implemented.
    Parameters
    ----------
    fget : callable
        The function that computes the value of this property (in particular,
        the function when this is used as a decorator) a la `property`.
    doc : str, optional
        The docstring for the property--by default inherited from the getter
        function.
    lazy : bool, optional
        If True, caches the value returned by the first call to the getter
        function, so that it is only called once (used for lazy evaluation
        of an attribute).  This is analogous to `lazyproperty`.  The ``lazy``
        argument can also be used when `classproperty` is used as a decorator
        (see the third example below).  When used in the decorator syntax this
        *must* be passed in as a keyword argument.
    Examples
    --------
    ::
        >>> class Foo:
        ...     _bar_internal = 1
        ...     @classproperty
        ...     def bar(cls):
        ...         return cls._bar_internal + 1
        ...
        >>> Foo.bar
        2
        >>> foo_instance = Foo()
        >>> foo_instance.bar
        2
        >>> foo_instance._bar_internal = 2
        >>> foo_instance.bar  # Ignores instance attributes
        2
    As previously noted, a `classproperty` is limited to implementing
    read-only attributes::
        >>> class Foo:
        ...     _bar_internal = 1
        ...     @classproperty
        ...     def bar(cls):
        ...         return cls._bar_internal
        ...     @bar.setter
        ...     def bar(cls, value):
        ...         cls._bar_internal = value
        ...
        Traceback (most recent call last):
        ...
        NotImplementedError: classproperty can only be read-only; use a
        metaclass to implement modifiable class-level properties
    When the ``lazy`` option is used, the getter is only called once::
        >>> class Foo:
        ...     @classproperty(lazy=True)
        ...     def bar(cls):
        ...         print("Performing complicated calculation")
        ...         return 1
        ...
        >>> Foo.bar
        Performing complicated calculation
        1
        >>> Foo.bar
        1
    If a subclass inherits a lazy `classproperty` the property is still
    re-evaluated for the subclass::
        >>> class FooSub(Foo):
        ...     pass
        ...
        >>> FooSub.bar
        Performing complicated calculation
        1
        >>> FooSub.bar
        1

    Thanks to http://docs.astropy.org/en/stable/_modules/astropy/utils/decorators.html#classproperty
    (https://github.com/astropy/astropy/blob/master/astropy/utils/decorators.py)
    for the code.
    """

    def __new__(cls, fget=None, doc=None, lazy=False):
        if fget is None:
            # Being used as a decorator--return a wrapper that implements
            # decorator syntax
            def wrapper(func):
                return cls(func, lazy=lazy)

            return wrapper

        return super().__new__(cls)

    def __init__(self, fget, doc=None, lazy=False):
        self._lazy = lazy
        if lazy:
            self._cache = {}
        fget = self._wrap_fget(fget)

        super().__init__(fget=fget, doc=doc)

        # There is a buglet in Python where self.__doc__ doesn't
        # get set properly on instances of property subclasses if
        # the doc argument was used rather than taking the docstring
        # from fget
        # Related Python issue: https://bugs.python.org/issue24766
        if doc is not None:
            self.__doc__ = doc

    def __get__(self, obj, objtype):
        if self._lazy and objtype in self._cache:
            return self._cache[objtype]

        # The base property.__get__ will just return self here;
        # instead we pass objtype through to the original wrapped
        # function (which takes the class as its sole argument)
        val = self.fget.__wrapped__(objtype)

        if self._lazy:
            self._cache[objtype] = val

        return val

    def getter(self, fget):
        return super().getter(self._wrap_fget(fget))

    def setter(self, fset):
        raise NotImplementedError(
            "classproperty can only be read-only; use a metaclass to "
            "implement modifiable class-level properties"
        )

    def deleter(self, fdel):
        raise NotImplementedError(
            "classproperty can only be read-only; use a metaclass to "
            "implement modifiable class-level properties"
        )

    @staticmethod
    def _wrap_fget(orig_fget):
        if isinstance(orig_fget, classmethod):
            orig_fget = orig_fget.__func__

        # Using stock functools.wraps instead of the fancier version
        # found later in this module ((astropy module)),
        # which is overkill for this purpose

        @functools.wraps(orig_fget)
        def fget(obj):
            return orig_fget(obj.__class__)

        return fget


def drf_sensitive_post_parameters(*parameters):
    """
    Indicate which POST parameters used in the decorated view are sensitive,
    so that those parameters can later be treated in a special way, for example
    by hiding them when logging unhandled exceptions.
    Accept two forms:
    * with specified parameters:
        @sensitive_post_parameters('password', 'credit_card')
        def my_view(request):
            pw = request.POST['password']
            cc = request.POST['credit_card']
            ...
    * without any specified parameters, in which case consider all
      variables are sensitive:
        @sensitive_post_parameters()
        def my_view(request)
            ...

    NOTE: Code has been modified from Django source to work with DRF.
    Here is a link to the reference implementation before modification:
    https://github.com/django/django/blob/b9cf764be62e77b4777b3a75ec256f6209a57671/django/views/decorators/debug.py

    Here is the issue in DRF that noted doing this is a possible solution:
    https://github.com/encode/django-rest-framework/issues/2768
    """

    def decorator(view):
        @functools.wraps(view)
        def sensitive_post_parameters_wrapper(request, *args, **kwargs):
            assert isinstance(request, (HttpRequest, Request)), (
                "sensitive_post_parameters didn't receive an HttpRequest or Request. "
                "If you are decorating a classmethod, be sure to use "
                "@method_decorator."
            )
            request.sensitive_post_parameters = parameters or "__ALL__"
            # Set the attribute on the wrapped _request also just in case if
            # we have a DRF Request.
            if isinstance(request, Request) and hasattr(request, "_request"):
                request._request.sensitive_post_parameters = (
                    request.sensitive_post_parameters
                )
            return view(request, *args, **kwargs)

        return sensitive_post_parameters_wrapper

    return decorator
