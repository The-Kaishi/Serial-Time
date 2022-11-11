from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from .models import Category, Genre, Serial, SerialShots, RatingStar, Rating, Actor, Reviews
# Register your models here.


from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget)

    class Meta:
        model = Serial
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class SerialShotsInline(admin.StackedInline):
    model = SerialShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='100' height='110'")

    get_image.short_description = 'Изображение'


@admin.register(Serial)
class SerialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'year', 'seasons', 'draft', 'url')
    list_display_links = ('title',)
    list_filter = ('year', 'seasons')
    search_fields = ('title',)
    inlines = [SerialShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    #fields = (('actors', 'genres', ), )
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    readonly_fields = ('get_image',)
    fieldsets = (
        (None, {
            'fields': (('title', 'year'),)
        }),
        (None, {
            'fields': ('description',)
        }),
        (None, {
            'fields': (('seasons', 'series'),)
        }),
        (None, {
            'fields': (('poster', 'get_image'),)
        }),
        (None, {
            'fields': (('country', 'world_premiere'),)
        }),
        ('More', {
            'classes': ('collapse',),
            'fields': (('actors', 'genres', 'category'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        })
    )

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.poster.url} width='140' height='140'")


    def unpublish(self, request, queryset):

        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} '
        self.message_user(request, f'{message_bit} записей были обновлены')

    def publish(self, request, queryset):

        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} '
        self.message_user(request, f'{message_bit} записей были обновлены')

    publish.short_description = 'Опубликовать'
    publish.allowed_permission = ('change', )

    publish.short_description = 'Снять с публикации'
    publish.allowed_permission = ('change',)

    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'serial', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'get_image')
    list_display_links = ('name',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='50' height='60'")

    get_image.short_description = 'Изображение'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


@admin.register(SerialShots)
class SerialShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'serial', 'get_image')
    list_display_links = ('title',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='50' height='60'")

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'serial', 'star')


admin.site.register(RatingStar)
#admin.site.register(Rating)


admin.site.site_title = 'Serial Time'
admin.site.site_header = 'Serial Time'
