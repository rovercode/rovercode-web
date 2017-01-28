from django.db import models

class Rover(models.Model):
    name = models.TextField()
    owner = models.TextField()
    local_ip = models.TextField()
    last_checkin = models.DateTimeField()

    def __str__(self):
        return self.name
