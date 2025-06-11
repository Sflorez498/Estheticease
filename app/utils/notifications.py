import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

class NotificationService:
    def __init__(self):
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT"))

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_appointment_confirmation(self, to_email: str, appointment_details: dict) -> bool:
        subject = "Confirmación de Cita - Estheticease"
        body = f"""
        <html>
            <body>
                <h2>¡Tu cita ha sido confirmada!</h2>
                <p>Detalles de tu cita:</p>
                <ul>
                    <li>Servicio: {appointment_details['servicio']}</li>
                    <li>Fecha: {appointment_details['fecha']}</li>
                    <li>Hora: {appointment_details['hora']}</li>
                    <li>Empleado: {appointment_details['empleado']}</li>
                </ul>
                <p>Si necesitas cancelar o reprogramar tu cita, por favor contáctanos con anticipación.</p>
                <p>¡Gracias por elegir Estheticease!</p>
            </body>
        </html>
        """
        return self.send_email(to_email, subject, body)

    def send_appointment_reminder(self, to_email: str, appointment_details: dict) -> bool:
        subject = "Recordatorio de Cita - Estheticease"
        body = f"""
        <html>
            <body>
                <h2>Recordatorio de tu próxima cita</h2>
                <p>Te recordamos que tienes una cita programada:</p>
                <ul>
                    <li>Servicio: {appointment_details['servicio']}</li>
                    <li>Fecha: {appointment_details['fecha']}</li>
                    <li>Hora: {appointment_details['hora']}</li>
                    <li>Empleado: {appointment_details['empleado']}</li>
                </ul>
                <p>¡Te esperamos!</p>
            </body>
        </html>
        """
        return self.send_email(to_email, subject, body)

    def send_password_reset(self, to_email: str, reset_token: str) -> bool:
        subject = "Restablecimiento de Contraseña - Estheticease"
        body = f"""
        <html>
            <body>
                <h2>Restablecimiento de Contraseña</h2>
                <p>Has solicitado restablecer tu contraseña. Usa el siguiente token para proceder:</p>
                <p><strong>{reset_token}</strong></p>
                <p>Este token expirará en 30 minutos.</p>
                <p>Si no solicitaste este cambio, por favor ignora este correo.</p>
            </body>
        </html>
        """
        return self.send_email(to_email, subject, body) 