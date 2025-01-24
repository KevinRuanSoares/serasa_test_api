from django.utils.translation import gettext_lazy as _

# Rule choices
SUPER_ADMIN = 'SUPER_ADMIN'
ADMIN = 'ADMIN'
SELLER = 'SELLER'

RULE_CHOICES = [
    (SUPER_ADMIN, _('Super Admin')),
    (ADMIN, _('Admin')),
    (SELLER, _('Seller')),
]
