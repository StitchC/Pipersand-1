from django.conf.urls import url
from game import views as game_views



urlpatterns = [
    url(r'^(\w+)$', game_views.cmd_proxy),
    url(r'^util/roll_back', game_views.roll_back),
    url(r'^long_loan', game_views.long_loan),
]
