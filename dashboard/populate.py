import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
from fileConverter import readConvertAdd
import django
from django.contrib.auth.models import User
django.setup()

from dashboard.models import Dataset, Datasource, Visualisation
import json
def users():
    add_superuser("test@test.com", "test")
    add_user("joe@test.com", "test")


def populate():
    datasource = add_datasource("test")

    crimeVis = add_visualisation(datasource, 'Crime', "bar", "Location", "Num of Crimes")
    add_dataset(crimeVis, dataset = [{
                "y": 32,
                "x": "Edinburgh"
            }, {
                "y": 13,
                "x": "Glasgow"
            }, {
                "y": 45,
                "x": "London"
            }, {
                "y": 13,
                "x": "Leeds"
            }, {
                "y": 12,
                "x": "Dublin"
            }])

    employmentNatureVis = add_visualisation(datasource, 'Employment Nature', "bar", "Nature", "Num of Employments")
    add_dataset(employmentNatureVis, dataset = [{
                "y": 5,
                "x": "Edinburgh"
            }, {
                "y": 3,
                "x": "Glasgow"
            }, {
                "y": 8,
                "x": "London"
            }, {
                "y": 3,
                "x": "Leeds"
            }])

    unemploymentVis = add_visualisation(datasource, 'Unemployment', "bar", "Location", "Num of Unemployments")
    add_dataset(unemploymentVis, dataset = [{
                "y": 4,
                "x": "Edinburgh"
            }, {
                "y": 8,
                "x": "Glasgow"
            }, {
                "y": 15,
                "x": "London"
            }, {
                "y": 16,
                "x": "Leeds"
            }, {
                "y": 23,
                "x": "Dublin"
            }])

    # One graph with two lines
    gdpPCVis = add_visualisation(datasource, 'GDP Per Head (Pounds) v Year', "line", "Year", "GDP Per Head", sizeY=2)
    add_dataset(gdpPCVis, dataset = [{
                "y": 152,
                "x": 2000
            }, {
                "y": 189,
                "x": 2002
            }, {
                "y": 179,
                "x": 2004
            }, {
                "y": 199,
                "x": 2006
            }, {
                "y": 134,
                "x": 2008
            }, {
                "y": 176,
                "x": 2010
            }])
    add_dataset(gdpPCVis, dataset = [{
                "y": 16,
                "x": 2000
            }, {
                "y": 200,
                "x": 2002
            }, {
                "y": 150,
                "x": 2004
            }, {
                "y": 230,
                "x": 2006
            }, {
                "y": 120,
                "x": 2008
            }, {
                "y": 110,
                "x": 2010
            }])

    employmentRateVis = add_visualisation(datasource, 'Employment Rate v Year', "line", "Year", "Percentage Employed", sizeY=2)
    add_dataset(employmentRateVis, [{
                "y": 20,
                "x": 2000
            }, {
                "y": 30,
                "x": 2002
            }, {
                "y": 50,
                "x": 2004
            }, {
                "y": 70,
                "x": 2006
            }, {
                "y": 80,
                "x": 2008
            }, {
                "y": 25,
                "x": 2010
            }])

    claimentCountVis = add_visualisation(datasource, 'Claimant Count Numbers', "bar", "Location", "Num of Claimants")
    add_dataset(claimentCountVis, [{
                "y": 152,
                "x": "Edinburgh"
            }, {
                "y": 189,
                "x": "Glasgow"
            }, {
                "y": 179,
                "x": "London"
            }, {
                "y": 199,
                "x": "Leeds"
            }, {
                "y": 134,
                "x": "Dublin"
            }, {
                "y": 176,
                "x": "Manchester"
            }])

    housePriceVis = add_visualisation(datasource, 'House Price v Year', "line", "Year", "House Prices (1000)", sizeY=2)
    add_dataset(housePriceVis, [{
                "y": 152,
                "x": 2000
            }, {
                "y": 189,
                "x": 2002
            }, {
                "y": 179,
                "x": 2004
            }, {
                "y": 199,
                "x": 2006
            }, {
                "y": 134,
                "x": 2008
            }, {
                "y": 176,
                "x": 2010
            }])

    # Add some test users
    add_superuser("test@test.com", "test")
    add_user("joe@test.com", "test")

def add_visualisation(dataSource, name, dataType, xLabel, yLabel, filename="", sizeX=2, sizeY=2):
    d = Visualisation.objects.get_or_create(dataSource=dataSource,
                                      name=name,
                                      type=dataType,
                                      sizeX=sizeX,
                                      sizeY=sizeY,
                                      xLabel=xLabel,
                                      yLabel=yLabel)[0]
    d.save()
    return d

def add_datasource(name):
    d = Datasource.objects.get_or_create(name=name)[0]
    return d

def add_dataset(visualisation, dataset={}, JSONdataset="", filename=""):
    if JSONdataset == "":
        JSONdataset = json.dumps(dataset);
    d = Dataset.objects.get_or_create(visualisation=visualisation, filename=filename, dataJSON=JSONdataset)
    return d

def add_user(name, password, email="test@example.com"):
    user = User.objects.create_user(name, email, password)
    return user

def add_superuser(name, password):
    u = User.objects.get_or_create(username=name)[0]
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()
    return u

if __name__ == '__main__':
    print "Starting population script..."
    readConvertAdd('./dashboard/static/data/employment.csv','test')
    readConvertAdd('./dashboard/static/data/full time employment.csv','test')
    readConvertAdd('./dashboard/static/data/unemployment.csv','test')
    readConvertAdd('./dashboard/static/data/wages.csv','test')
    populate()
