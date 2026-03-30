from import_export import resources, fields
from import_export.widgets import ManyToManyWidget
from .models import Movie, Genre, Actor


class MovieResource(resources.ModelResource):

    genres = fields.Field(
        column_name="genres",
        attribute="genres",
        widget=ManyToManyWidget(Genre, field="name")
    )

    actors = fields.Field(
        column_name="actors",
        attribute="actors",
        widget=ManyToManyWidget(Actor, field="name")
    )

    class Meta:
        model = Movie
        import_id_fields = ("id",)
        fields = (
            "id",
            "title",
            "description",
            "release_year",
            "duration",
            "genres",
            "actors",
            "thumbnail",
            "video",
            "created_at",
        )