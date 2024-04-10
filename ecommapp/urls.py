from django.contrib import admin
from django.urls import path
from ecommapp import views
from ecommapp.views import SimpleView
from ecommapp.views import NewView
from ecommapp.views import OldView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('contact',views.contact),
    path('home',views.home),
    path('edit/<rid>',views.edit),
    path('del1/<pid>',views.del1),
    path('myview',SimpleView.as_view()),
    path('hisview',NewView.as_view()),
    path('oldview',OldView.as_view()),
    path('index',views.newhome),
    path('page1',views.page2),
    path('homepage',views.page1),
    path('newpath',views.oldpath),
    path('oldpath',views.newpath),
    path('hello',views.hello),
    path('city',views.city),
    path('number',views.number),
    path('prod',views.prod),
    path('register',views.register),
    path('login2',views.user_login),
    path('logout',views.user_logout),
    path('pdetails/<pid>',views.productdetail),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('cart',views.cart),
    path('range',views.range),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
    path('viewcart',views.viewcart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('placeorder',views.placeorder),
    path('makepayment',views.makepayment)

]
if settings.DEBUG:
    urlpatterns+=(static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT))













