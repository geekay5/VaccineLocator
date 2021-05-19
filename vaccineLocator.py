#!/usr/bin/env python3

import os
import sys
import getopt
import hashlib
import time
import datetime
from cwutils import *

ERROR_MSG = "Usage: cowin.py -m <mobile> -p <pin> -d <date>"


def validateArgs(argv):
    global mobile, pin, date, dist_id, age, login
    mobile = "9999999999"
    pin = None
    date = None
    age = 18
    login = False
    dist_id = "294"  # 294 BBMP, 272 Bidar, 267 Gulbarga 265 BLR Urban

    try:
        opts, args = getopt.getopt(argv, "m:p:x:a:l")
    except getopt.GetoptError:
        print(ERROR_MSG)
        sys.exit(2)

    for opt, arg in opts:
        if opt is None:
            print(ERROR_MSG)
            sys.exit(2)
        if opt in ("-m"):
            mobile = arg
        elif opt in ("-p"):
            pin = arg
        elif opt in ("-x"):
            dist_id = arg
        elif opt in ("-a"):
            age = int(arg)
        elif opt in ("-l"):
            login = True
        else:
            print(ERROR_MSG)
            sys.exit(2)


def main():
    validateArgs(sys.argv[1:])
    today = datetime.date.today()
    date = today.strftime("%d-%m-%Y")
    while True:
        if pin is not None:
            centers = getCalByPin(pin, date)
        else:
            centers = getCalByDist(dist_id, date)
        found = findAvailableHosp(centers, age)
        if found is True:
            break
        else:
            time.sleep(10)
    if found is True:
        bookSlot = input("Slots found. Do you want to book vaccination (y/n)?")
        if bookSlot == 'y':
            txnId = generateOTP(mobile)
            # print(txnId)
            if txnId != None:
                otpPin = input("Enter OTP: ")
                otp = hashlib.sha256(otpPin.encode('utf-8')).hexdigest()
                # print(otp)
                token = confirmOTP(otp, txnId=txnId)
                setToken(token)
                # print(token)
                getBeneficiaries()


if __name__ == "__main__":
    main()
