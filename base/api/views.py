from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET']) # only allow GET requests 
def getRoutes(request):
    routes = [
        'GET /api/',
        'GET /api/rooms/',
        'GET /api/rooms/:id/',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True) # many=True because we are serializing a list of objects
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False) # many=True because we are serializing a list of objects
    return Response(serializer.data)