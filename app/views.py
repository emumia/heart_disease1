from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import joblib
import pycaret
import pandas as pd
#import sklearn
import pickle

# Create your views here.



@login_required(login_url='login')
def HomePage(request):
    if request.method =="POST":
        
        bmi=float(request.POST.get('BMI'))
        physicalHealth=request.POST.get('PhysicalHealth')
        mentalHealth=request.POST.get('MentalHealth')
        ageCategory=request.POST.get('AgeCategory')
        diabetic=request.POST.get('Diabetic')
        genHealth=request.POST.get('GenHealth')
        sleepTime=request.POST.get('SleepTime')
        smoking=request.POST.get('Smoking')
        alcohol_Drinking=request.POST.get('Alcohol_Drinking')
        stroke=request.POST.get('Stroke')
        diffwalk=request.POST.get('Diffwalking')
        sex=request.POST.get('Sex')
        race_Asian=request.POST.get('Race_Asian')
        race_Black=request.POST.get('Race_Black')
        race_Hispanic=request.POST.get('Race_Hispanic')
        race_Other=request.POST.get('Race_Other')
        race_White=request.POST.get('Race_White')
        physicalActivity=request.POST.get('PhysicalActivity')
        asthma=request.POST.get('Asthma')
        kidneyDisease=request.POST.get('KidneyDisease')
        skinCancer=request.POST.get('SkinCancer')

        # creating input data for the data frame

        input_data = pd.DataFrame({

            'BMI':[bmi],
            'PhysicalHealth':[physicalHealth],
            'MentalHealth':[mentalHealth],
            'AgeCategory':[ageCategory],        
            'Diabetic':[diabetic],
            'GenHealth':[genHealth],
            'SleepTime':[sleepTime],
            'Smoking':[smoking],
            'Alcohol_Drinking':[alcohol_Drinking],
            'Stroke':[stroke],
            'Diffwalking':[diffwalk],
            'Sex':[sex],
            'Race_Asian':[race_Asian],
            'Race_Black':[race_Black],
            'Race_Hispanic':[race_Hispanic],
            'Race_Other':[race_Other],
            'Race_White':[race_White],
            'PhysicalActivity':[physicalActivity],
            'Asthma':[asthma],
            'KidneyDisease':[kidneyDisease],
            'SkinCancer':[skinCancer],


        })

        #load the pre trained machine learning modelhere
        model=joblib.load('app/model_et.pkl')

        #make the prediction
        patient_status = model.predict(input_data)
        print(f"The result  is : {patient_status}")

        if patient_status[0]== 0:
            
            return render(request,'no_disease.html')
        else:
            return render(request,'heart_disease.html')
    
    
    return render(request,'home1.html')



def SignupPage(request):
    if request.method == 'POST':
        uname= request.POST.get('username')
        email= request.POST.get('email')
        pass1= request.POST.get('password1')
        pass2= request.POST.get('password2')

        if User.objects.filter(email=email,username=uname).exists():
            messages.warning(request,'Someone used this username or email already,Please try again!')
            return redirect('signup')

        if pass1 != pass2:
            #return HttpResponse("Your password and confirm password is not same!")
            messages.warning(request, "password and confirm password is not same")
            return redirect('signup')    
            
        else:    
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    
    return render(request,'signup.html')

def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("User name or password is incorrect")  

    return render(request,'login.html')

def Disease(request):
    return render(request,'disease.html')

def Not_Disease(request):
    return render(request,'ntdisease.html')

    
        


def LogoutPage(request):
    logout(request)
    return redirect('login')
