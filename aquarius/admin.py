from django.contrib import admin
from aquarius.models import City, Post, Comment, Report, HotTopic
from django.urls import reverse
from django.utils.html import format_html


class PostInline(admin.TabularInline):
    model = Post
    fields = ('topic', 'content', 'city', 'post_link')  
    can_delete = False
    readonly_fields = ('topic', 'content', 'post_link') 
    max_num = 0 
    extra = 0

    def post_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, "Analyze")
    
    post_link.short_description = "Action"

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('classification', 'topic', 'comment_link')  
    can_delete = False
    readonly_fields = ('classification','topic', 'comment_link') 
    max_num = 0 
    extra = 0

    def comment_link(self, obj):
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, "Analyze")
    
    comment_link.short_description = "Action"

class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # list_filter = ('field1', 'field4')
    search_fields = ('name',)
    can_delete = False
    inlines = [PostInline]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['additional_data'] = 'This is some additional data'
        
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(City, CityAdmin)
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'content', 'city')
    list_filter = ('city', 'source')
    search_fields = ('topic', 'content')
    can_delete = False
    readonly_fields = ('topic', 'content', 'city', 'source', 'total_comments') 
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'topic',)
    list_filter = ('classification',)
    can_delete = False
    readonly_fields = ('classification','topic', 'description', 'post') 
    search_fields = ('topic',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id', 'favour', 'against', 'neutral')
    search_fields = ('post_id',)

@admin.register(HotTopic)
class HotTopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'post_id', 'city')
    search_fields = ('city__name',)
    list_filter = ('city',)
