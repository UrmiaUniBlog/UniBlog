from django import forms

from blog.models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super(CommentForm, self).__init__(*args, **kwargs)

        if not user.is_superuser:
            self.fields['user'].disabled = True
            self.fields['article'].disabled = True
            self.fields['body'].disabled = True

    class Meta:
        model = Comment
        fields = ('user', 'article', 'body', 'status')
