# system_app/services/sync_service.py
import pandas as pd # pip install pandas openpyxl

def sync_from_spreadsheet(file_path):
    # ExcelでもCSVでも読み込めるように（ローカルの仮ファイルを指定可能）
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    for index, row in df.iterrows():
        # FreelancerまたはPartnerを更新
        Freelancer.objects.update_or_create(
            name=row['氏名'],
            defaults={
                'base_unit_price': row['単価'],
                'lower_limit_hours': row['下限'],
                'upper_limit_hours': row['上限'],
                # ... 他の項目も同様に
            }
        )
    return "同期完了"
