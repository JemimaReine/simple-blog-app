from django.contrib import admin
from .models import Post, User,Comment,LikeDislike,Contact

# Register your models here.

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(LikeDislike)
admin.site.register(Contact)
