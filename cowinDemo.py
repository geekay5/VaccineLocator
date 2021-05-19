################################################################
## This is the script targetting the Demo server for practice ##
################################################################

#!/usr/bin/env python3
import json
import hashlib
import requests
import os
import datetime

DEMO_SERVER = "https://api.demo.co-vin.in/api"
DEMO_API_KEY = "3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi"

OTP_DEMO_URL = "/v2/auth/generateOTP"
OTP_CNFRM_DEMO_URL = "/v2/auth/confirmOTP"

BOOKING_DEMO_URL = "/v2/appointment/schedule"
BOOKING_MOD_DEMO_URL = "/v2/appointment/reschedule"
BOOKING_CANCEL_DEMO_URL = "​/v2​/appointment​/cancel"

LIST_BY_PIN_DEMO_URL = "/v2/appointment/sessions/findByPin?pincode={0}&date={1}"
CAL_BY_PIN_DEMO_URL = "/v2/appointment/sessions/calendarByPin?pincode={0}&date={1}"
CAL_BY_DIST_DEMO_URL = "/v2/appointment/sessions/calendarByDistrict?district_id={0}&date={1}"
BENEFICIARIES_DEMO_URL = "/v2/appointment/beneficiaries"

BASE_HEADERS = {
    'content-type': 'application/json',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Accept-Language": "en_US"
}
BASE_HEADERS["x-api-key"] = DEMO_API_KEY


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


def generateDemoOTP(mobile):
    data = {
        "mobile": mobile,
    }
    jd = json.dumps(data)
    rd = sendPostRequest(DEMO_SERVER+OTP_DEMO_URL, jd=jd,
                         headers=BASE_HEADERS)
    if rd != None:
        return rd['txnId']
    return None


def confirmDemoOTP(otp, txnId):
    data = {
        "otp": otp
    }
    data["txnId"] = txnId
    jd = json.dumps(data)
    rd = sendPostRequest(DEMO_SERVER+OTP_CNFRM_DEMO_URL,
                         jd=jd, headers=BASE_HEADERS)
    if rd != None:
        print(rd)
        return rd['token']


def getBeneficiaries():
    heads = BASE_HEADERS
    heads["Authorization"] = "Bearer " + gToken
    rd = sendGetRequest(url=DEMO_SERVER+BENEFICIARIES_DEMO_URL, headers=heads)
    if rd != None:
        print(rd)
        return rd
    return None


def getCalByPin(pin, date):
    heads = BASE_HEADERS
    heads["Authorization"] = "Bearer " + gToken
    url = DEMO_SERVER+CAL_BY_PIN_DEMO_URL.format(pin, date)
    rd = sendGetRequest(url=url, headers=heads)
    if rd != None:
        return rd
    return None


def findAvailableHosp(centers):
    found = False
    if centers != None:
        for k in centers:
            for center in centers[k]:
                sessions = center["sessions"]
                for session in sessions:
                    if session["available_capacity"] > 2 and session["min_age_limit"] == age:
                        print(session["available_capacity"], "doses are available on ", session["date"],
                              "at ", center["name"], "located in area with pin ", center["pincode"])
                        found = True
        if found is True:
            os.system('afplay -t 60 alarm.mp3')
    return found


def main():
    mobile = "9035050504"
    pin = "560094"
    dist_id = "294"
    txnId = generateDemoOTP(mobile)
    # print(txnId)
    if txnId != None:
        otpPin = input("Enter OTP: ")
        otp = hashlib.sha256(otpPin.encode('utf-8')).hexdigest()
        # print(otp)
        token = confirmDemoOTP(otp, txnId=txnId)
        setToken(token)
        # print(token)
    else:
        exit(2)

    today = datetime.date.today()
    date = today.strftime("%d-%m-%Y")
    getBeneficiaries()
    centers = getCalByPin(pin, date)
    findAvailableHosp(centers)


if __name__ == "__main__":
    main()
