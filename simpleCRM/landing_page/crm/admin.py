from django.contrib import admin
from .models import Order, StatusCrm, CommentCrm


class Comment(admin.StackedInline):
    model = CommentCrm
    fields = ('comment_dt', 'comment_text')
    readonly_fields = ('comment_dt', )
    extra = 0



class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_status', 'order_name', 'phone', 'order_dt')
    list_display_links = ('id', 'order_name')
    search_fields = ('id', 'order_name', 'phone', 'order_dt')
    list_filter = ('order_status', )
    list_editable = ('order_status', 'phone')
    fields = ('id', 'order_status', 'order_dt', 'order_name', 'phone')
    readonly_fields = ('id', 'order_dt', 'order_name')
    inlines = [Comment]


admin.site.register(Order, OrderAdmin)
admin.site.register(StatusCrm)
admin.site.register(CommentCrm)