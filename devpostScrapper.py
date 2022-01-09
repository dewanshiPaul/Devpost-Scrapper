#imports
import requests
import pandas

class devpost:
    def __init__(self):
        self.pageNo = 1
        self.totalPage = 0

    def setUrlForEachPage(self):
        return 'https://devpost.com/api/hackathons?page={}&status[]=upcoming&status[]=open'.format(self.pageNo)

    def makeRequest(self):
        urlRecieve = self.setUrlForEachPage()
        return requests.get(urlRecieve)

    def getJson(self):
        self.data = self.makeRequest().json()
    
    def numberOfEvents(self):
        self.getJson()
        totalEvents = self.data['meta']['total_count']
        eventsShowPerPage = self.data['meta']['per_page']
        self.totalPage = totalEvents//eventsShowPerPage if totalEvents%eventsShowPerPage == 0 else totalEvents//eventsShowPerPage+1
        

    def extractData(self):
        #declarations of lists
        self.eventTitle = []
        self.eventDate = []
        self.eventTimeLeft = []
        self.eventLocation = []
        self.eventState = []
        self.eventOrganizationName = []
        self.eventTheme = []
        self.eventRegisteredCount = []
        self.eventUrl = []
        
        while (self.pageNo<self.totalPage+1):
            self.getJson()
            for events in self.data['hackathons']:
                self.eventTitle.append(events['title'])
                self.eventState.append(events['open_state'])
                self.eventDate.append(events['submission_period_dates'])
                self.eventTimeLeft.append(events['time_left_to_submission'])
                self.eventLocation.append(events['displayed_location']['location'])
                self.eventRegisteredCount.append(events['registrations_count'])
                self.eventUrl.append(events['url'])
                self.eventOrganizationName.append(events['organization_name'])
                themeTitle = []
                for theme in events['themes']:
                    themeTitle.append(theme['name'])
                self.eventTheme.append(themeTitle)  
            print("Page completed read....{}".format(self.pageNo))    
            self.pageNo += 1  

            

        
    def dataToCsv(self):
        tableData = pandas.DataFrame(self.eventTitle,columns=['Name'])
        tableData['Location'] = self.eventLocation
        tableData['Event State'] = self.eventState
        tableData['Event Duration'] = self.eventDate
        tableData['Time Left'] = self.eventTimeLeft
        tableData['Theme'] = self.eventTheme
        tableData['Registered Count'] = self.eventRegisteredCount
        tableData['Event hosted by'] = self.eventOrganizationName
        tableData['Event URL'] = self.eventUrl

        tableData.to_csv('DevpostHackathondata.csv',index=False)
    
devpostScrap = devpost()
devpostScrap.numberOfEvents()
devpostScrap.extractData()
devpostScrap.dataToCsv()