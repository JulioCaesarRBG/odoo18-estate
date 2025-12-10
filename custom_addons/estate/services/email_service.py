class EmailService:
    @staticmethod
    def send_pdf_email(env, email, pdf_data, pdf_filename, subject='Certificate Document'):
        body_html = """
        <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f9f9f9; padding: 40px 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                
                <h2 style="color: #333333; margin-top: 0; font-weight: 600; font-size: 24px;">
                    Document Ready
                </h2>
                
                <hr style="border: 0; border-top: 1px solid #eeeeee; margin: 20px 0;">
                
                <p style="color: #555555; font-size: 16px; line-height: 1.6; margin-bottom: 10px;">
                    Hello,
                </p>
                <p style="color: #555555; font-size: 16px; line-height: 1.6; margin-bottom: 20px;">
                    We are pleased to provide you with your digital certificate. 
                    Please find the <strong>PDF document attached</strong> to this email.
                </p>
                <p style="color: #555555; font-size: 16px; line-height: 1.6;">
                    You can download or save this file for your records.
                </p>

                <div style="margin-top: 40px; border-top: 1px solid #eeeeee; padding-top: 20px;">
                    <p style="color: #888888; font-size: 14px; margin: 0;">
                        Best regards,<br/>
                        <em>System Notification</em>
                    </p>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 20px;">
                <p style="font-size: 12px; color: #aaaaaa;">
                    This is an automated message, please do not reply.
                </p>
            </div>
        </div>
        """

        mail_values = {
            'subject': subject,
            'body_html': body_html,
            'email_to': email,
            'attachment_ids': [(0, 0, {
                'name': pdf_filename or 'Certificate.pdf',
                'datas': pdf_data,
                'type': 'binary',
                'mimetype': 'application/pdf',
            })],
        }
        env['mail.mail'].create(mail_values).send()
