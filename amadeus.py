#!/usr/bin/env python3

import json
import os
import re
import requests
import time
import sys
import uuid

from datetime import datetime, date, timedelta

from constants import AMADEUS_URL, AMADEUS_OAUTH2, CFG, ENV, HDR, PAYLOAD, RESULT

class Amadeus:
    def __init__(self, config):
        self._ValidateConfig(config)
        self._config = config
        self._api_key = os.environ.get(ENV.AMADEUS_API_KEY_TEST
            if self._config[CFG.env] == CFG.env_test else ENV.AMADEUS_API_KEY_PROD)
        self._api_secret = os.environ.get(ENV.AMADEUS_API_SECRET_TEST
            if self._config[CFG.env] == CFG.env_test else ENV.AMADEUS_API_SECRET_PROD)
        if not self._api_key or not self._api_secret:
            print(f"Amadeus API key and secret are not set as environment variables for {self._config[CFG.env]}.")
            sys.exit(1)
        self._fareClasses = config[CFG.fareClasses]
        self._jsonResult = {}
        self._minimumTix = config[CFG.minimumTix]

    def _initRequestPayload(self, payload_file : str, searchDate: str) -> str:
        with open(payload_file, 'r') as fin:
            body = json.load(fin)
            for idx in range(len(self._config[CFG.trips])):
                trip = self._config[CFG.trips][idx]
                segment = {
                    PAYLOAD.Id: idx + 1,
                    PAYLOAD.OriginLocationCode: trip[CFG.flightFrom],
                    PAYLOAD.DestinationLocationCode: trip[CFG.flightTo],
                    PAYLOAD.DepartureDateTime: {
                        PAYLOAD.Date: searchDate
                    }
                }
                if len(body[PAYLOAD.OriginDestinations]) > idx:
                    body[PAYLOAD.OriginDestinations][idx] = segment
                else:
                    body[PAYLOAD.OriginDestinations].append(segment)
            payload = json.dumps(body)
        return payload

    def _initRequestHeaders(self, hdr_file : str) -> json:
        with open(hdr_file, 'r') as fin:
            headers = json.load(fin)
        return headers

    def _ValidateConfig(self, config) -> None:
        if (not config[CFG.flightFrom] or
            not config[CFG.flightTo] or
            not config[CFG.searchBeginDate] or
            not config[CFG.searchEndDate]):
            print("config.json is not completely populated.")
            sys.exit(1)
        try:
            beginDate = date.fromisoformat(config[CFG.searchBeginDate])
            endDate = date.fromisoformat(config[CFG.searchEndDate])
            if (beginDate > endDate):
                print(f"{beginDate} is after {endDate}.")
                sys.exit(1)
            if (beginDate > date.today() + timedelta(config[CFG.TADIA]) or
                endDate > date.today() + timedelta(config[CFG.TADIA])):
                print(f"United doesn't make tickets available beyond {date.today() + timedelta(config[CFG.TADIA])}.")
                sys.exit(1)
        except ValueError as e:
            print(f"config.json does not contain expected search date format, YYYY-MM-DD. {e}")

    def getApiToken(self) -> str:
        payload = f"grant_type=client_credentials&client_id={self._api_key}&client_secret={self._api_secret}"
        headers = self._initRequestHeaders("headers_oauth2.json")
        headers[HDR.CONTENT_LENGTH] = f"{len(payload)}"
        if self._config[CFG.env] == CFG.env_test:
            url = AMADEUS_URL.OAUTH2_TOKEN_URL_TEST
        else:
            url = AMADEUS_URL.OAUTH2_TOKEN_URL_PROD
        res = requests.post(url, headers=headers, data=payload)
        return f"Bearer {res.json()[AMADEUS_OAUTH2.Access_Token]}"

    def getFlightAvailabilities(self, searchDate : str) -> int:
        if self._config[CFG.env] == CFG.env_test:
            url = AMADEUS_URL.FLT_AVAILABILITIES_TEST
        else:
            url = AMADEUS_URL.FLT_AVAILABILITIES_PROD
        data = self._initRequestPayload("data.json", searchDate)
        headers = self._initRequestHeaders("headers_flight_availabilities.json")
        headers[HDR.CONTENT_LENGTH] = f"{len(data)}"
        headers[HDR.AUTHORIZATION] = self.getApiToken()
        res = requests.post(url, headers=headers, data=data)
        self._jsonResult = res.json()
        with open("result.json", 'w') as fout:
            fout.write(json.dumps(self._jsonResult, indent=2))
        return res.status_code

    def parseAvailableSeats(self):
        if (len(self._jsonResult.get(RESULT.Data, {})) == 0):
            print("No flights returned. One possible reason is expired api key.")
            sys.exit(1)

        for flight in self._jsonResult[RESULT.Data]:
            segment = flight[RESULT.Segments][0]   # only 1 segment since it's a direct flight
            if (segment[RESULT.CarrierCode] != RESULT.CarrierCode_UA or (RESULT.Operating in segment
                and segment[RESULT.Operating][RESULT.CarrierCode] != RESULT.CarrierCode_UA)):
                continue
            for fareClass in segment[RESULT.AvailabilityClasses]:
                if fareClass[RESULT.Class] in self._fareClasses:
                    msg = f"{segment[RESULT.Departure][RESULT.IataCode]}-{segment[RESULT.Arrival][RESULT.IataCode]}"
                    msg += f" UA {segment[RESULT.Number]:>4} {fareClass[RESULT.Class]:^2} {fareClass[RESULT.NumberOfBookableSeats]}"
                    print(msg)
        print("-----------------------------------------------------")

    def searchAllFlights(self) -> None:
        beginDate = date.fromisoformat(self._config[CFG.searchBeginDate])
        endDate = date.fromisoformat(self._config[CFG.searchEndDate])
        print(f"Searched on {date.today()}\n")
        for d in range((endDate - beginDate).days + 1):
            searchDate = beginDate + timedelta(d)
            status_code = self.getFlightAvailabilities(f"{searchDate}")
            print(f"{searchDate} {searchDate.strftime('%A')}")
            print("-----------------------------------------------------")
            if status_code == 200:
                self.parseAvailableSeats()
            else:
                print(f"Status code: {status_code}")
                sys.exit(1)
            print("")
            # sleep between searches
            time.sleep(self._config[CFG.sleep_in_second])

def main() -> None:
    with open("config.json", 'r') as fin:
        config = json.load(fin)
    amadeus = Amadeus(config)
    amadeus.searchAllFlights()

if __name__ == '__main__':
    main()
