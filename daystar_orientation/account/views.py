from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Account
from .serializers import AccountSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

class PasswordResetRequestView(generics.GenericAPIView):
    '''Send a password reset link to the user's email'''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = Account.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"{request.scheme}://{request.get_host()}/api/password-reset-confirm/{uid}/{token}/"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset link sent.'}, status=status.HTTP_200_OK)
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(generics.GenericAPIView):
    '''Reset the user's password using the token sent to their email for any user.'''
    permission_classes = [IsAuthenticated]

    def post(self, request, uidb64, token):
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            if not new_password:
                return Response({'error': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password has been reset.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        '''Authenticate a user using login fields and return a token to be used for future requests.'''
        admission_number = request.data.get('admission_number')

        if not admission_number:
            return Response({'error': 'Admission number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, admission_number=admission_number)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'user_type': user.user_type,
            })
        else:
            return Response({'error': 'Admission number does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

class EmailConfirmationView(generics.GenericAPIView):
    '''Confirm the user's email address using the token sent to their email for any user.'''
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.email_verified = True  # Mark the email as verified
            user.save()
            return Response({'message': 'Email confirmed successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)

class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    def get_permissions(self):
        '''Allow any user to create an account, but only authenticated users to view the list.'''
        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(AccountList, self).get_permissions()

    #  send a confirmation email after account creation
    # def perform_create(self, serializer):
    #     '''Saves the new user and sends a confirmation email.'''
    #     user = serializer.save()
    #     #send_confirmation_email(user)

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]