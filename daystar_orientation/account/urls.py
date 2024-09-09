from django.urls import path
from .views import AccountList, AccountDetail, CustomAuthToken, FirstTimeUserPasswordChangeView, Contacts, StatsView, StatsData, DocumentUploadView, DocumentListView, DocumentDetailView, login_view, dashboard_view, studentsadd_view, studentedit_view, studentsdetails_view, delete_student, logout_view, G9_view
from .views import ResetPasswordView, ParseFreshMen, ResetAllFreshmenPassword


urlpatterns = [
    path('accounts/', AccountList.as_view(), name='account-list'),
    path('password-change/', ResetPasswordView.as_view(), name="resetpassword"),
    path('password-reset-freshmen/', ResetAllFreshmenPassword.as_view(), name="freshmenresetpassword"),
    path('parse-freshmen/', ParseFreshMen.as_view(), name="parse_freshmen"),
    path('accounts/<int:pk>/', AccountDetail.as_view(), name='account-detail'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('first-password-change/', FirstTimeUserPasswordChangeView.as_view(), name='first-password-change'),
    path('contacts/<int:pk>/', Contacts.as_view(), name='contacts'),
    path('statistics/', StatsView.as_view(), name='statistics'),
    path('statistics/data/', StatsData.as_view(), name='statistics-data'),
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('signin/', login_view, name='signin'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('students/edit/<int:student_id>/', studentedit_view, name='students_edit'),
    path('students/add/', studentsadd_view, name='students_add'),
    path('students/delete/<int:student_id>/', delete_student, name='students_delete'),
    path('G9/', G9_view, name='admin_add'),
    path('students/', studentsdetails_view, name='students_details'),
]