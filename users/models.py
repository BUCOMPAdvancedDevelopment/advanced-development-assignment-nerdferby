from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default.jpg", upload_to="profile_pics")
    karma = models.IntegerField(default=0)

    # def count_strikes(self):
    #     """
    #     Returns
    #     :return:
    #     """
    #     issued = Strike.objects.filter(user=self.user, strike_type="A").count()
    #     redacted = Strike.objects.filter(user=self.user, strike_type="R").count()
    #     return issued - redacted

    def __str__(self):
        """
        @return: Human readable name for the model
        @rtype: string
        """
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        """
        This overrides the default save function for profile so it can resize image to
        300px after saving. It first uploads the user's image, resizes and saves
        """
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
