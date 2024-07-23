from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Account
from .serializers import AccountSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import Account
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_confirmation_email


class PasswordResetRequestView(generics.GenericAPIView):
    '''Send a password reset link to the user's email anybody can access this view.'''
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
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
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        user_id = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=user_id)
        if user and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password has been reset.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        '''Authenticate a user using login fields and return a token to be used for future requests.'''
        admission_number = request.data.get('admission_number')
        password = request.data.get('password')
        
        user = authenticate(request, admission_number=admission_number, password=password)
        
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'user_type': user.user_type,
            })
        else:
            return Response({'error': 'Invalid admission number or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        
class EmailConfirmationView(generics.GenericAPIView):
    '''Confirm the user's email address using the token sent to their email for any user.'''
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.email_verified = True  # Mark the email as verified
                user.save()
                return Response({'message': 'Email confirmed successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None
            return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)


class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    '''Override the create method to send a confirmation email to the user.'''
    # def perform_create(self, serializer):
    #     user = serializer.save()
    #     send_confirmation_email(user)

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]