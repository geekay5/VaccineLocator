
import json
import requests
import os
import sys
import getopt
import hashlib
import time
import datetime

PRO_SERVER = "https://cdn-api.co-vin.in/api"
PRO_API_SECRET = "U2FsdGVkX1+z/4Nr9nta+2DrVJSv7KS6VoQUSQ1ZXYDx/CJUkWxFYG6P3iM/VW+6jLQ9RDQVzp/RcZ8kbT41xw=="

PRO_OTP_URL = "/v2/auth/generateMobileOTP"
PRO_OTP_CNFRM_URL = "/v2/auth/validateMobileOtp"
BOOKING_URL = "/v2/appointment/schedule"
BOOKING_MOD_URL = "/v2/appointment/reschedule"
BOOKING_CANCEL_URL = "​/v2​/appointment​/cancel"

LIST_BY_PIN_URL = "/v2/appointment/sessions/findByPin?pincode={0}&date={1}"
CAL_BY_PIN_URL = "/v2/appointment/sessions/calendarByPin?pincode={0}&date={1}"
CAL_BY_DIST_URL = "/v2/appointment/sessions/calendarByDistrict?district_id={0}&date={1}"
BENEFICIARIES_URL = "/v2/appointment/beneficiaries"


BASE_HEADERS = {
    'content-type': 'application/json',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Accept-Language": "en_US"
}


def setToken(token):
    global gToken
    gToken = token


def sendPostRequest(url, jd, headers):
    print(url)
    r = requests.post(url, jd, headers=headers)
    if r.status_code != 200:
        print("Error: ", r.status_code)
        return None
    return r.json()


def sendGetRequest(url, headers):
    print(url)
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Error: ", r.status_code)
        return None
    return r.json()


def generateOTP(mobile):
    data = {
        "mobile": mobile,
        "secret": PRO_API_SECRET
    }
    jd = json.dumps(data)
    rd = sendPostRequest(PRO_SERVER+PRO_OTP_URL, jd=jd, headers=BASE_HEADERS)
    if rd != None:
        return rd['txnId']
    return None


def confirmOTP(otp, txnId):
    data = {
        "otp": otp
    }
    data["txnId"] = txnId
    jd = json.dumps(data)
    rd = sendPostRequest(PRO_SERVER+PRO_OTP_CNFRM_URL,
                         jd=jd, headers=BASE_HEADERS)
    if rd != None:
        print(rd)
        return rd["token"]


def getBeneficiaries():
    heads = BASE_HEADERS
    heads["Authorization"] = "Bearer " + gToken
    rd = sendGetRequest(url=PRO_SERVER+BENEFICIARIES_URL, headers=heads)
    if rd != None:
        print(rd)


def getListByPin(pin, date):
    heads = BASE_HEADERS
    heads["Authorization"] = "Bearer " + gToken
    url = PRO_SERVER + LIST_BY_PIN_URL.format(pin, date)
    rd = sendGetRequest(url=url, headers=heads)
    if rd != None:
        print(rd)


def getCalByPin(pin, date):
    heads = BASE_HEADERS
    heads["Authorization"] = "Bearer " + gToken
    url = PRO_SERVER+CAL_BY_PIN_URL.format(pin, date)
    rd = sendGetRequest(url=url, headers=heads)
    if rd != None:
        return rd
    return None


def findAvailableHosp(centers, age):
    found = False
    if centers != None:
        for k in centers:
            for center in centers[k]:
                sessions = center["sessions"]
                for session in sessions:
                    if session["available_capacity_dose1"] > 2 and session["min_age_limit"] == age:
                        print(session["available_capacity_dose1"], "doses are available on ", session["date"],
                              "at ", center["name"], "located in area with pin ", center["pincode"])
                        found = True
                        # print(center)
        if found is True:
            os.system('afplay -t 60 alarm.mp3')
    return found


def getStates():
    url = "/v2/admin/location/states"
    rd = sendGetRequest(url=url, headers=BASE_HEADERS)
    if rd != None:
        print(rd)


def getDistricts():
    state_id = "16"  # Karnataka state_id 32 - Telangana
    url = "/v2/admin/location/districts/" + state_id
    rd = sendGetRequest(url=url, headers=BASE_HEADERS)
    if rd != None:
        print(rd)


def getCalByDist(dist_id, date):
    url = PRO_SERVER+CAL_BY_DIST_URL.format(dist_id, date)
    rd = sendGetRequest(url=url, headers=BASE_HEADERS)
    if rd != None:
        return rd
    return None
