from django.shortcuts import render
import datetime

from app.models import Users
from paymyrent.settings import MEDIA_URL, BASE_DIR, DEBUG


def addGlobalData(request, data):
    """
        General data requested from the user
    """
    data['authenticated'] = True if not request.user.is_anonymous() else False
    data['user'] = request.user

    myuser = None
    base_template = "base.html"

    if not request.user.is_anonymous():
        base_template = "base2.html"
        myuser = Users.objects.get(user=request.user)

    data['myuser'] = myuser
    data['base_template'] = base_template

    data['currenttime'] = datetime.datetime.now()
    data['years'] = [(x, x) for x in range(1950, 2010)]

    data['media_url'] = MEDIA_URL
    data['base_dir'] = BASE_DIR
    data['debug'] = DEBUG

    if DEBUG:
        data['domain_url'] = "{}{}".format('http://', request.get_host())
    else:
        data['domain_url'] = "{}{}".format('https://', request.get_host())

    data['is_delete'] = False


def index(request):
    """
        Renders frontend homepage
    """
    data = {'title': 'Welcome to Pay My Rent'}
    addGlobalData(request, data)
    return render(request, 'index.html', data)


def residents(request):
    """
        residents information page
    """
    data = {'title': 'PayMyRent - Residents Overview'}
    addGlobalData(request, data)
    return render(request, 'overviews/residents.html', data)


def propertymanagers(request):
    """
        property managers information page
    """
    data = {'title': 'PayMyRent - Property Managers Overview'}
    addGlobalData(request, data)
    return render(request, 'overviews/property-managers.html', data)

def landlords(request):
    """
        landlords information page
    """
    data = {'title': 'PayMyRent - Landlords Overview'}
    addGlobalData(request, data)
    return render(request, 'overviews/landlords.html', data)


def pricing(request):
    """
        pricing information page
    """
    data = {'title': 'PayMyRent - Pricing Overview'}
    addGlobalData(request, data)
    return render(request, 'overviews/pricing.html', data)