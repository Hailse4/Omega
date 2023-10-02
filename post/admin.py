from django.contrib import admin
from .models import PostModel ,LikeCount, CommentModel 


admin.site.register(PostModel)
admin.site.register(LikeCount)
admin.site.register(CommentModel)
