import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

def send_email_notification(contact_message):
    """
    Отправка email уведомления через Gmail SMTP
    """
    try:
        # Создаем сообщение
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🔔 Новое сообщение от {contact_message.name}"
        msg['From'] = settings.GMAIL_USER
        msg['To'] = settings.GMAIL_USER  # Отправляем себе
        
        # HTML версия письма
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px 10px 0 0;">
                <h2 style="color: white; margin: 0;">📬 Новое сообщение с портфолио</h2>
            </div>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 0 0 10px 10px; border: 1px solid #e9ecef;">
                <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                    <h3 style="color: #495057; margin-top: 0;">👤 Отправитель</h3>
                    <p><strong>Имя:</strong> {contact_message.name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{contact_message.email}">{contact_message.email}</a></p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                    <h3 style="color: #495057; margin-top: 0;">📝 Сообщение</h3>
                    <p><strong>Тема:</strong> {contact_message.subject}</p>
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff;">
                        <p style="margin: 0; line-height: 1.6;">{contact_message.message}</p>
                    </div>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 8px;">
                    <h3 style="color: #495057; margin-top: 0;">⏰ Детали</h3>
                    <p><strong>Дата:</strong> {contact_message.created_at.strftime('%d.%m.%Y в %H:%M')}</p>
                    <p><strong>ID сообщения:</strong> #{contact_message.id}</p>
                </div>
                
                <div style="text-align: center; margin-top: 20px;">
                    <a href="http://127.0.0.1:8000/admin/contacts/contactmessage/{contact_message.id}/change/" 
                       style="background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        📋 Открыть в админке
                    </a>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 12px;">
                <p>Это автоматическое уведомление с портфолио Виталия</p>
            </div>
        </body>
        </html>
        """
        
        # Текстовая версия
        text_content = f"""
🔔 НОВОЕ СООБЩЕНИЕ С ПОРТФОЛИО

👤 ОТПРАВИТЕЛЬ:
Имя: {contact_message.name}
Email: {contact_message.email}

📝 СООБЩЕНИЕ:
Тема: {contact_message.subject}
Текст: {contact_message.message}

⏰ ДЕТАЛИ:
Дата: {contact_message.created_at.strftime('%d.%m.%Y в %H:%M')}
ID: #{contact_message.id}

Админка: http://127.0.0.1:8000/admin/contacts/contactmessage/{contact_message.id}/change/
        """
        
        # Добавляем обе версии
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)
        
        # Отправляем через Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(settings.GMAIL_USER, settings.GMAIL_APP_PASSWORD)
            server.send_message(msg)
            
        logger.info(f"Email notification sent for contact message: {contact_message.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email notification: {str(e)}")
        return False

def send_telegram_notification(contact_message):
    """
    Отправка Telegram уведомления
    """
    try:
        # Форматируем сообщение для Telegram
        message = f"""
🔔 <b>НОВОЕ СООБЩЕНИЕ С ПОРТФОЛИО</b>

👤 <b>Отправитель:</b>
• <b>Имя:</b> {contact_message.name}
• <b>Email:</b> <code>{contact_message.email}</code>

📝 <b>Сообщение:</b>
• <b>Тема:</b> {contact_message.subject}
• <b>Текст:</b> 
<blockquote>{contact_message.message}</blockquote>

⏰ <b>Детали:</b>
• <b>Дата:</b> {contact_message.created_at.strftime('%d.%m.%Y в %H:%M')}
• <b>ID:</b> #{contact_message.id}

🔗 <a href="http://127.0.0.1:8000/admin/contacts/contactmessage/{contact_message.id}/change/">Открыть в админке</a>
        """
        
        # Отправляем через Telegram Bot API
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        
        payload = {
            'chat_id': settings.TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Telegram notification sent for contact message: {contact_message.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send Telegram notification: {str(e)}")
        return False

def send_contact_notification(contact_message):
    """
    Главная функция отправки уведомлений (Email + Telegram)
    """
    results = {
        'email': False,
        'telegram': False
    }
    
    # Отправляем Email
    results['email'] = send_email_notification(contact_message)
    
    # Отправляем Telegram
    results['telegram'] = send_telegram_notification(contact_message)
    
    # Логируем результаты
    if results['email'] and results['telegram']:
        logger.info(f"All notifications sent successfully for message: {contact_message.id}")
    elif results['email'] or results['telegram']:
        logger.warning(f"Partial notification success for message: {contact_message.id} - Email: {results['email']}, Telegram: {results['telegram']}")
    else:
        logger.error(f"All notifications failed for message: {contact_message.id}")
    
    return results
