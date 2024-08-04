from django.http import JsonResponse
from rest_framework.views import APIView


class UserDetailsAPIView(APIView):

    def get(self, request):
        username = request.user.username
        name = request.user.name
        profile_picture = request.user.profile_picture.url if request.user.profile_picture else None
        return JsonResponse({"username": username, "name": name, "profile_picture": profile_picture})
