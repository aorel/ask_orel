from django.contrib import admin

# Register your models here.

from askme import models

'''
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Article, ArticleAdmin)
'''


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('custom_admin_display',)


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Answer, AnswerAdmin)
