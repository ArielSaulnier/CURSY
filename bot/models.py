from tortoise.models import Model
from tortoise import fields


class GuildConfig(Model):
    id = fields.BigIntField(pk=True, unique=True, nullable=False)
    prefix = fields.TextField(nullable=True, default="$")
    welcome_enabled = fields.BooleanField(default=False)
    leave_enabled = fields.BooleanField(default=False)


class WelcomeConfig(Model):
    id = fields.BigIntField(pk=True, unique=True, nullable=False)
    channel_id = fields.BigIntField(nullable=False)
    message = fields.TextField(nullable=True)


class LeaveConfig(Model):
    id = fields.BigIntField(pk=True, unique=True, nullable=False)
    channel_id = fields.BigIntField(nullable=False)
    message = fields.TextField(nullable=True)
