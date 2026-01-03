# system_app/services/email_service.py
import imaplib
import email
from django.conf import settings
from ..models import PurchaseOrder
from django.core.files.base import ContentFile
from datetime import datetime

def search_and_sync_emails(client_name, start_date=None, end_date=None):
    """
    指定された条件でXServerのメールを検索し、PDFを保存する
    """
    # ここではIMAPの検索クエリを組み立てる例
    search_criteria = []
    
    # 件名または本文にクライアント名が含まれるものを探す設定
    if client_name:
        search_criteria.append(f'SUBJECT "{client_name}"')
    
    # 日付条件 (IMAP形式: 01-Jan-2023)
    if start_date:
        d = datetime.strptime(start_date, '%Y-%m-%d')
        search_criteria.append(f'SINCE {d.strftime("%d-%b-%Y")}')
    
    # ... (前回のIMAP接続ロジックをベースに、mail.searchでこのcriteriaを使用) ...
    # query = " ".join(search_criteria)
    # status, messages = mail.search(None, query)
    
    return f"「{client_name}」のメール検索が完了しました（※現在はシミュレーション動作です）"

def sync_purchase_orders_from_mail():
    """
    XServerのメールから「注文書」という件名のメールを探し、PDFを保存する
    """
    if settings.DEBUG:
        # 【Mockモード】ローカルの特定フォルダから読み込んだことにする
        print("DEBUGモード: ローカルファイルから注文書をシミュレートします")
        return "Mock実行完了"

    # --- 本番接続用設定 ---
    # XServerのホスト名（例: sv***.xserver.jp）
    IMAP_SERVER = "sv***.xserver.jp" 
    EMAIL_USER = "your-email@example.com"
    EMAIL_PASS = "your-password"

    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("INBOX")

    # 「注文書」という件名の未読メールを検索（例）
    status, messages = mail.search(None, '(SUBJECT "注文書")')
    
    for num in messages[0].split():
        res, msg_data = mail.fetch(num, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                received_date = email.utils.parsedate_to_datetime(msg.get("Date"))
                
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart': continue
                    if part.get('Content-Disposition') is None: continue
                    
                    filename = part.get_filename()
                    if filename and ".pdf" in filename.lower():
                        # DBに保存
                        po = PurchaseOrder(
                            client_name="メールから自動解析", # ここに送信者名抽出ロジックを入れる
                            received_at=received_date,
                        )
                        po.file.save(filename, ContentFile(part.get_payload(decode=True)))
                        po.save()

    mail.close()
    mail.logout()
    return "同期が完了しました"
