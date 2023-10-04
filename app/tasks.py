# tasks.py

from celery import shared_task
import socket
import re
from collections import defaultdict
from datetime import datetime, timedelta
from django.core.cache import cache
from celery.signals import task_success
from .models import TaskResult
from celery.signals import task_success

import requests
from pprint import pprint
import bs4
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin




@shared_task(bind=True)
def scan_xss(self,url, payloads_file="/home/sakshi/hackathon/team2/app/payloads.txt"):
    # Get all forms
    soup = bs(requests.get(url).content, "html.parser")
    forms = soup.find_all("form")

    vulnerabilities_found = 0
    for form in forms:
        # Extract form details
        details = {}
        action = form.attrs.get("action", "").lower()
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            inputs.append({"type": input_type, "name": input_name})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        
        # Submit form for each payload
        with open(payloads_file, "r") as file:
            payloads = file.read().splitlines()

        for payload in payloads:
            print(payload)
            # Prepare data
            target_url = urljoin(url, details["action"])
            data = {}
            for input in details["inputs"]:
                if input["type"] == "text" or input["type"] == "search":
                    input["value"] = payload
                input_name = input.get("name")
                input_value = input.get("value")
                if input_name and input_value:
                    data[input_name] = input_value
            
            # Make the request
            if details["method"] == "post":
                response = requests.post(target_url, data=data)
            else:
                response = requests.get(target_url, params=data)
            
            content = response.content.decode()
            if payload in content:
                pprint(details)
                vulnerabilities_found += 1
    print("Vulnerabilities Found", vulnerabilities_found)
 
    task_id = self.request.id
   
    return {
        "vulnerabilities_found": vulnerabilities_found,
        "task_id": task_id
    }


@task_success.connect(sender=scan_xss)
def save_data(sender, result, **kwargs):
    vulnerabilities_found = result["vulnerabilities_found"]
    task_id = result["task_id"]
    scan_result = TaskResult(task_id=task_id,xss_number=vulnerabilities_found)
    scan_result.save()

    # vulnerable_result.save()
  