import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone


class Workplace(models.Model):
    name  = models.CharField('場所名', max_length=100)
    order = models.PositiveIntegerField('表示順', default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = verbose_name_plural = '所属場所'

    def __str__(self):
        return self.name


class Employee(models.Model):
    name            = models.CharField('氏名', max_length=100)
    employee_number = models.CharField('スタッフ番号', max_length=20, unique=True)
    workplace       = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.SET_NULL, related_name='employees', verbose_name='所属場所')
    qr_token        = models.UUIDField('QRトークン', default=uuid.uuid4, unique=True, editable=False)
    is_active       = models.BooleanField('在籍中', default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['employee_number']
        verbose_name = verbose_name_plural = 'スタッフ'

    def __str__(self):
        return self.name


class AttendanceRecord(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='records', verbose_name='スタッフ')
    date      = models.DateField('日付')
    check_in  = models.TimeField('出勤', null=True, blank=True)
    check_out = models.TimeField('退勤', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('employee', 'date')]
        ordering = ['-date', 'employee']
        verbose_name = verbose_name_plural = '勤怠記録'

    def __str__(self):
        return f'{self.employee.name} {self.date}'

    @property
    def work_duration(self):
        if self.check_in and self.check_out:
            dt_in  = timezone.datetime.combine(self.date, self.check_in)
            dt_out = timezone.datetime.combine(self.date, self.check_out)
            mins   = int((dt_out - dt_in).total_seconds() / 60)
            if mins < 0:
                return '-'
            return f'{mins // 60}時間{mins % 60:02d}分'
        return '-'

    @property
    def status(self):
        if self.check_in and self.check_out:
            return 'completed'
        if self.check_in:
            return 'working'
        return 'absent'
