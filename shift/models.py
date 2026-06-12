import re
import uuid
from django.db import models


def normalize_name(name):
    """全角スペース→半角、連続スペース除去、前後トリム"""
    name = name.replace('　', ' ')
    name = re.sub(r'\s+', ' ', name).strip()
    return name


class Project(models.Model):
    AUTH_NAME = 'name'
    AUTH_CODE = 'code'
    AUTH_CHOICES = [
        (AUTH_NAME, '名前入力モード'),
        (AUTH_CODE, 'コード＋パスワードモード'),
    ]

    name = models.CharField(max_length=100, verbose_name='案件名')
    auth_mode = models.CharField(max_length=10, choices=AUTH_CHOICES, default=AUTH_NAME, verbose_name='認証モード')
    start_date = models.DateField(null=True, blank=True, verbose_name='開始日')
    end_date = models.DateField(null=True, blank=True, verbose_name='終了日')
    deadline = models.DateTimeField(verbose_name='提出期限')
    info_message = models.TextField(blank=True, verbose_name='お知らせ')
    copy_guide_message = models.TextField(blank=True, verbose_name='コピー案内メッセージ')
    confirm_message = models.TextField(blank=True, verbose_name='確認画面メッセージ')
    # 案件ごとの提出用トークン（1つのURL）
    submit_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '案件'
        verbose_name_plural = '案件'

    def __str__(self):
        return self.name

    def get_dates(self):
        if not self.start_date or not self.end_date:
            return []
        from datetime import timedelta
        days = []
        d = self.start_date
        while d <= self.end_date:
            days.append(d)
            d += timedelta(days=1)
        return days


class ShiftType(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='shift_types', verbose_name='案件')
    name = models.CharField(max_length=60, verbose_name='シフト名')
    short_name = models.CharField(max_length=3, blank=True, verbose_name='略称')
    time_range = models.CharField(max_length=30, blank=True, verbose_name='時間帯')
    color = models.CharField(max_length=7, default='#2563eb', verbose_name='カラー')
    order = models.PositiveIntegerField(default=0, verbose_name='表示順')

    class Meta:
        ordering = ['order']
        verbose_name = 'シフト枠'
        verbose_name_plural = 'シフト枠'

    def __str__(self):
        return f'{self.project.name} - {self.name}'


class Staff(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='staff_members', verbose_name='案件')
    code = models.CharField(max_length=20, blank=True, verbose_name='コード')
    name = models.CharField(max_length=50, verbose_name='氏名')
    password = models.CharField(max_length=100, blank=True, verbose_name='パスワード')

    class Meta:
        ordering = ['code', 'name']
        verbose_name = 'スタッフ'
        verbose_name_plural = 'スタッフ'

    def __str__(self):
        return f'{self.code} {self.name}'.strip()


class Manager(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='managers', verbose_name='案件')
    role = models.CharField(max_length=20, blank=True, verbose_name='役割')
    name = models.CharField(max_length=50, verbose_name='氏名')

    class Meta:
        verbose_name = '担当者'
        verbose_name_plural = '担当者'

    def __str__(self):
        return self.name


class Submission(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='submissions', verbose_name='案件')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, related_name='submissions', verbose_name='スタッフ')
    submitted = models.BooleanField(default=False, verbose_name='提出済み')
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name='提出日時')
    notes = models.TextField(blank=True, verbose_name='特記事項')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('project', 'staff')]
        verbose_name = '提出'
        verbose_name_plural = '提出'

    def __str__(self):
        staff_name = self.staff.name if self.staff else '不明'
        return f'{self.project.name} - {staff_name}'


class ShiftSelection(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='selections', verbose_name='提出')
    date = models.DateField(verbose_name='日付')
    shift_types = models.ManyToManyField(ShiftType, blank=True, verbose_name='シフト')

    class Meta:
        unique_together = [('submission', 'date')]
        ordering = ['date']
        verbose_name = 'シフト選択'
        verbose_name_plural = 'シフト選択'

    def __str__(self):
        return f'{self.submission} - {self.date}'
