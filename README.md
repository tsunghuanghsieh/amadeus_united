# Find Available Seats of fare class on United Airlines flights using Amadeus Self-Service APIs

This is a separate attempt to automate finding United upgrade fare class, `PN`, `PZ` and `RN`, using [Flight Availabilities Search](https://developers.amadeus.com/self-service/category/flights/api-doc/flight-availabilities-search) in Amadeus [Self-Service APIs](https://developers.amadeus.com/self-service). It levarages Amadeus Global Distribution Systems (GDS) to find United ticket availabilities which contain avaiable seats in different fare class.

Unfortunately, `Self-Service APIs` does not provide full fare class ladder. Award (`JN`, `ZN`, `IN`, etc.), upgrade (`PN`, `PZ` and `RN`) and several discounted economy ticket fare classes are not in the response returned by `Flight Availabilities Search` API. Only the version in `Enterprise APIs` does that.

## Instructions

* Populate Amadeus API key and secret in `secret.sh` which will be then used to set up environment variables used in python script, `amadeus.py`.
* Run `source setup.sh`.
* Update `env`, `fareClasses`, `flightFrom`, `flightTo`, `searchBeginDate` and `searchEndDate` in `config.json`.
* Execute `amadeus.py`.
