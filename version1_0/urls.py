from django.urls import path, register_converter
from .views import CharBeeURLRegister as URLRegister
from django.conf.urls.static import static
from . import converter
register_converter(converter.signedInteger, 'sing')

urlpatterns = [
    # path(r'detail',views.GetBeverageDetailedInfo),
    # path(r'about',views.GetBeverageSimpleInfo),
    path(r'', URLRegister.IndexHandle),
    path(r'Index', URLRegister.IndexHandle),
    path(r'Index/', URLRegister.IndexHandle),

    path(r'AboutUs', URLRegister.AboutUsHandle),
    path(r'AboutUs/', URLRegister.AboutUsHandle),

    path(r'BeverageInfo/<str:_id>', URLRegister.BeverageInfoHandle),
    path(r'BeverageInfo/<str:_id>/', URLRegister.BeverageInfoHandle),
    path(r'BeverageInfo/<str:_id>/<str:capacity>',
         URLRegister.BeverageInfoHandle),
    path(r'BeverageInfo/<str:_id>/<str:capacity>/',
         URLRegister.BeverageInfoHandle),

    path(r'ShopMenu/<str:shop>', URLRegister.ShopMenuHandle),
    path(r'ShopMenu/<str:shop>/', URLRegister.ShopMenuHandle),
    path(r'ShopMenu/<str:shop>/<sing:focusPage>', URLRegister.ShopMenuHandle),
    path(r'ShopMenu/<str:shop>/<sing:focusPage>/', URLRegister.ShopMenuHandle),

    path(r'Result', URLRegister.ResultHandle),
    path(r'Result/', URLRegister.ResultHandle),
    path(r'Result/<sing:focusPage>', URLRegister.ResultHandle),
    path(r'Result/<sing:focusPage>/', URLRegister.ResultHandle),

    path(r'Compare', URLRegister.IndexHandle),
    path(r'Compare/', URLRegister.IndexHandle),
] + static('/static/')
