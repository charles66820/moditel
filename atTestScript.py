#!/usr/bin/python3

import os
import serial
import sys

DEVICE_PORT = "COM3"
PHONE_NUMBER = "0769709286"
BAND_RATE = 115200  # 9600


modems = []


def modemConnection():
  modem = serial.Serial(DEVICE_PORT, baudrate=BAND_RATE, timeout=1)
  modems.append(modem)
  return modem


def modemDisconnect(modem):
  modem.write(str.encode("AT\B\r"))
  modems.remove(modem)


def modemDisableEcho(modem):
  # Suppression echo
  modem.write(str.encode("ATE0\r"))


def printCallInfo(modemInfos):
  if ("DATE" in modemInfos):
    callDate = (modemInfos[5:]).strip(" \t\n\r")
  if ("TIME" in modemInfos):
    callHours = (modemInfos[5:]).strip(" \t\n\r")
  if ("NMBR" in modemInfos):
    callNumber = (modemInfos[5:]).strip(" \t\n\r")
    print("Call date: " + callDate + ", hours: " +
          callHours + ", phone number: " + callNumber + "\n")


def modemProductCode(modem):
  modem.write(str.encode("ATI0\r"))
  rawData = modem.read(100)
  productCode = rawData[8:12]
  print("Modem product code: ", productCode.decode())


def modemFirmWareVersion(modem):
  modem.write(str.encode("ATI3\r"))
  rawData = modem.read(100)
  firmwareVersion = rawData[2:35]
  print("Modem firmware version: ", firmwareVersion.decode())


def modemDialAPhoneNumber(modem):
  modem.write(str.encode("ATDT" + PHONE_NUMBER + ";\r"))
  rawData = modem.read(100)
  composedNum = rawData[5:15]
  print("Composed number: ", composedNum.decode())


def modemLastComposedPhoneNumber(modem):
  modem.write(str.encode("ATDL?\r"))
  rawData = modem.read(100)
  lastPhoneNumber = rawData[2:11]
  print("Last composed phone number: ", lastPhoneNumber.decode())


def modemReadAllReceiveData(modem):
  while True:
    modemInfos = modem.readline()
    modemInfos = modemInfos.decode()
    if modemInfos != "":
      print(modemInfos)
      printCallInfo(modemInfos)


def mainContent():
  modem = modemConnection()

  modemDisableEcho(modem)
  modemProductCode(modem)
  modemFirmWareVersion(modem)
  modemDialAPhoneNumber(modem)
  modemLastComposedPhoneNumber(modem)

  modemReadAllReceiveData(modem)


def main():
  try:
    mainContent()
  except KeyboardInterrupt:
    print("Interrupted")
    for modem in modems:
      modemDisconnect(modem)

    # Close app
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)


if __name__ == "__main__":
  main()
