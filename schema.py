from .models import Image, Directory
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter.fields import DjangoFilterConnectionField

from graphql_jwt.decorators import login_required
from utils.logger import logger, dump


class ImageNode(DjangoObjectType):
    class Meta:
        model = Image
        filter_fields = (
            "file_name",
            "directory",
            "file_size",
            "width",
            "height",
            "type",
            "time_taken",
        )
        interfaces = (graphene.relay.Node,)

    pk = graphene.Int()

    def resolve_pk(self, info):
        return self.pk


class ImageType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = Image
        fields = (
            "owner",
            "file_name",
            "directory",
            "file_size",
            "width",
            "height",
            "type",
            "time_taken",
        )


class DirectoryNode(DjangoObjectType):
    class Meta:
        model = Directory
        filter_fields = ("owner", "relative_path")
        interfaces = (graphene.relay.Node,)

    pk = graphene.Int()

    def resolve_pk(self, info):
        return self.pk


class DirectoryType(DjangoObjectType):
    id = graphene.ID(source="pk", required=True)

    class Meta:
        model = Directory
        fields = ("relative_path",)


class Query(graphene.ObjectType):
    all_images = graphene.List(ImageType)
    image = graphene.relay.Node.Field(ImageNode)
    images = DjangoFilterConnectionField(ImageNode)

    def resolve_all_images(root, info):
        return Image.objects.all()


class CreateDirectory(graphene.Mutation):
    class Arguments:
        relative_path = graphene.String(required=True)

    directory = graphene.Field(DirectoryType)

    @classmethod
    @login_required
    def mutate(cls, root, info, relative_path):
        directory = Directory(relative_path=relative_path)
        directory.owner = info.context.user
        directory.clean()
        directory.save()
        return CreateDirectory(directory=directory)


class CreateImage(graphene.Mutation):
    class Arguments:
        file_name = graphene.String(required=True)
        relative_path = graphene.String(required=True)
        file_size = graphene.Int(required=True)
        width = graphene.Int(required=True)
        height = graphene.Int(required=True)
        type = graphene.String(required=True)
        time_taken = graphene.String()

    image = graphene.Field(ImageType)

    @classmethod
    @login_required
    def mutate(cls, root, info, **input):
        relative_path = input.pop("relative_path").strip().replace("\\", "/").strip("/")
        try:
            directory = Directory.objects.get(relative_path=relative_path)
        except Directory.DoesNotExist:
            directory = Directory(relative_path=relative_path)
            directory.owner = info.context.user
        directory.save()
        input["directory"] = directory
        image = Image(**input)
        image.owner = info.context.user
        image.clean()
        image.save()
        return CreateImage(image=image)


class Mutation(graphene.ObjectType):
    create_directory = CreateDirectory.Field()
    create_image = CreateImage.Field()
