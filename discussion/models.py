from django.db import models
from django.contrib.auth.models import User

# 3rd app fields
from ckeditor.fields import RichTextField

# Create your models here.
VOTES_CHOICES = (
    ('L', 'Like'),
    ('D', 'Dislike'),
)
# Questions for discussion forum
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_user')
    title = models.CharField(max_length=300)
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    # This tell whether the question is replied
    is_answered = models.BooleanField(default=False)
    # This tell whether the question is solved - Instructors can close the questions
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # Get amount of answers in the questions
    def get_answers_count(self):
        return Answer.objects.filter(question=self).count()

# Answer for the question
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_user')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    # Calculate the amount of like and dislike
    def calculate_votes(self):
        l_votes = Vote.objects.filter(answer=self, vote='L').count()
        d_votes = Vote.objects.filter(answer=self, vote='D').count()
        self.votes = l_votes - d_votes
        self.save()
        return self.votes

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote_user')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_vote')
    vote = models.CharField(choices=VOTES_CHOICES, max_length=1)
    date = models.DateTimeField(auto_now_add=True)