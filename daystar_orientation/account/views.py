from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Account
from .serializers import AccountSerializer, PasswordChangeSerializer
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
                'user_type': user.user_type,
                'campus': user.campus,
                'email': user.email,
                'admission_number': user.admission_number,
                'course': user.course,
                'phone_number': user.phone_number,
            })
        else:
            return Response({'error': 'Invalid admission number or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    def get_permissions(self):
        '''Allow authenticated user to create and view an account.'''
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(AccountList, self).get_permissions()


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]