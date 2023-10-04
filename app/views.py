from django.http import HttpResponseForbidden
import socket
from django.shortcuts import render
from django.http import HttpResponse 
from celery import shared_task
from django.template import loader
from django.core.cache import cache
from django.http import JsonResponse
from celery.signals import task_success
from .models import TaskResult
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import scan_xss
from time import sleep
from celery.result import AsyncResult



def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())




@csrf_exempt
def show_result(request):
    # Attempt to retrieve the latest task result
    print("show data working")
    if request.method == "POST":
        url = request.POST.get('url1')
        print("reciever url:",url)
        task=scan_xss.delay(url=url)
        id =  task.task_id
        print(id)
      
    return JsonResponse({'status': 'started', 'id': id})
   
    
   


@csrf_exempt
def show_scan(request):
    # Fetch the results from the database
    latest_task = TaskResult.objects.all().order_by('-created_at').first()
    # print(latest_task.task_id)
    context = {
        'vulnerabilities': latest_task.xss_number
        # 'result': latest_task.result,
        # 'ip_address': latest_task.ip_address
    }
    sleep(360)
    return render(request, 'report.html', context)

    
@csrf_exempt
def check_task_status(request):
    if request.method == "POST":
        id =  request.POST.get('id')

    print (id)

    # task = TaskResult.objects.all().order_by('-created_at').first()
    # task.filter
    # print("Received task_id:", task.task_id) 
    # # task = AsyncResult(task_id)
    
    response_data = {
        'task_id': id,  # Optional: if you want to send any result data as well
    }
    
    return JsonResponse(response_data)


