from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GroupSerializer, GroupMemberSerializer, GroupListSerializer
from .models import Group, GroupMember, GroupEvent
from kafka import KafkaProducer
import json
from datetime import datetime



class GroupCreationView(APIView):
    """
    Handles group creation. 
    - Creates a Group.
    - Adds the creator as an admin member.
    - Logs event in GroupEvent.
    - Publishes group_created event to Kafka.
    """

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
    
            group = serializer.save(
                creator_id=request.user.id,
                member_count=1
            )

            GroupMember.objects.create(
                group=group,
                user_id=request.user.id,
                role='admin'
            )

            GroupEvent.objects.create(
                group=group,
                user_id=request.user.id,
                event_type='created'
            )

            try:
                producer = KafkaProducer(
                    bootstrap_servers='kafka:9092',
                    value_serializer=lambda v: json.dumps(v).encode('utf-8')
                )

                message = {
                    'group_id': group.id,
                    'name': group.name,
                    'creator_id': group.creator_id,
                    'created_at': group.created_at.isoformat(),
                }

                producer.send('group_created', value=message)
                producer.flush()
            except Exception as e:
                print(f"⚠️ Kafka error: {e}")

            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupJoinView(APIView):
    """
    Handles joining a group.
    - Checks if group exists and is not full (limit 30).
    - Adds user as a member.
    - Logs join event.
    - Publishes user_joined event to Kafka.
    """

    def post(self, request):
        group_id = request.data.get('group_id')

        if not group_id:
            return Response({'error': 'group_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            group_obj = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

      
        if GroupMember.objects.filter(group=group_obj, user_id=request.user.id).exists():
            return Response({'error': 'User already a member'}, status=status.HTTP_400_BAD_REQUEST)

        if group_obj.member_count >= 30:
            return Response({'error': 'Group is full'}, status=status.HTTP_400_BAD_REQUEST)

      
        join = GroupMember.objects.create(
            group=group_obj,
            user_id=request.user.id,
            role='member'
        )

        group_obj.member_count += 1
        group_obj.save()

        GroupEvent.objects.create(
            group=group_obj,
            user_id=request.user.id,
            event_type='joined'
        )

        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

            message = {
                'group_id': group_obj.id,
                'user_id': request.user.id,
                'role': join.role,
                'joined_at': join.joined_at.isoformat()
            }

            producer.send('user_joined', value=message)
            producer.flush()
        except Exception as e:
            print(f"⚠️ Kafka error: {e}")

        return Response(GroupMemberSerializer(join).data, status=status.HTTP_201_CREATED)
    

class GroupLeaveView(APIView):

    def post(self, request):

        group_id = request.data.get('group_id')

        if not group_id:
            return Response({'error': 'group_id is required'},status=status.HTTP_400_BAD_REQUEST)

        try:
            group_obj = Group.objects.get(id=group_id)

        except Group.DoesNotExist:
            return Response({'error': 'group does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        group_obj.member_count -= 1
        group_obj.save()

        GroupMember.objects.update(left_at=datetime.now())
        GroupEvent.objects.create(
            group=group_obj,
            user_id=request.user.id,
            event_type='left'
        )

from django.utils import timezone

class GroupLeaveView(APIView):
    """
    Handles leaving a group.
    - Checks if group exists.
    - Ensures user is a member.
    - Marks the member as left (sets left_at).
    - Decreases member_count.
    - Logs event.
    - Publishes user_left event to Kafka.
    """

    def post(self, request):
        group_id = request.data.get('group_id')

        if not group_id:
            return Response({'error': 'group_id is required'}, status=status.HTTP_400_BAD_REQUEST)

      
        try:
            group_obj = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'error': 'Group does not exist'}, status=status.HTTP_404_NOT_FOUND)

 
        try:
            membership = GroupMember.objects.get(group=group_obj, user_id=request.user.id, left_at__isnull=True)
        except GroupMember.DoesNotExist:
            return Response({'error': 'User is not a member of this group'}, status=status.HTTP_400_BAD_REQUEST)

     
        membership.left_at = timezone.now()
        membership.save()

       
        if group_obj.member_count > 0:
            group_obj.member_count -= 1
            group_obj.save()


        GroupEvent.objects.create(
            group=group_obj,
            user_id=request.user.id,
            event_type='left'
        )

        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

            message = {
                'group_id': group_obj.id,
                'user_id': request.user.id,
                'left_at': membership.left_at.isoformat()
            }

            producer.send('user_left', value=message)
            producer.flush()
        except Exception as e:
            print(f"⚠️ Kafka error: {e}")

        return Response({'message': 'Successfully left group'}, status=status.HTTP_200_OK)


class GroupListView(APIView):
    """
    Returns all groups the current user is a member of,
    along with group details and members/events.
    """

    def get(self, request):
    
        memberships = GroupMember.objects.filter(user_id=request.user.id)

      
        groups = Group.objects.filter(id__in=memberships.values_list('group_id', flat=True))

        serializer = GroupListSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupDetailView(APIView):
    """
    Returns details of a single group, including members and events.
    """

    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'error': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GroupListSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)