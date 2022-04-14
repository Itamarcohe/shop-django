from django.urls import path
from .views import CustomAccountCreate, BlacklistTokenView
app_name = 'accounts'

urlpatterns = [
    path('register/', CustomAccountCreate.as_view(), name='create_user'),
    path('logout/blacklist/', BlacklistTokenView.as_view(),
         name='blacklist')

]