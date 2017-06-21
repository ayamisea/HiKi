from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy

def user_valid(function=None, redirect_url=None):
    """The requet is redirected to ``redirect_url`` (``user_dashboard`` by
    default) if the user is valid.
    """
    if redirect_url is None:
        redirect_url = reverse_lazy(settings.DASHBOARD_URL)

    actual_decorator = user_passes_test(
        lambda u: u.is_valid_user,
        login_url=redirect_url, redirect_field_name=None,
    )

    if function:
        return actual_decorator(function)
    return actual_decorator
