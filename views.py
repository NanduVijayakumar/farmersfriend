from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.db.models import Max
from .models import user_login

from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
# from django.db.models import  Sum

from django.views.decorators.csrf import csrf_exempt
import razorpay


def index(request):
    return render(request, './myapp/index.html')


def about(request):
    return render(request, './myapp/about.html')


def contact(request):
    return render(request, './myapp/contact.html')

############## ADMIN ###########################
def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='admin')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/admin_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/admin_login.html',context)


def admin_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/admin_home.html')


def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='admin')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)

from .models import crop_type
def admin_crop_type_add(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':

        type_name = request.POST.get('type_name')

        hd = crop_type(type_name=type_name)
        hd.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_crop_type_add.html', context)
    else:
        return render(request, './myapp/admin_crop_type_add.html')

def admin_crop_type_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        type_name = request.POST.get('type_name')
        hd = crop_type.objects.get(id=int(s_id))

        hd.type_name = type_name
        hd.save()
        msg = 'Record Updated'
        hd_l = crop_type.objects.all()
        context = {'crop_list': hd_l, 'msg': msg}
        return render(request, './myapp/admin_crop_type_view.html', context)
    else:
        id = request.GET.get('id')
        hd = crop_type.objects.get(id=int(id))
        context = {'type_name':hd.type_name,'s_id':hd.id}
        return render(request, './myapp/admin_crop_type_edit.html',context)

def admin_crop_type_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    hd = crop_type.objects.get(id=int(id))
    hd.delete()
    msg = 'Record Deleted'
    hd_l = crop_type.objects.all()
    context = {'crop_list': hd_l,'msg':msg}
    return render(request, './myapp/admin_crop_type_view.html',context)

def admin_crop_type_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    hd_l = crop_type.objects.all()
    context = {'crop_list':hd_l}
    return render(request, './myapp/admin_crop_type_view.html',context)

from .models import expert_details

def admin_expert_details_add(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':


        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        status = 'ok'
        uname = email
        password ='1234'

        ul = user_login.objects.filter(uname=uname, u_type='expert')
        print(len(ul))
        if len(ul) == 1:
            context = {'msg': 'User Email Should Be Unique Registered'}
            return render(request, 'myapp/admin_expert_details_view.html', context)

        ul = user_login(uname=uname, passwd=password, u_type='expert')
        ul.save()

        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        pd = expert_details(user_id=user_id,fname=fname,lname=lname,contact=contact,email=email,status=status)
        pd.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_expert_details_add.html', context)
    else:

        context = { 'msg': ''}
        return render(request, './myapp/admin_expert_details_add.html', context)



def admin_expert_details_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        pd = expert_details.objects.get(id=int(s_id))

        pd.fname = fname
        pd.lname = lname
        pd.contact = contact
        pd.email = email

        pd.save()
        msg = 'Record Updated'
        pd_l = expert_details.objects.all()
        context = {'expert_list': pd_l, 'msg': msg}
        return render(request, './myapp/admin_expert_details_view.html', context)
    else:
        id = request.GET.get('id')

        od = expert_details.objects.get(id=int(id))
        context = {'od':od,'s_id':od.id}
        return render(request, './myapp/admin_expert_details_edit.html',context)

def admin_expert_details_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)

    pd = expert_details.objects.get(id=int(id))
    ul = user_login.objects.get(id = pd.user_id)
    ul.delete()
    pd.delete()
    msg = 'Record Deleted'
    pd_l = expert_details.objects.all()
    context = {'expert_list': pd_l,'msg':msg}
    return render(request, './myapp/admin_expert_details_view.html',context)

def admin_expert_details_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    pd_l = expert_details.objects.all()
    context = {'expert_list':pd_l}
    return render(request, './myapp/admin_expert_details_view.html',context)

def admin_seller_details_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    pd_l = seller_details.objects.all()
    context = {'seller_list':pd_l}
    return render(request, './myapp/admin_seller_details_view.html',context)

def admin_user_details_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    pp_l = user_details.objects.all()
    context = {'user_list':pp_l}
    return render(request, './myapp/admin_user_details_view.html',context)

def admin_user_details_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)

    pd = user_details.objects.get(id=int(id))
    ul = user_login.objects.get(id = pd.user_id)
    ul.delete()
    pd.delete()
    msg = 'Record Deleted'
    pd_l = user_details.objects.all()
    context = {'user_list': pd_l,'msg':msg}
    return render(request, './myapp/admin_user_details_view.html',context)

def admin_crop_master_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    pd_l = crop_master.objects.all()
    hs_l = crop_type.objects.all()
    context = {'crop_list': pd_l, 'type_list': hs_l, 'msg': ''}
    return render(request, './myapp/admin_crop_master_view.html', context)

from .models import seller_details
def admin_seller_details_add(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':


        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        status = 'ok'
        uname = email
        password ='1234'

        ul = user_login.objects.filter(uname=uname, u_type='seller')
        print(len(ul))
        if len(ul) == 1:
            context = {'msg': 'User Email Should Be Unique Registered'}
            return render(request, 'myapp/admin_seller_details_view.html', context)

        ul = user_login(uname=uname, passwd=password, u_type='seller')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        pd = seller_details(user_id=user_id,fname=fname,lname=lname,addr=addr, pin=pin,contact=contact,email=email,status=status)
        pd.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_seller_details_add.html', context)
    else:

        context = { 'msg': ''}
        return render(request, './myapp/admin_seller_details_add.html', context)


def admin_seller_details_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        contact = request.POST.get('contact')
        email = request.POST.get('email')

        pd = seller_details.objects.get(id=int(s_id))

        pd.fname = fname
        pd.lname = lname
        pd.addr = addr
        pd.pin = pin
        pd.contact = contact
        pd.email = email

        pd.save()
        msg = 'Record Updated'
        pd_l = seller_details.objects.all()
        context = {'seller_list': pd_l, 'msg': msg}
        return render(request, './myapp/admin_seller_details_view.html', context)
    else:
        id = request.GET.get('id')

        od = seller_details.objects.get(id=int(id))
        context = {'od':od,'s_id':od.id}
        return render(request, './myapp/admin_seller_details_edit.html',context)


def admin_seller_details_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)

    pd = seller_details.objects.get(id=int(id))
    ul = user_login.objects.get(id = pd.user_id)
    ul.delete()
    pd.delete()
    msg = 'Record Deleted'
    pd_l = seller_details.objects.all()
    context = {'seller_list': pd_l,'msg':msg}
    return render(request, './myapp/admin_seller_details_view.html',context)

###########################################
############ EXPERT #######################
def expert_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='expert')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/expert_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/expert_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/expert_login.html',context)


def expert_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return expert_login(request)
    else:
        return render(request,'./myapp/expert_home.html')


def expert_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return expert_login(request)
    else:
        return expert_login(request)

def expert_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='expert')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/expert_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/expert_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/expert_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/expert_changepassword.html', context)

from .models import crop_master
def expert_crop_master_add(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return expert_login(request)

    if request.method == 'POST':

        crop_type_id = int(request.POST.get('crop_type_id'))
        crop_name = request.POST.get('crop_name')
        crop_sname = request.POST.get('crop_sname')
        crop_descp = request.POST.get('crop_descp')
        crop_area = request.POST.get('crop_area')

        pd = crop_master(crop_type_id=crop_type_id,crop_name=crop_name,crop_sname=crop_sname,
                         crop_descp=crop_descp,crop_area=crop_area)
        pd.save()
        hs_l = crop_type.objects.all()
        context = {'type_list':hs_l,'msg': 'Record Added'}
        return render(request, './myapp/expert_crop_master_add.html', context)
    else:
        hs_l = crop_type.objects.all()
        context = {'type_list': hs_l, 'msg': ''}
        return render(request, './myapp/expert_crop_master_add.html', context)



def expert_crop_master_edit(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return expert_login(request)

    if request.method == 'POST':
        s_id = request.POST.get('s_id')
        crop_type_id = int(request.POST.get('crop_type_id'))
        crop_name = request.POST.get('crop_name')
        crop_sname = request.POST.get('crop_sname')
        crop_descp = request.POST.get('crop_descp')
        crop_area = request.POST.get('crop_area')

        pd = crop_master.objects.get(id=int(s_id))

        pd.crop_type_id = crop_type_id
        pd.crop_name = crop_name
        pd.crop_sname = crop_sname
        pd.crop_descp = crop_descp
        pd.crop_area = crop_area

        pd.save()
        msg = 'Record Updated'
        pd_l = crop_master.objects.all()
        hs_l = crop_type.objects.all()
        context = {'crop_list': pd_l,'type_list':hs_l, 'msg': msg}
        return render(request, './myapp/expert_crop_master_view.html', context)
    else:
        id = request.GET.get('id')
        hs_l = crop_type.objects.all()
        shd = crop_master.objects.get(id=int(id))
        context = {'shd':shd,'s_id':shd.id,'type_list':hs_l}
        return render(request, './myapp/expert_crop_master_edit.html',context)

def expert_crop_master_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return expert_login(request)

    id = request.GET.get('id')
    print('id = '+id)

    pd = crop_master.objects.get(id=int(id))
    pd.delete()
    msg = 'Record Deleted'

    pd_l = crop_master.objects.all()
    hs_l = crop_type.objects.all()
    context = {'crop_list': pd_l,'type_list':hs_l,'msg':msg}
    return render(request, './myapp/expert_crop_master_view.html',context)

def expert_crop_master_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return expert_login(request)

    pd_l = crop_master.objects.all()
    hs_l = crop_type.objects.all()
    context = {'crop_list': pd_l, 'type_list': hs_l, 'msg': ''}
    return render(request, './myapp/expert_crop_master_view.html', context)

from .models import crop_pics
from django.core.files.storage import FileSystemStorage
from datetime import datetime

def expert_crop_pics_add(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)

        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        pp = crop_pics(crop_id=crop_id,pic_path=pic_path)
        pp.save()

        context = {'msg':'Picture added','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_pics_add.html',context)

    else:
        crop_id = request.GET.get('crop_id')
        context = {'msg':'','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_pics_add.html',context)

def expert_crop_pics_delete(request):
    id = request.GET.get('id')
    crop_id = request.GET.get('crop_id')
    print("id="+id)
    pp = crop_pics.objects.get(id=int(id))
    pp.delete()

    pp_l = crop_pics.objects.filter(crop_id=int(crop_id))
    context ={'pic_list':pp_l,'crop_id': crop_id,'msg':'Picture deleted'}
    return render(request,'myapp/expert_crop_pics_view.html',context)

def expert_crop_pics_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = crop_pics.objects.filter(crop_id=crop_id)
    context = {'pic_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/expert_crop_pics_view.html', context)

from .models import crop_variety
def expert_crop_variety_add(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)
        variety_name = request.POST.get('variety_name')
        variety_sname = request.POST.get('variety_sname')
        crop_descp = request.POST.get('crop_descp')
        crop_area = request.POST.get('crop_area')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        pp = crop_variety(crop_id=crop_id,pic_path=pic_path,variety_name=variety_name,
                          variety_sname=variety_sname,crop_descp=crop_descp,crop_area=crop_area)
        pp.save()

        context = {'msg':'Picture added','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_variety_add.html',context)

    else:
        crop_id = request.GET.get('crop_id')
        context = {'msg':'','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_variety_add.html',context)

def expert_crop_variety_delete(request):
    id = request.GET.get('id')
    crop_id = request.GET.get('crop_id')
    print("id="+id)
    pp = crop_variety.objects.get(id=int(id))
    pp.delete()

    pp_l = crop_variety.objects.filter(crop_id=int(crop_id))
    context ={'variety_list':pp_l,'crop_id': crop_id,'msg':'Picture deleted'}
    return render(request,'myapp/expert_crop_variety_view.html',context)

def expert_crop_variety_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = crop_variety.objects.filter(crop_id=crop_id)
    context = {'variety_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/expert_crop_variety_view.html', context)

from .models import cultivation_details
def expert_crop_cultivation_add(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)
        land_type = request.POST.get('land_type')
        soil_concentration = request.POST.get('soil_concentration')
        descp = request.POST.get('descp')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        pp = cultivation_details(crop_id=crop_id,pic_path=pic_path,descp=descp,
                          land_type=land_type,soil_concentration=soil_concentration)
        pp.save()

        context = {'msg':'Cultivation Details added','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_cultivation_add.html',context)

    else:
        crop_id = request.GET.get('crop_id')
        context = {'msg':'','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_cultivation_add.html',context)

def expert_crop_cultivation_delete(request):
    id = request.GET.get('id')
    crop_id = request.GET.get('crop_id')
    print("id="+id)
    pp = cultivation_details.objects.get(id=int(id))
    pp.delete()

    pp_l = cultivation_details.objects.filter(crop_id=int(crop_id))
    context ={'cultivation_list':pp_l,'crop_id': crop_id,'msg':'Cultivation Details deleted'}
    return render(request,'myapp/expert_crop_cultivation_view.html',context)

def expert_crop_cultivation_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = cultivation_details.objects.filter(crop_id=crop_id)
    context = {'cultivation_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/expert_crop_cultivation_view.html', context)


from .models import fertilizer_master
def expert_crop_fertilizer_add(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        image = fs.save(uploaded_file.name, uploaded_file)

        f_type = request.POST.get('f_type')
        f_name = request.POST.get('f_name')
        descp = request.POST.get('descp')
        application = request.POST.get('application')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        pp = fertilizer_master(crop_id=crop_id,image=image,descp=descp,
                          f_type=f_type,f_name=f_name,application=application)
        pp.save()

        context = {'msg':'Fertilizer Details added','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_fertilizer_add.html',context)

    else:
        crop_id = request.GET.get('crop_id')
        context = {'msg':'','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_fertilizer_add.html',context)

def expert_crop_fertilizer_delete(request):
    id = request.GET.get('id')
    crop_id = request.GET.get('crop_id')
    print("id="+id)
    pp = fertilizer_master.objects.get(id=int(id))
    pp.delete()

    pp_l = fertilizer_master.objects.filter(crop_id=int(crop_id))
    context ={'fertilizer_list':pp_l,'crop_id': crop_id,'msg':'Fertilizer Details deleted'}
    return render(request,'myapp/expert_crop_fertilizer_view.html',context)

def expert_crop_fertilizer_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = fertilizer_master.objects.filter(crop_id=crop_id)
    context = {'fertilizer_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/expert_crop_fertilizer_view.html', context)

from .models import pesticides_master
def expert_crop_pesticides_add(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        image = fs.save(uploaded_file.name, uploaded_file)

        pt_type = request.POST.get('pt_type')
        product_name = request.POST.get('product_name')
        company = request.POST.get('company')
        descp = request.POST.get('descp')
        application = request.POST.get('application')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        pp = pesticides_master(crop_id=crop_id,image=image,descp=descp,company=company,
                          pt_type=pt_type,product_name=product_name,application=application)
        pp.save()

        context = {'msg':'Pesticides Details added','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_pesticides_add.html',context)

    else:
        crop_id = request.GET.get('crop_id')
        context = {'msg':'','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_pesticides_add.html',context)

def expert_crop_pesticides_delete(request):
    id = request.GET.get('id')
    crop_id = request.GET.get('crop_id')
    print("id="+id)
    pp = pesticides_master.objects.get(id=int(id))
    pp.delete()

    pp_l = pesticides_master.objects.filter(crop_id=int(crop_id))
    context ={'pesticides_list':pp_l,'crop_id': crop_id,'msg':'Pesticides Details deleted'}
    return render(request,'myapp/expert_crop_pesticides_view.html',context)

def expert_crop_pesticides_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = pesticides_master.objects.filter(crop_id=crop_id)
    context = {'pesticides_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/expert_crop_pesticides_view.html', context)

from .models import disease_master
def expert_crop_disease_add(request):
    if request.method == 'POST':
        crop_id = request.POST.get('crop_id')
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        pic_path = fs.save(uploaded_file.name, uploaded_file)


        name = request.POST.get('name')

        descrp = request.POST.get('descrp')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        pp = disease_master(crop_id=crop_id,pic_path=pic_path,descrp=descrp,name=name)
        pp.save()

        context = {'msg':'disease Details added','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_disease_add.html',context)

    else:
        crop_id = request.GET.get('crop_id')
        context = {'msg':'','crop_id':crop_id}
        return render(request, 'myapp/expert_crop_disease_add.html',context)

def expert_crop_disease_delete(request):
    id = request.GET.get('id')
    crop_id = request.GET.get('crop_id')
    print("id="+id)
    pp = disease_master.objects.get(id=int(id))
    pp.delete()

    pp_l = disease_master.objects.filter(crop_id=int(crop_id))
    context ={'disease_list':pp_l,'crop_id': crop_id,'msg':'Pesticides Details deleted'}
    return render(request,'myapp/expert_crop_disease_view.html',context)

def expert_crop_disease_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = disease_master.objects.filter(crop_id=crop_id)
    context = {'disease_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/expert_crop_disease_view.html', context)


def expert_ask_expert_view(request):

    msg = ''
    user_id = request.session['user_id']
    sd_l = user_details.objects.all()
    shd = expert_details.objects.get(user_id = int(user_id))
    suc_l = ask_expert.objects.filter(expert_id=shd.id)

    context = {'user_list': sd_l, 'chat_list': suc_l, 'msg': msg}
    return render(request, './myapp/expert_ask_expert_view.html', context)

def expert_ask_expert_reply(request):
    if request.method == 'POST':

        user_id = request.session['user_id']
        message_id = int(request.POST.get('message_id'))
        answer = request.POST.get('answer')

        suc = ask_expert.objects.get(id=int(message_id))
        suc.answer = answer
        suc.status='replied'
        suc.save()

        sd_l = user_details.objects.all()
        shd = expert_details.objects.get(user_id=int(user_id))
        suc_l = ask_expert.objects.filter(expert_id=shd.id)

        context = {'user_list': sd_l, 'chat_list': suc_l, 'msg': 'updated'}
        return render(request, './myapp/expert_ask_expert_view.html', context)
    else:
        user_id = request.session['user_id']
        message_id = int(request.GET.get('id'))


        context = {'message_id': message_id}
        return render(request, './myapp/expert_ask_expert_reply.html', context)






##########################################
########### USER ###########################
from .models import user_details

def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}
            #send_mail('Login','welcome'+uname,uname)
            return render(request, 'myapp/user_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):

    context = {'fname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)
    #send_mail("heoo", "hai", 'snehadavisk@gmail.com')

def user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        kcno = request.POST.get('kcno')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname=email
        #status = "new"
        if user_details.objects.filter(email=email).exists():
            context = {'msg': 'Email already exits'}
            return render(request, 'myapp/user_details_add.html', context)
        else:
            ul = user_login(uname=uname, passwd=password, u_type='user')
            ul.save()
            user_id = user_login.objects.all().aggregate(Max('id'))['id__max']
            ud = user_details(user_id=user_id,fname=fname, lname=lname, kcno=kcno, gender=gender, age=age,addr=addr, pin=pin, contact=contact, email=email )
            ud.save()
            print(user_id)
            context = {'msg': 'User Registered'}
            return render(request, 'myapp/user_login.html',context)

    else:
        return render(request, 'myapp/user_details_add.html')

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)

            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/user_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/user_changepassword.html', context)
    else:
        return render(request, './myapp/user_changepassword.html')



def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)

def user_crop_master_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return user_login_check(request)
    pd_l = crop_master.objects.all()
    context = {'crop_list':pd_l}
    return render(request, './myapp/user_crop_master_view.html',context)

def user_crop_master_search(request):

    if request.method == 'POST':
        query = request.POST.get('query')
        pd_l = crop_master.objects.filter(crop_name__contains=query)
        hs_l = crop_type.objects.all()
        context = {'crop_list': pd_l, 'type_list': hs_l, 'msg': ''}
        return render(request, './myapp/user_crop_master_view.html', context)
    else:
        return render(request, 'myapp/user_crop_master_search.html')

def user_crop_pics_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = crop_pics.objects.filter(crop_id=crop_id)
    context = {'pic_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/user_crop_pics_view.html', context)


def user_crop_variety_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = crop_variety.objects.filter(crop_id=crop_id)
    context = {'variety_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/user_crop_variety_view.html', context)


def user_crop_cultivation_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = cultivation_details.objects.filter(crop_id=crop_id)
    context = {'cultivation_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/user_crop_cultivation_view.html', context)

def user_crop_fertilizer_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = fertilizer_master.objects.filter(crop_id=crop_id)
    context = {'fertilizer_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/user_crop_fertilizer_view.html', context)

def user_crop_pesticides_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = pesticides_master.objects.filter(crop_id=crop_id)
    context = {'pesticides_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/user_crop_pesticides_view.html', context)

def user_crop_disease_view(request):
    crop_id = request.GET.get('crop_id')
    pp_l = disease_master.objects.filter(crop_id=crop_id)
    context = {'disease_list': pp_l, 'crop_id': crop_id, 'msg': ''}
    return render(request, 'myapp/user_crop_disease_view.html', context)

def user_expert_details_view(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return user_login_check(request)
    pd_l = expert_details.objects.all()
    context = {'expert_list':pd_l}
    return render(request, './myapp/user_expert_details_view.html',context)

from .models import ask_expert
def user_ask_expert_add(request):
    if request.method == 'POST':

        user_id = request.session['user_id']
        expert_id = int(request.POST.get('expert_id'))
        question=request.POST.get('question')

        answer = 'not answered'
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'ok'
        suc = ask_expert(user_id=user_id,expert_id=expert_id,question=question,
                                 answer=answer,dt=dt,tm=tm,status=answer)
        suc.save()

        sd_l = expert_details.objects.all()
        context = {'expert_list': sd_l, 'msg': 'Question Record Added'}
        return render(request, './myapp/user_expert_details_view.html', context)
    else:
        expert_id = int(request.GET.get('expert_id'))
        sd_l = expert_details.objects.all()
        context = {'expert_list': sd_l, 'expert_id': expert_id, 'msg': ''}
        return render(request, './myapp/user_ask_expert_add.html', context)

def user_ask_expert_delete(request):
    id = request.GET.get('id')
    print('id = '+id)
    suc = ask_expert.objects.get(id=int(id))
    suc.delete()

    msg = 'Record Deleted'
    user_id = request.session['user_id']
    sd_l = expert_details.objects.all()
    suc_l = ask_expert.objects.filter(user_id=int(user_id))


    context = {'expert_list': sd_l, 'chat_list': suc_l, 'msg':msg}
    return render(request, './myapp/user_ask_expert_view.html',context)


def user_ask_expert_view(request):
    msg = ''
    user_id = request.session['user_id']
    sd_l = expert_details.objects.all()
    suc_l = ask_expert.objects.filter(user_id=int(user_id))

    context = {'expert_list': sd_l, 'chat_list': suc_l, 'msg': msg}
    return render(request, './myapp/user_ask_expert_view.html', context)


#####################Seller############################
def seller_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='seller')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/seller_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/seller_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/seller_login.html',context)


def seller_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return seller_login(request)
    else:
        return render(request,'./myapp/seller_home.html')


def seller_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return seller_login(request)
    else:
        return seller_login(request)

def seller_changepassword(request):
        if request.method == 'POST':
            opasswd = request.POST.get('opasswd')
            npasswd = request.POST.get('npasswd')
            cpasswd = request.POST.get('cpasswd')
            uname = request.session['user_name']
            try:
                ul = user_login.objects.get(uname=uname, passwd=opasswd, u_type='seller')
                if ul is not None:
                    ul.passwd = npasswd
                    ul.save()
                    context = {'msg': 'Password Changed'}
                    return render(request, './myapp/seller_changepassword.html', context)
                else:
                    context = {'msg': 'Password Not Changed'}
                    return render(request, './myapp/seller_changepassword.html', context)
            except user_login.DoesNotExist:
                context = {'msg': 'Password Err Not Changed'}
                return render(request, './myapp/seller_changepassword.html', context)
        else:
            context = {'msg': ''}
            return render(request, './myapp/seller_changepassword.html', context)

from .models import product_details
def seller_product_details_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        image = fs.save(uploaded_file.name, uploaded_file)
        user_id = int(request.session['user_id'])
        p_name = request.POST.get('p_name')
        descp = request.POST.get('descp')
        price = request.POST.get('price')

        pda = product_details(user_id=user_id,p_name=p_name,image=image,descp=descp,
                          price=price)
        pda.save()

        context = {'msg':'Product Details added'}
        return render(request, 'myapp/seller_product_details_add.html',context)

    else:
        user_id = int(request.session['user_id'])
        context = {'msg':'','user_id':user_id}
        return render(request, 'myapp/seller_product_details_add.html',context)

def seller_product_details_view(request):
    msg = ''
    user_id = request.session['user_id']
    sd_l = product_details.objects.filter(user_id=user_id)

    context = {'product_list': sd_l, 'msg': msg}
    return render(request, './myapp/seller_product_details_view.html', context)

def user_product_view(request):
    msg = ''
    #user_id = request.session['user_id']
    sd_l = product_details.objects.all()

    context = {'product_list': sd_l, 'msg': msg}
    return render(request, './myapp/user_product_view.html', context)

from.models import user_transaction
def user_transaction_add(request):
    RAZORPAY_API_KEY = 'rzp_test_V3Uo0HLMkxXIO6'
    RAZORPAY_API_SECRETKEY = 'nXn2myk1jy7dDCuRdSZRALgD'

    if request.method == 'POST':

        user_id = request.session['user_id']
        product_id = int(request.POST.get('product_id'))
        amt = request.POST.get('amt')
        addr = request.POST.get('addr')
        # card_no = request.POST.get('card_no')
        # cvv = request.POST.get('cvv')
        # expiry = request.POST.get('expiry')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = request.POST.get('status')


        suc = user_transaction(amt=int(amt),product_id=product_id,user_id=int(user_id),
                                   addr=addr,status=status,dt=dt,tm=tm)
        suc.save()
        return user_transaction_view(request)
        # context = {'msg': 'Item Purchased'}
        # return render(request, './myapp/user_transaction_add.html', context)
    else:
        product_id = int(request.GET.get('product_id'))

        l_l = product_details.objects.get(id=product_id)
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRETKEY))
        order_amount = int(l_l.price) * 100;
        order_currency = 'INR'
        payment_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))

        payment_order_id = payment_order['id']
        context = {
            'amt': order_amount, 'api_key': RAZORPAY_API_KEY, 'order_id': payment_order_id,'product':l_l
        }

        return render(request, './myapp/user_transaction_add.html', context)

def user_transaction_view(request):
    user_id = request.session['user_id']
    sd_l = product_details.objects.all()
    suc_l = user_transaction.objects.filter(user_id=int(user_id))

    ud_l = user_details.objects.all()
    context = {'product_list': sd_l, 'transaction_list': suc_l, 'msg': '', 'user_list': ud_l}
    return render(request, './myapp/user_transaction_view.html', context)

def seller_transaction_view(request):
    user_id = request.session['user_id']
    sd_l = product_details.objects.filter(user_id=int(user_id))

    pm_l = user_transaction.objects.filter(product_id__in=list(map(lambda d: d.id , sd_l)))

    msg = ''
    if len(pm_l) == 0:
        msg = 'No Data'

    ud_l = user_details.objects.all()
    context = {'product_list': sd_l, 'transaction_list': pm_l, 'msg': msg, 'user_list': ud_l}
    return render(request, './myapp/seller_transaction_view.html', context)

def export_pdf(request):


        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; attachment; filename=User Details' +'.pdf'
        response['Content-Transfer-Encoding'] = 'binary'

        try:
            uname = request.session['user_name']
            print(uname)
        except:
            return admin_login(request)
        pp_l = user_details.objects.all()
        context = {'myapp': pp_l}
        # return render(request, './myapp/pdf-output.html', context)



        html_string = render_to_string('./myapp/pdf-output.html',{ 'myapp':pp_l})
        html = HTML(string=html_string)



        result = html.write_pdf()



        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output.seek(0)
            response.write(output.read())



        return response


def export_pdf_invoice(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=User Details' + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    sd_l = product_details.objects.all()


    ud_l = user_details.objects.all()
    id = int(request.GET.get('product_id'))
    pp_l = user_transaction.objects.filter(id=id)
    # return render(request, './myapp/pdf-output.html', context)

    context = {'product_list': sd_l, 'cs': pp_l[0], 'msg': '', 'user_list': ud_l}
    html_string = render_to_string('./myapp/pdf-output-invoice.html', context)
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response

def export_pdf_seller(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=User Details' + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    # user_id = request.session['user_id']
    # sd_l = product_details.objects.filter(user_id=int(user_id))
    # shd = product_details.objects.get(user_id=int(user_id))
    # pm_l = user_transaction.objects.filter(product_id=shd.id)
    # msg = ''
    # if len(pm_l) == 0:
    #     msg = 'No Data'
    #
    # ud_l = user_details.objects.all()
    # context = {'product_list': sd_l, 'transaction_list': pm_l, 'msg': msg, 'user_list': ud_l}

    user_id = request.session['user_id']
    sd_l = product_details.objects.filter(user_id=int(user_id))
    pm_l = user_transaction.objects.filter(product_id__in=list(map(lambda d: d.id , sd_l)))
    msg = ''
    if len(pm_l) == 0:
        msg = 'No Data'
    ud_l = user_details.objects.all()
    context = {'product_list': sd_l, 'transaction_list': pm_l, 'msg': msg, 'user_list': ud_l}

    html_string = render_to_string('./myapp/pdf-output-seller.html', context)
    html = HTML(string=html_string)

    result = html.write_pdf()


    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response