from django.contrib import admin

# Register your models here.
from cart.models import Goods


class GoodsAdmin(admin.ModelAdmin):
    """
    注册一个管理员
    """

    list_display = ('id', 'name', 'price', 'image')
    search_fields = ('name', )


admin.site.register(Goods, GoodsAdmin)