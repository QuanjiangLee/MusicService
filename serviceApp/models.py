from django.db import models
#from django.contrib.auth.models import User
# Create your models here.


class userInf(models.Model):
    user_id = models.AutoField(primary_key=True, null=False)
    user_name = models.CharField(max_length = 30)
    user_nickname = models.CharField(max_length = 30)
    user_passwd = models.CharField(max_length=100)
    def __str__(self):
        return self.user_name

class songsInf(models.Model):
    song_id = models.AutoField(primary_key=True, null=False)
    song_name = models.CharField(max_length = 40)
    song_author = models.CharField(max_length = 40)
    song_url = models.CharField(max_length = 255)
    song_lyric = models.CharField(max_length = 4000)
    def __str__(self):
        return self.song_name

class songShare(models.Model):
    share_id = models.AutoField(primary_key=True, null=False)
    share_from = models.ForeignKey(userInf, related_name='share_from_user', on_delete=models.DO_NOTHING)
    share_to = models.ForeignKey(userInf, related_name='share_to_user', on_delete=models.DO_NOTHING)
    share_song = models.ForeignKey(songsInf, related_name='share_song', on_delete=models.DO_NOTHING)
    share_commit = models.CharField(max_length = 255)
    share_date = models.DateTimeField(auto_now_add = True)
    class Meta:  #按时间下降排序
        ordering = ['-share_date']
    def __str__(self):
        return self.share_commit

class songCommit(models.Model):
    commit_song = models.ForeignKey(songsInf, related_name='commit_song', on_delete=models.DO_NOTHING)
    commit_user = models.ForeignKey(userInf, related_name='commit_user', on_delete=models.DO_NOTHING)
    commit_details = models.CharField(max_length = 255)
    commit_date = models.DateTimeField(auto_now_add = True)
    class Meta:  #按时间下降排序
        ordering = ['-commit_date']
    def __str__(self):
        return self.commit_details

class songLikes(models.Model):
    like_id = models.AutoField(primary_key=True, null=False)
    like_user = models.ForeignKey(userInf, related_name='like_user', on_delete=models.DO_NOTHING)
    like_song = models.ForeignKey(songsInf, related_name='like_song', on_delete=models.DO_NOTHING)
    like_date = models.DateTimeField(auto_now_add = True)
    class Meta:  #按时间下降排序
        ordering = ['-like_date']