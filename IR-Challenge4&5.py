from motor import motor
from line_tracker import line_tracker
import time

newAddress = '192.168.0.104' 
lt = line_tracker(newAddress) 
mot = motor(newAddress) 
lt.start() 
robotPath = [];
findDestination = True
reverseToStart = False
tres = 350
pathstring = ''
shortPath = []
turnToStart = False

while True:
    try:
        while findDestination==True:
            try:
                if type(lt.data) == int:
                    time.sleep(0.3)
                    continue
                #to go straight forward
                if (lt.data[2] < tres) and (lt.data[1] > tres) and (lt.data[3] > tres):
                    mot.command('forward', 1, 0.3)
                    print("Straight: ", lt.data)
                    #shift left
                elif (lt.data[1] < tres and lt.data[0] > tres and lt.data[2] > tres and lt.data[3] > tres and lt.data[4] > tres):
                    mot.command('left', 3, 0.3)
                    print("Shift left", lt.data)
                elif (lt.data[0] < tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[3] > tres and lt.data[4] > tres):
                    mot.command('left', 3.5, 0.3)
                    print("Shift left: ", lt.data)
                    #shift right
                elif (lt.data[3] < tres and lt.data[0] > tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[4] > tres):
                    mot.command('right', 2.5, 0.3)
                    print("Shift right: ", lt.data)
                elif (lt.data[4] < tres and lt.data[0] > tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[3] > tres):
                    mot.command('right', 3, 0.3)
                    print("Shift right: ", lt.data)
                else:
                    #reach destination
                    if (lt.data[0] < tres and lt.data[1] < tres and lt.data[2] < tres and lt.data[3] < tres and lt.data[4] < tres):
                        mot.command('forward', 4, 0.2)
                        print("DETECT ALL BLACK AND MOVE FORWARD 1: ", lt.data)
                        mot.command('forward', 4, 0.2)
                        print("DETECT ALL BLACK AND MOVE FORWARD 2: ", lt.data)
                        if(lt.data[0] < tres and lt.data[1] < tres and lt.data[2] < tres and lt.data[3] < tres and lt.data[4] < tres):
                            print('REACH DESTINATION')
                            findDestination = False
                            reverseToStart = True
                        else:
                            mot.command('backward', 4, 0.2)
                            mot.command('backward', 4, 0.2)
                    #turn left
                    elif ((lt.data[0] < tres or lt.data[1] < tres) and lt.data[2] < tres):
                        pathstring = pathstring + 'L'
                        print("TURN LEFT")
                        while (lt.data[2] < tres and lt.data[1] > tres and lt.data[3] > tres) != True:
                            #mot.command('backward', 1.0, 0.2)
                            mot.command('left', 4.0, 0.1)
                            print("TURN LEFT: ", lt.data)
                            time.sleep(1)
                        
                    #forward and right junction  
                    elif ((lt.data[3] < tres or lt.data[4] < tres) and lt.data[2] < tres):
                        mot.command('forward', 4, 0.4)
                        #check if theres forward line
                        if lt.data[2] < tres and lt.data[0] > tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[3] > tres:
                            mot.command('forward', 7, 0.3)
                            print("DECIDE TO GO STRAIGHT: ", lt.data)
                            pathstring = pathstring + 'S'
                            #if no forward line, TURN RIGHT
                            #elif lt.data[2] > tres:
                        else:
                            mot.command('backward', 4, 0.1)
                            pathstring = pathstring + 'R'
                            print("TURN RIGHT")
                            while (lt.data[2] < tres and lt.data[3] > tres and lt.data[4] > tres) != True:
                                #mot.command('backward', 1.0, 0.2)
                                mot.command('right', 4.0, 0.3)
                                print("TURN RIGHT: ", lt.data)
                                time.sleep(1)
                            
                    else:
                        time.sleep(1)
                        pathstring = pathstring + 'B'
                        print("U-TURN / BACK")
                        while(lt.data[0] < tres or lt.data[1] < tres or lt.data[2] < tres or lt.data[3] < tres or lt.data[4] < tres) != True:
                            mot.command('backward', 3.0, 0.2)
                            mot.command('left', 7.0, 0.4)
                            print("U-TURN / BACK: ", lt.data)
                            time.sleep(1)
            
            except KeyboardInterrupt:
                    findDestination = False            
        
        while reverseToStart==True: 
            print('Reverse to Start')
            if type(lt.data) == int:
                time.sleep(0.3)
                continue
            while (lt.data[2] < tres and lt.data[3] < tres and lt.data[4] < tres and lt.data[0] < tres and lt.data[1] < tres) == True:
                            mot.command('backward', 4, 0.2)
                            print('Reverse to Start')
                            turnToStart = True
            #mot.command('backward', 4, 0.2)
            #print('Reverse to Start')
            a = 0
            b = 0
            c = 0
            d = 0
            e = 0
            f = 0
            g = 0
            h = 0
            Match = True
            while Match:
                if(pathstring.replace('SBL' , 'R')):
                    pathstring = pathstring.replace('SBL' , 'R')
                    print('Out: ', pathstring)
                else:
                    a = 0
                    #print('In: ', pathstring)
                if(pathstring.replace('SBS' , 'B')):
                    pathstring = pathstring.replace('SBS' , 'B')
                    #print('Out: ', pathstring)
                else:
                    b = 0
                if(pathstring.replace('RBL' , 'B')):
                    pathstring = pathstring.replace('RBL' , 'B')
                    #print('Out: ', pathstring)
                else:
                    c = 0
                if(pathstring.replace('LBR' , 'B')):
                    pathstring = pathstring.replace('LBR' , 'B')
                    #print('Out: ', pathstring)
                else:
                    d = 0
                if(pathstring.replace('LBS' , 'R')):
                    pathstring = pathstring.replace('LBS' , 'R')
                    #print('Out: ', pathstring)
                else:
                    e = 0
                if(pathstring.replace('LBL' , 'S')):
                    pathstring = pathstring.replace('LBL' , 'S')
                    #print('Out: ', pathstring)
                else:
                    f = 0
                if(a, b, c, d, e, f == 0):
                    Match = False

            print('SHORTEST PATH FROM START TO END: ', pathstring)
            #inversestring
            shortPath = list(pathstring[::-1])
            #replace L and R in inversetring
            for j in range (len(shortPath)):
                if(shortPath[j]=='R'):
                    shortPath[j]='L'
                elif(shortPath[j]=='L'):
                    shortPath[j]='R'
            stringinverse = ''.join(shortPath)
            print('SHORTEST PATH FROM END TO START: ', stringinverse)
            
            if (lt.data[2] < tres and lt.data[3] > tres and lt.data[4] > tres) == True  and (turnToStart==True):
                time.sleep(1)
                mot.command('backward', 3.0, 0.2)
                mot.command('left', 7.0, 0.4)
                print("U-TURN / BACK: ", lt.data)
                time.sleep(1)
            while (lt.data[2] < tres and lt.data[3] > tres and lt.data[4] > tres) != True and (turnToStart==True):
                mot.command('backward', 3.0, 0.2)
                mot.command('left', 7.0, 0.3)
                mot.command('forward', 3.0, 0.2)
                print("TURN LEFT TO U-TURN: ", lt.data)
            
            turnToStart = False
            
            #to go straight forward
            if (lt.data[2] < tres) and (lt.data[1] > tres) and (lt.data[3] > tres):
                mot.command('forward', 7, 0.3)
                print("Straight: ", lt.data)
            #shift left
            elif (lt.data[1] < tres and lt.data[0] > tres and lt.data[2] > tres and lt.data[3] > tres and lt.data[4] > tres):
                mot.command('left', 3, 0.3)
                print("Shift left", lt.data)
            elif (lt.data[0] < tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[3] > tres and lt.data[4] > tres):
                mot.command('left', 3.5, 0.3)
                print("Shift left: ", lt.data)
            #shift right
            elif (lt.data[3] < tres and lt.data[0] > tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[4] > tres):
                mot.command('right', 2.5, 0.3)
                print("Shift right: ", lt.data)
            elif (lt.data[4] < tres and lt.data[0] > tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[3] > tres):
                mot.command('right', 3, 0.3)
                print("Shift right: ", lt.data)
            else:
                for x in range (len(shortPath)):
                    if(shortPath[x]=='L') and ((lt.data[0] < tres or lt.data[1] < tres) and lt.data[2] < tres):
                        while (lt.data[2] < tres and lt.data[1] > tres and lt.data[3] > tres) != True:
                            #mot.command('backward', 1.0, 0.2)
                            mot.command('left', 4.0, 0.1)
                            print("TURN LEFT: ", lt.data)
                    elif(shortPath[x]=='R') and ((lt.data[3] < tres or lt.data[4] < tres) and lt.data[2] < tres):
                        while (lt.data[2] < tres and lt.data[3] > tres and lt.data[4] > tres) != True:
                            #mot.command('backward', 1.0, 0.2)
                            mot.command('right', 4.0, 0.1)
                            print("TURN RIGHT: ", lt.data)
                    elif(shortPath[x]=='S') and ((lt.data[3] < tres or lt.data[4] < tres) and lt.data[2] < tres):
                        while (lt.data[2] < tres and lt.data[3] > tres and lt.data[4] > tres) != True:
                            #mot.command('backward', 1.0, 0.2)
                            mot.command('forward', 4.0, 0.3)
                            print("MOVE STRAIGHT: ", lt.data)
                    elif(shortPath[x]=='B') and (lt.data[2] < tres and lt.data[3] < tres and lt.data[4] < tres):
                        print("U-TURN / BACK")
                        while(lt.data[0] < tres or lt.data[1] < tres or lt.data[2] < tres or lt.data[3] < tres or lt.data[4] < tres) != True:
                            mot.command('backward', 3.0, 0.2)
                            mot.command('left', 7.0, 0.4)
                            print("U-TURN / BACK: ", lt.data)
                            time.sleep(1)
                    else:
                        #to go straight forward
                        if (lt.data[2] < tres) and (lt.data[1] > tres) and (lt.data[3] > tres):
                            mot.command('forward', 7, 0.3)
                            print("Straight: ", lt.data)
                        #shift left
                        elif (lt.data[1] < tres and lt.data[0] > tres and lt.data[2] > tres and lt.data[3] > tres and lt.data[4] > tres):
                            mot.command('left', 3, 0.3)
                            print("Shift left", lt.data)
                        elif (lt.data[0] < tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[3] > tres and lt.data[4] > tres):
                            mot.command('left', 3.5, 0.3)
                            print("Shift left: ", lt.data)
                        #shift right
                        elif (lt.data[3] < tres and lt.data[0] > tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[4] > tres):
                            mot.command('right', 2.5, 0.3)
                            print("Shift right: ", lt.data)
                        elif (lt.data[4] < tres and lt.data[0] > tres and lt.data[1] > tres and lt.data[2] > tres and lt.data[3] > tres):
                            mot.command('right', 3, 0.3)
                            print("Shift right: ", lt.data)
                #finish
                mot.stop()
                lt.stop()
                print("END")
                reverseToStart = False
            
        time.sleep(0.5)

    except KeyboardInterrupt:
        mot.stop()
        lt.stop()
        break

