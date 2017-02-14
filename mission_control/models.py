from django.db import models
from rovercode_web.users.models import User

class Rover(models.Model):
    name = models.TextField()
    owner = models.TextField()
    local_ip = models.TextField()
    last_checkin = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BlockDiagram(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField()
    content = models.TextField()

    def __str__(self):
        return self.name
