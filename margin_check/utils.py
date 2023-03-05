from django.core.mail import EmailMessage
from django.template import loader


class TemplateEmail(EmailMessage):
    template_name = None
    context = {}

    def __init__(self, *args, **kwargs):
        self.template_name = kwargs.pop("template_name", self.template_name)
        self.context = kwargs.pop("context", self.context)
        super().__init__(*args, **kwargs)

    def render(self):
        template = loader.get_template(self.template_name)
        content = template.render(self.context).strip()
        self.body = content

    def send(self, *args, **kwargs):
        self.render()
        super().send(*args, **kwargs)
