# Register your models here.
from django.contrib import admin
from .models import Freelancer, MonthlyProcess, TaskStatus

@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    # 管理画面の一覧に表示する項目
    list_display = ('name', 'client_name', 'base_unit_price', 'lower_limit_hours', 'upper_limit_hours')
    fieldsets = (
        ("基本情報", {
            'fields': ('name', 'email', 'client_name', 'project_name')
        }),
        ("精算条件（自動計算用）", {
            'fields': (
                'base_unit_price', 
                'lower_limit_hours', 
                'upper_limit_hours', 
                'deduction_unit_price', 
                'overtime_unit_price'
            )
        }),
        ("契約期間", {
            'fields': ('contract_start', 'contract_end')
        }),
    )

@admin.register(MonthlyProcess)
class MonthlyProcessAdmin(admin.ModelAdmin):
    list_display = ('year_month', 'is_completed')
    readonly_fields = ('is_completed',) # 管理画面でも自動計算結果を上書きできないようにする

@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('monthly_process', 'freelancer', 'status', 'payment_amount')
    list_filter = ('monthly_process', 'status') # 絞り込み機能を追加
