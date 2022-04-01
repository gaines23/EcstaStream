import django_filters
from .models import *

class UserFavoritesFilter(django_filters.FilterSet):
    model = FavoriteListData
    fields = ['user', 'mov_show_id', 'date_added']