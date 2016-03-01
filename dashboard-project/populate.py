# coding=UTF8
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
import django
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files import File
from csv_processor.models import CsvFile, Dimension
from dashboard.models import Category, Datasource, Visualisation, DashboardDataset
import os, json
django.setup()


from dashboard.models import DashboardDataset, DashboardDatasource, Visualisation, Category
from csv_processor.models import CsvFile, Dimension
from dataset_importer import util
import json, datetime

def populate():
    datasource = add_datasource("Fake Data Test", "http://example.com")
    crimeCategory = add_category("Crime")
    employmentCategory = add_category("Employment")
    housingCategory = add_category("Housing")
    economyCategory = add_category("Economy")
    healthCategory = add_category("Health")

    crimeVis = add_visualisation(datasource, 'Crime', crimeCategory, "bar", "Location", "Num of Crimes")
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

    employmentNatureVis = add_visualisation(datasource, 'Employment Nature', employmentCategory, "bar", "Nature", "Num of Employments")
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

    unemploymentVis = add_visualisation(datasource, 'Unemployment', employmentCategory, "bar", "Location", "Num of Unemployments")
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
    gdpPCVis = add_visualisation(datasource, 'GDP Per Head (Pounds)', economyCategory, "line", "Year", "GDP Per Head", sizeY=2)
    add_dataset(gdpPCVis, dataset = [{
                "y": 152,
                "x": datetime.datetime(2000,1,1)
            }, {
                "y": 189,
                "x": datetime.datetime(2002,1,1)
            }, {
                "y": 179,
                "x": datetime.datetime(2004,1,1)
            }, {
                "y": 199,
                "x": datetime.datetime(2006,1,1)
            }, {
                "y": 134,
                "x": datetime.datetime(2008,1,1)
            }, {
                "y": 176,
                "x": datetime.datetime(2010,1,1)
            },{
                "y": 180,
                "x": datetime.datetime(2012,1,1)
            }])
    add_dataset(gdpPCVis, dataset = [{
                "y": 16,
                "x": datetime.datetime(2000,1,1)
            }, {
                "y": 200,
                "x": datetime.datetime(2002,1,1)
            }, {
                "y": 150,
                "x": datetime.datetime(2004,1,1)
            }, {
                "y": 230,
                "x": datetime.datetime(2006,1,1)
            }, {
                "y": 120,
                "x": datetime.datetime(2008,1,1)
            }, {
                "y": 110,
                "x": datetime.datetime(2010,1,1)
            },{
                "y": 150,
                "x": datetime.datetime(2012,1,1)
            }])

    employmentRateVis = add_visualisation(datasource, 'Employment Rate', employmentCategory, "line", "Year", "Percentage Employed", sizeY=2)
    add_dataset(employmentRateVis, [{
                "y": 20,
                "x": datetime.datetime(2000,1,1)
            }, {
                "y": 30,
                "x": datetime.datetime(2002,1,1)
            }, {
                "y": 50,
                "x": datetime.datetime(2004,1,1)
            }, {
                "y": 70,
                "x": datetime.datetime(2006,1,1)
            }, {
                "y": 80,
                "x": datetime.datetime(2008,1,1)
            }, {
                "y": 25,
                "x": datetime.datetime(2010,1,1)
            }])

    claimantCountVis = add_visualisation(datasource, 'Claimant Count Numbers', economyCategory, "bar", "Location", "Num of Claimants")
    add_dataset(claimantCountVis, [{
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

    housePriceVis = add_visualisation(datasource, 'House Price', housingCategory, "line", "Year", "House Prices (1000)", sizeY=2)
    add_dataset(housePriceVis, [{
                "y": 152,
                "x": datetime.datetime(2000,1,1)
            }, {
                "y": 189,
                "x": datetime.datetime(2002,1,1)
            }, {
                "y": 179,
                "x": datetime.datetime(2004,1,1)
            }, {
                "y": 199,
                "x": datetime.datetime(2006,1,1)
            }, {
                "y": 134,
                "x": datetime.datetime(2008,1,1)
            }, {
                "y": 176,
                "x": datetime.datetime(2010,1,1)
            }])
    
    #Add CSV file data
    realDataSource = add_datasource("Real Data Test", "http://example.com");
    basepath = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(basepath, "csv_processor", "static", "csv_processor", "test", "data", "test_real_monthly.csv"))
    f = File(open(filepath))
    csvFile = add_csvFile("Monthly House Pricing Sept 2015", housingCategory, realDataSource, f, "http://example.com")
    add_dimension("Dumfries and Galloway", "row", 2, 151, "currency", "£", False, csvFile, indexForLabel=1)
    add_dimension("Scotland", "row", 2, 151, "currency", "£", False, csvFile, indexForLabel=1)
    add_dimension("Month-Year", "row", 2, 151, "date", "%b-%y", True, csvFile, index=5)
    csvFile.createDashboardInfo()

    
    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "council-stock-testing.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Council Stock", economyCategory, realDataSource, f, "http://statistics.gov.scot/data/council-stock")
    add_dimension("Dumfries", "row", 3, 8, "numeric", "", False, csvFile, indexForLabel=2)
    #add_dimension("Scotland", "row", 3, 8, "numeric", "", False, csvFile, indexForLabel=2) # Does not scale well on graph at all.
    add_dimension("Year", "row", 3, 8, "date", "%Y", True, csvFile, index=8)
    csvFile.createDashboardInfo()

    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "full time employment.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Full time Employment", employmentCategory, realDataSource, f, "http://statistics.gov.scot/data/full-time-employment")
    add_dimension("Dumfries and Galloway", "row", 3, 10, "numeric", "", False, csvFile, indexForLabel=2)
    #add_dimension("Scotland", "row", 3, 8, "numeric", "", False, csvFile, indexForLabel=2) # Does not scale well on graph at all.
    add_dimension("Year", "row", 3, 10, "date", "%Y", True, csvFile, index=7)
    csvFile.createDashboardInfo()

    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "energy-consumption.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Energy Consumption", economyCategory, realDataSource, f, "http://statistics.gov.scot/data/energy-consumption")
    add_dimension("Dumfries and Galloway", "row", 3, 11, "numeric", "", False, csvFile, indexForLabel=2)
    add_dimension("Year", "row", 3, 11, "date", "%Y", True, csvFile, index=9)
    csvFile.createDashboardInfo()

    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "hospital-admissions.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Hospital Admissions", healthCategory, realDataSource, f, "http://statistics.gov.scot/data/hospital-admissions")
    add_dimension("Dumfries and Galloway", "row", 3, 13, "numeric", "", False, csvFile, indexForLabel=2)
    add_dimension("Year", "row", 3, 13, "date", "%Y", True, csvFile, index=10)
    csvFile.createDashboardInfo()

    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "neet.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Not in Education, Employment, or Training", employmentCategory, realDataSource, f, "http://statistics.gov.scot/data/neet")
    add_dimension("Dumfries and Galloway", "row", 3, 10, "numeric", "", False, csvFile, indexForLabel=2)
    add_dimension("Year", "row", 3, 10, "date", "%Y", True, csvFile, index=7)
    csvFile.createDashboardInfo()

    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "never-worked.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Never Worked", employmentCategory, realDataSource, f, "http://statistics.gov.scot/data/never-worked")
    add_dimension("Dumfries and Galloway", "row", 3, 10, "numeric", "", False, csvFile, indexForLabel=2)
    add_dimension("Year", "row", 3, 10, "date", "%Y", True, csvFile, index=8)
    csvFile.createDashboardInfo()

    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "reconvictions.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Reconvictions", crimeCategory, realDataSource, f, "http://statistics.gov.scot/data/reconvictions")
    add_dimension("Dumfries and Galloway", "row", 3, 12, "numeric", "", False, csvFile, indexForLabel=2)
    add_dimension("Year", "row", 3, 12, "date", "%Y", True, csvFile, index=9)
    csvFile.createDashboardInfo()

    realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "recorded-crime.csv" ))
    f = File(open(filepath))
    csvFile = add_csvFile("Recorded Crime", crimeCategory, realDataSource, f, "http://statistics.gov.scot/data/recorded-crime")
    add_dimension("Dumfries and Galloway", "row", 3, 19, "numeric", "", False, csvFile, indexForLabel=2)
    add_dimension("Year", "row", 3, 19, "date", "%Y", True, csvFile, index=8)
    csvFile.createDashboardInfo()

    # realDataSource = add_datasource("Scottish Government Statistics Beta", "http://statistics.gov.scot");
    # filepath = os.path.abspath(os.path.join(basepath, "dashboard", "static","dashboard","data", "employment.csv" ))
    # f = File(open(filepath))
    # csvFile = add_csvFile("Employment General", economyCategory, realDataSource, f, "http://statistics.gov.scot/data/employment")
    # add_dimension("Dumfries and Galloway", "row", 3, 31, "numeric", "", False, csvFile, indexForLabel=2)
    # add_dimension("Year", "row", 3, 31, "date", "%Y", True, csvFile, index=9)
    # csvFile.createDashboardInfo()


    # Add some test users
    add_superuser("test@test.com", "test")
    add_user("joe@test.com", "test")

def add_visualisation(dataSource, name, category, dataType, xLabel, yLabel, filename="", sizeX=2, sizeY=1):
    d = Visualisation.objects.get_or_create(dataSource=dataSource,
                                      name=name,
                                      category=category,
                                      type=dataType,
                                      sizeX=sizeX,
                                      sizeY=sizeY,
                                      xLabel=xLabel,
                                      yLabel=yLabel)[0]
    d.save()
    return d

def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c

def add_datasource(name, link):
    d = DashboardDatasource.objects.get_or_create(name=name, link=link)[0]
    return d

def add_dataset(visualisation, dataset={}, JSONdataset="", name="Dumfries And Galloway"):
    if JSONdataset == "":
        JSONdataset = json.dumps(dataset, cls=util.DatetimeEncoder);
    d = DashboardDataset.objects.get_or_create(visualisation=visualisation, name=name, dataJSON=JSONdataset)[0]
    return d

def add_user(name, password, email="test@example.com"):
    try:
        user = User.objects.get(username=name, email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(name, email, password)
    return user
    

def add_superuser(name, password):
    u = User.objects.get_or_create(username=name)[0]
    u.set_password(password)
    u.is_superuser = True
    u.is_staff = True
    u.save()
    return u

def add_csvFile(visualisationName, category, dataSource, file, source):
    c = CsvFile.objects.get_or_create(name=visualisationName,
                                      visualisationName=visualisationName,
                                      category=category,
                                      dataSource=dataSource,
                                      upload=file,
                                      source=source)[0]
    return c

def add_dimension(label, type, dataStartIndex, dataEndIndex, dataType, dataFormat, makeXaxisOnGraph, csvFile, indexForLabel=None, index=None):
    d = Dimension.objects.get_or_create(label=label,
                                        type=type,
                                        dataStartIndex=dataStartIndex,
                                        dataEndIndex=dataEndIndex,
                                        dataType=dataType,
                                        dataFormat=dataFormat,
                                        makeXaxisOnGraph=makeXaxisOnGraph,
                                        csvFile=csvFile,
                                        indexForLabel=indexForLabel,
                                        index=index)[0]
    return d



if __name__ == '__main__':
    print "Starting population script..."
    populate()



