from django.db import models

class Rover(models.Model):
    name = models.TextField()
    owner = models.TextField()
    local_ip = models.TextField()
    last_checkin = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
