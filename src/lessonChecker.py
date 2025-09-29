from requests import get
from bs4 import BeautifulSoup
import json
import sys

from request_manager import RequestManager
from token_fetcher import TokenFetcher

COURSE_SELECTION_URL = "https://obs.itu.edu.tr/api/ders-kayit/v21/"
COURSE_TIME_CHECK_URL = "https://obs.itu.edu.tr/api/ogrenci/Takvim/KayitZamaniKontrolu"
TARGET_URL = "https://obs.itu.edu.tr/ogrenci/DersKayitIslemleri/DersKayit"
ITU_HELPER_LESSONS_URL = "https://raw.githubusercontent.com/itu-helper/data/main/lessons.psv"
ITU_HELPER_COURSES_URL = "https://raw.githubusercontent.com/itu-helper/data/main/courses.psv"
ITU_LISANS_BRANS_KODU_ID_URL = "https://obs.itu.edu.tr/public/DersProgram/SearchBransKoduByProgramSeviye?programSeviyeTipiAnahtari=LS"
ITU_LISANS_DERS_SORGU_URL = "https://obs.itu.edu.tr/public/DersProgram/DersProgramSearch?programSeviyeTipiAnahtari=LS&dersBransKoduId={0}"

def enrollInCourse(crn):
    fetcher=TokenFetcher(TARGET_URL,data.get("account").get("username"),data.get("account").get("password"))
    fetcher.start_driver()
    token=fetcher.fetch_token()
    request_manager = RequestManager(token, COURSE_SELECTION_URL, COURSE_TIME_CHECK_URL)
    response=request_manager.request_course_selection([crn],[])

CONFIG_FILE_PATH = "itu-ders-secici/data/config.json"
data=json.load(open(CONFIG_FILE_PATH))
codeList=get(ITU_LISANS_BRANS_KODU_ID_URL).json()
codeIdDictionary=dict()
for code in codeList:
    codeIdDictionary[code["dersBransKodu"]]=code["bransKoduId"]

lesson_lines = get(ITU_HELPER_LESSONS_URL).text.split("\n")
crn_to_lesson = {lesson.split("|")[0] : lesson.split("|")[1][0:3] for lesson in lesson_lines if len(lesson.split("|")) > 1}
for crn in data.get("courses")["crn"]:
    lessonBranchId=codeIdDictionary[crn_to_lesson[crn]]
    soup=BeautifulSoup(get(ITU_LISANS_DERS_SORGU_URL.format(lessonBranchId)).text,"html.parser")
    table = soup.find("table", {"id": "dersProgramContainer"})
    headers = [cell.get_text(strip=True) for cell in table.find("thead").find_all("td")]
    for tr in table.find("tbody").find_all("tr"):
        row = [cell.get_text(strip=True) for cell in tr.find_all("td")]
        if(row[0]==crn):#row 0 is crn 
            if(int(row[10])<int(row[9])):
                enrollInCourse(crn)








