from django.contrib import admin

from askme import models


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title',)


class QuestionVoteAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'vote',)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'some_text',)


class AnswerVoteAdmin(admin.ModelAdmin):
    list_display = ('answer', 'user', 'vote',)


admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.QuestionVote, QuestionVoteAdmin)
admin.site.register(models.Answer, AnswerAdmin)
admin.site.register(models.AnswerVote, AnswerVoteAdmin)
