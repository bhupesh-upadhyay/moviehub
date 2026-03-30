import csv
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from .models import Movie, Actor, Genre
from django.http import HttpResponse
from django.urls import path

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "release_year"]
    search_fields = ["title", 'genres__name']
    list_filter = ['genres__name']
    list_per_page = 25
    actions = ["export_as_csv"]  # ✅ add this
    change_list_template = "admin/movie_changelist.html"

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="movies.csv"'

        writer = csv.writer(response)

        # Header
        writer.writerow([
            "id",
            'tmdb_id',
            "title",
            "description",
            "release_year",
            "duration",
            "genres",
            "actors",
            "created_at",
        ])

        for movie in queryset:
            genres = " | ".join([g.name for g in movie.genres.all()])
            actors = " | ".join([a.name for a in movie.actors.all()])

            writer.writerow([
                movie.id,
                movie.tmdb_id,
                movie.title,
                movie.description,
                movie.release_year,
                movie.duration,
                genres,
                actors,
                movie.created_at,
            ])

        return response
    
    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("file")

            if not csv_file:
                messages.error(request, "No file uploaded")
                return redirect("..")

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:

                movie, created = Movie.objects.update_or_create(
                    title=row["title"],  # 🔥 unique identifier
                    tmdb_id=row["tmdb_id"],  # 🔥 unique identifier
                    defaults={
                        "description": row["description"],
                        "release_year": int(row["release_year"]),
                        "duration": int(row["duration"]),
                    }
                )
                # Clear old relations first
                movie.genres.clear()
                movie.actors.clear()

                # Handle genres
                genres = row.get("genres", "").split("|")
                for g in genres:
                    if g.strip():
                        genre_obj, _ = Genre.objects.get_or_create(name=g.strip())
                        movie.genres.add(genre_obj)

                # Handle actors
                actors = row.get("actors", "").split("|")
                for a in actors:
                    if a.strip():
                        actor_obj, _ = Actor.objects.get_or_create(name=a.strip())
                        movie.actors.add(actor_obj)

            messages.success(request, "CSV imported successfully")
            return redirect("..")

        return render(request, "admin/import_csv.html")
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-csv/", self.admin_site.admin_view(self.import_csv)),
        ]
        return custom_urls + urls
    
    export_as_csv.short_description = "Export selected movies as CSV"
    