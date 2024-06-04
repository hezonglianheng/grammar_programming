from django.db import models

# Create your models here.
class ReplacePair(models.Model):
    rp_pair = models.CharField("替换对", max_length=100)

class SentencePair(models.Model):
    """
    句子对
    """
    rp_pair = models.ForeignKey(ReplacePair, on_delete=models.CASCADE)
    # 句子1信息
    context1 = models.TextField("句子1")
    context1_filepath = models.CharField("句子1文件路径", max_length=200)
    # 句子2信息
    context2 = models.TextField("句子2")
    context2_filepath = models.CharField("句子2文件路径", max_length=200)
