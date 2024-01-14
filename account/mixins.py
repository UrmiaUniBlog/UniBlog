from django.shortcuts import redirect


class AuthorizedAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_author \
                or request.user.is_superuser \
                or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account:profile')


class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = [
            "title", "subtitle", "slug", "category",
            "description", "thumbnail", "publish",
            "is_special", "status"
        ]
        if request.user.is_superuser or request.user.is_staff:
            self.fields.append("author")
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser or self.request.user.is_staff:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'r':
                self.obj.status = 'd'
        return super().form_valid(form)
