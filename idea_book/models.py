from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Tag(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")


class IdeaBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='idea_book')
    title = models.CharField(_("title"), max_length=100)
    tag = models.ManyToManyField(Tag, related_name="idea_book", verbose_name=_("tag"))
    description = models.TextField(_("description"), null=True, blank=True)
    images = models.ImageField(_("images"), upload_to=None, null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.title


class FeedBack(models.Model):
    feedback_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    feedback_on = models.ForeignKey(IdeaBook, on_delete=models.CASCADE, related_name='feedback')
    text = models.TextField(_("text"), null=True, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.text


class Like(models.Model):
    like_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_by')
    like_on = models.ForeignKey(IdeaBook, on_delete=models.CASCADE, related_name='like_on')
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.like_by