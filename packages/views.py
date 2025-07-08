from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Package
from .serializers import PackageSerializer, PackageCreateUpdateSerializer


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def list_create_packages(request):
    """List all active packages (GET) or create a new package (POST)"""
    if request.method == 'GET':
        packages = Package.objects.filter(is_active=True)
        serializer = PackageSerializer(packages, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'count': len(serializer.data)
        })
    
    elif request.method == 'POST':
        serializer = PackageCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            package = serializer.save()
            response_serializer = PackageSerializer(package)
            return Response({
                'status': 'success',
                'message': 'Package created successfully',
                'data': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def package_detail(request, package_id):
    """Get package details (GET), update package (PUT), or delete package (DELETE)"""
    package = get_object_or_404(Package, id=package_id)
    
    if request.method == 'GET':
        serializer = PackageSerializer(package)
        return Response({
            'status': 'success',
            'data': serializer.data
        })
    
    elif request.method == 'PUT':
        serializer = PackageCreateUpdateSerializer(package, data=request.data, partial=True)
        if serializer.is_valid():
            updated_package = serializer.save()
            response_serializer = PackageSerializer(updated_package)
            return Response({
                'status': 'success',
                'message': 'Package updated successfully',
                'data': response_serializer.data
            })
        return Response({
            'status': 'error',
            'message': 'Validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        package.delete()
        return Response({
            'status': 'success',
            'message': 'Package deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
