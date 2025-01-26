from rest_framework import serializers
from .models import Subject, Graduate, Teacher, Feedback
from rest_framework.exceptions import ValidationError  


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ['slug', 'last_updated', 'created_at']

class GraduateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graduate
        fields = '__all__'
        read_only_fields = ['slug', 'last_updated', 'created_at']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        read_only_fields = ['slug', 'last_updated', 'created_at']

# class FeedbackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feedback
#         fields = ['first_name', 'last_name', 'phone_number', 'text', 'slug', 'last_updated', 'created_at']
#         read_only_fields = ['slug', 'last_updated', 'created_at']

#     def create(self, validated_data):
#         validated_data['email'] = self.context['request'].user.email
#         return super().create(validated_data)

class FeedbackSerializer(serializers.ModelSerializer):  
    email = serializers.EmailField(required=False)  

    class Meta:  
        model = Feedback  
        fields = ['first_name', 'last_name', 'phone_number', 'text', 'slug', 'last_updated', 'created_at', 'email']  
        read_only_fields = ['slug', 'last_updated', 'created_at']  

    def create(self, validated_data):
        request = self.context['request']

        if request.user.is_authenticated:
            validated_data['email'] = request.user.email
        else:
            email = validated_data.get('email')
            if not email:
                raise ValidationError("Email обязателен для незарегистрированных пользователей")
        return super().create(validated_data)
