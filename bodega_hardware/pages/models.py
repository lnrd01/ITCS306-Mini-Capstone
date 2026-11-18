from django.db import models


class SiteSettings(models.Model):
    """One row of editable landing-page content (edit it in the admin)."""

    about_title = models.CharField(max_length=150, default="Tools for every job, in one place")
    about_text = models.TextField(
        default="Bodega Hardware supplies tools, fasteners and building materials "
        "for homeowners, contractors and workshops."
    )
    address = models.CharField(max_length=255, default="Your location")
    phone = models.CharField(max_length=50, default="09XX-XXX-XXXX")
    email = models.EmailField(default="hello@example.com")

    class Meta:
        verbose_name_plural = "site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # only ever one row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"
