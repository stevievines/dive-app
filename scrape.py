



def scrapeMeetInfo(meetInfoPage):
	'''
		Scrapes Meet information with the specified meet number
        https://secure.meetcontrol.com/divemeets/system/meetinfoext.php?meetnum=<meetNumber>
		Returns a dictionary with start_date, end_date, name, type, rules, sponsor, pool, dmId
        
        :param meetNumber:  Divemeets Meet number
	'''
    start_date = 111
    end_date = 111
    name = 111
    type = 111
    rules = 111
    sponsor = 111
    pool = 111
    divemeets_id = 111
    
    return {'start_date':start_date, 'end_date':end_date, 'name':name, 
            'type':type, 'rules':rules, 'sponsor':sponsor, 'pool':pool, 'divemeets_id':divemeets_id}
    
    
    pass


def scrapeEvent(meetInfo,eventPage)
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
    
    meet = meetInfo.get('divemeets_id', 'ERROR')
    event_date = 1111
    rules = meetInfo.get('rules', 'ERROR')
    
    first_divesheet = {}
    num_dives = 11111
    num_scores = 11111
    num_judges = 11111
    num_scores_kept = 1111
    board = 11111
    individual = 11111
    format = 11111
    iscompleted = 111111
    
    event = {'meet':meet, 'event_date':event_date, 'rules':rules, 'num_dives':num_dives, 'num_scores':num_scores, 
             'num_judges':num_judges, 'num_scores_kept':num_scores_kept, 'board':board, 'individual':individual,
             'format':format, 'isCompleted':isCompleted}
    
    pass
    
def scrapeDiverInfo(diverInfoPage):
    '''
        Scrapes diver info
        
        returns dictionary: 	- Name	- City/state	- Country	- Gender	- Birthday	- Divemeets #id	- Photo
    
    '''
    
    pass
    
def scrapeDiveSheet(diveSheetPage):
    '''
        Scrapes the dive sheet of a diver
        
    '''
    
    
def scrapeDiveScores(diveScorePage):
    '''
        Scrapes dive score page
        
        
    '''

    
def scrapeJudgeInfo(judgeInfoPage):
    '''
        Scrapes information for a judge
    
    '''
    


    
