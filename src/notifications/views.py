from rest_framework import viewsets, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from account.models import User
from .models import Notification
from .serializers import NotificationSerializer

from django.db.models import Q
from django.shortcuts import get_object_or_404

from extensions.pagination import CustomPagination
#TODO Add ability for users to tunr on & off notifications

@api_view(['GET'])
@permission_classes((AllowAny,))
def NotificationView(request):
    notify_list = Notification.objects.filter(
        to_user=request.user,
    ).order_by('-id')
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(notify_list,request)
    noti_count = Notification.objects.filter(
        to_user=request.user
    ).count()
    """
    instead of doing ,if 0 then not show notificaton badge in client side 
    we just send null value to notification count from server if count is 0
    """
    if noti_count == 0:
        noti_count  = None  
    serializer = NotificationSerializer(result_page, many=True, context={
                                        
                                        'request': request
                                        })
    # return Response(serializer.data)
    return paginator.get_paginated_response({'data':serializer.data,'noti_count': noti_count})
    
class NotificationSeen(APIView):
    permission_classes = (AllowAny, )
    
    def post(self,request):
        data = request.data
        notification = get_object_or_404(Notification,id=data.get('notify_id'))
        if notification.to_user == request.user:
            notification.user_has_seen =  True
            notification.delete()
            return Response({"notification_deleted": True})
    
class NotificationDelete(APIView):
    permission_classes = (AllowAny, )

    def post(self,request):
        data = request.data
        notification = get_object_or_404(Notification,id=data.get('notify_id'))
        if notification.to_user == request.user:
            notification.user_has_seen =  True
            notification.delete()
            return Response({"notification_deleted": True})
