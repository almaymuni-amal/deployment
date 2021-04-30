from django.urls import path
from . import views
                    
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('wishes', views.welcome),
    path('login', views.login),
    path('logout', views.logout),
    # render add page
    path('wishes/new', views.new_wish),
    # create wish
    path('wishes/add', views.add_wish),
    path('cancel', views.cancel),
    path('wishes/<int:w_id>/remove', views.remove_wish),
    path('wishes/edit/<int:w_id>', views.edit_wish),
    path('wishes/update/<int:w_id>', views.update_wish),
    path('wishes/granted/<int:w_id>', views.granted_wish),
    path('wishes/like/<int:w_id>', views.make_like),
    path('wishes/view', views.view_stats),

]