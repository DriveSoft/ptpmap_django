from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View

from .models import *
from .forms import *

import json
from django.contrib.staticfiles import finders
import datetime
from django.core.files import File
import io
import os
from django.conf import settings as djangoSettings




class EditorView(LoginRequiredMixin, View):
    template = 'mapedit/editor.html'
    #login_url = '/login/'
    #redirect_field_name = 'redirect_to'

    def get(self, request, city_name):
        if request.user.is_authenticated:
            CityObj = get_object_or_404(city, sysname = city_name)
            #CityObj = city.objects.get(sysname = city_name) # получаем id города, который используется

            isAllow = UserCity.objects.filter(city_id=CityObj.id, user_id=request.user.id).count() # проверяем есть ли у пользователя разрешение для данного города
            if isAllow > 0 or request.user.is_staff:
                form = PTPForm()
                ptp_data = ptp.objects.filter(city_id=CityObj.id)
                context = {'CityObj': CityObj, 'ptp_data': ptp_data, 'form': form, 'lat': request.GET.get('lat'), 'lng': request.GET.get('lng')  } #, 'lat': lat, 'lng': lng
                return render(request, self.template, context)

            else:
                return HttpResponse("Access denied")

        else:
            return HttpResponseRedirect(reverse('login'))


    def post(self, request, city_name):
        if request.user.is_authenticated:
            CityObj = get_object_or_404(city, sysname = city_name)
            #print(idCity)

            #isAllow = UserCity.objects.filter(city_id=request.POST.get('city'), user_id=request.user.id).count() # проверяем есть ли у пользователя разрешение для данного города
            isAllow = UserCity.objects.filter(city_id=CityObj.id, user_id=request.user.id).count() # проверяем есть ли у пользователя разрешение для данного города

            #print(UserCity.objects.get(city='sofia').id)

            if isAllow > 0 or request.user.is_staff:

                record_id = request.POST.get('record_id') # получаем объект ptp если редактируем

                if not request.POST._mutable:
                    request.POST._mutable = True # позволяет изменять значения в запросе

                request.POST['datetime'] = datetime.datetime.strptime(request.POST['datetime'], '%d/%m/%Y %H:%M').strftime(' %Y-%m-%d %H:%M:%S') #меняем формат даты для БД

                #request.POST['datetime'] = '2019-01-01 00:00:00'
                #print(request.POST.get('datetime'))

                if record_id:
                    ptp_object = get_object_or_404(ptp, pk=record_id)
                else:
                    ptp_object = None


                form = PTPForm(request.POST, instance=ptp_object) # заполняем форму данными из POST, такжа добавляется объекта записи, если редактируем


                if form.is_valid():
                    new_ptp = form.save(commit=False)
                    new_ptp.city_id = CityObj.id
                    new_ptp = form.save()
                    response = redirect('editor', city_name = CityObj.sysname)
                    response['Location'] += '?lat='+ str(new_ptp.latitude) + '&lng=' + str(new_ptp.longitude)
                    return response
                    #return render(request, self.template, context={'form': form})
            else:
                return HttpResponse("Access denied")
        else:
            return HttpResponseRedirect(reverse('login'))




class PtpDelete(View):

    def get(self, request, city_name, ptp_id):
        if request.user.is_staff:
            ptp_record = get_object_or_404(ptp, pk=ptp_id)
            ptp_record.delete()
            return redirect('editor', city_name = city_name) #HttpResponseRedirect(reverse('editor'))
        else:
            return HttpResponse("Access denied")



class PtpImport(View):

    def get(self, request):
        if request.user.is_staff:
            ptp.objects.all().delete()

            with open(finders.find('all.geojson'), encoding='utf-8') as read_file:
                data = json.load(read_file)
                features = data["features"]

            for feature in features:
                datetime = feature["properties"]["DateTime"]
                ptptype = feature["properties"]["ptptype"]
                carRedSignal = feature["properties"]["carRedSignal"]
                carTurnLeft = feature["properties"]["carTurnLeft"]
                carTurnRight = feature["properties"]["carTurnRight"]
                pedRedSignal = feature["properties"]["pedRedSignal"]
                pedWrongCross = feature["properties"]["pedWrongCross"]
                pedKid = feature["properties"]["pedKid"]
                danger = feature["properties"]["danger"]
                description = feature["properties"]["description"]
                lng = feature["geometry"]["coordinates"][0]
                lat = feature["geometry"]["coordinates"][1]

                if ptptype=='pedestrian':
                    ptptype = 1

                if ptptype=='car':
                    ptptype = 2

                if ptptype=='bicycle':
                    ptptype = 3

                if ptptype=='motorcycle':
                    ptptype = 4

                datetime = datetime.replace('T', ' ')
                datetime = datetime.replace('.000Z', '')

                ptprecord = ptp(city_id=1, latitude=lat, longitude=lng, description=description, datetime=datetime, ptptype_id=ptptype, carRedSignal=carRedSignal, carTurnLeft=carTurnLeft, carTurnRight=carTurnRight, pedRedSignal=pedRedSignal, pedWrongCross=pedWrongCross, pedKid=pedKid, danger=danger)
                ptprecord.save()

            return HttpResponseRedirect(reverse('editor'))
        else:
            return HttpResponse("Access denied")




class HeatMap(View):
    template = 'mapedit/heatmap.html'

    def get(self, request, city_name):
        CityObj = get_object_or_404(city, sysname = city_name)
        #ptp_data = ptp.objects.filter(city_id=CityObj.id) # из базы получаем данные

        # из JSON файла получаем данные (папка STATIC)
        #with open(finders.find(city_name+'.json'), encoding='utf-8') as read_file:
        with open('./mapedit/dataptp/'+city_name+'.json', encoding='utf-8') as read_file: #./static/
            jsonfile = json.load(read_file)

        fromYear = jsonfile["fromYear"]
        toYear = jsonfile["toYear"]

        context = {'CityObj': CityObj, 'jsonfile': jsonfile, 'fromYear': fromYear, 'toYear': toYear}
        #context = {'ptp_data': ptp_data, 'CityObj': CityObj, 'jsonfile': jsonfile}
        return render(request, self.template, context)



class UpdateData(View):
    def get(self, request, city_name):
        CityObj = get_object_or_404(city, sysname = city_name)
        #ptp_data = ptp.objects.all()
        ptp_data = ptp.objects.filter(city_id=CityObj.id)

        #print(ptp_data.aggregate(Max('datetime')).year())
        arg = ptp_data.order_by('datetime').first()
        fromYear = arg.datetime.year
        fromYear -= 1 #костыль, -1 год значит показываем в шаблоне все дтп

        arg = ptp_data.order_by('-datetime').first()
        toYear = arg.datetime.year


        ptpJsonData = {
            "type": "FeatureCollection",
            "fromYear": fromYear,
            "toYear": toYear,
            "features": []
        }

        if ptp_data:
            for ptpItem in ptp_data:
                ptpJson = {
                  "type": "Feature",
                  "geometry": {
                    "type": "Point",
                    "coordinates": [ptpItem.longitude, ptpItem.latitude]
                  },

                  "properties": {
                    "id": ptpItem.id,
                    "city": ptpItem.city_id,
                    "DateTime": ptpItem.datetime.strftime("%d/%m/%Y %H:%M"),
                    "ptptype": '{}'.format(ptpItem.ptptype),
                    "carRedSignal": int(ptpItem.carRedSignal),
                    "carTurnLeft": int(ptpItem.carTurnLeft),
                    "carTurnRight": int(ptpItem.carTurnRight),
                    "pedRedSignal": int(ptpItem.pedRedSignal),
                    "pedWrongCross": int(ptpItem.pedWrongCross),
                    "pedKid": int(ptpItem.pedKid),
                    "danger": int(ptpItem.danger),
                    "year": ptpItem.datetime.year,
                    "month": ptpItem.datetime.month,
                    "hours": ptpItem.datetime.hour,
                    "description": '{}'.format(ptpItem.description),
                  }
                }

                ptpJsonData["features"].append(ptpJson)


        #with io.open('./mapedit/dataptp/'+city_name+'.json', 'w', encoding='utf8') as f:
        #print('FF'+os.path.join(djangoSettings.BASE_DIR, "/static"))
        with io.open('./mapedit/dataptp/'+city_name+'.json', 'w', encoding='utf8') as f:
            myfile = File(f)
            myfile.write( json.dumps(ptpJsonData, ensure_ascii=False) )

        myfile.closed
        f.closed
        return HttpResponse("Updated")


        #context = {'ptp_data': ptp_data, 'CityObj': CityObj} #, 'lat': lat, 'lng': lng
        #return render(request, self.template, context)
