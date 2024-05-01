from django.db import models

# Create your models here.
# 之后可以考虑将语料原文竖着存储到数据库中
# 另一个修改路径：
# 在TextInfo中存储角色信息，查询角色信息时直接在TextInfo中查询
# 在TextInfo中用外键关联SpaceInfo
# 这样可以减少查询时间？

class OriginalText(models.Model):
    """表示原文数据表的类"""
    title = models.CharField(max_length=200) # 书本标题
    subtitle = models.CharField(max_length=200) # 子标题，用来分章
    context = models.TextField() # 原文内容

    def __str__(self) -> str:
        return f"{self.title}-{self.subtitle}"

class TextInfo(models.Model):
    """存储文字，起始索引和终结索引"""
    text = models.CharField(max_length=200) # 文字
    start = models.IntegerField() # 起始值索引
    end = models.IntegerField() # 终点值索引

    def __str__(self) -> str:
        return self.text

class SpaceInfo(models.Model):
    """表示空间信息的类"""
    # 来源
    source = models.ForeignKey("OriginalText", on_delete=models.CASCADE, blank=True, null=True)
    # 射体1
    trajectory1 = models.ForeignKey("TextInfo", on_delete=models.CASCADE, blank=True, null=True, related_name="_trajectory1")
    # 射体2
    trajectory2 = models.ForeignKey("TextInfo", on_delete=models.CASCADE, blank=True, null=True, related_name="_trajectory2")
    # 界标
    landmark = models.ForeignKey("TextInfo", on_delete=models.CASCADE, blank=True, null=True, related_name="_landmark")
    # 事件
    event = models.ForeignKey("TextInfo", on_delete=models.CASCADE, blank=True, null=True, related_name="_event")
    # 介词
    preposition = models.ForeignKey("TextInfo", on_delete=models.CASCADE, blank=True, null=True, related_name="_preposition")
    # 方位词
    location = models.ForeignKey("TextInfo", on_delete=models.CASCADE, blank=True, null=True, related_name="_location")
    # 类型
    spatial_type = models.CharField(max_length=200)
    # 形式模式
    pattern = models.CharField(max_length=200, default="")
