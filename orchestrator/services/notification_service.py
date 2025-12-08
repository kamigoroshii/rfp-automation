"""
Notification Service - Handles alerts and notifications for the RFP system
"""
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from orchestrator.config import settings

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.enabled = bool(settings.EMAIL_HOST and settings.EMAIL_USER)
        self.team_emails = ["team@example.com"]  # In real app, load from DB/Config

    async def notify_high_value_rfp(self, rfp):
        """
        Send alert for RFPs > $1 Million
        """
        try:
            # Check threshold (1 Million)
            if rfp.get('total_estimate', 0) < 1000000:
                return

            logger.info(f"🚨 TRIGGERING HIGH VALUE ALERT for RFP: {rfp.get('rfp_id')}")
            
            subject = f"🚨 HIGH VALUE ALERT: ${rfp.get('total_estimate'):,.2f} - {rfp.get('title')}"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #d32f2f;">💰 High Value Opportunity Detected!</h2>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; border: 1px solid #ddd;">
                    <p><strong>RFP ID:</strong> {rfp.get('rfp_id')}</p>
                    <p><strong>Title:</strong> {rfp.get('title')}</p>
                    <p><strong>Client:</strong> {rfp.get('source')}</p>
                    <p><strong>Est. Value:</strong> <span style="font-size: 1.2em; font-weight: bold; color: #388e3c;">${rfp.get('total_estimate'):,.2f}</span></p>
                    <p><strong>Deadline:</strong> {rfp.get('deadline')}</p>
                </div>
                
                <h3>Action Required:</h3>
                <ul>
                    <li>Review technical specs immediately.</li>
                    <li>Assign Lead Engineer.</li>
                    <li>Check competitor activity.</li>
                </ul>
                
                <p><a href="http://localhost:5173/rfp/{rfp.get('rfp_id')}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View RFP Details</a></p>
            </body>
            </html>
            """
            
            await self._send_email(subject, body, self.team_emails)
            return True
            
        except Exception as e:
            logger.error(f"Error sending high value notification: {e}")
            return False

    async def _send_email(self, subject: str, html_body: str, recipients: list):
        """Send email via SMTP"""
        if not self.enabled:
            logger.warning(f"Notification Service Disabled. Would have sent: {subject}")
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_USER
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Connect to SMTP Server
            # Note: In production you might use Celery/Async here
            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, 465)
            server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_USER, recipients, msg.as_string())
            server.quit()
            
            logger.info(f"Notification sent to {recipients}")
            
        except Exception as e:
            logger.error(f"SMTP Error: {e}")
