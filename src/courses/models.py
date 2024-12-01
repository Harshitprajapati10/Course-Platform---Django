import uuid
from django.db import models
import helpers
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
# Create your models here.

helpers.cloudinary_init()

class AccessRequirement(models.TextChoices):
    ANYONE = "any" , "Anyone"
    EMAIL_REQUIRED = "email" , "Email Required"

class PublishStatus(models.TextChoices):
    PUBLISHED = "publish" , "Published"
    COMING_SOON = "soon" , "Coming Soon"
    DRAFT =  "draft" , "Draft"

def handle_upload(instance, filename):
    return f"{filename}"


def generate_public_id(instance,*args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-","")
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"


def get_public_id_prefix(instance,*args, **kwargs):
    if hasattr(instance,'path'):
        path = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:   
        return f"{model_name_slug}"
    return f"{model_name_slug}/{public_id}"

def get_display_name(instance,*args, **kwargs):
    if hasattr(instance, 'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance, 'title'):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} Upload"

# Course Model
class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=120, blank = True, null = True, db_index=True)

    image = CloudinaryField(
        "image", 
        null = True, 
        public_id_prefix = get_public_id_prefix, 
        display_name = get_display_name,
        tags = ["course", "thumbnail"]
    )

    access = models.CharField(
        max_length=5,
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED,
    )

    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.path

    @property  
    def path(self):
        return f"/courses/{self.public_id}"

    def get_display_name(self):
        return f"{self.title}-Courses"

    def get_thumbnail(self):
        if not self.image:
            return None
        return helpers.get_cloudinary_image_object(
            self,
            field_name="image",
            as_html=False,
            width=382,
        )
    
    def get_display_image(self):
        if not self.image:
            return None
        return helpers.get_cloudinary_image_object(
            self,
            field_name="image",
            as_html=False,
            width=750,
        )

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    
    # @property
    # def image_admin_url(self):
    #     return helpers.get_cloudinary_image_object(
    #         self,
    #         field_name="image",
    #         as_html=False,
    #         width=200,
    #     )
    
    # def get_image_thumbnail(self, as_html = False, width = 500):
    #     return helpers.get_cloudinary_image_object(
    #         self,
    #         field_name="image",
    #         as_html=as_html,
    #         width=width,
    #     )
        
    # def get_image_detail(self, as_html = False, width = 750):
    #     return helpers.get_cloudinary_image_object(
    #         self,
    #         field_name="image",
    #         as_html=as_html,
    #         width=width,
    #     )


# Lesson Model
"""
-Lessons
    -Title
    -Description
    -Video
    -Status: Published, Coming Soon, Draft
"""
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=120, blank = True, null = True,db_index=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)

    thumbnail = CloudinaryField(
                "image",
                public_id_prefix = get_public_id_prefix, 
                display_name = get_display_name,
                tags = ['thumbnail', 'lessons'],
                blank=True,null=True,
        )

    video = CloudinaryField(
                "video",
                public_id_prefix = get_public_id_prefix, 
                display_name = get_display_name,
                tags = ['video','lessons'],
                type = "private",
                blank=True,
                null=True, 
                resource_type='video',
        )

    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False, help_text="If user does not have access to course, can they see this?")
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED,
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order','updated']

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.path

    @property  
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/lessons/{self.public_id}"

    @property
    def requires_email(self):
        return self.course.access == AccessRequirement.EMAIL_REQUIRED

    def get_display_name(self):
        return f"{self.title}-{self.course.get_display_name()}"

    @property
    def is_coming_soon(self):
        return self.status == PublishStatus.COMING_SOON
    
    @property
    def has_video(self):
        return self.video is not None
    
    def get_thumbnail(self):
        width = 382
        if self.thumbnail:
            return helpers.get_cloudinary_image_object(
                self,
                field_name="thumbnail",
                format="jpg",
                as_html=False,
                width=width,
            )

        elif self.video:
            return helpers.get_cloudinary_image_object(
                self,
                field_name="video",
                format="jpg",
                as_html=False,
                width=width,
            )
    
        return
# admin , 11111

