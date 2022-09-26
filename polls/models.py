import django.utils.timezone
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# models

class Room(models.Model):
    # Fields
    id = models.AutoField(primary_key=True)
    room_number = models.IntegerField(help_text="Enter the room number")
    room_type = models.ForeignKey('Type', on_delete=models.CASCADE, null=True)

    ROOM_STATUS = (
        ('o', 'Occupied'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=ROOM_STATUS, help_text="room availability", blank=True)

    class Meta:
        ordering = ["room_number"]
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return str(self.room_number)


class Type(models.Model):
    # Fields
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text="Type name of the room", blank=True)
    capacity = models.IntegerField(help_text="Number of people that can stay")
    price = models.IntegerField(help_text="Price for one night")
    description = models.CharField(max_length=200, help_text="Description of the room", blank=True)
    has_wifi = models.BooleanField(default=False)
    has_dryer = models.BooleanField(default=False)
    has_room_service = models.BooleanField(default=False)
    has_breakfast = models.BooleanField(default=False)
    has_air_conditioning = models.BooleanField(default=False)
    has_spa = models.BooleanField(default=False)
    has_mini_bar = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_electronic_safe = models.BooleanField(default=False)


    class Meta:
        ordering = ["id"]
        verbose_name = "Room Type"
        verbose_name_plural = "Room Types"

    def __str__(self):
        return self.name


class Images(models.Model):
    # Fields
    id = models.AutoField(primary_key=True)
    room_type_id = models.ForeignKey(Type, on_delete=models.CASCADE, null=True)
    image = CloudinaryField(blank=True, help_text="Add room image")
    description = models.CharField(max_length=100, help_text="Description of the image", blank=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return str(self.id)


class Profile(models.Model):
    # fields
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = CloudinaryField(blank=True, help_text="Profile picture of user",
                                  default="http://res.cloudinary.com/dfl4tcmei/image/upload/v1524552656/empty_profile.png")
    address = models.CharField(blank=True, help_text="Address of user", max_length=50)

    class Meta:
        ordering = ["id"]
        verbose_name = "hotel User"
        verbose_name_plural = "Hotel Users"

    def __str__(self):
        return self.user_id.first_name + " " + self.user_id.last_name


# TODO: apply check so its only created for non-admin users
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user_id=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Registration(models.Model):
    # fields
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    occupants = models.IntegerField(help_text="number of people staying")
    check_in_date = models.DateTimeField(help_text="Date of check in")
    check_out_date = models.DateTimeField(help_text="Date of check out")
    payment = models.IntegerField(help_text="total expense of rooms")

    class Meta:
        ordering = ["id"]
        verbose_name = "Registration"
        verbose_name_plural = "Registrations"

    def __str__(self):
        return self.user.user_id.first_name + " " + self.user.user_id.last_name + "," + str(id)


class RegistrationDetails(models.Model):
    # fields
    id = models.AutoField(primary_key=True)
    registration_id = models.ForeignKey(Registration, on_delete=models.CASCADE, related_name='details', null=True)
    room_id = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Registration Detail"
        verbose_name_plural = "Registration Details"

    def __str__(self):
        return str(self.registration_id)


class Review(models.Model):
    # fields
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField(help_text="Rating from 1 to 5")
    review = models.CharField(max_length=200, help_text="Review description", blank=True)
    review_date = models.DateField(default=django.utils.timezone.now, blank=True)

    class Meta:
        ordering = ["rating", "review_date"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.user_id.user_id.first_name + " " + self.user_id.user_id.last_name
