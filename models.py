from django.db import models
from django.contrib.auth import get_user_model

class PhotoItem(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=None)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Directory(PhotoItem, models.Model):
    relative_path = models.CharField(max_length=127, unique=True, null=False)

    class Meta:
        verbose_name_plural = "directories"

    def __str__(self):
        return self.relative_path

    def clean(self):
        if self.relative_path:
            self.relative_path = (
                self.relative_path.strip().replace("\\", "/").strip("/")
            )


class Image(PhotoItem, models.Model):
    file_name = models.CharField(max_length=127)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, default=None)
    file_size = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    type = models.CharField(max_length=15)
    time_taken = models.DateTimeField(null=True)

    def __str__(self):
        return self.directory.relative_path + "/" + self.file_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["directory", "file_name"], name="unique_file_name"
            )
        ]
