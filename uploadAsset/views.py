from rest_framework import generics,status, viewsets, views, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import uploadAsset,AssetVersion
from .serializers import *
from account.renders import UserRenderer
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from organization.models import Organization, addMember
from library.models import Library
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from rest_framework.parsers import FileUploadParser

######### upload Multiple Asset ###########
class AssetListsCreateView(views.APIView):
    parser_classes = (MultiPartParser, FormParser)
    # parser_classes = [FileUploadParser]
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        flag = 1
        arr = []
        form_data = {}
        title = request.data.get('title')
        library = request.data.get('library')
        location = request.data.get('location')
        organization = request.data.get('organization')
        description = request.data.get('description')
        
        member = addMember.objects.filter(organization=organization)
        for i in member:
            if i.user == request.user:
                if i.role == 'Admin' or i.role == 'Contributor':
                    break
                else:
                    return Response({"message":"You don't have permission to Upload Asset."})
        
        form_data['title'] = title
        form_data['library'] = library
        form_data['location'] = location
        form_data['organization'] = organization
        form_data['description'] = description
        
        for img in request.FILES.getlist('asset'):
            print(img)
            form_data['asset'] = img 
            serializer = uploadAssetSerializer(data=form_data)
            if serializer.is_valid():
                serializer.save()
                arr.append(serializer.data)
            else:
                flag = 0
        if flag == 1:
            return Response({'Data':arr}, status=status.HTTP_201_CREATED)
        return Response({'message' : 'Error!'}, status=status.HTTP_400_BAD_REQUEST)   
        
    
######### Library asset Showing ###########
class AssetListCreateView(generics.ListCreateAPIView):
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'tags__tag_name']  # Include tags in search_fields

    def get_queryset(self):
        # Get the library_id from the URL parameter
        library_id = self.kwargs.get('library_id')
        search_query = self.request.query_params.get('search', '')
        
        if library_id is None:
            # Return a response with an error message if library_id is missing
            return Response({'error': 'Library ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = self.request.user
        org = Library.objects.filter(organization__owner = user)
        
        for i in org:
            if i.id == library_id:     
                queryset = uploadAsset.objects.filter(library_id=library_id)
                return queryset
        org_m = Library.objects.filter(organization__member = user)
        for i in org_m:
            if i.id == library_id:
                queryset = uploadAsset.objects.filter(library_id=library_id)
                # print(queryset)
                return queryset
        # return Response({'message':"This library not valid this user"}, status=status.HTTP_400_BAD_REQUEST)
        
######### Download Asset #######
class FileDownloadAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id, format=None):
        queryset = uploadAsset.objects.get(id = id)
        file_handle = queryset.file.path
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/msword')
        response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.file.name
        return response
    
class AssetViewSet(viewsets.ModelViewSet):
    queryset = uploadAsset.objects.all()
    serializer_class = AssetSerializer

    def retrieve(self, request, pk=None):
        asset = uploadAsset.objects.get(pk=pk)
        serializer = self.get_serializer(asset)
        return Response(serializer.data)   
   
     
class AssetRetrieveView(generics.RetrieveAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]        

class AssetUpdateView(generics.UpdateAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_update(self, serializer):
        pk = self.kwargs.get('pk')  
           
        try:   
            up_asset = uploadAsset.objects.get(id = pk)
            org_ow = addMember.objects.filter(organization=up_asset.organization)
            for i in org_ow:
                if i.user == self.request.user:
                    if i.role == 'Admin' or i.role == 'Contributor':
                        serializer.save()
                        return Response({'message':'Update Successfully'})
                    else:
                        return Response({'message':"You don't have permission to Update."})
            serializer.save()
            
            return Response({'message':'Update Successfully'})
        except uploadAsset.DoesNotExist:
            return Response({
                'message':'Not valid asset'
            })
        
     
class AssetDeleteView(generics.DestroyAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = uploadAssetSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')    
       
        try:   
            up_asset = uploadAsset.objects.get(id = pk)
            org_ow = addMember.objects.filter(organization=up_asset.organization)
            for i in org_ow:
                if i.user == request.user:
                    if i.role == 'Admin':
                        up_asset.delete()
                        return Response({'message':'Delete Successfully'})
                    else:
                        return Response({'message':"You don't have permission to Delete."})
            up_asset.delete()
            return Response({'message':'Delete Successfully'})
        except uploadAsset.DoesNotExist:
            return Response({
                'message':'Not valid asset'
            })

#asset version control views.....

class PreviousAssetVersionsView(generics.ListAPIView):
    serializer_class = PreviousVersionSerializer

    def get_queryset(self):
        # Get the asset_id from the URL parameter
        asset_id = self.kwargs['asset_id']

        # Retrieve the asset instance
        try:
            asset_instance = uploadAsset.objects.get(id=asset_id)
        except uploadAsset.DoesNotExist:
            asset_instance = None

        # If the asset instance is found, return its previous versions
        if asset_instance:
            return asset_instance.versions.all()
        else:
            return AssetVersion.objects.none()
    
    # def get_queryset(self):
    #     asset_id = self.kwargs.get('asset_id')

    #     if asset_id is None:
    #         # Return a response with an error message if library_id is missing
    #         return Response({'error': 'assert_id ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     queryset = AssetVersion.objects.filter(id=asset_id)
    #     return queryset

class CurrentAssetView(generics.RetrieveAPIView):
    queryset = uploadAsset.objects.all()
    serializer_class = CurrentAssetSerializer        

class AssetVersionListView(generics.ListAPIView):
    queryset = AssetVersion.objects.all()
    serializer_class = AssetVersionSerializer

#### Image Filter API View ####
class ImageFilter(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        asset = uploadAsset.objects.filter(organization_id=pk)
        lst = []
        for i in asset:
            st = str(i.asset)
            txt = st.split('.')
            if txt[1] != 'mp3' and txt[1] != 'mp4':
                dic = {}
                dic['id'] = i.id
                dic['organization'] = i.organization_id
                dic['title'] = i.title
                dic['library'] = i.library_id    
                dic['description'] = i.description
                dic['asset'] = i.asset.url
                dic['location'] = i.location
                lst.append(dic)     
        return Response(lst)
     
#### Audio Filter API View ####
class AudioFilter(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        asset = uploadAsset.objects.filter(organization_id=pk)
        lst = []
        for i in asset:
            st = str(i.asset)
            txt = st.split('.')
            if txt[1] == 'mp3':
                dic = {}
                dic['id'] = i.id
                dic['organization'] = i.organization_id
                dic['title'] = i.title
                dic['library'] = i.library_id    
                dic['description'] = i.description
                dic['asset'] = i.asset.url
                dic['location'] = i.location
                lst.append(dic)      
        return Response(lst)
    
#### Video Filter API View ####
class VideoFilter(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        created_at = request.GET.get('created_at')
        print(created_at)
        asset = uploadAsset.objects.filter(organization_id=pk)
        
        lst = []
        for i in asset:
            st = str(i.asset)
            txt = st.split('.')
            if txt[1] == 'mp4':
                dic = {}
                dic['id'] = i.id
                dic['organization'] = i.organization_id
                dic['title'] = i.title
                dic['library'] = i.library_id    
                dic['description'] = i.description
                dic['asset'] = i.asset.url
                dic['location'] = i.location
                dic['created_at'] = i.created_at
                lst.append(dic)     
        return Response(lst)
    
    