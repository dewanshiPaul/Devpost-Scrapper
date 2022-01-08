#imports
import requests
import pandas as pd

#function to change url as per page number
def multiplePages(url,pageNo):
    return 'https://devpost.com/api/hackathons?page={}&status[]=upcoming&status[]=open'.format(pageNo)

url = 'https://devpost.com/api/hackathons?page=0&status[]=upcoming&status[]=open'

request = requests.get(url)

hackathons = request.json()
events = hackathons['meta']

#calculation of number of pages present
totalEvents = events['total_count']
eventsShownPerPage = events['per_page'] 
pages = totalEvents//eventsShownPerPage if totalEvents%eventsShownPerPage == 0 else (totalEvents//eventsShownPerPage)+1

#data to stores
eventTitle = []
eventDate = []
eventTimeLeft = []
eventLocation = []
eventState = []
eventOrganizationName = []
eventTheme = []
eventRegisteredCount = []
eventUrl = []

#extracting hackathon detials for all available images
for eachPage in range(0,pages+1):
    setUrl = multiplePages(url,eachPage)
    request= requests.get(setUrl)
    hackathons = request.json()
    hackathonDetails = hackathons['hackathons']
    for events in hackathonDetails:
        hackathonTitle = events['title']
        state = events['open_state']
        dates = events['submission_period_dates']
        timeLeft = events['time_left_to_submission']
        location = events['displayed_location']['location']
        themes = events['themes']
        themeList = []
        for theme in themes:
            themeList.append(theme['name'])
        registeredCount = events['registrations_count']    
        Url = events['url']
        eventTheme.append(themeList)    
        eventTitle.append(hackathonTitle)
        eventState.append(state)
        eventLocation.append(location)
        eventDate.append(dates)
        eventTimeLeft.append(timeLeft)
        eventRegisteredCount.append(registeredCount)
        eventUrl.append(Url)
        
#dataframe
df = pd.DataFrame(eventTitle,columns=['Event Title'])
df['Location'] = eventLocation
df['Event State'] = eventState
df['Event Duration'] = eventDate
df['Time Left'] = eventTimeLeft
df['Registered Count'] = eventRegisteredCount
df['Theme'] = eventTheme
df['Event URL'] = eventUrl

df.to_csv('data.csv',index=False)
