from django.db import models
from directory.base_models import TimestampedModel

class Directory(TimestampedModel):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('lifestyle', 'Lifestyle'),
        ('travel', 'Travel'),
        ('food', 'Food'),
        ('fashion', 'Fashion'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('health', 'Health'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('science', 'Science'),
        ('art', 'Art'),
        ('music', 'Music'),
        ('books', 'Books'),
        ('business', 'Business'),
        ('fitness', 'Fitness'),
        ('cooking', 'Cooking'),
        ('pets', 'Pets'),
        ('gaming', 'Gaming'),
        ('other', 'Other'),
    ]
    domain = models.CharField(max_length=100, null=False, unique=True)
    title = models.TextField(default="")
    description = models.TextField(default="")
    da = models.IntegerField(default=0)
    moz_rank = models.IntegerField(default=0)
    semrush_rank = models.IntegerField(default=0)
    facebook_like = models.FloatField(default=0)
    worth = models.FloatField(default=0)
    image_url = models.CharField(max_length=255, default="")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
    )

    def __str__(self):
        return self.domain
    class Meta:
        app_label = 'directory' 