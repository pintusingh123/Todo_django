 
from django.contrib import admin
from django.urls import path,include
# from tudoapp.urls import todo
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("tudoapp.urls"))
]
