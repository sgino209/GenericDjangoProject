from django.db import connection
# (c) Shahar Gino, July-2018, sgino209@gmail.com
#
# Models registration

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Author, Genre, Book, BookInstance


admin.site.site_header = 'Generic Django Site'

# ---------------------------------------------------------------------------------------------------------------------

# Define an inline admin descriptor for Employee model, which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# ---------------------------------------------------------------------------------------------------------------------

# Define the admin class
class AuthorAdmin(ImportExportModelAdmin):

    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# ---------------------------------------------------------------------------------------------------------------------

# Define the admin class
class GenreAdmin(ImportExportModelAdmin):
    pass

# Register the admin class with the associated model
admin.site.register(Genre, GenreAdmin)

# ---------------------------------------------------------------------------------------------------------------------

# Inline editing of associated records
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Register the Admin classes for Book using the decorator
class BookAdmin(ImportExportModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

admin.site.register(Book, BookAdmin)

# ---------------------------------------------------------------------------------------------------------------------

# Register the Admin classes for BookInstance using the decorator
class BookInstanceAdmin(ImportExportModelAdmin):
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )

admin.site.register(BookInstance, BookInstanceAdmin)

# ---------------------------------------------------------------------------------------------------------------------
