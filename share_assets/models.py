from django.db import models
from account.models import User
from uploadAsset.models import uploadAsset
from django.utils import timezone
import shortuuid

class SharedAsset(models.Model):
    EXPIRATION_CHOICES = [
        (86400, '1 Day'),
        (259200, '3 Days'),
        (604800, '1 Week'),
        (2592000, '1 Month'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(uploadAsset, on_delete=models.CASCADE)
    short_url = models.CharField(max_length=22, default=shortuuid.uuid)
    expiration_duration = models.PositiveIntegerField(choices=EXPIRATION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.short_url