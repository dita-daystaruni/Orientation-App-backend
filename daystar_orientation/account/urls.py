from django.urls import path
from .views import AccountList, AccountDetail, CustomAuthToken, FirstTimeUserPasswordChangeView, ParentChildrenView, ChildParentView, AdminParentChildrenView, AdminParentChildrenDetailView, login_view, dashboard_view, studentsadd_view, studentsdetails_view


urlpatterns = [
    path('accounts/', AccountList.as_view(), name='account-list'),
    path('accounts/<int:pk>/', AccountDetail.as_view(), name='account-detail'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('first-password-change/', FirstTimeUserPasswordChangeView.as_view(), name='first-password-change'),
    path('parent-children/', ParentChildrenView.as_view(), name='parent-children'),
    path('child-parent/', ChildParentView.as_view(), name='child-parent'),
    path('admin-parents/', AdminParentChildrenView.as_view(), name='admin-parents'),
    path('admin-parents/<str:admission_number>/', AdminParentChildrenDetailView.as_view(), name='parent-admission'),
    path('signin/', login_view, name='signin'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('students/add/', studentsadd_view, name='students_add'),
    path('students/', studentsdetails_view, name='students_details'),
]