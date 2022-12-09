from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User


REVIEW_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)


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
    review = models.CharField(_("review choices"), max_length=20, null=True, blank=True, choices=REVIEW_CHOICES)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def __str__(self):
        return self.text


class Like(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_by')
    liked_on = models.ForeignKey(IdeaBook, on_delete=models.CASCADE, related_name='liked_on')
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
