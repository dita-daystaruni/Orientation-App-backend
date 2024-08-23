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
from hods.models import HOD
from hods.serializers import ContactsSerializer

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
            return Response({'error': 'Invalid admission number or the user is not a first-time user.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.is_first_time_user = False
        user.save()
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        '''Authenticate a user using login fields and return a token to be used for future requests.'''
        admission_number = request.data.get('admission_number')
        password = request.data.get('password')

        if not admission_number or not password:
            return Response({'error': 'Admission number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, admission_number=admission_number, password=password)


        if user is not None:
            if user.user_type == 'regular' and user.is_first_time_user:
                return Response({'message': 'First time user, please change your password.'}, status=status.HTTP_403_FORBIDDEN)

            token, created = Token.objects.get_or_create(user=user)

            parent_details = None
            if user.parent:
                parent_details = {
                    'id': user.parent.id,
                    'first_name': user.parent.first_name,
                    'last_name': user.parent.last_name,
                    'admission_number': user.parent.admission_number,
                    'campus': user.parent.campus
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
                'course': user.course,
                'phone_number': user.phone_number,
                'gender': user.gender,
                'accomodation': user.accomodation,
                'parent': parent_details
            })
        else:
            return Response({'error': 'Invalid admission number or password.'}, status=status.HTTP_401_UNAUTHORIZED)

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
            serializer = ContactSerializer(children, many=True)
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
            return Response({"error": "Invalid user type"}, status=404)
        
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
                return render(request, 'signin.html', {
                    'error_message': 'Only Admins(G9) are allowed to login to the web version of the application'
                })

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            request.session['auth_token'] = token.key
            return redirect('students_details')
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
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        gender = request.POST.get('gender')
        admission_number = request.POST.get('admissionNumber')
        course = request.POST.get('courseName')
        phone_number = request.POST.get('phoneNumber')
        accomodation = request.POST.get('accomodation')
        campus = request.POST.get('campus')

        if not (first_name and last_name and gender and admission_number and course and phone_number and accomodation and campus):
            messages.error(request, 'All fields are required.')
            return render(request, 'students_add.html')

        if Account.objects.filter(admission_number=admission_number).exists():
            messages.error(request, "Admission number already exists.")
            return render(request, 'students_add.html')

        Account.objects.create(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            admission_number=admission_number,
            course=course,
            phone_number=phone_number,
            accomodation=accomodation,
            campus=campus
        )

        messages.success(request, 'Student details added successfully!')
        return redirect('students_add')

    return render(request, 'students_add.html')

@login_required
def studentsdetails_view(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    students = Account.objects.filter(user_type='regular')
    return render(request, 'students.html', {'students': students})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')