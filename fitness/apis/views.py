from django.shortcuts import render
import smtplib
from email.mime.text import MIMEText
from django.http import JsonResponse, FileResponse
from django.http import HttpResponse
import math, random
from apis.firebase_calls import firebase_data_api
import boto3
import requests
import json

s = smtplib.SMTP('smtp.gmail.com',587)



client = boto3.client(
    "sns",
    aws_access_key_id="AKIA4HPAZ567QXB4GCEG",
    aws_secret_access_key="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",
    region_name="ap-south-1"
)


gym = firebase_data_api("apis/fitnessv1-f3d22-firebase-adminsdk-dwou5-c1a931d3d0.json")


test_string = "None"

def generateOTP(mobile_number):
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    client.publish(
        PhoneNumber="+91"+mobile_number,
        Message="Welcome to FitMark !\nYour verification code is "+OTP
    )
    return OTP


def send_sms(request):
    client.publish(
        PhoneNumber="+91"+request.GET['mobile'],
        Message="Welcome to FitMark !\nYour verification code is "+request.GET['sms_body']
    )
    return JsonResponse({'status':"sent"})


def otp_verification(request):
    otp = generateOTP(request.GET['mobile'])
    return JsonResponse({'Otp':otp})

def send_email(request):
    s.starttls()
    s.login("paishrikrishna98@gmail.com", "shrikrishnanarayanpai@1498")
    s.sendmail("paishrikrishna98@gmail.com", request.GET['email'], request.GET['message'])
    s.quit()
    return JsonResponse({'status':"sent"})



def dashboard_apis(request):
    if request.GET['dashboard'] == 'New Members Added Today':
        count = gym.members_added_today(request.GET['gym_id'])
    elif request.GET['dashboard'] == 'Total Visits Today':
        count = gym.total_visit_count_today(request.GET['gym_id'])
    elif request.GET['dashboard'] == 'Memberships expiring today':
        count = gym.membership_expiring_today(request.GET['gym_id'])

    return JsonResponse({'count':str(count)})



def membership_data(request):
    return JsonResponse({'count':gym.membership_exists(request.GET['status'],request.GET['gym_id'],request.GET['user_id'])})



def user_data(request):
    return JsonResponse({'count':gym.user_exists_in_system(request.GET['user_id'])})


def available_dashboards(request):
    return JsonResponse({'dashboards':gym.available_dashboards(request.GET['gym_id'])})


def add_dashboard(request):
    return JsonResponse({'dashboards':gym.add_dashoard(request.GET['gym_id'],request.GET['dashboard'])})

def todays_attendance_record(request):
    if request.GET['dashboard'] == 'Total Visits Today':
        user_data = gym.todays_visit(request.GET['gym_id'])
        cols = ['Date','Name','Time']
        page_title = "Total Visits Today"
    elif request.GET['dashboard'] == 'New Members Added Today':
        user_data = gym.new_memebers(request.GET['gym_id'])
        cols = ['Valid Till','Name','Membership Amount']
        page_title = "Memberships added today"
    elif request.GET['dashboard'] == 'Memberships expiring today':
        user_data = gym.expiring_membership(request.GET['gym_id'])
        cols = ['Plan Started from','Name','Membership Amount']
        page_title = "Memberships expiring today"

    return JsonResponse({'user_data':user_data,'cols':cols,'page_title':page_title})



def membership_detail(request):
    return JsonResponse(gym.membership_details(request.GET['gym_id'],request.GET['user_id']))



def test(request):
    return JsonResponse({"test":"test req"})

def user_exists(request):

	user_detail_data = ['test']
	offset = 0

	while len(user_detail_data) > 0:
		
		response = requests.get('https://api.adalo.com/v0/apps/159805a3-ce5f-441e-abf5-2b2a5aa25edb/collections/t_dc2d5eac4c3a417797c3f8e3178b55a8?offset={start}&limit={end}'.format(start = offset,end = offset + 1000), 
		headers = {"Authorization":"Bearer 8yf6exu1tomzbf7620rcc5xpz","Content-Type":"application/json"}).text
		user_detail_data = json.loads(response)['records']
		offset += 1000
		
		for details in user_detail_data:
			if int(details['Mobile Number']) == int(request.GET['mobile_number']):
				return JsonResponse({"status":200})

	return JsonResponse({"status":404})



def user_exists_prod(request):

	user_detail_data = ['test']
	offset = 0

	while len(user_detail_data) > 0:
		
		response = requests.get('https://api.adalo.com/v0/apps/'+str(request.GET['app_id'])+'/collections/'+str(request.GET['collection_id'])+'?offset={start}&limit={end}'.format(start = offset,end = offset + 1000), 
		headers = {"Authorization":"Bearer "+str(request.GET['token']),"Content-Type":"application/json"}).text
		user_detail_data = json.loads(response)['records']
		offset += 1000
		
		for details in user_detail_data:
			if int(details['Mobile Number']) == int(request.GET['mobile_number']):
				return JsonResponse({"status":200})

	return JsonResponse({"status":404})

