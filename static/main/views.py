from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from datetime import datetime, timedelta
from django.db.models import Q 
from django.contrib import messages
from .form import chequeInfoForm


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='signin')
def dashboard(request):
    listing= chequeInfo.objects.all()

    # for total amount in dashboard.
    total_money = listing.aggregate(Sum('amount'))
    total_money = total_money['amount__sum']

    # to calculate the gain percentage
    last_month = datetime.today() - timedelta(days=30)
    items = chequeInfo.objects.filter(cheque_received_date__gte=last_month)
    last_month_money = items.aggregate(Sum('amount'))
    last_month_money = last_month_money['amount__sum']
    last_month_gain = (last_month_money/total_money)*100

    # to count all transcations and find gain percent for last month
    total_transcation = listing.count()
    last_month_transaction_count = items.count()
    last_month_transaction_count_gain = (last_month_transaction_count/total_transcation)*100

    # to count cleared transactions.
    cleared_transactions = listing.filter(cheque_released=True)
    cleared_transactions =  cleared_transactions.count()
    cleared_transaction_percentage = (cleared_transactions/total_transcation)*100

    # no of cheques due this week
    seven_days = datetime.today() + timedelta(days=7)
    sevendayitems = chequeInfo.objects.filter(cheque_due_date__gte=datetime.today())
    sevendayitems= sevendayitems.filter(cheque_due_date__lte=seven_days)
    sevendayitems = sevendayitems.filter(cheque_released=False)
    sevendayitems= sevendayitems.count()



    # total due amt
    non_cleared_transactions = listing.filter(cheque_released=False)
    non_cleared_transactions_count = non_cleared_transactions.count()




    context={
        'lists':listing,
        'items':items,
        'total_money': total_money,
        'last_month_money': last_month_money,
        'last_month_gain': last_month_gain,
        'total_transcation':total_transcation,
        'last_month_transaction_count':last_month_transaction_count,
        'last_month_transaction_count_gain': last_month_transaction_count_gain,
        'cleared_transactions' : cleared_transactions,
        'cleared_transaction_percentage': cleared_transaction_percentage,
        'non_cleared_transactions_count': non_cleared_transactions_count,
        'sevendayitems':sevendayitems,
    }
    return render(request, "main/dashboardmain.html", context)

@login_required(login_url='signin')
def records(request):

    sort = request.GET.get('sort',"")
    status = request.GET.get('status',"")
    search = request.GET.get('search',"")

    if search:
        listing = chequeInfo.objects.filter(Q(party_name__icontains=search) | Q(account_holders_name__icontains=search) | Q(cheque_number__icontains=search)  | Q(bank_name__icontains=search))
    else:
        listing= chequeInfo.objects.all()
    
    if status:
        listing = listing.filter(cheque_released=status)

    if sort:
        listing= listing.order_by(sort)

    context={
        'lists':listing,
    }
    return render(request, "main/records.html", context)


@login_required(login_url='signin')
def about(request):
    context={}
    return render(request, "main/about.html", context)

@login_required(login_url='signin')
def addrecord(request):
    form = chequeInfoForm()
    if request.method=="POST":
        #print(request.POST)
        form = chequeInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('records')

    context={
        'form':form,
    }
    return render(request,"main/record_form.html", context)

@login_required(login_url='signin')
def updaterecord(request, pk):
    record = chequeInfo.objects.get(id=pk)
    form = chequeInfoForm(instance=record)
    if request.method=="POST":
        #print(request.POST)
        form = chequeInfoForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('records')

    context={
        'form':form,
    }
    return render(request,"main/record_form.html", context)

@login_required(login_url='signin')
def notifications(request):
    try:

        three_days = datetime.today() + timedelta(days=3)
        items = chequeInfo.objects.filter(cheque_due_date__gte=datetime.today())
        items= items.filter(cheque_due_date__lte=three_days)
        items = items.filter(cheque_released=False)
        items = items.order_by('cheque_due_date')

        duedate = datetime.today() - timedelta(days=1)
        duedup = chequeInfo.objects.filter(cheque_due_date__lte=duedate)
        
        duedup = duedup.filter(cheque_released=False)
        duedup = duedup.order_by('cheque_due_date')

        context={
            'items':items,
            'duedup':duedup,
        }
        return render(request,"main/notification.html",context)
    except:
        return render(request,"main/notification.html",{ })

@login_required(login_url='signin')
def reports(request):
    context={

    }
    return render(request, "main/reports.html", context)

@login_required(login_url='signin')
def generatepdf(request):
    if request.method =="POST":
        fromdate= request.POST.get('fromdate')
        todate= request.POST.get('todate')
        list = chequeInfo.objects.filter(cheque_received_date__gte=fromdate)
        list = list.filter(cheque_received_date__lte=todate)
        total = list.aggregate(Sum('amount'))
        total = total['amount__sum']
        releasedcheques = list.filter(cheque_released=True).count()
        unreleasedcheques = list.filter(cheque_released=False).count()
        num = list.count()
        
        template_path = 'main/reporttable.html'
        context = {'list': list, 'total':total, 'releasedcheques':releasedcheques, 'unreleasedcheques':unreleasedcheques,'num':num}
        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ' filename="report.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


@login_required(login_url='signin')
def generateall(request):

    list = chequeInfo.objects.all()
    total = list.aggregate(Sum('amount'))
    total = total['amount__sum']
    releasedcheques = list.filter(cheque_released=True).count()
    unreleasedcheques = list.filter(cheque_released=False).count()
    num = list.count()
    template_path = 'main/reporttable.html'
    context = {'list': list, 'total':total,  'releasedcheques':releasedcheques, 'unreleasedcheques':unreleasedcheques, 'num':num}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:

        context={}
        if request.method =="POST":
            username= request.POST.get('username')
            password= request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request,'Username or password is incorrect')
                return render(request, "main/sign-in.html", context)

        return render(request, "main/sign-in.html", context)

def signout(request):
    logout(request)
    return redirect('signin')