from django.shortcuts import redirect, render
from .forms import SignupForm, NotesForm
from .models import signupMaster
from django.contrib.auth import logout
from django.core.mail import send_mail
from BatchProject import settings
import requests
import json
import random

# Create your views here.

def index(request):
    if request.method=='POST':
        if request.POST.get('signup')=='signup':
            signupfrm=SignupForm(request.POST)
            if signupfrm.is_valid():
                signupfrm.save()
                print("Signup Successfully!")

                mail_sub="Account Creation Confirmation!"
                mail_msg="Hello User, \nThis is system genrated mail!\nYour account has been created successfully with us!\nHappy Coding\nThanks & Regards\n+91 9510456230 | hardikmendapara369@gmail.com"
                mail_from=settings.EMAIL_HOST_USER
                mail_to=request.POST["username"]
                send_mail(mail_sub,mail_msg,mail_from,[mail_to])
                return redirect('notes')
            else:
                print(signupfrm.errors)
        elif request.POST.get('login')=='login':
            usernm=request.POST['username']
            pas=request.POST['password']

            signup=signupMaster.objects.filter(username=usernm,password=pas)

            userid=signupMaster.objects.get(username=usernm)
            print("Userid:",userid.id)

            otp=random.randint(11111,99999)
            if signup:
                print("Login Successfully!")
                request.session['user']=usernm
                request.session['userid']=userid.id

                url = "https://www.fast2sms.com/dev/bulk"
                
                # create a dictionary
                my_data = {
                    # Your default Sender ID
                    'sender_id': 'FSTSMS', 
                    
                    # Put your message here!
                    'message': f'\nYour Account is login!\nYour OTP is {otp}', 
                    
                    'language': 'english',
                    'route': 'p',
                    
                    # You can send sms to multiple numbers
                    # separated by comma.
                    'numbers': '9510456230,9724799469'    
                }
                
                # create a dictionary
                headers = {
                    'authorization': '0sXBTdwZlPH1NkSreFJAq9f8cORQpjo5Gyx4D3Umnb7CYKgV6vvC31QKjsfMGlJ7WPIowO28SayD5cYm',
                    'Content-Type': "application/x-www-form-urlencoded",
                    'Cache-Control': "no-cache"
                }

                # make a post request
                response = requests.request("POST",
                                            url,
                                            data = my_data,
                                            headers = headers)
            
                returned_msg = json.loads(response.text)
                
                # print the send message
                print(returned_msg['message'])
                return redirect('notes')
            else:
                print("Error...Login fail!")
    return render(request,'index.html')

def profile(request):
    user=request.session.get('user')
    userid=request.session.get('userid')
    id=signupMaster.objects.get(id=userid)

    if request.method=='POST':
        updateForm=SignupForm(request.POST)
        if updateForm.is_valid():
            updateForm=SignupForm(request.POST,instance=id)
            updateForm.save()
            print("Your profile has been updated!")
            return redirect('notes')
        else:
            print(updateForm.errors)
    return render(request,'profile.html',{'user':user, 'userData':signupMaster.objects.get(id=userid)})

def userlogout(request):
    logout(request)
    return redirect('/')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def services(request):
    return render(request,'services.html')

def notes(request):
    user=request.session.get('user')
    if request.method=="POST":
        uploadNotes=NotesForm(request.POST, request.FILES)
        if uploadNotes.is_valid():
            uploadNotes.save()
            print("Your notes has been uploaded!")
        else:
            print(uploadNotes.errors)
    return render(request,'notes.html',{'user':user})