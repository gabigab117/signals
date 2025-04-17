from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, **kwargs):
        if not email:
            raise ValueError("L'email est requis")
        if not first_name:
            raise ValueError("Le prénom est requis")
        if not last_name:
            raise ValueError("Le nom est requis")
        email = self.normalize_email(email)
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if kwargs.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")
        return self.create_user(email, first_name, last_name, password, **kwargs)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return self.email


class Profile(models.Model):
     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Utilisateur")
     is_seller = models.BooleanField(default=True, verbose_name="Vendeur")
     
     class Meta:
         verbose_name = "Profil"
         verbose_name_plural = "Profils"
 
     def __str__(self):
         return self.user.email

"""
Déclenche tous les pre_save enregistrés.

Fait la sauvegarde réelle (INSERT ou UPDATE).

Déclenche tous les post_save.


Sender : l’émetteur. C’est généralement un modèle ou un événement de Django (ex: .save(), .delete()...).

Signal : c’est un canal de communication. Ex : post_save, pre_delete, etc.

Receiver : c’est une fonction que tu branches au signal. Elle sera appelée automatiquement quand le signal est déclenché.
"""


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_delete, sender=CustomUser)
def print_delete_message(sender, instance, **kwargs):
    print(f"{instance} supprimée")


@receiver(pre_save, sender=CustomUser)
def print_pre_message(sender, instance, **kwargs):
    print(f"{instance} va être sauvegardée")


@receiver(post_save, sender=CustomUser)
def print_post_message(sender, instance, created, **kwargs):
    print(f"{instance} a été sauvegardée")


@receiver(user_logged_in)
def print_login_message(sender, request, user, **kwargs):
    print(f"{user} s'est connecté")
    # Envoi de mail
    # Maj et mettre le statut à en ligne
