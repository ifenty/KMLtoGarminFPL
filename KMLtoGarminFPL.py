#!/usr/bin/env python
#
# September 2022
# Severine Fournier, Tom Hutchinson, and Ian Fenty
#
##############################################
## 
##############################################
    
import os
import numpy as np
import datetime
import sys, getopt

def main(argv):

    print ('\n\n')
    print ('==============================================\n')
    print ('Welcome to the KML to Garmin FPL tool\n')
    print ('  -----------------------------------')
    print ('  |   Severine Fournier (NASA/JPL)  |')
    print ('  | Tom Hutchinson (Kenn Borek Air) |')
    print ('  |       Ian Fenty (NASA/JPL)      |')
    print ('  -----------------------------------\n')

    input_file = ''
    waypoint_prefix = 'A'

    try:
        opts, args = getopt.getopt(argv,"i:n:",["input_file=","waypoint_prefix="])
    except getopt.GetoptError:
        print ('KMLtoGarminFPL.py -i <input_kml_file> -n <waypoint_prefix')
        sys.exit(2)
   
    for opt, arg in opts:
        if opt == '-h':
            print('KMLtoGarminFPL.py -i <input_kml_file> -n <waypoint_prefix>')
            sys.exit()
        elif opt in ("-i", "--input_kml_file"):
            input_file = arg
        elif opt in ("-n", "--waypoint_prefix"):
            waypoint_prefix = arg

    if waypoint_prefix == '':
        print ('ERROR: you should specify a waypoint prefix like "A", "B", etc. using "-n A" or "-n B" etc.')
        print ('       using "A" by default')

    fileout_base = input_file.split('.kml')[0]
    fileout_kml = fileout_base + '_as_waypoints_' + waypoint_prefix + '.kml' 
    fileout_fpl = fileout_base + '_as_waypoints_and_route_' + waypoint_prefix + '.fpl' 

    print ('Input KML filename is ', input_file)
    print ('Waypoint prefix is ', waypoint_prefix)
    print ('\nOutput files will be ')
    print ('   kml waypoints: ' + fileout_kml)
    print ('   fpl waypoints and route: ' + fileout_fpl)

    ####### Read lines from input KML file, calculate distance per leg, and estimate time ##########	
    # filename=input_file
    print('\nopening ', input_file)

    text_file = open(input_file, "r")
    
    # a list with elements that correspond to each line in the input file (kml)
    lines = text_file.readlines()
    text_file.close()
    num_lines = len(lines)

    # define parse_file (boolean T/F) to be True
    parse_file = True

    li = 0
    latitude=[]
    longitude=[]
    
    while parse_file:
        li += 1
        if li >= num_lines:
            parse_file = False
        else:
            line = lines[li]
            if 'coordinates' in line:            
                y= line.split('coordinates>')[1] 
                y= y.split('</')[0]
                yy=y.split(' ')
                for el in yy:
                    el=el.split(',')
                    longitude.append(np.float32(el[0]))
                    latitude.append(np.float32(el[1]))

    coord=[list(x) for x in zip(longitude, latitude)]
    print ('\nCoordinates read from the input kml file')
    print (' #     lon      lat')
    print ('---------------------')
    for ci, c in enumerate(coord):
        print (f'{ci+1:3}  {c[0]:6.3f}  {c[1]:6.3f}')

    ####### Write output KML file ##########	

#    fileout_kml=output_file_noformat+'.kml'
    print('\nWrite KML file: '+fileout_kml)

    with open(fileout_kml, 'w') as f:
        # define the initial block of text for the kml file
        lines = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">',
            '<Document>',
            '\t<name>'+fileout_kml+'</name>',
            '\t<Folder>',
            '\t\t<name>'+fileout_kml+'</name>']

        # write each line in the initial block of text to the kml file
        for line in lines:
            f.write(line)
            # add a newline character '\n' after each line
            f.write('\n')

        # loop through each coordinate and write each one to the kml file 
        i = 1
        for c in coord:
            f.write('<Placemark><name>'+str(waypoint_prefix)+str(i).zfill(2)+'</name><Point><coordinates>'+'%.3f' % c[0]+','+'%.3f' % c[1]+',0</coordinates></Point></Placemark>')
            f.write('\n')
            i=i+1
            
        # write the end block of the kml file
        f.write('\t''</Folder>')
        f.write('\n</Document>')
        f.write('\n</kml>')
    

    ####### Write output FPL file ##########
    #fileout_fpl=output_file_noformat+'.fpl'
    print('\nWrite FPL file: '+ fileout_fpl)

    with open(fileout_fpl, 'w') as f:
        # define the header, first few lines of the fpl file
        lines = ['<?xml version="1.0" encoding="utf-8"?>\n',
                '<flight-plan xmlns="http://www8.garmin.com/xmlschemas/FlightPlan/v1">\n',
                '\t<created>'+datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")+'</created>\n',
                '\t<waypoint-table>\n']

        # write each line of the headerto the new fpl file
        for line in lines:
            f.write(line)	
        
        # write each waypoint block to the file
        # -------------------------------------

        # i is the index for each waypoint, starting with 1
        i = 0
        # coord is a list of number pairs and looks like this:
        # coord[0] = [lon0, lat0]
        # coord[1] = [lon1, lat1]
        #  ...
        # coord[n] = [lonn, latn]

        # loop through each lon/lat pair in coord
        for c in coord:
            # the ith index of coord is c_i
            # c_i looks like this:
            # c_i = [lon_i, lat_i]
            # c_i[0] = lon_i
            # c_i[1] = lat_i

            # new coordinate, increment i by 1.
            i = i+1
            # str(i) converts the number i into a string 'i'
            # if you have more than 99 points, then zfill to 3 so numbers go from 001 to 999
            
            lines = ['\t\t<waypoint>\n',
            '\t\t\t<identifier>'+str(waypoint_prefix)+str(i).zfill(2)+'</identifier>\n',
            '\t\t\t<type>USER WAYPOINT</type>\n',
            '\t\t\t<country-code></country-code>\n',
            '\t\t\t<lat>'+'%.6f' % c[1]+'</lat>\n',
            '\t\t\t<lon>'+'%.6f' % c[0]+'</lon>\n',
            '\t\t\t<comment></comment>\n',
            '\t\t</waypoint>\n']
                
            # loop through each element of 'lines' and write each one to the file
            for line in lines:
                f.write(line)
                    

        # we've looped through every coordinate pair in coor and written each
        # one to the fpl file as a block starting with <waypoint> and ending with
        # </waypoint>
        # now end the 'waypoint table' with a </waypoint-table> tag
        f.write('\t</waypoint-table>\n')

        # write the route block
        # ---------------------

        # begin the route block with a <route> tag, route name, and index number
        lines = ['\t<route>\n',
        '\t\t<route-name>ROUTE'+str(waypoint_prefix)+'</route-name>\n',
        '\t\t<flight-plan-index>1</flight-plan-index>\n']
       
        # write 3 lines to the file 
        # 1) beginning of route section <route>
        # 2) define route name <route-name>... bla blah </route-name>
        # 3) define flight plan index 

        for line in lines:
            f.write(line)
            
        # now, loop through each coord pair again and write each coordinate as a route entry

        # construct route entry blocks in 'lines' and then save each block to the file
        for i in range(len(coord)):
            lines = ['\t\t<route-point>\n',
            '\t\t\t<waypoint-identifier>'+str(waypoint_prefix)+str(i+1).zfill(2)+'</waypoint-identifier>\n',
            '\t\t\t<waypoint-type>USER WAYPOINT</waypoint-type>\n',
            '\t\t\t<waypoint-country-code></waypoint-country-code>\n',
            '\t\t</route-point>\n']

            # loop through each 'line' in the new route entry block and write each one to the
            # file
            for line in lines:
                f.write(line)
            
        # construct the final lines of the fpl file. 
        # the first line closes the route list </route>
        # the second closes the flight plan itself </flight-plan>
        lines = ['\t</route>\n',  '</flight-plan>\n']  
            
        # write each of these lines to the file
        for line in lines:
            f.write(line) 

    print ('\n\n              GOOD LUCK! ')
    print ('\n==============================================\n')

##################
if __name__ == "__main__":
    print ('KMLtoGarminFPL.py -i <input_kml_file> -o <output_file_noformat> -n <waypoint_prefix>')
    main(sys.argv[1:])
