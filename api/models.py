from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    profile_picture = CloudinaryField("image", blank=True)
    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)
    read_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user", "-created"]
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username.capitalize()} profile"


class Novel(models.Model):
    class NovelStatus(models.TextChoices):
        UPCOMING = "UPG", "Upcoming"
        ONGOING = "ONG", "Ongoing"
        STOPPED = "STP", "Stopped"
        COMPLETED = "CPD", "Completed"
        MOST_POPULAR = "MPL", "Most Popular"
        LATEST_RELEASE = "LTS", "Latest Release"
        HOT_NOVEL = "HOT", "Hot Novel"
        __empty__ = ""

    GENRE_CHOICES = [
        (
            "Fiction",
            (
                ("AAC", "Action and adventure"),
                ("ALH", "Alternate history"),
                ("ANT", "Anthology"),
                ("CHL", "Chick lit"),
                ("CHD", "CHILDREN'S"),
                ("CLS", "Classic"),
            ),
        ),
        (
            "Non Fiction",
            (
                ("ARC", "Art/architecture"),
                ("AUB", "Autobiography"),
            ),
        ),
    ]
    title = models.CharField(max_length=100)
    image = CloudinaryField("image", blank=True)
    description = models.TextField()
    status = models.CharField(
        max_length=3, choices=NovelStatus.choices, default=NovelStatus.UPCOMING
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    view_count = models.PositiveBigIntegerField(default=0)
    genre = models.CharField(max_length=3, choices=GENRE_CHOICES, default="CHD")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    alt_names = models.CharField(max_length=300, null=True)
    source = models.CharField(max_length=300, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created", "title"]

    def __str__(self):
        return self.title


class Chapter(models.Model):
    class LikesChoices(models.IntegerChoices):
        ONE = 1, "Boring"
        TWO = 2, "Normal"
        THREE = 3, "Biased"
        FOUR = 4, "Somewhat Interesting"
        FIVE = 5, "Interesting"

    title = models.CharField(max_length=100)
    chapter_no = models.PositiveIntegerField(default=0, unique=True)
    content = models.TextField()
    likes = models.IntegerField(choices=LikesChoices.choices, default=0)
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["chapter_no"]

    def __str__(self):
        return f"Chapter {self.chapter_no} - {self.title}"


class Comment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    commentor = models.ManyToManyField(User)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"Comment {self.id}"


class CommentResponse(models.Model):
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"Comment {self.comment.id} Response {self.id}"
