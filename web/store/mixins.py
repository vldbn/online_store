from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from store.models import Wish


class WishMixin:
    """Mixin for views with like button."""

    def post(self, request, **kwargs):
        user = User.objects.get(id=request.user.id)
        if 'wish' in request.POST:
            product_id = request.POST.get('wish')
            Wish.objects.create(
                user=user,
                product_id=product_id
            )
        if 'del' in request.POST:
            product_id = request.POST.get('del')
            wishes = Wish.objects.filter(product_id=product_id)
            wish = wishes.filter(user_id=user.id)
            wish.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
