from django.db.models import TextChoices


class MARGIN_CLASS_CHOICES(TextChoices):
    SPAN = "span"
    IMSM = "imsm"
    CESM = "cesm"
    AMPO = "ampo"
    AMEM = "amem"
    AMCO = "amco"
    AMCU = "amcu"
    AMWI = "amwi"
    DMEM = "dmem"
