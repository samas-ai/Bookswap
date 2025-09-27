from django.contrib import admin

# Register your models here.
from .models import User, Book, Trade

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Trade)