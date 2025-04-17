from django.contrib import admin
from .models import CustomUser, Profile
from django.contrib.auth.admin import UserAdmin


admin.site.register(Profile)

class CustomUserAdmin(UserAdmin):
   model = CustomUser
   
   # Configuration de la liste des utilisateurs
   list_display = ("email", "is_staff", "is_active",)
   list_filter = ("email", "is_staff", "is_active",)
   search_fields = ("email", "zip_code",)
   ordering = ("email",)

   # Configuration du formulaire d'édition
   fieldsets = (
       (None, {"fields": ("email", "password")}),
       ("Informations personnelles", {"fields": ("first_name", "last_name")}),
       ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
       ("Dates importantes", {"fields": ("last_login", "date_joined")}),
   )

   # Configuration du formulaire de création
   add_fieldsets = (
       (None, {
           "classes": ("wide",),
           "fields": (
               "email", "password1", "password2",
               "is_staff", "is_active", "groups", "user_permissions", "is_superuser"
           )}
       ),
   )

admin.site.register(CustomUser, CustomUserAdmin)
