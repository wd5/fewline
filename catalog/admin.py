from django.contrib import admin
from catalog.models import Product, ProductPhoto, Category, Section, File, CategoryProduct

class PhotoInline(admin.StackedInline):
    model = ProductPhoto

class FilesInline(admin.StackedInline):
    model = File

admin.site.register(ProductPhoto)

class CategoryProductinline(admin.TabularInline):
    model = CategoryProduct
    sortable_field_name = "position"

class CategoryProductinline2(admin.TabularInline):
    model = CategoryProduct

class ProductsAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = Product.objects.exclude(category__slug__in=['outdoor', 'indoor'])
        return qs

    inlines = [PhotoInline, FilesInline, CategoryProductinline2]
    list_display = ('name', 'price', 'quantity', 'created_at', 'updated_at')
    list_per_page = 50
    ordering = ['name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug' : ('name',)}

    class Media:
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/js/tinymce_setup.js',]

admin.site.register(Product, ProductsAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    inlines = [CategoryProductinline]
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description',]
    prepopulated_fields = {'slug' : ('name',)}

    class Media:
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/js/tinymce_setup.js',]

admin.site.register(Category, CategoriesAdmin)

class CategoryInline(admin.TabularInline):
    fields = ('name', 'position',)
    model = Category
    sortable_field_name = "position"

class SectionsAdmin(admin.ModelAdmin):
        inlines = [CategoryInline]
        prepopulated_fields = {'slug' : ('name',)}

        class Media:
            js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/js/tinymce_setup.js',]

admin.site.register(Section, SectionsAdmin)
