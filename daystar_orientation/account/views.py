from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdmin
from .models import Account, Documents
from .serializers import AccountSerializer, PasswordChangeSerializer, ContactSerializer, DocumentSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.cache import add_never_cache_headers
from rest_framework.views import APIView
from hods.models import HOD, Course
from hods.serializers import ContactsSerializer
from .forms import StudentForm 
from django.core.paginator import Paginator
from notifications.models import Notification
from activities.models import Activity
from django.utils import timezone
from .parser_fresh import extract_freshman_info

class FirstTimeUserPasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        admission_number = serializer.validated_data['admission_number']
        new_password = serializer.validated_data['new_password']

        try:
            user = Account.objects.get(admission_number=admission_number, is_first_time_user=True, user_type='regular')
        except Account.DoesNotExist:
            return Response({'message': 'Invalid admission number or the user is not a first-time user.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.is_first_time_user = False
        user.save()
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    
class ResetPasswordView(APIView):
    """
    View To Change Users Password
    """
    def post(self, request, *args, **kwargs):
        """
        Changes A User Password
        """
        admission_number = request.data.get('admission_number')
        password = request.data.get('password')
        try:
            user = Account.objects.get(admission_number=admission_number)
            if user.user_type == 'regular':
                user.set_password("freshman")
                user.is_first_time_user = True
                user.save()
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            else:
                if password is None:
                    return Response({'message': 'Password Is Required'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user.set_password(password)
                    user.save()
                    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)        
        except Account.DoesNotExist:
            return Response({'message': 'Invalid admission number or Admission Number'}, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        '''Authenticate a user using login fields and return a token to be used for future requests.'''
        admission_number = request.data.get('admission_number')
        password = request.data.get('password')

        if not admission_number or not password:
            return Response({'message': 'Admission number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, admission_number=admission_number, password=password)

        if user is not None:
            if user.user_type == 'regular' and user.is_first_time_user:
                return Response({'message': 'First time user, please change your password.'}, status=status.HTTP_412_PRECONDITION_FAILED)

            token, created = Token.objects.get_or_create(user=user)

            parent_details = None
            if user.parent:
                parent_details = {
                    'id': user.parent.id,
                    'first_name': user.parent.first_name,
                    'last_name': user.parent.last_name,
                    'admission_number': user.parent.admission_number,
                    'campus': user.parent.campus,
                    'phone_number': user.parent.phone_number,
                    'email': user.parent.email,
                }
            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'user_type': user.user_type,
                'campus': user.campus,
                'email': user.email,
                'admission_number': user.admission_number,
                'course': user.course.name,
                'phone_number': user.phone_number,
                'gender': user.gender,
                'accomodation': user.accomodation,
                'parent': parent_details
            })
        else:
            return Response({'message': 'Invalid admission number or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
class ParseFreshMen(APIView):
    """
    Parses Freshmen Data
    """
    def post(self, request, *args, **kwargs):
        """
        Parses Freshmen data
        """
        file = request.data.get("file")

        if not file:
            return Response({'message': 'File Is Required'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        freshman_info = extract_freshman_info(file)

        # clean the data
        for data in freshman_info:
            # check if there is more than one name
            if len(data["first_name"].split(" ")) > 0:
                data["first_name"] = data["first_name"].split(" ")[0]
            if len(data["last_name"].split(" ")) > 0:
                data["last_name"] = data["last_name"].split(" ")[-1]

            # change casing of first and last name to a common one
            data["first_name"] = data["first_name"].capitalize()
            data["last_name"] = data["last_name"].capitalize()
            # get course object
            data["course"] = Course.objects.get(name=data["course"])
            data["username"] = data["first_name"] +  data["last_name"]\
                  + data["admission_number"]
            data["phone_number"] = "00000000000"
            data["email"] = None

        # create the accounts
        for freshman in freshman_info:
            try:
                freshman_account = Account(**freshman)
                freshman_account.save()
            except Exception as e:
                raise e
        return Response("LGTM")

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return Account.objects.all()
        return Account.objects.filter(id=self.request.user.id)
    
    def get_permissions(self):
        '''Allow authenticated user to create and view an account.'''
        if self.request.method == 'POST':
            self.permission_classes = [IsAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(AccountList, self).get_permissions()


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'admin':
            return Account.objects.all()
        return Account.objects.filter(id=self.request.user.id)
    
    def get_permissions(self):
        '''Allow authenticated users to view, update their accounts and only admins to delete their account.'''
        if self.request.method in ['DELETE']:
            self.permission_classes = [IsAdmin]
        return super(AccountDetail, self).get_permissions()
    
class Contacts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(Account, pk=pk)
        
        if user.user_type == 'admin':
            parents = Account.objects.filter(user_type='parent')
            serializer = ContactSerializer(parents, many=True)
            return Response(serializer.data)
        
        elif user.user_type == 'parent':
            children = user.children.all()
            serializer = AccountSerializer(children, many=True)
            return Response(serializer.data)
        
        elif user.user_type == 'regular':
            response_data = []

            admins = Account.objects.filter(user_type='admin')
            response_data.extend(ContactSerializer(admins, many=True).data)

            if user.parent:
                response_data.append(ContactSerializer(user.parent).data)

            hods = HOD.objects.filter(course=user.course)
            response_data.extend(ContactsSerializer(hods, many=True).data)

            return Response(response_data)
        
        else:
            return Response({"message": "Invalid user type"}, status=404)

class DocumentUploadView(generics.CreateAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DocumentListView(generics.ListAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Documents.objects.all()

class DocumentDetailView(generics.RetrieveAPIView):
    queryset = Documents.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

class StatsView(APIView):
    def get(self, request):
        course = request.query_params.get('course')

        regular_users = Account.objects.filter(user_type='regular', checked_in=True)
        if course:
            regular_users = regular_users.filter(course=course)

        total_students = regular_users.count()
        male_students = regular_users.filter(gender='Male').count()
        female_students = regular_users.filter(gender='Female').count()
        nairobi_students = regular_users.filter(campus='Nairobi').count()
        athi_river_students = regular_users.filter(campus='Athi river').count()
        dayscholar_students = regular_users.filter(accomodation='Dayscholar').count()
        boarder_students = regular_users.filter(accomodation='Boarder').count()

        data = {
            'total_students': total_students,
            'male_students': male_students,
            'female_students': female_students,
            'nairobi_students': nairobi_students,
            'athi_river_students': athi_river_students,
            'dayscholar_students': dayscholar_students,
            'boarder_students': boarder_students
        }

        return Response(data)
    

class StatsData(APIView):
    def get(self, request):
        """
        """
        course = request.query_params.get('course')

        regular_users = Account.objects.filter(user_type='regular', checked_in=True)
        if course:
            regular_users = regular_users.filter(course=course)
        serializer = AccountSerializer(regular_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Web views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    response = render(request, 'signin.html')
    
    add_never_cache_headers(response)

    if request.method == 'POST':
        admission_number = request.POST.get('admission_number')
        password = request.POST.get('password')

        if not admission_number or not password:
            messages.error(request, 'Admission number and password are required.')
            return render(request, 'signin.html')

        user = authenticate(request, admission_number=admission_number, password=password)

        if user is not None:
            if user.user_type != 'admin':
                messages.error(request, 'Only Admins(G9s) can see the administrative view')
                return render(request, 'signin.html')

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            request.session['auth_token'] = token.key
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid admission number or password.')
            return render(request, 'signin.html')

    return render(request, 'signin.html')

def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required
def studentsadd_view(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    if request.method == 'POST':
        try:
            # Handle form submission
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            gender = request.POST.get('gender')
            admission_number = request.POST.get('admissionNumber')
            course_name = request.POST['course']  
            phone_number = request.POST.get('phoneNumber')
            email = request.POST.get('email')
            parent_id = request.POST.get('parentName')
            campus = request.POST.get('campus')
            accomodation = request.POST.get('accomodation')
            checked_in = request.POST.get('checked_in', False) 

            course = Course.objects.get(name=course_name) if course_name else None
            parent = Account.objects.get(pk=parent_id) if parent_id else None

            new_student = Account.objects.create_user(
                user_type='regular',
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                admission_number=admission_number,
                course=course,
                phone_number=phone_number,
                email=email,
                parent=parent,
                campus=campus,
                accomodation=accomodation,
                checked_in=checked_in,
                username=None
            )
            new_student.save()

            messages.success(request, 'Student added successfully.')
            return redirect('students_details')

        except Exception as e:
            messages.error(request, f'Error adding student: {e}')
            return redirect('students_add')

    courses = Course.objects.all()
    parents = Account.objects.filter(user_type='parent')

    return render(request, 'students_add.html', {
        'courses': courses,
        'parents': parents
    })

@login_required
def studentedit_view(request, student_id):
    student = get_object_or_404(Account, id=student_id)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Student details updated successfully.')
                return redirect('students_details')
            except Exception as e:
                messages.error(request, f'Error occurred: {str(e)}')
        else:
            messages.error(request, 'There was an error with your form submission.')
    
    else:
        form = StudentForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
        'courses': Course.objects.all()
    }
    return render(request, 'students_edit.html', context)


@login_required
def delete_student(request, student_id):
    student = get_object_or_404(Account, id=student_id)
    
    try:
        student.delete()
        messages.success(request, 'Student has been deleted successfully.')
    except Exception as e:
        messages.error(request, f'Error occurred: {str(e)}')
    
    return redirect('students_details')


@login_required
def studentsdetails_view(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    student_list = Account.objects.filter(user_type='regular').order_by('admission_number')
    paginator = Paginator(student_list, 15) 
    
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'students.html', {'page_obj': page_obj})

def G9_view(request):
    if request.method == 'POST':
        user_type = request.POST['user_type']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        admission_number = request.POST['admission_number']
        course_name = request.POST['course']
        password = request.POST['password'] 
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        campus = request.POST['campus']
        
        try:
            course = Course.objects.get(name=course_name)
            
            Account.objects.create_user(
                user_type=user_type,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                admission_number=admission_number,
                course=course,
                password=password,
                phone_number=phone_number,
                email=email,
                campus=campus,
                checked_in=True,
                username=None
            )
            
            messages.success(request, 'Account successfully created.')
            return redirect('admin_add')
        
        except Course.DoesNotExist:
            messages.error(request, f"The course '{course_name}' does not exist.")
            return redirect('admin_add')
        
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('admin_add')

    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'admin_parent.html', context)


@login_required
def dashboard_view(request):
    new_students_count = Account.objects.filter(user_type='regular').count()
    checked_in_count = Account.objects.filter(user_type='regular', checked_in=True).count()
    not_checked_in_count = Account.objects.filter(user_type='regular', checked_in=False).count()

    # Recent Notifications
    recent_notifications = Notification.objects.filter(is_admin_viewer=True).order_by('-created_at')[:4]
    if not recent_notifications:
        messages.info(request, 'No recent notifications available.')

    # New Students List
    new_students = Account.objects.filter(user_type='regular').order_by('-id')[:3]
    if not new_students:
        messages.info(request, 'No new students registered.')

    # Main Sessions
    today = timezone.now().date()
    main_sessions = Activity.objects.filter(is_session=True, date=today).order_by('start_time')[:3]
    if not main_sessions:
        messages.info(request, 'No main sessions scheduled for today.')

    # Today's Schedule
    todays_schedule = Activity.objects.filter(is_session=False, date=today).order_by('start_time')[:3]
    if not todays_schedule:
        messages.info(request, 'No activities scheduled for today.')

    context = {
        'new_students_count': new_students_count,
        'checked_in_count': checked_in_count,
        'not_checked_in_count': not_checked_in_count,
        'recent_notifications': recent_notifications,
        'new_students': new_students,
        'main_sessions': main_sessions,
        'todays_schedule': todays_schedule,
    }
    return render(request, 'dashboard.html', context)