         # -*- coding: utf-8 -*-
import re
from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.core import urlresolvers
from django.template import RequestContext
from catalog.models import Category, Product, Section
from django.http import HttpResponseRedirect, HttpResponse
from cart import cart
import threading
from django.core.mail import send_mail
from cart import settings

def index(request):
    page_title = u'Монтаж видеонаблюдения, установка видеонаблюдения - Цептум. Москва'
    meta_keywords = """установка систем видеонаблюдения монтаж камер лицензия сигнализация прайс
     лист стоимость услуги в квартира офис школа помещение"""
    meta_description = """Все для Видеонаблюдения - установка и монтаж систем видеонаблюдени.
     Продажа видеокамер, видеорегистраторов и аксессуаров по доступным ценам"""
    sections = Section.objects.all()
    return render_to_response("main/index.html", locals(), context_instance=RequestContext(request))

def cats(request):
    cats = Category.objects.all()
    sections = Section.objects.all()
    return render_to_response("main/cats.html", locals(), context_instance=RequestContext(request))

def show_category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    if request.method == 'POST':
        cart.add_to_cart(request)
        url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(url)
    else:
        products = category.product_set.filter(is_active=True).order_by('categoryproduct__position')
    if category.section.name == category.name:
        page_title = u'%s - Цептум' % category.section
    else:
        page_title = u'%s %s - Цептум' % (category.section, category)
    meta_keywords = category.meta_keywords
    meta_description = category.meta_descriotion
    meta_keywords = category.meta_keywords
    sections = Section.objects.filter(is_active=True)
    return render_to_response("main/catalog.html", locals(), context_instance=RequestContext(request))


def show_section(request, section_slug):
    section = Section.objects.get(slug=section_slug)
    sections = Section.objects.filter(is_active=True)
    cats = section.category_set.filter(is_active=True)
    page_title = section.name + u' - Fewline'
    return render_to_response("main/section.html", locals(), context_instance=RequestContext(request))

def show_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    photos = product.productphoto_set.all()
    if request.method == 'POST':
        postdata = request.POST.copy()
        if 'product_slug' in postdata:
            cart.add_to_cart(request)
            url = urlresolvers.reverse('show_cart')
            return HttpResponseRedirect(url)
    page_title = u'%s - Цептум' % product.name
    meta_keywords = page_title
    meta_description = "%s - %s" % (page_title, product.mini_html_description)
    sections = Section.objects.all()
    return render_to_response("main/tovar.html", locals(), context_instance=RequestContext(request))

def all_goods(request):
    if request.method == 'POST':
        cart.add_to_cart(request)
        url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(url)
    products = Product.objects.filter(is_active=True)
    page_title = u'Цептум Все товары'
    meta_keywords = page_title
    return render_to_response("main/catalog.html", locals(), context_instance=RequestContext(request))

def about(request):
    page_title = u'О нас - Цептум'
    return render_to_response('main/about.html', locals(), context_instance=RequestContext(request))

def delivery(request):
    page_title = u'Оплата и Монтаж - Цептум'
    return render_to_response('main/delivery.html', locals(), context_instance=RequestContext(request))

def internal_error(request):
    return render_to_response('500.html', locals(), context_instance=RequestContext(request))

def take_call_form(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if not "href" in postdata['message']:
            if settings.SEND_ADMIN_EMAIL:
                t = threading.Thread(target= send_mail, args=[
                    u'Перезвонить, %s' % postdata['name'],
                    u'Имя: %s \nТелефон: %s\nСообщение: %s\n' % (postdata['name'], postdata['phone'], postdata['message']),
                   settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
                t.setDaemon(True)
                t.start()
        return HttpResponse()

def take_vk_comment(request):
    if request.method == 'POST':
        param = request.POST['comment']
        if settings.SEND_ADMIN_EMAIL:
            t = threading.Thread(target= send_mail, args=[
            u'Новый комментарий',
            u'%s' % param, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], 'fail_silently=False'])
            t.setDaemon(True)
            t.start()
    return HttpResponse()
