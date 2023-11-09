from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, views, status, filters, generics
from account.models import User
from organization.models import *
from account.renders import UserRenderer
from .models import Library
from .serializers import CreateLibrarySerializer
from uploadAsset.models import uploadAsset
from uploadAsset.serializers import uploadAssetSerializer

class CreateLibraryAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    
    def post(self, request):
        serializer = CreateLibrarySerializer(data=request.data, context = {'user':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        
        
###### Library Update View #######
class LibraryUpdateView(UpdateAPIView):
    queryset = Library.objects.all()
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        pk = self.kwargs.get('pk')
        org = self.request.data['organization']
        
        try:
            library = Library.objects.get(id = pk)
            member = addMember.objects.filter(organization=org)
            for i in member:
                if i.user == self.request.user:
                    if i.role == 'Admin' or i.role == 'Contributor':
                        serializer.save()
                        return response.Response({'message':'Update Successfully.'})
                    else:
                        return response.Response({'message':"You don't have permission to Delete."})
            serializer.save()
            
            return response.Response({'message':'Update Successfully'})
        except Library.DoesNotExist:
            return response.Response({"message":"Error"})
            
    
##### Library Delete View ######
class LibraryDeleteView(DestroyAPIView):
    queryset = Library.objects.all()
    serializer_class = CreateLibrarySerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')       
        
        try:
            library = Library.objects.get(id = pk)
            try:
                org = Organization.objects.get(id = library.organization.id)
                member = addMember.objects.filter(organization=org)
                for i in member:
                    if i.user == self.request.user:
                        if i.role == 'Admin':
                            library.delete()
                            return response.Response({'message':'Delete Successfully.'})
                        else:
                            return response.Response({'message':"You don't have permission to Delete"})
                library.delete()
                return response.Response({'message':'Delete Successfully.'})
            except Organization.DoesNotExist:
                response.Response({"message":"Error"})
        except Library.DoesNotExist:
            return response.Response({'message':"Error"})
            

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
            org = Organization.objects.get(organization_name=i.organization)
            lib_r['org_id'] = org.id
            lib_r['org_name'] = org.organization_name
            list_lib.append(lib_r)
       
            
        return response.Response(list_lib)


######## Organization All Asset Showing  ############
# class assetAllImageView(views.APIView):
#     permission_classes = [IsAuthenticated]
#     renderer_classes = [UserRenderer]
    
#     def get(self, request, org_id): 
#         query = request.GET.get('keyword')
#         org_owner = Organization.objects.filter(owner=request.user)
#         org_member = Organization.objects.filter(member=request.user)
#         temp = [] 
#         print("Query", query)
       
#         if org_owner.exists():
#             print(org_owner)
#             for i in org_owner:
#                 if i.id == org_id:
#                     lib = Library.objects.filter(organization__id = org_id)      
#                     for k in lib:
#                         asset = uploadAsset.objects.filter(library = k.id)          
#                         for j in asset:
#                             tem = {}
#                             tem['id'] = j.id
#                             tem['title'] = j.title
#                             tem['description'] = j.description
#                             tem['asset'] = j.asset.url
#                             temp.append(tem)
        
#         if  org_member.exists():   
       
#             for i in org_member:
#                 if i.id == org_id:
#                     lib = Library.objects.filter(organization__id = org_id)    
#                     for k in lib:
#                         asset = uploadAsset.objects.filter(library = k.id)          
#                         for j in asset:
#                             tem = {}
#                             tem['id'] = j.id
#                             tem['title'] = j.title
#                             tem['description'] = j.description
#                             tem['asset'] = j.asset.url
#                             temp.append(tem)
        
#         total_img = {}  
#         total_img['total_img'] = len(temp)
#         lstt = []
#         lstt.append(total_img)
#         print(temp)           
#         print(temp)
#         return response.Response({'len':lstt, 
#                                   'asset': temp}, status=status.HTTP_200_OK)
        
#### Organization Search ##############
class assetAllImageView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = uploadAssetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        org_id = (self.kwargs.get('org_id'))
  
        if org_id is None:
            return response.Response({'message':'Organization Id is Required'})
        user = self.request.user
        org_owner = Organization.objects.filter(owner=user)
        for i in org_owner:
            if i.id == org_id:
                queryset = uploadAsset.objects.filter(organization_id = org_id)   
                return queryset
        org_member = Organization.objects.filter(owner=user)
        for i in org_member:
            if i.id == org_id:
                queryset = uploadAsset.objects.filter(organization_id = org_id)
                return queryset        
        
