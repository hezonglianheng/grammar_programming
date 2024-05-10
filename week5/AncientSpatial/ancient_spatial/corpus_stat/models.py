from django.db import models

# 修改：不再计算统计结果
# 将统计结果数据预先算出，存储到数据库中

class AbstractStat(models.Model):
    """统计表的抽象基类"""
    stat_type = models.CharField(max_length=200, default='') # 抽象
    all_cases = models.IntegerField(default=0) # 统计数量
    place = models.IntegerField(default=0) # 地点
    departure = models.IntegerField(default=0) # 出发地
    destination = models.IntegerField(default=0) # 目的地
    orientation = models.IntegerField(default=0) # 朝向
    direction = models.IntegerField(default=0) # 方向
    path = models.IntegerField(default=0) # 路径
    part = models.IntegerField(default=0) # 部件处所

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.stat_type}-{self.all_cases}"

class SpatialTypeStat(models.Model):
    """空间类型统计"""
    spatial_type = models.CharField(max_length=200, default='') # 空间类型
    all_cases = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.spatial_type}: {self.all_cases}"
    
class PrepStat(AbstractStat):
    """介词统计"""
    pass

class VerbStat(AbstractStat):
    """动词统计"""
    pass

class PatternStat(AbstractStat):
    """形式模式统计"""
    pass
