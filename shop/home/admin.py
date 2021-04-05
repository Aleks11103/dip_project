from django.contrib import admin
from home.models import User, Category, Subcategory, Brand, MadeIn, Product, Comment



class UserAdmin(admin.ModelAdmin):
    list_dsplay = ['username', 'first_name', 'last_name', 'sex', 'role', 'birth_date', 'land', 'city']
admin.site.register(User, UserAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_id', 'slug']
    list_filter = ['category_id']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Subcategory, SubcategoryAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Brand, BrandAdmin)


class MadeInAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(MadeIn, MadeInAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'discount_price', 'count', 'available', 'created', 'updated', 'brand_id', 'category_id', 'made_in_id', 'subcategory_id']
    exclude = ['discount']      # Скрыть поле
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['available', 'created', 'updated']
    list_editable = ['description', 'price', 'discount_price', 'count', 'available']
admin.site.register(Product, ProductAdmin)
    


class CommentAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'user', 'created', 'text']
    list_filter = ['created', 'user']
admin.site.register(Comment, CommentAdmin)