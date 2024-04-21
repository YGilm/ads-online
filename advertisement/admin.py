from django.contrib import admin
from .models import Ad, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    min_num = 0
    fields = ['text', 'author', 'created_at']
    readonly_fields = ['created_at']


class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'description', 'author', 'created_at']
    search_fields = ['title', 'description', 'author__email']
    list_filter = ['created_at', 'price']
    readonly_fields = ['id', 'created_at']
    inlines = [ReviewInline]

    fieldsets = (
        (None, {'fields': ('title', 'price', 'description', 'image', 'author')}),
        ('Date Information', {'fields': ('created_at',)}),
    )


admin.site.register(Ad, AdAdmin)
admin.site.register(Review)
