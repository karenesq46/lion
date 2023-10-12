from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from openpyxl import Workbook


from .models import Profile, Task, Bitacora
from .forms import ProfileForm, TaskForm


# Create your views here.
def helloworld(request):
    if request.method =='POST':
        form=ProfileForm(request.POST)
    print(request.POST)

    return HttpResponse('<h3>Bienvenidos</h3>')

#

def signup(request):
    if request.method=='GET':
        return render (request, 'signup.html',{
            'form':UserCreationForm
        })
    else:

        if request.POST['password1']==request.POST['password2']:

         try:
             user=User.objects.create_user(username=request.POST['username'],
             password=request.POST['password1'])
             print(request.POST)
             user.save()
             login(request, user)
             return redirect('home')
         except:
             return render(request, 'signup.html', {
                 'form':UserCreationForm,
                 'error_existe':'Usuario ya existe'
             })
        return render(request, 'signup.html', {
                 'form':UserCreationForm,
                 'error_match':'Las contraseñas no coinciden'
            })


#INICIAR SESION
def signin(request):
    if request.method =='GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            print(request.POST)
            return render (request, 'signin.html', {
                'form':AuthenticationForm,
                'error_match':'Usuario o contraseña son incorrectos'
            })
        else:
            login(request, user)
            return redirect('home')
        
#CERRAR SESION
def close(request):
    logout(request)
    return redirect('signin')



#INSERTAR
def home(request): 
    #profile = Profile.objects.filter(status = True) # Mostras los usuarios activos
    profile = Profile.objects.filter(user=request.user).first() # Mostrar todos los usuarios
    error_profile=None #inicializa rvariable error_profile
    #profile = Profile.objects.exclude(status=True)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)#, request.FILES
        if form.is_valid():     
            if profile is None: 
                new_profile= form.save(commit=False) #comprobacion antes de guardar bd (logica)
                new_profile.user=request.user 
                print(request.POST)
                new_profile.save()
                
                Bitacora.objects.create(
                user=request.user,
                action=f"Se creo el perfil:{new_profile.name}"
                )
                #form.save()
                #
                return redirect('home')
            else:
               error_profile='Ya tienes un perfil creado'  
               Bitacora.objects.create(
                   user=request.user,
                   action=f"Se intento crear un perfil existente"
               )         
    else:
        form = ProfileForm()

    context = {
        'form': form,
        'profile': profile,
        'error_profile':error_profile
    }

    return render(request, 'home.html', context) # Renderiza la vista

def edit_profile(request, profile_id):

    profile = get_object_or_404(Profile, pk=profile_id)

    if request.method=='POST':
        form=ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print(request.POST)
            update_profile=form.save(commit=False)
            update_profile.save()

            Bitacora.objects.create(
                user=request.user,
                action=f'Se actualizo el perfil:{update_profile.name}'
            )

            return redirect('home')
    else:
        form=ProfileForm(instance=profile)

        context = {
            'profile':profile
        }

        return render(request, 'edit_profile.html', context)
        

def trash_profile(request, profile_id):
    #Obtener el perfil, en caso de no existir mandar un error 404
    profile = get_object_or_404(Profile, pk=profile_id)
    profile.delete() #Borrar de la db

    Bitacora.objects.create(
        user=request.user,
        action=f'Se dio de baja el perfil: {profile.name}'
    )

    return redirect('home') #Redirigir a home



def detail_profile(request, profile_id):

    profile = get_object_or_404(Profile, pk=profile_id)

    if request.method=='POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('home')
    else:
        form=ProfileForm(instance=profile)

    context = {
            'form':form,
            'profile':profile
    }

    return render(request, 'detail-profile.html', context)

def delete_profile(request, profile_id):

    profile=get_object_or_404(Profile, pk=profile_id)

    profile.delete()
    return redirect ('home')

def list(request):
    profile = Profile.objects.filter().all()


#login_required
    return render(request, 'history.html', {'profiles':profile})


def tasks(request):
    profile=Profile.objects.filter(user=request.user)
    tasks=Task.objects.filter(user=request.user)

    total_t =Task.objects.filter(user=request.user).count()
    
    total_t_a=Task.objects.filter(user=request.user, important=True).count()
    
    total_t_d=Task.objects.filter(user=request.user, important=False).count()
  

    search_query = request.GET.get('filter', '')
    if search_query:
        tasks=tasks.filter(
            Q(title__icontains=search_query)|
            Q(description__icontains=search_query)
        )
    
    if request.method=='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            new_task=form.save(commit=False)
            new_task.user=request.user
            new_task.save()
            return redirect('tasks')
    else:
        form=TaskForm()

    context={
        'profile': profile,
        'tasks':tasks,
        'total':total_t,
        'total_tareas_activas':total_t_a,
        'total_tareas_pendientes':total_t_d,
        
    }
    return render(request, 'tasks.html',context)

def edit_task(request, task_id):
    profile=Profile.objects.filter(user=request.user)
    task=get_object_or_404(Task, pk=task_id)

    if request.method=='POST':
       form=TaskForm(request.POST, instance=task)
       if form.is_valid():
            print(request.POST)
            update_task=form.save(commit=False)
            update_task.save()
            return redirect('tasks') 
    else:
        form=TaskForm(instance=task)
           
        context={
               'profile': profile,
               'task':task,
        }
        return render(request, 'edit_task.html', context)

def history(request):
    profile=Profile.objects.filter().all()
    total_profile=profile.count()

  
    profile_a=Profile.objects.filter(estatus=True)
    total_profile_a=profile_a.count()

    profile_d=Profile.objects.filter(estatus=False)
    total_profile_d=profile_d.count()


    search_history = request.GET.get('filter_p', '')
    if search_history:
       profile=profile.filter(
            Q(name__icontains=search_history) |
            #Q(email__icontains=search_history)
            Q(phone__icontains=search_history)
        )
       
    context={
        'profile': profile,
        'total': total_profile,
        'total_profile_active':total_profile_a,
        'total_profile_inactive':total_profile_a,
        'search_history':search_history,
    }

    return render(request, 'history.html', context)

def report(request):
    tasks = Task.objects.filter(user=request.user)

    wb=Workbook() 
    ws=wb.active

    ws.append(['Title', 'Description', 'Important', 'Profile'])

    for task in tasks:
        ws.append([task.title, task.description, task.important])

    response =HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=tasks.xlsx'

    wb.save(response)
    return response

def bitacora(request):
    profile_user=Profile.objects.filter(user=request.user)
    action_list=Bitacora.objects.all().order_by('timestamp')

    search_bitacora=request.GET.get('filter_a','') #capturar
    if search_bitacora:
        action_list=action_list.filter(
            Q(action__icontains=search_bitacora)|
            Q(timestamp__icontains=search_bitacora)
        )

    paginator=Paginator(action_list,5)
    page_number= request.GET.get('page')
    action= paginator.get_page(page_number)

    context={
        'profile':profile_user,
        'actions':action,
        'search_bitacora':search_bitacora
    }
    return render(request, 'bitacora.html', context)

def inicio(request):
    return render(request, 'inicio.html')