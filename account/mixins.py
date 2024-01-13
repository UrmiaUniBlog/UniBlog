from django.shortcuts import redirect


class AuthorizedAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_author \
                or request.user.is_superuser \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account:profile')
