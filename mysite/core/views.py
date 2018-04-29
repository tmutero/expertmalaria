from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from mysite.core.forms import SignUpForm
from mysite.core.models import Patient


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
   # patient_record=PatientRecords.objects.filter(patient_id=id)
    print("============================================================")


    contex={'patient':patient,
            }
    return render(request,'patient/view.html',contex)

def create_patient_clinical(request):
    if not request.user.is_authenticated:
        return redirect('home')
    patient_id=request.POST.get('patient_id')


    return redirect('view_patient_record',patient_id)

