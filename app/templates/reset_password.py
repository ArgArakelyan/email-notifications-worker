from jinja2 import Template

reset_template = Template(
    """
<div style="font-family: Arial, sans-serif; max-width: 600px;">
    <h2>Сброс пароля</h2>
    <p>Ваш код для сброса пароля:</p>
    <div style="background: #f5f5f5; padding: 20px; text-align: center; 
                font-size: 24px; font-weight: bold; 
                letter-spacing: 4px; margin: 20px 0;">
        {{ reset_code }}
    </div>
    <p>Код действителен 10 минут.</p>
    <hr>
    <small>Это письмо отправлено автоматически</small>
</div>
"""
)
