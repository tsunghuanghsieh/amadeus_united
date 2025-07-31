# Admadeus Flight Availability Search on United flights

This is a separate attempt to automate finding United upgrade fare class, `PN`, `PZ` and `RN`, using [Flight Availabilities Search](https://developers.amadeus.com/self-service/category/flights/api-doc/flight-availabilities-search) in Amadeus [Self-Service APIs](https://developers.amadeus.com/self-service). It levarages Amadeus Global Distribution Systems (GDS) to find United ticket availabilities which contain avaiable seats in different fare class.

Unfortunately, `Self-Service APIs` does not provide full fare class ladder. Award (`JN`, `ZN`, `IN`, etc.), upgrade (`PN`, `PZ` and `RN`) and several discounted economy ticket fare classes are not in the response returned by `Flight Availabilities Search` API. Only the version in `Enterprise APIs` does that.

> Disclaimer: This project is not affiliated with or endorsed by Amadeus IT Group or United Airlines, Inc. Amadeus® is a registered trademark of Amadeus IT Group.

## Purpose
Seat availability search for specific fare classes on United direct flight between 2 locations over a range of departure dates.

## Prerequisites
* Python 3.12

## 🚀 Quick Start

### 1. Clone this repository
### 2. Get your own Amadeus Self-Service APIs **key** and **secret** for [your app](https://developers.amadeus.com/my-apps).
### 3. Populate your **key** and **secret** generated in previous step into `secret.sh`.
### 4. Set environment variables
If you use [Anaconda](https://www.anaconda.com/) to manage your python environments, run `source setup.sh` from your terminal. Otherwise, you can run `source secret.sh` instead.
### 5. Configure `env`, `fareClasses`, `flightFrom`, `flightTo`, `searchBeginDate` and `searchEndDate` in `config.json`.
The value for `env` can be `test` or `prod`. The `test` environment uses cached data, hence the result could be very different from that of `prod` environment.

United fare class available in `Self-Service APIs` are `J`, `C`, `D`, `Z`, `P`, `O`, `A`, `R`, `Y`, `B` and `M`. Though, none of those matter.

`flightFrom` and `flightTo` are airport IATA code, and can be more than 1 pair.
```
  "trips": [
    {
      "flightFrom": "SFO",
      "flightTo": "AKL"
    },
    {
      "flightFrom": "SFO",
      "flightTo": "PPT"
    }
  ]
```

`searchBeginDate` and `searchEndDate` are the departure dates to search for the flight(s) listed under `trips` and have the date format `YYYY-MM-DD`.

If any fare class in `fareClasses` are in the response, it will output to `stdout`.
```
SFO-AKL UA 917 P  3
```

### 6. Execute `amadeus.py`.
```
./amadeus.py
```

## 📚 References
* [United Airlines Fare Classes](https://thepointsguy.com/airline/united-fare-classes/)
* Amadeus [Self-Service APIs](https://developers.amadeus.com/self-service) [Flight Availabilities Search](https://developers.amadeus.com/self-service/category/flights/api-doc/flight-availabilities-search)
