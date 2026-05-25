import ssl
from django.core.mail.backends.smtp import EmailBackend


class NoVerifyEmailBackend(EmailBackend):
    """Backend SMTP que omite verificación SSL del certificado.
    Usar solo en desarrollo cuando el servidor SMTP tiene hostname mismatch.
    """

    def open(self):
        if self.connection:
            return False
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            self.connection = self.connection_class(
                self.host,
                self.port,
                timeout=self.timeout,
                context=ssl_context,
            )
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls(context=ssl_context)
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except OSError:
            if not self.fail_silently:
                raise
