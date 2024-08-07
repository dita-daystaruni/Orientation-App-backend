from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdmin, IsChild, IsParent
from .models import Account
from .serializers import AccountSerializer, ParentSerializer, PasswordChangeSerializer, ChildSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

class FirstTimeUserPasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = Account.objects.get(
                admission_number=serializer.validated_data['admission_number'],
                is_first_time_user=True,
                user_type='regular'
            )
        except Account.DoesNotExist:
            return Response(
                {'error': 'Invalid admission number or the user is not a first-time user.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(serializer.validated_data['new_password'])
        user.first_time_user = False
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
                return Response({'message': 'First time user, please change your password.'}, status=status.HTTP_200_OK)

            token, created = Token.objects.get_or_create(user=user)
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
                'parent': user.parent
            })
        else:
            return Response({'error': 'Invalid admission number or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
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

class ParentChildrenView(generics.ListAPIView):
    '''Parents see their children.'''
    serializer_class = ParentSerializer
    permission_classes = [IsParent]

    def get_queryset(self):
        return Account.objects.filter(id=self.request.user.id, user_type='parent')

class ChildParentView(generics.RetrieveAPIView):
    '''Children to see their parent's details.'''
    serializer_class = ChildSerializer
    permission_classes = [IsChild]

    def get_object(self):
        return self.request.user
    
class AdminParentChildrenView(generics.ListAPIView):
    '''Admins to see all parents and their children.'''
    serializer_class = ParentSerializer
    permission_classes = [IsAdmin]  

    def get_queryset(self):
        return Account.objects.filter(user_type='parent')

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'admin':
            return Response({'error': 'Only an admin can see this.'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)

class AdminParentChildrenDetailView(generics.RetrieveAPIView):
    '''Admins to see an exact parent and their children.'''
    serializer_class = ParentSerializer
    permission_classes = [IsAdmin] 

    def get_queryset(self):
        return Account.objects.filter(user_type='parent')

    def get_object(self):
        admission_number = self.kwargs.get('admission_number')
        if admission_number:
            try:
                return Account.objects.get(admission_number=admission_number, user_type='parent')
            except Account.DoesNotExist:
                return Response({'error': 'Parent not found.'}, status=status.HTTP_404_NOT_FOUND)
        return super().get_object()
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'admin':
            return Response({'error': 'Only an admin can see this.'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)