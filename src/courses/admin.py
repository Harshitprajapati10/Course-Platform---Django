import helpers
from django.contrib import admin
from cloudinary import CloudinaryImage
from django.utils.html import format_html
from .models import Course, Lesson

class LessonInline(admin.StackedInline):
    model = Lesson
    readonly_fields = [
        'public_id',
        'updated',
        'display_image',
        'display_video',
    ]
    extra = 0

    def display_image(self, obj, *args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            obj,
            field_name="thumbnail",
            width=200,
        )
        return format_html(f"<img src = {url} />")
    display_image.short_description = "Current Image"

    def display_video(self, obj, *args, **kwargs):
        video_embed_html = helpers.get_cloudinary_video_object(
            obj,
            field_name="video",
            as_html=True,
            width=500,
        )
        return video_embed_html
    display_video.short_description = "Current Video"

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['title','status','access']
    list_filter = ['status','access']
    fields = ['public_id','title', 'description','status','image','access','display_image']
    readonly_fields = ['public_id','display_image']

    def display_image(self, obj, *args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            obj,
            field_name="image",
            width=200,
        )
        return format_html(f"<img src = {url} />")
    
    display_image.short_description = "Current Image"