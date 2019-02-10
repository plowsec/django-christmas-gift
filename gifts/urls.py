from django.urls import path

from . import views

app_name = "gifts"
urlpatterns = [
    path('', views.ListPersons.as_view(), name='listPersons'),
    path('person/create', views.AddPerson.as_view(), name='addPerson'),
    path('person/<int:pk>/delete', views.DeletePerson.as_view(), name='deletePerson'),
    path('person/<int:pk>/update', views.UpdatePerson.as_view(), name='updatePerson'),    
    path('person/<int:pk>', views.DetailPerson.as_view(), name='detailPerson'),
    path('gift/add/<int:person>', views.AddGift.as_view(), name="addGift"),
    path('gift/<int:pk>/update', views.UpdateGift.as_view(), name='updateGift'),
    path('gift/<int:pk>/delete', views.DeleteGift.as_view(), name='deleteGift'),
    #path('gift/<int:pk>/setWrapped/<int:b>', views.SetGiftWrapped.as_view(), name='setGiftWrapped'),
]
