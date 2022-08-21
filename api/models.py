from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follower(models.Model):
    who = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="followers",
    )
    user = models.OneToOneField(
        'Profile',
        on_delete=models.CASCADE,
        primary_key=True,
    )


    def __str__(self):
        return f"{self.user.user} is a follower of {self.who.user}"

class Following(models.Model):
    who = models.ForeignKey(
        "Profile",
        on_delete=models.CASCADE,
        related_name="followings",
    )
    user = models.OneToOneField(
        'Profile',
        on_delete=models.CASCADE,
        primary_key=True,
    )


    def __str__(self):
        return f"{self.who.user} is following {self.user.user}"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    profile_picture = CloudinaryField("image", blank=True)
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
        ("None", ""),
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
        return f"{self.title} - {self.chapter_set.count()} chapters"


class Like(models.Model):
    class LikesChoices(models.IntegerChoices):
        ONE = 1, "Boring"
        TWO = 2, "Normal"
        THREE = 3, "Biased"
        FOUR = 4, "Somewhat Interesting"
        FIVE = 5, "Interesting"

    value = models.IntegerField(choices=LikesChoices.choices, default=1)
    chapter = models.ForeignKey("Chapter", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")

    class Meta:
        ordering = ["chapter"]
        constraints = [
            models.UniqueConstraint(
                fields=["chapter", "user"], name="unique_like_for_user_for_like"
            ),
        ]

    def __str__(self):
        return f"{self.user.username} gave {self.chapter.novel} {self.chapter.chapter_no} ---> {self.value}/5"


class Chapter(models.Model):
    title = models.CharField(max_length=100)
    chapter_no = models.PositiveIntegerField(default=0)
    content = models.TextField()
    novel = models.ForeignKey(Novel, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ch_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    class Meta:
        ordering = ["novel__title", "chapter_no"]
        constraints = [
            models.UniqueConstraint(
                fields=["chapter_no", "novel_id"], name="unique_chapter_in_novel"
            ),
        ]

    def __str__(self):
        return f"{self.novel.title} | Chapter {self.chapter_no} - {self.title} --> {self.comment_set.count()} comments"


class Comment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"{self.chapter.novel.title} - chapter {self.chapter.chapter_no}| Comment {self.id}"


class CommentResponse(models.Model):
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"{self.comment.chapter.novel.title} - chapter {self.comment.chapter.chapter_no} | Comment {self.comment.id} Response {self.id}"
