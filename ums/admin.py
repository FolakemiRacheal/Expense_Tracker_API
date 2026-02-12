from django.contrib import admin

# # Register your models here.
# from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from .models import UserProfile


# User = get_user_model()


# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     fields = ["date_of_birth", "profile_picture"]
#     readonly_fields = ["created_at", "updated_at"]


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     list_display = [
#         "id",
#         "username",
#         "email",
#         "is_staff",
#         "is_superuser",
#         "is_active",
#         "date_joined",
#     ]
#     search_fields = ["username", "email"]
#     fieldsets = (
#         (None, {"fields": ("username", "password")}),
#         (("Personal info"), {"fields": ("email",)}),
#         (
#             ("Permissions"),
#             {
#                 "fields": (
#                     "is_active",
#                     "is_staff",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 ),
#             },
#         ),
#         (("Important dates"), {"fields": ("last_login", "date_joined")}),
#     )
#     readonly_fields = ("last_login", "date_joined")
#     ordering = ("-date_joined",)


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ["user", "date_of_birth"]
#     search_fields = ["user__email", "user__username"]
#     raw_id_fields = ["user"]
#     readonly_fields = ["created_at", "updated_at"]

