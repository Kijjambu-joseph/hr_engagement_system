"""Auth endpoints for the custom user model.

These views are intentionally lightweight and use Django REST framework plus
SimpleJWT instead of model classes that do not exist.
"""

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    LoginSerializer,
    ProfileSerializer,
    UpdateProfileSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    RefreshTokenSerializer,
)


User = get_user_model()


def login_page(request):
    return render(request, 'login.html')


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(
            request,
            username=username_or_email,
            password=password,
        )

        if not user:
            if '@' in username_or_email:
                try:
                    user_obj = User.objects.get(email__iexact=username_or_email)
                except User.DoesNotExist:
                    user_obj = None
                if user_obj:
                    user = authenticate(
                        request,
                        username=user_obj.username,
                        password=password,
                    )
            else:
                try:
                    user_obj = User.objects.get(username__iexact=username_or_email)
                except User.DoesNotExist:
                    user_obj = None
                if user_obj:
                    user = authenticate(
                        request,
                        username=user_obj.username,
                        password=password,
                    )

        if not user:
            return Response(
                {'error': 'Invalid credentials.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Determine redirect URL based on explicit role first, then groups
        role = getattr(user, 'role', None)

        if role == 'branch_staff' or user.groups.filter(name='Employee').exists():
            redirect_url = '/employeedash/'
            role_label = 'employee'
        elif role == 'branch_manager' or user.groups.filter(name__iexact='Branch managers').exists():
            redirect_url = '/branchmanager/'
            role_label = 'branch_manager'
        elif role in ('hrbp', 'hr_specialist') or user.groups.filter(name__iexact='HR').exists() or user.groups.filter(name__iexact='Hr').exists():
            redirect_url = '/genmanagerdash/'
            role_label = 'hr'
        elif role == 'executive' or user.groups.filter(name__iexact='Executives').exists():
            redirect_url = '/genmanagerdash/'
            role_label = 'executive'
        else:
            # fallback to group-based checks or general manager dashboard
            if user.groups.filter(name__icontains='manager').exists() or user.groups.filter(name='Managers').exists():
                redirect_url = '/genmanagerdash/'
                role_label = 'manager'
            else:
                redirect_url = '/genmanagerdash/'
                role_label = role or 'regular'

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'redirect_url': redirect_url,
            'role': role_label,
        })


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class CurrentUserAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class UpdateProfileAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'Incorrect password.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            validate_password(serializer.validated_data['new_password'], user=user)
        except ValidationError as exc:
            return Response({'new_password': list(exc.messages)}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        return Response({'detail': 'Password updated successfully.'})


class ForgotPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'detail': 'If the account exists, a reset link can be sent.'})


class ResetPasswordAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        new_password = serializer.validated_data['new_password']
        try:
            validate_password(new_password, user=user)
        except ValidationError as exc:
            return Response({'new_password': list(exc.messages)}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save(update_fields=['password'])
        return Response({'detail': 'Password reset successfully.'})


class RefreshTokenAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken(serializer.validated_data['refresh'])
        return Response({'access': str(refresh.access_token)})

def home(request):
    return redirect('/genmanagerdash/')