
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from tripsservice.models.EmployeeModel import Employee
from tripsservice.views.EmployeePermission import IsViewAllEmployeePermission
from tripsservice.serializers.EmployeeSerializer import EmployeeSerializer


class EmployeeView(APIView):
    
    permission_classes = [IsAuthenticated, IsViewAllEmployeePermission]

    def get(self, request):
        employees = Employee.objects.all()
        return Response({
            "employees": EmployeeSerializer(employees, many=True).data,
        })