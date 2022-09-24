# KMLtoGarminFPL

This repository contains a Python program that converts a flight plan defined in a KML file to the Garmin FPL flight plan (FPL) format. The python program, KMLtoGarminFPL.py", makes it easy to add new "waypoints" and "routes" into Garmin GNS models 400w/500w series from flight plans created in KML files.

## Instructions ##

1. Create a new flight plan and save it as a KML file. For example, 'new_flight_plan.kml'
2. Decide on a prefix to name the waypoints of the new flight plan. For example, if you choose the prefix "A", the waypoints will be named: A01, A02, ..., A99.
3. Use python to run the KMLtoGarminFPL.py program like this:  "python ./KMLtoGarminFPL.py -i new_flight_plan.kml -n A"
4. The program will generate two files: "new_flight_plan_as_waypoints_A.kml" and "new_flight_plan_as_waypoints_A.fpl"
5. Load the "new_flight_plan_as_waypoints_A.fpl" file onto a Garmin card using the Garmin FlightPlan Migrator software and the Garmin FlightPlan Migrator Kit's special card reader.
6. From the cockpit, remove the original card from the slot on the right side of the Garmin GNS unit.
7. Insert the card with the new FPL file into the slot on the right side of the Garmin GNS unit.
8. Power on the Garmin GNS unit.
8. Using the Garmin menu system, load the waypoints and flight plan. 
9. << IMPORTANT >> Turn off the Garmin GNS unit, remove the card with the FPL file, replace it with the original card, and then turn the Garmin GNS unit on
10. Confirm that the new waypoints and flight plan are loaded.


## Software Required ##
1. Python 3
2. Garmin FlightPlan Migrator with USB Drivers software version 3.10: https://www8.garmin.com/support/download_details.jsp?id=4471


## Hardware Required ##
1. Computer with a windows operating system
2. Garmin FlightPlan Migrator Kit: https://www.garmin.com/en-US/p/35228/pn/010-11308-20


### Garmin FlightPlan Migrator Hardware and Software ###

To transfer FPL files to a Garmin GNS unit via card, you need the special Garmin card reader/writer and the FlightPlan Migrator software. The card and reader seem to be proprietory. Even after installing the drivers, the card reader with the card inserted do not appear as external drives from Windows (unlike a typical USB drive, for example). The Garmin FlightPlan Migrator software lets you load FPL files on the card into one of 19 spaces.

The Garmin card reader/writer unit is available for $70 from Amazon (as of Sep 2022). https://www.amazon.com/dp/B01JTFZPFG?psc=1&ref=ppx_yo2ov_dt_b_product_details

As for the cards, I don't know where they come from, maybe you can only get them from the Garmin FlightPlan Migrator Kit.

## Flight Plan KML files ##

In our project we defined flight plans as vector multi-part line shapefiles in QGIS and then exported them as KML. The resulting KML defines the flight plan by a set of locations that define the start/end point of each segment like this:

```
<MultiGeometry><LineString><coordinates>-148.409488684457,70.1879369846318 -150.185878001433,71.3641064917923 -151.868207666983,71.6826939896295 -151.786142805248,71.7138328639197 -150.110904212891,71.395591937114 -150.025993171817,71.4296743112763 -151.700658574275,71.7449206097164 -151.610999271859,71.7760539944028 -149.93793727737,71.4646961861542 -149.843591676177,71.4996543291621 -151.526088230785,71.8074996278754 -151.438032336339,71.8388928343137 -149.75553578173,71.535544895473 -149.67376959403,71.5713682569899 -151.356266148638,71.869255081541 -151.258775694072,71.9034760808731 -149.585713699583,71.6051398244629 -149.503947511882,71.6368702451494 -151.164430092879,71.9376346478209 -151.082663905178,71.9697842051396 -149.415891617436,71.6725038002111 -149.340415136481,71.7021474148267 -150.997752864105,71.9999349054457 -150.903407262912,72.0310070735427 -149.258648948781,71.730758889851 -149.183172467826,71.7612957842083 -150.824785928584,72.0600901208561 -150.752454301003,72.0891276428685 -149.104551133499,71.7917833693959 -148.409538538044,70.1842836276263</coordinates></LineString></MultiGeometry>
```

As you can see, each "longitude, latitude" pair, separated by a space, like this:

Your input KML file has to have the same general format for the code to work, or you will have to modify the code to read the coordinates of the start and ends points of each line.

== Example == 
