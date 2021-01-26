import datetime

from django.http import HttpResponse
from django.utils.timezone import make_aware
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .forms import CreateSms
from .models import Outbox, Inbox, DeliveryReport


def outbox(request):
    outbox = Outbox.objects.all()
    search_term = ''
    clicked = request.GET.get('clicked', 'outbox')
    if 'search' in request.GET:
        search_term = request.GET.get('search')
        outbox = outbox.filter(text__icontains=search_term)
    paginator = Paginator(outbox, 5)
    page = request.GET.get('page')
    outbox = paginator.get_page(page)
    context = {'outbox': outbox, 'active': clicked, 'search_term': search_term}
    return render(request, "smsapp/outbox.html", context)


def create_sms(request):
    form = CreateSms()
    if request.method == "POST":
        form = CreateSms(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            message = form.cleaned_data.get("message")
            Outbox.send(phone_number, message)
            return redirect('outbox')

    return render(request, "smsapp/createsms.html", {"form": form})


@csrf_exempt
@require_POST
def incoming_message(request):
    """
    sample incoming message from phone through AfricasTalking API
    {  'from': ['+2547278153xx'],
     'linkId': ['28a92cdf-2d63-4ee3-93df-4233d3de0356'],
       'text': ['heey this is a message from a phone'],
         'id': ['b68d0989-d856-494f-92ee-7c439e96e1d9'],
       'date': ['2021-01-14 08:10:15'],
         'to': ['17163'] }
    """
    date = request.POST.get('date')
    text = request.POST.get('text')
    phoneNo = request.POST.get('from')
    to = request.POST.get('to')
    linkId = request.POST.get('linkId')
    date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    aware_datetime = make_aware(date)
    Inbox_object = Inbox(
                        date=aware_datetime,
                        text=text,
                        phone=phoneNo,
                        to=to,
                        linkId=linkId
                        )
    Inbox_object.save()
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def incoming_delivery_reports(request):
    """
    sample delivery report from Africas Talking API
    {'phoneNumber': ['+254727815xx'],
      'retryCount': ['0'],
          'status': ['Success'],
     'networkCode': ['63902'],
              'id': ['ATXid_29bc0ee2e3566472cd947d2f2918ab2f']}>
    """
    phoneNumber = request.POST.get('phoneNumber')
    retryCount = request.POST.get('retryCount')
    status = request.POST.get('status')
    networkCode = request.POST.get('networkCode')
    identifier = request.POST.get('id')
    DeliveryReport_object = DeliveryReport(identifier=identifier,
                                           phoneNumber=phoneNumber,
                                           retryCount=retryCount,
                                           status=status,
                                           networkCode=networkCode)
    DeliveryReport_object.save()
    return HttpResponse(status=200)


def delivery_reports(request):
    clicked = request.GET.get('clicked')
    all_delivery_reports = DeliveryReport.objects.all()
    paginator = Paginator(all_delivery_reports, 5)
    page = request.GET.get('page')
    all_delivery_reports = paginator.get_page(page)
    context = {'all_delivery_reports': all_delivery_reports, 'active': clicked}
    return render(request, "smsapp/deliveryreports.html", context)


def inbox(request):
    clicked = request.GET.get('clicked')
    all_inbox_items = Inbox.objects.all()
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET.get('search')
        all_inbox_items = all_inbox_items.filter(text__icontains=search_term)
    paginator = Paginator(all_inbox_items, 5)
    page = request.GET.get('page')
    all_inbox_items = paginator.get_page(page)
    context = {
      "all_inbox_items": all_inbox_items, 'active': clicked, 'search_term': search_term  # noqa: E501
    }
    return render(request, "smsapp/inbox.html", context)
