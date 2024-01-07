from django.contrib import admin

# Admin header change
admin.site.site_header = "University Blog"


# Register your models here.
def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    message_bit = "Published"
    modeladmin.message_user(request, "{} article {}".format(rows_updated, message_bit))


make_published.short_description = "Publish selected articles"


def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status='d')
    message_bit = "Drafted"
    modeladmin.message_user(request, "{} article {}".format(rows_updated, message_bit))


make_draft.short_description = "Draft selected articles"
