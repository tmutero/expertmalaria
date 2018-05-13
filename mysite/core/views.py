import time
import datetime

import pandas as pd
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

from mysite.core.forms import SignUpForm
from mysite.core.models import Patient, PatientRecords


@login_required
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def create_patient(request):
    if not request.user.is_authenticated:
        return redirect('home')
    patient = Patient(firstname=request.POST['firstname'], lastname=request.POST['lastname'],
                       contact=request.POST['contact'],address=request.POST['address'],
                      gender=request.POST['gender'],birth_date=request.POST['birth_date'])

    patient.save()
    return redirect('read_patient')


def read_patient(request):
    if not request.user.is_authenticated:
        return redirect('home')
    patients = Patient.objects.all()

    print(patients)
    context = {'patients': patients}
    return render(request, 'patient/list.html', context)


def edit_patient(request, id):
    patient = Patient.objects.get(id=id)
    context = {'patient': patient}
    return render(request, 'patient/edit.html', context)


def update_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient.firstname = request.POST['firstname']
    patient.lastname = request.POST['lastname']
    patient.save()
    return redirect('/read_patient/')

def view_patient_record(request, id):
    if not request.user.is_authenticated:
        return redirect('home')
    print("-------------------------",id)
    patient=Patient.objects.get(id=id)
    patient_record=PatientRecords.objects.filter(patient_id=id)


    contex={'patient':patient,
            'patient_record':patient_record,

            }
    return render(request,'patient/view.html',contex)

def create_patient_clinical(request):
    if not request.user.is_authenticated:
        return redirect('home')
    patient_id = request.POST.get('patient_id')

    patient_record = PatientRecords(body_mass=request.POST.get('bodymass'),
                                    temperature=request.POST.get('temperature'),
                                    diastolic=request.POST.get('diastolic'),
                                    systolic=request.POST.get('systolic'),
                                     patient_id=patient_id
                                    )
    print("========================================================", patient_record)
    patient_record.save()




    return redirect('view_patient_record',patient_id)

def process(request):

    if not request.user.is_authenticated:
        return redirect('home')


    patientRecord_id = request.POST.get('patientRecord_id')
    patient_id = request.POST.get('patient_id')

    patient = Patient.objects.get(id=patient_id)
    # print("record -------------------------------------------",patientRecord_id)
    weakness=request.POST['weakness']
    vomiting=request.POST['vomiting']
    jointPain=request.POST['jointPain']
    fever = request.POST['fever']
    convulision = request.POST['convulision']
    diarrhea = request.POST['diarrhea']
    sweating = request.POST['sweating']
    coma = request.POST['coma']
    abnormalPain = request.POST['abnormalPain']
    cough = request.POST['cough']
    bodyPain = request.POST['bodyPain']
    cold = request.POST['cold']
    chills = request.POST['chills']
    headache = request.POST['headache']
    musclePain = request.POST['musclePain']

    print(weakness)

    print(int(vomiting))
    print(jointPain)
    print(fever)
    print(convulision)
    print(diarrhea)
    print(sweating)
    print(coma)
    print(abnormalPain)
    print(cough)
    print(bodyPain)
    print(cold)
    print(chills)
    print(headache)
    print(musclePain)





    data = pd.read_csv("D:/Projects/Final Systems/malaria/mysite/uploads/dataset.csv")
    data=data[[
    "weakness",
    "abnormalPain",
    "cough",
    "bodyPain",
    "cold",
    "chills",
    "headache",
    "musclePain",
    "vomiting",
    "jointPain",
    "convulision",
    "diarrhea",
    "sweating",
    "coma",
    "fever",
    "class"


    ]].dropna(axis=0, how='any')

# Split dataset in training and test datasets
    X_train, X_test = train_test_split(data, test_size=0.5, random_state=int(time.time()))
    gnb = GaussianNB()
    used_features =[
    "weakness",
    "abnormalPain",
    "cough",
    "bodyPain",
    "cold",
    "chills",
    "headache",
    "musclePain",
    "vomiting",
    "jointPain",
    "convulision",
    "diarrhea",
    "sweating",
    "coma",
    "fever",



    ]
    gnb.fit(
    X_train[used_features].values,
    X_train["class"]
    )
   # y_pred = gnb.predict(X_test[used_features])
    print(data.head())
    print ("Dataset Lenght:: ", len(data))
    print ("Dataset Shape:: ", data.shape)

    predict=gnb.predict([[int(weakness),int(abnormalPain),int(cough),int(bodyPain),int(cold),int(chills),
                          int(headache),int(musclePain),int(vomiting),int(jointPain),int(convulision),
                          int(diarrhea),int(sweating),int(coma),int(fever)]])


    print("=============================================================",predict)

    context = {'predict': predict, 'patient': patient, }
    template = loader.get_template('diagnosis.html')
    return HttpResponse(template.render(context, request))