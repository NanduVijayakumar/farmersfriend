from django.contrib import admin

# Register your models here.
from .models import user_login, user_details

#user_login,user_details,expert_details,crop_type,crop_master,crop_pics,crop_variety,fertilizer_master,
#pesticides_master,disease_master,cultivation_details,cultivation_pics,ask_expert,feedback
from .models import user_login,user_details,expert_details,seller_details,crop_type,crop_master,crop_pics,crop_variety,fertilizer_master
from .models import pesticides_master,disease_master,cultivation_details,ask_expert,feedback,product_details

admin.site.register(user_login)
admin.site.register(user_details)
admin.site.register(expert_details)
admin.site.register(seller_details)
admin.site.register(crop_type)
admin.site.register(crop_master)
admin.site.register(crop_pics)
admin.site.register(crop_variety)
admin.site.register(fertilizer_master)
admin.site.register(pesticides_master)
admin.site.register(disease_master)
admin.site.register(cultivation_details)

admin.site.register(ask_expert)
admin.site.register(feedback)
admin.site.register(product_details)
