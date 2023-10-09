from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Library
from .serializers import CreateLibrarySerializer


class CreateLibraryAPIView(CreateAPIView):
    queryset = Library.objects.all()
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]

class LibraryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Library.objects.all()
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]

# class ListLibraryAPIView(ListAPIView):
#     serializer_class = CreateLibrarySerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         org_id = self.kwargs.get('org_id')
#         lib  = Library.objects.filter(organization__id=org_id)
#         list_lib = []
#         for i in lib:
#             lib_r={}
#             lib_r['id'] = i.id
#             lib_r['library_name'] = i.library_name
#             lib_r['description'] = i.description
#             lib_r['organization'] = i.organization
#             list_lib.append(lib_r)
#             # print(i.id,"<<<<")
#         # print(org_id, lib , "<<<<<<<<<")
#         print(list_lib)
#         return  list_lib


from rest_framework import response, views


class ListLibraryAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, org_id):   
        lib = Library.objects.filter(organization__id=org_id)
        list_lib = []
        for i in lib:
            lib_r = {}
            lib_r['id'] = i.id
            lib_r['library_name'] =i.library_name
            lib_r['description'] = i.description
            lib_r['organization'] = i.description
            list_lib.append(lib_r)
        print(list_lib)
        return response.Response(list_lib)