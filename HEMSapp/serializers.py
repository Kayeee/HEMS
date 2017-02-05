# from rest_framework import serializers
# from MDBsite.models import Project, File, MDBUser
#
# class ProjectSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     upload = serializers.PrimaryKeyRelatedField(many=True, queryset=File.objects.all())
#
#     class Meta:
#         model = Project
#         fields = ('id', 'title', 'owner', 'upload')
#
#
# class FileSerializer(serializers.ModelSerializer):
#     project = serializers.ReadOnlyField(source='project.id')
#
#     class Meta:
#         model = File
#         fields = ('id', 'title', 'upload', 'project')
#
# class UserSerializer(serializers.ModelSerializer):
#     project = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
#
#     class Meta:
#         model = MDBUser
#         fields = ('id', 'username', 'email', 'date_of_birth', 'is_active',
#                     'is_admin', 'first_name', 'last_name', 'project')
