from rest_framework import serializers
from clinic.models import DoctorDb,AppointmentDb

class Doctor_serializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDb
        #fields = ['id', 'doctor_name']
        fields ="__all__"
        read_only_fields = ["id"]
class Appointment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentDb
        fields = "__all__"
        read_only_fields = ["id"]
    def validate (self,validated_data):
        phone = validated_data.get("phone")
        date = validated_data.get("appointment_date")
        if AppointmentDb.objects.filter(
            phone = phone,
            appointment_date = date).exists():
            raise serializers.ValidationError("Already Booked")
        else:
            return validated_data
