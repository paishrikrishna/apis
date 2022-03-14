from django.shortcuts import render
import smtplib
from email.mime.text import MIMEText
from django.http import JsonResponse, FileResponse
from django.http import HttpResponse
import math, random
from apis.firebase_calls import firebase_data_api




gym = firebase_data_api("apis/fitnessv1-f3d22-firebase-adminsdk-dwou5-c1a931d3d0.json")


test_string = "None"

def generateOTP():
    digits = "123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP



def otp_verification(request):
    otp = generateOTP()
    message = """Subject: Login OTP

{}
    """
    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login("paishrikrishna98@gmail.com", "shrikrishnanarayanpai@1498")
    mailserver.sendmail("paishrikrishna98@gmail.com", "paishrikrishna98@gmail.com",message.format("Your 6 digit verification code is {}".format(otp)))
    mailserver.quit()
    return JsonResponse({'Otp':otp})


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
    # Import QRCode from pyqrcode
    import qrcode

    img = qrcode.make('test text')

    print(img.size)

    img.save('/home/paishrikrishna98/fitness_v1/apis/gym_images/myqr.png')

    img = open('/home/paishrikrishna98/fitness_v1/apis/gym_images/myqr.png', 'rb')

    response = FileResponse(img)
    global test_string
    try:
        for filename, file in request.FILES.iteritems():
            name = request.FILES[filename].name

        test_string = name
    except:
        pass

    #return response

    return JsonResponse({"test":test_string})

