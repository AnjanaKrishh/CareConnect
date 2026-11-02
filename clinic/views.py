from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from clinic.models import DoctorDb,AppointmentDb
from clinic.serializer import Doctor_serializer,Appointment_Serializer
from datetime import time,datetime,timedelta
from rest_framework import serializers

# Create your views here.
class DoctorListCreateView(APIView):
    def get(self, request):
        qs= DoctorDb.objects.all()
        serializer_instance = Doctor_serializer(qs, many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data = request.data
        serializer_instance = Doctor_serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)
        
class DoctorRetrieveUpdateDeleteView(APIView):
    def get(self,request,pk):
        qs = get_object_or_404(DoctorDb,id=pk)
        serializer_instance = Doctor_serializer(qs)
        return Response(data=serializer_instance.data)
    def put(self, request, pk):
        form_data = request.data
        doctor_object = get_object_or_404(DoctorDb, id=pk)
        serializer_instance = Doctor_serializer(doctor_object, data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)     
    def delete(self,request,pk):
            doctor_obj =get_object_or_404(DoctorDb,id=pk)
            doctor_obj.delete()
            return Response(data={
                "Message": "Deleted..!"
            })
class AppointmentListCreateView(APIView):
    def get(self,request):
        qs = AppointmentDb.objects.all()
        serializer_instance = Appointment_Serializer(qs,many=True)
        return Response(data=serializer_instance.data)
    def post(self,request):
        form_data = request.data
        serializer_instance = Appointment_Serializer(data=form_data)
        if serializer_instance.is_valid():
            appointment_date = serializer_instance.validated_data.get("appointment_date")
            doctor_id = serializer_instance.validated_data.get("doctor_id")
            
            last_appointment = AppointmentDb.objects.filter(
                appointment_date = appointment_date,
                doctor_id = doctor_id
            ).order_by("-token_number").first()
            
            if last_appointment is None:
                form_data["token_number"]=1
                form_data["appointment_time"] = time(10,0)
            else:
                form_data["token_number"] = last_appointment.token_number + 1
                current_time = datetime.combine(appointment_date,last_appointment.appointment_time)
                # form_data["appointment_time"] =(current_time + timedelta(minutes=15)).time()
                next_time = current_time + timedelta(minutes=15)
                # adding lunch break
                if next_time.time()== time(12, 30):
                    next_time = datetime.combine(appointment_date,time(13, 30))
                # slot completion
                if next_time.time() ==time(17, 00):
                    raise serializers.ValidationError("Booking Closed for Today")
                form_data["appointment_time"]= next_time    
                    
            qs = AppointmentDb.objects.create(**form_data)
            serializer_instance = Appointment_Serializer(qs)
            return Response(data = {
                "Status" :"Booked Succesfully",
                "Token Number" : form_data ["token_number"],
                "Appointment Time" : form_data["appointment_time"]
                
            })
        else:
            return Response(data=serializer_instance.errors) 