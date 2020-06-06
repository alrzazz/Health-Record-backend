from account.permissions import IsDoctor, IsPatient
from .models import *
from .serializer import *
from rest_framework import viewsets, mixins, status, views, generics
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from .pagination import ItemlimitPagination
import datetime
from rest_framework.filters import SearchFilter, OrderingFilter


def get_object_or_404(queryset, *filter_args, **filter_kwargs):
    try:
        return _get_object_or_404(queryset, *filter_args, **filter_kwargs)
    except:
        raise Http404


class ManageSymptomView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = SymptomSerializer
    pagination_class = ItemlimitPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        return Symptom.objects.all().filter(
            doctor__user_id=self.request.user.id)


class ManageDiseaseView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = DiseaseSerializer
    pagination_class = ItemlimitPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        self.get_object
        return Disease.objects.all().filter(
            doctor__user_id=self.request.user.id)


class ManageAdviceView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = AdviceSerializer
    pagination_class = ItemlimitPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        return Advice.objects.all().filter(
            doctor__user_id=self.request.user.id)


class ManageMedicineView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = MedicineSerializer
    pagination_class = ItemlimitPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name"]

    def get_queryset(self):
        return Medicine.objects.all().filter(
            doctor__user_id=self.request.user.id)


class DoctorCalendarView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    serializer_class = CalendarSerializer
    pagination_class = ItemlimitPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ["day", "start_time"]
    queryset = Calendar.objects.all()

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(doctor__user_id=self.request.user.id)

        start = self.request.query_params.get("start") 
        queryset = queryset.filter(day__gte=start) if start not in [None, ""] else queryset

        end = self.request.query_params.get("end")
        queryset = queryset.filter(day__lte=end) if end not in [None, ""] else queryset

        delta_day = self.request.query_params.get("delta_day")
        if delta_day not in [None, ""]:
            start = datetime.date.today()
            end = start + datetime.timedelta(days=int(delta_day))
            queryset = queryset.filter(day__gte=start, day__lte=end)
        
        return queryset


class PatientListTurnView(viewsets.ModelViewSet):
    permission_classes = [IsPatient]
    pagination_class = ItemlimitPagination
    serializer_class = PatientCalendarSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["doctor__first_name",
                     "doctor__last_name", "doctor__speciality"]
    ordering_fields = ["day", "start_time"]
    queryset = Calendar.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            day__gte=datetime.date.today() + datetime.timedelta(days=1), remained__gt=0)

        start = self.request.query_params.get("start")
        queryset = queryset.filter(
            day__gte=start) if start not in [None, ""] else queryset

        end = self.request.query_params.get("end")
        queryset = queryset.filter(day__lte=end) if end not in [None,""] else queryset

        return queryset

    def update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        response = {'message': 'Update function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        serializer = TurnReserveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = request.data.get("action")
        calendar_id = request.data.get("calendar_id")
        print(action)
        if action == "accept":
            try:
                app = get_object_or_404(
                    Appointment.objects.all(), patient__user_id=request.user.id, calendar_id=calendar_id)
            except:
                calendar = get_object_or_404(
                    self.get_queryset(), id=calendar_id)
                turn = calendar.total - calendar.remained + 1
                patient = Patient.objects.get(user__id=self.request.user.id)
                Appointment.objects.create(
                    calendar=calendar, turn=turn, patient=patient)
                calendar.remained -= 1
                calendar.save()
                return Response(data={"message": "Your Turn reserved"}, status=status.HTTP_200_OK)
        if action == "status":
            app = get_object_or_404(
                Appointment.objects.all(), calendar_id=calendar_id, patient__user_id=request.user.id)
            return Response(data={"message": "You already reserve this calendar"}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        delta = (instance.total - instance.remained) * \
            datetime.timedelta(minutes=20)
        instance.time = (datetime.datetime.combine(
            datetime.date(1, 1, 1), instance.start_time) + delta).time()
        serializer = PatientCalendarSerializerDetails(instance)
        return Response(serializer.data)


class DoctorAppointmentView(viewsets.ModelViewSet):
    permission_classes = [IsDoctor]
    # serializer_class = AppointmentSerializer
    pagination_class = ItemlimitPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["patient__first_name",
                     "patient__last_name"]
    ordering_fields = ["calendar__day", "calendar__start_time"]

    def create(self, request, pk=None):
        response = {'message': 'create function is not offered in this path.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        app = self.get_object()
        if app.done == False:
            app.done = True
            app.save()
        return super().partial_update(request, pk)

    def get_queryset(self):
        queryset = Appointment.objects.all().filter(
            calendar__doctor__user_id=self.request.user.id)

        start = self.request.query_params.get("start")
        queryset = queryset.filter(
            calendar__day__gte=start) if start not in [None, ""] else queryset

        end = self.request.query_params.get("end")
        queryset = queryset.filter(
            calendar__day__lte=end) if end not in [None, ""] else queryset

        calendar = self.request.query_params.get("calendar")
        queryset = queryset.filter(
            calendar_id=calendar) if calendar not in [None, ""] else queryset

        done = self.request.query_params.get("done")
        done = True if done == "true" else False if done == "false" else None
        queryset = queryset.filter(
            done=done) if done != None else queryset

        queryset.order_by("calendar__day", "calendar__start_time")

        return queryset

    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "GET":
            return AppointmentReadonlySerializer
        return AppointmentSerializer


class PatientAppointmentView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    permission_classes = [IsPatient]
    serializer_class = AppointmentReadonlySerializer
    pagination_class = ItemlimitPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["calendar__doctor__first_name",
                     "calendar__doctor__last_name"]
    ordering_fields = ["calendar__day", "calendar__start_time"]

    def get_queryset(self):
        queryset = Appointment.objects.all().filter(
            patient__user_id=self.request.user.id)

        start = self.request.query_params.get("start")
        queryset = queryset.filter(
            calendar__day__gte=start) if start not in [None,""] else queryset

        end = self.request.query_params.get("end")
        queryset = queryset.filter(
            calendar__day__lte=end) if end not in [None,""] else queryset

        done = self.request.query_params.get("done")
        done = True if done == "true" else False if done == "false" else None
        queryset = queryset.filter(
            done=done) if done != None else queryset

        queryset.order_by("calendar__day", "calendar__start_time")

        return queryset
