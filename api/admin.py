from django.contrib import admin
from .models import Wallet

admin.site.site_header='Test Project Admin Panel'
admin.site.index_title='Create Wallet'


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass