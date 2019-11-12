import sqlite3
from sqlite3 import Error
from app.utils import randomString
from datetime import datetime, timedelta
from enum import Enum

class RequestType(Enum):
    Good = 1
    Bad = 2

def create_connection(db_file):
    ''' open connection with the db '''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn

def select_link_by_LongUrl(conn, longUrl):
    cur = conn.cursor()
    query = "SELECT * FROM urlLinks WHERE longUrl='" + longUrl + "';"
    cur.execute(query)
 
    rows = cur.fetchone()
    return rows

def select_link_by_ShortUrl(conn, shortUrl):
    cur = conn.cursor()
    query = "SELECT * FROM urlLinks WHERE shortUrl='" + shortUrl + "';"
    cur.execute(query)
 
    row = cur.fetchone()
    return row


def check_if_ShortUrl_exist(conn, shortUrl):
    cur = conn.cursor()
    query = "SELECT * FROM urlLinks WHERE shortUrl='" + shortUrl + "';"
    cur.execute(query)
 
    rows = cur.fetchall()
    if len(rows) > 0:
        return True
    else:
        return False

def insert_ShortUrl_to_db(conn, longUrl, shortUrl):
    cur = conn.cursor()
    query = "INSERT INTO urlLinks (longUrl, shortUrl) VALUES('" + longUrl + "','" + shortUrl + "');"
    cur.execute(query)

        

def count_links(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(id) FROM urlLinks;")
 
    rows = cur.fetchone()
    return rows[0]


def get_lastDay_urlRequests(conn, requestType):

    reqType ='IS NOT'
    if requestType == RequestType.Bad:
        reqType = 'IS'

    cur = conn.cursor()
    # last_time_date_time = datetime.now() - timedelta(days = 1)
    today = datetime.today()
    last_time_date_time = datetime(year=today.year, month=today.month, day=today.day, hour=0, second=0)

    lasTimeStr = last_time_date_time.strftime('%Y-%m-%d %H:%M:%S')
    query = "SELECT strftime('%H',date) AS hour, count(id) AS Amount FROM urlRequests WHERE linkId "+reqType+" NULL AND date BETWEEN '"+lasTimeStr+"' AND datetime('now', 'localtime') GROUP BY hour;"
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def get_lastHour_urlRequests(conn, requestType):

    reqType ='IS NOT'
    if requestType == RequestType.Bad:
        reqType = 'IS'

    cur = conn.cursor()
    last_time_date_time = datetime.now() - timedelta(hours = 1)
    lasTimeStr = last_time_date_time.strftime('%Y-%m-%d %H:%M:%S')
    query = "SELECT strftime('%M',date) AS minute, count(id) AS Amount FROM urlRequests WHERE linkId "+reqType+" NULL AND date BETWEEN '"+lasTimeStr+"' AND datetime('now', 'localtime') GROUP BY minute;"
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def get_lastMinute_urlRequests(conn, requestType):

    reqType ='IS NOT'
    if requestType == RequestType.Bad:
        reqType = 'IS'

    cur = conn.cursor()
    last_time_date_time = datetime.now() - timedelta(minutes = 1)
    lasTimeStr = last_time_date_time.strftime('%Y-%m-%d %H:%M:%S')
    query = "SELECT strftime('%S',date) AS second, count(id) AS Amount FROM urlRequests WHERE linkId "+reqType+" NULL AND date BETWEEN '"+lasTimeStr+"' AND datetime('now', 'localtime') GROUP BY second;"
    cur.execute(query)
    rows = cur.fetchall()
    return rows

def insert_new_urlRequest(conn, dateStr, linkId):
    cur = conn.cursor()
    query = ''
    if linkId == None:
        query = "INSERT INTO urlRequests (date) VALUES ('"+dateStr+"');"
    else:
        query = "INSERT INTO urlRequests (date,linkId) VALUES ('"+ str(dateStr) +"',"+ str(linkId) +");"
    cur.execute(query)


def getShotUrlByLongUrl(longUrl):
    database = r"ShortUrlDb"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        row = select_link_by_LongUrl(conn, longUrl)
        if row != None:
            return row[2]
        else:
            # generate new shortUrl and insert to the Db
            shortUrl =''
            while shortUrl=='':
                tempShortUrl = randomString()
                if(check_if_ShortUrl_exist(conn, tempShortUrl) == False):
                    shortUrl = tempShortUrl
            #insert to the db
            insert_ShortUrl_to_db(conn,longUrl,shortUrl)
            return shortUrl

def getLongUrlByShortUrl(shortUrl):
    database = r"ShortUrlDb"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        row = select_link_by_ShortUrl(conn, shortUrl)
        if row != None:
            return row[1]
        else:
            return None

def getLinkEntityByShortUrl(shortUrl):
    database = r"ShortUrlDb"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        row = select_link_by_ShortUrl(conn, shortUrl)
        return row


def getDbStatistics():
    database = r"ShortUrlDb"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        redirectionsCount = count_links(conn)
        lastDayRequestsGood = get_lastDay_urlRequests(conn, RequestType.Good)
        lastHourRequestsGood = get_lastHour_urlRequests(conn, RequestType.Good)
        lastMinuteRequestsGood = get_lastMinute_urlRequests(conn, RequestType.Good)

        lastDayRequestsBad = get_lastDay_urlRequests(conn, RequestType.Bad)
        lastHourRequestsBad = get_lastHour_urlRequests(conn, RequestType.Bad)
        lastMinuteRequestsBad = get_lastMinute_urlRequests(conn, RequestType.Bad)

        statistics = {
            "redirectionsCount": redirectionsCount,
            "lastDayRequestsGood": lastDayRequestsGood,
            "lastHourRequestsGood": lastHourRequestsGood,
            "lastMinuteRequestsGood": lastMinuteRequestsGood,
            "lastDayRequestsBad": lastDayRequestsBad,
            "lastHourRequestsBad": lastHourRequestsBad,
            "lastMinuteRequestsBad": lastMinuteRequestsBad
        }
        return statistics


def addUrlRequest(linkId):
    database = r"ShortUrlDb"
    currentDateStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # create a database connection
    conn = create_connection(database)
    with conn:
        insert_new_urlRequest(conn,currentDateStr,linkId)
        
            

