Introduction
============

Slugmeta is a small utility to be used together with the very handy
transmeta package (http://code.google.com/p/django-transmeta/). It is
used for generating `AdminModel`s where the prepopulated fields are
translated with transmeta (I used it for translating slugs, hence the
name).

An example
==========

Consider the following model

    class Product(models.Model):
        __metaclass__ = TransMeta
        name = models.CharField(max_length=255)
        slug = models.SlugField(max_length=255, unique=True)

        class Meta:
            translate = ('name', 'slug')

With the following admin model

    class ProductAdmin(admin.ModelAdmin):
        prepopulated_fields = {"slug": ("name",)}
    admin.site.register(models.Product, ProductAdmin)

This will fail.

    'ProductAdmin.prepopulated_fields' refers to field 'slug' that is missing from model 'Product'

Quite naturally, transmeta helpfully created `slug_$LANG` for each
specified language for us, and removed the `slug` field.

Enter slugmeta
==============

With slugmeta, you set the SlugMeta as the metaclass of your
`ModelAdmin`, and specify another member
`prepopulated_fields_translate` instead of `prepopulated_fields`. We
still have the same `Product` class as above.

    import slugmeta

    class ProductAdmin(admin.ModelAdmin):
        __metaclass__ = slugmeta.SlugMeta
        prepopulated_fields_translate = {"slug": ("name",)}
    admin.site.register(models.Product, ProductAdmin)

This will loop through all the languages in your `settings.LANGUAGES`
and create `prepopulated_fields` for all of them. For example, if your
languages would be Spanish and Swedish, the above would be equivalent
to

    class ProductAdmin(admin.ModelAdmin):
        prepopulated_fields = {"slug_es": ("name_es",),
                               "slug_sv": ("name_sv",)}

You can combine this with normal -- untranslated --
`prepopulated_fields`. The following

    class ProductAdmin(admin.ModelAdmin):
        __metaclass__ = slugmeta.SlugMeta
        prepopulated_fields = {"author_slug": ("author",)}
        prepopulated_fields_translate = {"slug": ("name",)}

is equivalent to

    class ProductAdmin(admin.ModelAdmin):
        prepopulated_fields = {"author_slug": ("author",),
                               "slug_es": ("name_es",),
                               "slug_sv": ("name_sv",)}

Limitations
===========

Currently, all field names in `prepopulated_fields_translate` are
considered to be translated. This is because the `ModelAdmin` class
has no idea about what `Model` class its operating on. One solution
would be to add a reference to the class for which it is the admin, so
it could check the `Meta.translate` member of that class.

License
=======

Copyright (c) 2011 Magnus Hult <magnus@magnushult.se>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
