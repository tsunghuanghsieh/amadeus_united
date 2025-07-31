#!/usr/bin/env python3

class AMADEUS_URL:
  OAUTH2_TOKEN_URL_PROD = "https://api.amadeus.com/v1/security/oauth2/token"
  OAUTH2_TOKEN_URL_TEST = "https://test.api.amadeus.com/v1/security/oauth2/token"
  FLT_AVAILABILITIES_PROD = "https://api.amadeus.com/v1/shopping/availability/flight-availabilities"
  FLT_AVAILABILITIES_TEST = "https://test.api.amadeus.com/v1/shopping/availability/flight-availabilities"

class AMADEUS_OAUTH2:
  Access_Token = "access_token"

class CFG:
  env = "env"
  env_test = "test"
  env_prod = "prod"
  fareClasses = "fareClasses"
  flightFrom = "flightFrom"
  flightTo = "flightTo"
  minimumTix = "minimumTix"
  searchBeginDate = "searchBeginDate"
  searchEndDate = "searchEndDate"
  sleep_in_second = "sleep_in_second"
  TADIA = "tix_available_days_in_advance"
  trips = "trips"

class ENV:
  AMADEUS_API_KEY_PROD = "AMADEUS_API_KEY_PROD"
  AMADEUS_API_SECRET_PROD = "AMADEUS_API_SECRET_PROD"
  AMADEUS_API_KEY_TEST = "AMADEUS_API_KEY_TEST"
  AMADEUS_API_SECRET_TEST = "AMADEUS_API_SECRET_TEST"

class HDR:
  AUTHORIZATION = "Authorization"
  CONTENT_LENGTH = "Content-Length"

class PAYLOAD:
  Date = "date"
  DepartureDateTime = "departureDateTime"
  DestinationLocationCode = "destinationLocationCode"
  Id = "id"
  OriginDestinations = "originDestinations"
  OriginLocationCode = "originLocationCode"

class RESULT:
  Arrival = "arrival"
  AvailabilityClasses = "availabilityClasses"
  CarrierCode = "carrierCode"
  CarrierCode_UA = "UA"
  Class = "class"
  Data = "data"
  Departure = "departure"
  IataCode = "iataCode"
  Number = "number"
  NumberOfBookableSeats = "numberOfBookableSeats"
  Operating = "operating"
  Segments = "segments"
