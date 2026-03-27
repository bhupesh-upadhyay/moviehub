import csv
from django.contrib import admin
from django.shortcuts import render
from .models import Movie, Actor, Genre

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["name", "birth_date"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]
  
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "release_year"]

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path("upload-csv/", self.upload_csv),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["file"]

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                Movie.objects.create(
                    title=row["title"],
                    description=row["description"],
                    release_year=row["release_year"],
                    duration=row["duration"],
                    video_url=row.get("video_url", ""),
                )

            self.message_user(request, "CSV uploaded successfully")

        return render(request, "admin/csv_upload.html")
    
    def video_preview(self, obj):
        if obj.video:
            return f'<video width="200" controls><source src="{obj.video.url}"></video>'
        return "No video"

    video_preview.allow_tags = True