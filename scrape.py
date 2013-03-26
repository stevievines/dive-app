from bs4 import BeautifulSoup
import bs4
import requests
import  pprint, re, logging,  datetime, Queue, threading, copy, json
divers = {}
coaches = {}
dives = {}
    
    
# setup logger
logging.basicConfig(filename='scraper.log',level=logging.DEBUG)
logging.info("Log of scraper at time %s", datetime.date.today())

    
    
# thread class 
class FunctionThread(threading.Thread):
    ''' Execute blocks of code using threads, pushes return of function to results queue '''
    def __init__(self, todo, results):
        threading.Thread.__init__(self)
        self.todo = todo
        self.results = results
    
    def run(self):
        while not self.todo.empty():
            # function to run
            f = self.todo.get()
            
            # runs function
            self.results.put(f())
            
            self.todo.task_done()
            
            
    
def scrapeMeet(meetnum, thread=True):
    
    meetinfo = scrapeMeetInfo(meetnum)
    meet_root = "https://secure.meetcontrol.com/divemeets/system/meetresultsext.php?meetnum="
    soup = BeautifulSoup(requests.get(meet_root + str(meetnum)).text)
    
    # pull all events for the meet
    events_links = soup.find('td', text="Events").parent.findNext('tr').findAllNext('tr')[:-2]
    
    events = []
    todo = Queue.Queue()
    
    for tr in events_links:
        def f(c):
            # creates a closure so can pass function with c instantiated
            def g():
                d = {}
                #c = tr.contents
                try:
                    d['event_name'] = c[0].text
                   
                    link = c[0].contents[0].attrs.get('href')
                    
                    search = re.search('.*eventnum=(\d*)&eventtype=(\d*)', link)
                    d['eventnum'] = search.group(1)
                    d['eventtype'] = search.group(2)
                    d['event_data'] = scrapeEvent(meetnum, d['eventnum'], d['eventtype'], thread=thread)
                    
                    
                    logging.info("Scraped Event %s", d['eventnum'])
                    return d
                except:
                    logging.warning("Could not scrape diver with text")
            return g
        
        if tr.contents[0].attrs.get('colspan') == "4":
            break
        if not thread:
            events.append(f(tr.contents)())
            break
        else:
            g = f(tr.contents)
            
            todo.put(g)

    # if running threads, create threads and go!
    if thread:
        events = startThreads(todo, 4)
    
    return {'meetnum':meetnum, 'meetinfo':meetinfo, 'events':events}
    


def scrapeMeetInfo(meetnum):
    '''
        Scrapes Meet information with the specified meet number
        https://secure.meetcontrol.com/divemeets/system/meetinfoext.php?meetnum=<meetnum>
        Returns a dictionary with start_date, end_date, name, type, rules, sponsor, pool, dmId
        
        :param meetnum:  Divemeets Meet number
    '''
    
    meetInfoRoot = "https://secure.meetcontrol.com/divemeets/system/meetinfoext.php?meetnum=" + str(meetnum) + "#"
    soup = BeautifulSoup(requests.get(meetInfoRoot).text)
  
    try:
        d = {}
        d['name'] = soup.find('td', text=re.compile("Name:")).next.next.next.text
        d['start_date'] = soup.find('td', text=re.compile("Start Date:")).next.next.next.text
        d['end_date'] = soup.find('td', text=re.compile("End date:")).next.next.next.text
        d['rules']= soup.find('td', text=re.compile("Rules:")).next.next.next.text
        d['sponsor'] = soup.find('td', text=re.compile("Sponsor:")).next.next.next.text
        d['pool'] = soup.find('td', text=re.compile("Pool:")).next.next.next.text
        logging.info("Processed meetinfo %s", meetnum)
        
        return d
    except:
        logging.warning("Error processing meetinfo # %s, website %s", meetnum, meetInfoRoot)
    

def startThreads(todo, nThreads):
    ''' General method to start threads given queue of tasks and number threads '''
    results = Queue.Queue()
    for i in range(nThreads):
        t = FunctionThread(todo, results)
        t.setDaemon(True)
        t.start()
    todo.join()

    divers = []
    while not results.empty():
        divers.append(results.get())
    
    return divers


def scrapeEvent(meetnum, eventnum, eventtype, thread=False):
    ''' 
        Scrapes an event
        https://secure.meetcontrol.com/divemeets/system/eventresultsext.php?meetnum=2017&eventnum=180&eventtype=9
        Meet (from meetInfo),
        Rules (from meetInfo),
        
        Date (from eventPage),
        Age-group (from eventPage),
        Board (eventPage)
        
        Number of dives (from a sheet),
        Number of scores (from a sheet)
        
        Number of judges (sheet -> dive)
        Number of scores kept (sheet -> dive)
        
        Individual? (?????????????????????????)
        Format (11-dive, 6-dive, other) (sheet?)
        is completed (eventPage)
            
        
    '''
    
    event_link = 'https://secure.meetcontrol.com/divemeets/system/eventresultsext.php?meetnum='+str(meetnum)+'&eventnum='+str(eventnum)+'&eventtype='+str(eventtype)
    soup = BeautifulSoup(requests.get(event_link).text)
    
    # find all divers in event
    divers_links = soup.find('td', text="Diver").parent.findNext('tr').findAllNext('tr')[:-1]
    divers = []
    
    todo = Queue.Queue()
    
    for tr in divers_links:
        def f(c):
            # creates a closure so can pass function with c instantiated
            def g():
                d = {}
                #c = tr.contents
                try:
                    d['diver']= c[0].text
                    d['diver_id'] = re.search('.*=(.*)', c[0].contents[0].attrs.get('href')).group(1)
                    
                    d['team'] =  c[1].text
                    d['team_id'] = re.search('.*=(.*)', c[1].contents[0].attrs.get('href')).group(1)
                    
                    d['place'] = c[2].text
                    d['score'] = c[3].text
                    d['sheet'] = scrapeDiveSheet(meetnum, eventnum, d['diver_id'], eventtype, thread=thread)
                    d['diff'] = c[4].text
                    
                    logging.info("Scraped Diver %s event: %s" %(d['diver'], eventnum))
                    return d
                except Exception as e:
                    logging.warning("Could not scrape diver with exception %s, and address %s", e, event_link)
            return g
        
        if not thread:
            divers.append(f(tr.contents)())
        else:
            g = f(tr.contents)
            todo.put(g)
            #print c
            #todo.put(lambda : f(c))

    # if running threads, create threads and go!
    if thread:
        divers = startThreads(todo, 5)
    
    return {'divers':divers}
    
    
def scrapeDiveSheet(meetnum, eventnum, dvrnum, eventtype, thread = True):
    '''
        Scrapes the dive sheet of a diver
        returns a list of dive dictionaries
        {'dive number', 'competed_dd', 'dive_position', 
         'dive_name', 'scores', 'net_total', 'dm_net_total', 
         'dm_total', 'dm_total', 'isScored', 'list_order', 'isBalk', 'isFailed'}

    '''
    
    dv_root = "https://secure.meetcontrol.com/divemeets/system/"
    dv_sheet_page = "https://secure.meetcontrol.com/divemeets/system/divesheetresultsext.php?meetnum="+str(meetnum)+"&eventnum="+str(eventnum)+"&dvrnum="+str(dvrnum)+"&eventtype="+str(eventtype)
    soup = BeautifulSoup(requests.get(dv_sheet_page).text)
    place = soup.find(text="Place: ").parent.contents[1].text
    dives = []
    trs = soup.findAll('tr', {"bgcolor":"dddddd"})
    
    # queue for threads
    todo = Queue.Queue()
    
    # scrape dive sheets
    for tr in trs:
        def f(tr):
            def g():
                try:
                    d = {}
                    d['dive_order']= tr.contents[0].text
                    d['dive_number'] = tr.contents[1].text
                    d['height'] = tr.contents[2].text
                    d['description'] = tr.contents[3].text
                    d['net_score'] = tr.contents[4].text
                    d['competed_dd'] = tr.contents[5].text
                    d['score'] = tr.contents[6].text
                    d['score_link'] = tr.contents[6].contents[0].attrs.get('href')
                    if int(d['dive_order']) != 0:
                        d['scores'] = scrapeDiveScores(meetnum, eventnum, dvrnum, d['dive_order'], eventtype, thread=thread)
                    
                    d['round_place'] = tr.contents[7].text
                    return d
                except:
                    logging.warning("Had a problem scraping divesheet %s", dv_sheet_page)
            return g
        
        if not thread:
            dives.append(f(tr)())
        else:
            g = f(tr)
            todo.put(g)
    
    if thread:
        dives = startThreads(todo, 6)
    
        
                
    return {'dives':dives, 'place':place}
    
def scrapeDiveScores(meetnum, eventnum, dvrnum, divord, eventtype, thread=False):
    '''
        :param competedDive:  foreign key to competedDive???
        Scrapes dive score page
        - Judge (fk to coach)
        - Value
        - Dropped (boolean)
        - Competed Dive (fk to competed dive)
            
    '''
    def isDropped(color):
        '''
        Something about the color of the score
        '''
        return color == "red" or color == "navy"

    
    #judge = scrapeJudgeInfo(SOMETHING)
    #value = 1111
    #dropped = isDropped(SOMETHING)
    #competed_dive = 1111
    
    
    jg_info_pg = "https://secure.meetcontrol.com/divemeets/system/judgesscoresext.php?meetnum=" +str(meetnum)+"&eventnum="+str(eventnum)+"&dvrnum="+str(dvrnum)+"&divord="+str(divord)+"&eventtype="+str(eventtype)
    
    soup = BeautifulSoup(requests.get(jg_info_pg).text)
    
    dives = soup.find('td',text=re.compile("Judge")).parent.findAllNext('tr')[1:-4]
    
    scores = []
    todo = Queue.Queue()
    for tr in dives:
        #pprint.pprint(tr)
        def f(tr):
        
            def g():
                try:
                    cols = tr.findAll('td')
                    # should only be 3 columns Judge Num | Judge | Net Score
                    d = {}
                    d['judge_num'] = cols[0].text
                    d['judge_name'] = cols[1].text
                    d['judge_id'] = re.search(".*number=(.*)", cols[1].contents[0].attrs.get('href')).groups()[0]
                    d['score'] = cols[2].text
                    d['color'] = re.search(".*color:(.*)", cols[2].attrs.get('style')).groups()[0]
                    d['dropped'] = isDropped(d['color'])
                    return d
                except:
                    logging.warning("Error with scraping divesheet %s", jg_info_pg)
            return g
            
        
        if not thread:
            scores.append(f(tr)())
        else:
            g = f(tr)
            todo.put(g)
    if thread:
        scores = startThreads(todo, 5)
    
    return scores
    
def scrapeTeam(soup):
    team_info = []
    current = soup.find(text=re.compile("Teams"))
    while True:
        if type(current) is bs4.element.Tag:
            if current.name == "table":
                break
        team_info.append(current)
        current = current.next
    
    return team_info
   
    
def scrapeDiverInfo(diverNum):
    '''
        Scrapes diver info
        
        returns dictionary:     - Name    - City/state    - Country    - Gender    - Birthday    - Divemeets #id    - Photo
    
    '''
    diver_link = "https://secure.meetcontrol.com/divemeets/system/profile.php?number=" + str(diverNum)
    text = re.sub('<br>', ' ', requests.get(diver_link).text)
    text = re.sub('<br/>', ' ',text)
    
    soup = BeautifulSoup(text)
    
    try:
        d = {}
        d['name'] = soup.find(text=re.compile("Name:")).next
        d['city_state'] = soup.find(text=re.compile("City/State:")).next
        d['country'] = soup.find(text=re.compile("Country:")).next
        d['gender'] = soup.find(text=re.compile("Gender:")).next
        d['divemeets_id'] = soup.find(text=re.compile("DiveMeets #:")).next
        d['teams'] = scrapeTeam(soup)
        d['age'] = soup.find(text=re.compile("Age:")).next
        d['fina_age'] = soup.find(text=re.compile("FINA Age:")).next
        d['hs_grad'] = soup.find(text=re.compile("High School Graduation:")).next
        
        logging.info("Processed diver %d", diverNum)
        return d
    except:
        logging.warning("Error processing diver %d, page %s", diverNum, diver_link)
        
    
def scrapeJudgeInfo(judge_num):
    '''
        Scrapes information for a judge
        
            - Name
            - City/State
            - Country
            - Gender
            - Divemeets id
        
    '''
    judge_link = "https://secure.meetcontrol.com/divemeets/system/profilej.php?number=" + str(judge_num)
    text = re.sub('<br>', ' ', requests.get(judge_link).text)
    text = re.sub('<br/>', ' ',text)
    
    soup = BeautifulSoup(text)
    
    
    try:
        d = {}
        d['name'] = soup.find(text=re.compile("Name:")).next
        d['city_state'] = soup.find(text=re.compile("City/State:")).next
        d['country'] = soup.find(text=re.compile("Country:")).next
        d['gender'] = soup.find(text=re.compile("Gender:")).next
        d['divemeets_id'] = soup.find(text=re.compile("DiveMeets #:")).next
        d['teams'] = scrapeTeam(soup)
        
        logging.info("Processed judge %d", judge_num)
        return d
    except:
        logging.warning("Error processing judge %d", judge_num)
        

def test_scrapeDiveSheet(): 
    ''' 
    Test scraping judge, using my zones a 1m first dive 
    https://secure.meetcontrol.com/divemeets/system/judgesscoresext.php?meetnum=2386&eventnum=7180&dvrnum=13689&divord=1&eventtype=9
    '''
    
    
    meetnum = 2386
    eventnum = 7180
    dvrnum = 13689
    eventtype = 9
    
    result = scrapeDiveSheet(meetnum, eventnum, dvrnum, eventtype, thread=True)
    pprint.pprint(result)
    
def test_scrapeDiveScores():
    ''' 
    Test scraping judge, using my zones a 1m first dive 
    https://secure.meetcontrol.com/divemeets/system/judgesscoresext.php?meetnum=2386&eventnum=7180&dvrnum=13689&divord=1&eventtype=9
    '''
    
    
    meetnum = 2386
    eventnum = 7180
    dvrnum = 13689
    divord = 1
    eventtype = 9
    
    scores = scrapeDiveScores(meetnum, eventnum, dvrnum, divord, eventtype)
    pprint.pprint(scores)
    
def test_scrapeEvent():
    ''' 
    Test scraping judge, using my zones a 1m first dive 
    https://secure.meetcontrol.com/divemeets/system/judgesscoresext.php?meetnum=2386&eventnum=7180&dvrnum=13689&divord=1&eventtype=9
    '''
    meetnum = 2386
    eventnum = 7180
    dvrnum = 13689
    divord = 1
    eventtype = 9
    
    event = scrapeEvent(meetnum, eventnum, eventtype, thread=True)
    pprint.pprint(event)
   
def test_scrapeMeetInfo():   
    meetnum = 2386
    meetinfo = scrapeMeetInfo(meetnum)
    pprint.pprint(meetinfo)
    
def test_scrapeJudgeInfo():
    judge_num = 20098
    judge = scrapeJudgeInfo(judge_num)
    pprint.pprint(judge)
    
def test_scrapeDiverInfo():
    diver_num = 13689
    judge = scrapeDiverInfo(diver_num)
    pprint.pprint(judge)

    
def test_scrapeMeet():
    meetnum = 2386
    meet = scrapeMeet(meetnum, thread=True)
    json.dump(meet, open('test_meet.json', 'w'))
    pprint.pprint(meet)
    
test_scrapeMeet()