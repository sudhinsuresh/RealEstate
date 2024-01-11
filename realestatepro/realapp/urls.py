
from django.urls import path
from realapp import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.handlelogin,name="login"),
    path('logout/',views.handlelogout,name='logout'),
    path('adminlogin/',views.admin_login,name='admin_login'),
    path('property_details/<int:id>/',views.property_details,name='property_details'),
    path('sellproperty/',views.sellproperty,name="sellproperty"),
    path('byproperty/<int:id>/',views.byproperty,name="byproperty"),
    path('profile/',views.profile,name="profile"),
    path('addprofile/',views.addprofile,name="addprofile"),
    path('about/',views.about,name="about"),
    path('contact/',views.contactus,name="contact"),
    path('profiledetails/',views.profiledetails,name="profiledetails"),
    path('assigntenantunit/',views.assigntenantunit,name='assign_tenant_unit'),
    path('tenantprofile/<int:id>/',views.tenantprofile,name="tenantprofile"),
    path('search/', views.search, name='search'),
    
]