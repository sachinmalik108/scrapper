from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from datetime import datetime
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import time
df = pd.DataFrame()
df3 = pd.DataFrame()
scorecarddf = pd.DataFrame()
driver = webdriver.Chrome()
i = 1
driver.get("https://crex.live/fixtures/match-list")

format = "%b %d, %Y, %I:%M:%S %p"

def getelement(elements,index):
    t = 0
    for element in elements:
        values = element.find_element(By.CSS_SELECTOR,".d-flex.justify-content-center.align-item-center")
        if(t == index):
           return values
        else:
            t= t+1
   
def get_players(players):
    playernames = ''
    for player in players:
        playernames = playernames +  player.find_element(By.CLASS_NAME,"profile").text + ' ,'

    return playernames       
         
def check_exists(classname , element):
    try:
        classname.find_element(By.CLASS_NAME,element)
    except NoSuchElementException:
        return False
    return True
def check_existsforcss(classname , element):
    try:
        classname.find_element(By.CSS_SELECTOR,element)
    except NoSuchElementException:
        return False
    return True

def check_existstag(classname):
    if (len(classname) == 0):
        return False
    else:
     return True
while True:
    time.sleep(2)
    # execute the scraper function
    matches = driver.find_elements(By.CLASS_NAME, "match-card-container")
    
    
    
    
    for match in matches:
     team1info = match.find_element(By.CLASS_NAME,"team-wrapper")
     team1Name = team1info.find_element(By.CLASS_NAME,"team-name")

     check = check_exists(team1info,'team-score')
     if check:

       team1score = team1info.find_element(By.CLASS_NAME,"team-score").text
     else:
         team1score = '--'
     check = check_exists(team1info,'total-overs')
     if (check):
          team1overs = team1info.find_element(By.CLASS_NAME,"total-overs").text
     else:
         team1overs = '--'
    # team 2 info   
     team2info = match.find_element(By.CSS_SELECTOR,".team-wrapper.right-team-name")
     team2Name = team2info.find_element(By.CLASS_NAME,"team-name")
     check = check_exists(team2info,'team-score')
     if check:

       team2score = team2info.find_element(By.CLASS_NAME,"team-score").text
     else:
        team2score = '--'
    
     check = check_exists(team2info,'total-overs')
     if (check):
         team2overs = team2info.find_element(By.CLASS_NAME,"total-overs").text
     else:
         team2overs = '--'
    
     
     hrf = match.find_element(By.CLASS_NAME , "match-card-wrapper")
     ahrfvalue = hrf.get_attribute("href")
     ahrfvalue = ahrfvalue[:ahrfvalue.rfind('/')] + "/info"
     df2 = pd.DataFrame({'Team 1': [team1Name.text], 'Team2': [team2Name.text],   'score team 1'  :  [team1score] , 'score team 2'  :  team2score ,'overs team 1'  :  [team1overs] ,'overs team 2'  :  [team2overs] , 'link' : [ahrfvalue] })
     df = pd.concat([df,df2])
    
    try:
        # find and click the next page link
        next_page_link = driver.find_element(By.CLASS_NAME, "next-button")
      
        
        if next_page_link.is_enabled():
            driver.execute_script("arguments[0].click();", next_page_link)
            
            
        else:
            break;    
    except NoSuchElementException:
        print("No more pages available")
        break
     
    


count = df[df.columns[0]].count()
p = 0
while(p < count):
      ahrfvalue = df['link'].values[p]
      
      try:
        driver.get(ahrfvalue)
        time.sleep(2)
        Matchinfo = driver.find_element(By.CLASS_NAME, "match-detail-route-wrap")
        
        check = check_exists(Matchinfo,'s-name')
        if (check):
         series_name = Matchinfo.find_element(By.CLASS_NAME,"s-name").text
        else:
         series_name = '--'
         

        check = check_exists(Matchinfo,'s-format')
        if (check):
          Match_No = Matchinfo.find_element(By.CLASS_NAME,"s-format").text
        else:
         Match_No = '--'


        check = check_exists(Matchinfo,'match-date')
        if (check):
          Match_date = Matchinfo.find_element(By.CLASS_NAME,"match-date").text
        else:
         Match_date = '--'

        
        check = check_existsforcss(Matchinfo,'.flex.align-center')
        if (check):
         Last_5_matches = Matchinfo.find_elements(By.CSS_SELECTOR,".flex.align-center")
         Last_5_matches1 = Last_5_matches[0].text
         if(len(Last_5_matches)== 2):
            Last_5_matches2 = Last_5_matches[1].text
         else:
            Last_5_matches2 = '--'
        else:
         Last_5_matches1 = '--'
         Last_5_matches2 = '--'
        
        

        check = check_exists(Matchinfo,'team1-wins')
        if (check):
         Team_1_wins = Matchinfo.find_element(By.CLASS_NAME,"team1-wins").text
        else:
         Team_1_wins = '--'

        
        check = check_exists(Matchinfo,'team2-wins')
        if (check):
         Team_2_wins = Matchinfo.find_element(By.CLASS_NAME,"team2-wins").text
        else:
         Team_2_wins = '--'

        check = check_exists(Matchinfo,'match-count')
        if (check):
         Match_venue_count = Matchinfo.find_element(By.CLASS_NAME,"match-count").text
        else:
         Match_venue_count = '--'
        

        
        
        check = check_existsforcss(Matchinfo,'.match-win-per.low-score-color')
        if (check):
         Batting_second = Matchinfo.find_element(By.CSS_SELECTOR,".match-win-per.low-score-color").text
        else:
         Batting_second = '--'



        check = check_exists(Matchinfo,'match-win-per')
        if (check):
         Batting_first = Matchinfo.find_element(By.CLASS_NAME,"match-win-per").text
        else:
         Batting_first = '--'

        
        check = check_exists(Matchinfo,'playingxi-card-row')
        if (check):
         Team_1_players = Matchinfo.find_elements(By.CLASS_NAME,"playingxi-card-row")
         team1players = get_players(Team_1_players)
         
        else:
         team1players = '--'
        

        check = check_exists(Matchinfo,'umpire-val')
        if (check):
          Umpires = Matchinfo.find_elements(By.CLASS_NAME,"umpire-val")
          field_Umpire = Umpires[0].text
          Third_Umpire = Umpires[1].text
          Refree = Umpires[2].text
        else:
           field_Umpire = '--'
           Third_Umpire  = '--'
           Refree = '--'



        check = check_exists(Matchinfo,'wicket-count')
        if (check):
         wicket_on_ground = Matchinfo.find_elements(By.CLASS_NAME,"wicket-count")
         wicket_on_groundpace = wicket_on_ground[0].text
         wicket_on_groundspin = wicket_on_ground[1].text
        else:
         wicket_on_groundpace ='-'
         wicket_on_groundspin = '-'
        
        
        
        check = check_exists(Matchinfo,'playingxi-button')
        if (check):
          button = Matchinfo.find_elements(By.CLASS_NAME, "playingxi-button")
          driver.execute_script("arguments[0].click();", button[1])
    
        check = check_exists(Matchinfo,'playingxi-card-row')
        if (check):
         Team_2_players = Matchinfo.find_elements(By.CLASS_NAME,"playingxi-card-row")
         team2players = get_players(Team_2_players)
        else:
         team2players = '--'
        p = p + 1
        df2 = pd.DataFrame({'team 1 squad': [team1players], 'series name': [series_name], 
                              'match no'  :  [Match_No],'match date'  :  [Match_date] , 
                            'team 1 wins'  :  [Team_1_wins] ,'team 2 wins'  :  [Team_2_wins] ,
                            'match venue'  :  [Match_venue_count] , 'Batting_first wins' : [Batting_first],
                          'Batting_second wins': [Batting_second], 'team 2 squad': [team2players],
                           'last 5 matches team 1': [Last_5_matches1],'last 5 matches team 2': [Last_5_matches2],
                             'Pace wicket on ground':[wicket_on_groundpace]  ,  'spin wicket on ground': [wicket_on_groundspin]  ,
                               'On field Umpire':[field_Umpire] ,  'Third Umpire':   [Third_Umpire]   ,  'Refree':     [Refree]        })
        df3 = pd.concat([df3,df2])
        
      except NoSuchElementException:
           
           print("No more element available")
           df2 = pd.DataFrame({'team 1 squad':['--'], 'series name': ['--'], 
                              'match no'  :  ['--'],'match date'  :  ['--'] , 
                            'team 1 wins'  :  ['--'] ,'team 2 wins'  :  ['--'] ,
                            'match venue'  :  ['--'] , 'Batting_first wins' : ['--'],
                          'Batting_second wins': ['--'], 'team 2 squad': ['--'],
                           'last 5 matches team 1': ['--'],'last 5 matches team 2': ['--'],
                             'Pace wicket on ground':['--']  ,  'spin wicket on ground': ['--']  ,
                               'On field Umpire':['--'] ,  'Third Umpire':   ['--']
                                ,  'Refree':   ['--']       })
           df3 = pd.concat([df3,df2])

           p = p + 1
           break
df = pd.concat([df, df3], axis=1)
print(df)
# df.to_csv('match_schdule.csv' , encoding='utf-16')

count  = df[df.columns[0]].count()  
 
p = 0
while (p < count):
 dateget = df['match date'].values[p]
 while(dateget == '--'):
    p = p+1
    dateget = df['match date'].values[p]
 print(dateget)
 dateget = df['match date'].values[p]
 datetime_str = datetime.strptime(dateget, format)
       
 if datetime.today() > datetime_str:
    ahrfvalue = df['link' ].values[p]
    ahrfvalue = ahrfvalue[:ahrfvalue.rfind('/')] + "/scorecard"
    print(ahrfvalue)
    driver.get(ahrfvalue)
    time.sleep(2)
    matchdetails = driver.find_element(By.CLASS_NAME, "match-detail-route-wrap")
    Livewrapper = driver.find_element(By.CSS_SELECTOR, ".d-md-none.lcp-element-match")
    check = check_exists(matchdetails,'team-details')
    if(check):
        button = matchdetails.find_elements(By.CLASS_NAME, "team-details")
        driver.execute_script("arguments[0].click();", button[0])
        Scorecard1 = matchdetails.find_elements(By.TAG_NAME, "tbody")
        Heading1 = matchdetails.find_elements(By.TAG_NAME, "h3")
        Inning1team =  matchdetails.find_elements(By.CLASS_NAME, "team-name")
        partnership1st = matchdetails.find_elements(By.CLASS_NAME, "p-section-wrapper") 
        team1names = button[0].text
        if(check_existstag(Scorecard1)):
          batting1st_scorecard = Scorecard1[0].text
          bowling1st_scorecard = Scorecard1[1].text
        else:
           batting1st_scorecard = '--'
           bowling1st_scorecard = '--'
        if(len(Scorecard1) == 3):
          
           fallofwicket1 = Scorecard1[2].text
        
        else:
           
           fallofwicket1 = '--'
        
    else:
        team1names = '--'
        fallofwicket1 = '--'
        batting1st_scorecard = '--'
        bowling1st_scorecard = '--'
        partnership1st = '--'
    if(check):
        button = matchdetails.find_elements(By.CLASS_NAME, "team-details")
        if(len(button) == 2):
          driver.execute_script("arguments[0].click();", button[1])
          Scorecard2 = matchdetails.find_elements(By.TAG_NAME, "tbody")
          Heading2 = matchdetails.find_elements(By.TAG_NAME, "h3")
          partnership2st = matchdetails.find_elements(By.CLASS_NAME, "p-section-wrapper") 
          Inning2team =  matchdetails.find_elements(By.CLASS_NAME, "team-name")  
          team2names = '--'
          team2names = button[1].text

          if(check_existstag(Scorecard2)):
             
            batting2st_scorecard = Scorecard2[0].text
            bowling2st_scorecard = Scorecard2[1].text
          else:
              batting2st_scorecard = '--'
              bowling2st_scorecard = '--'
          if(len(Scorecard2)== 3):
             
             fallofwicket2 = Scorecard2[2].text
          
          else:
             fallofwicket2  = '--'
        else:
           team2names = '--'
           batting2st_scorecard = '--'
           bowling2st_scorecard = '--'
           partnership2st = '--'
           fallofwicket2 = '--'
    df2 = pd.DataFrame({'team 1 name score': [team1names],'team 2 name score': [team2names],  
                              'batting 1 scorecard'  :  [batting1st_scorecard],'batting 2 scorecard'  :  [batting2st_scorecard] , 
                            'bowling 1 scorecard'  :  [bowling1st_scorecard] ,'bowling 2 scorecard'  :  [bowling2st_scorecard] ,
                            'partnership 1st inning'  :  [partnership1st] , 'partnership 2nd' : [partnership2st],
                             'fall of wicket 1st inning'  :  [fallofwicket1] , 'fall of wicket 2nd' : [fallofwicket2] })
    scorecarddf = pd.concat([scorecarddf,df2])
    p = p+1
    

 else:
  break
  
scorecarddf.to_csv('scorecard.csv' , encoding='utf-16')
df.to_csv('match_schdule.csv' , encoding='utf-16')


#  code for automation 



driver.close()



