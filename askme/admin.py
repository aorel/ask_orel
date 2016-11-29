from django.contrib import admin

from askme import models


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
