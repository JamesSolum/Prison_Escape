#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Simulation

Author: James Solum

This will be the main file that will build and run our simulation

"""
#from player import *
import player as p
from sys import argv

def runSimulation():
    # CONSTANTS
    ###############################################

    ## Players ##
    BILLY      = True # Lol don't change this one
    PERIMGUARD = True
    PATHGUARD  = True
    BISHOP     = True
    ROOK       = True
    KNIGHT     = True # Should this have a line of sight?
    TELEPORTER = True # no line of sight

    ## Powers ##
    BILLY_SPRINT = False
    SMART_BILLY  = False# Fix probabilities
    BILLY_LOS    = False 
    BILLY_SUPER  = False # not implemented yet, both Smart and LOS
    WEAPON       = False 

    GUARD_LOS       = False 
    CENTER_ALARM    = False 
    QUARTILE_ALARMS = False 
    GUARD_SPRINT    = False

    ### More Constants ###
    BORDER = 4 # Distance from center

    ### Alarm Params ###
    CENTER_ALARM_TRIGGERED = False   
    ALARM_BORDER           = 1
    ALARM_CENTER_LOCATION  = (0,0)

    QUARTILE_1_TRIGGER     = False
    QUARTILE_1_LOCATION    = (-2, -2)

    QUARTILE_2_TRIGGER     = False
    QUARTILE_2_LOCATION    = (-2, 2)

    QUARTILE_3_TRIGGER     = False
    QUARTILE_3_LOCATION    = (2, 2)

    QUARTILE_4_TRIGGER     = False
    QUARTILE_4_LOCATION    = (2, -2)

    ## Player Specific Constants ##
    SQUARE_GUARD_PATROL_BORDER = 5
    GUARD_PATH = [(1,1),(2,1),(1,2),(2,2),(1,3),(0,4),(0,3),(-1,2),(-1,1),(-1,0),(-1,-1),(0,-1)]
    CHANGE_IN_PROB = 0.1
    WEAPON_PROB = 0.1
    ######################################################

    Guards = []
    LineOSGuards = []
    quartileAlarms = []

    # Simulation Update Functions
    def guardLosUpdate(*guard):
        for g in guard:
            g.lineOfSight()
        
    def billyUpdate(billy, guards):
        if SMART_BILLY:
                billy.smartUpdate()
                billy.weaponCheck(guards, p=WEAPON_PROB)
                #caughtHuh(billy, guards)
        if BILLY_LOS:
            billy.lineOfSight(guards)
            billy.weaponCheck(guards, p=WEAPON_PROB)
        if BILLY_SUPER:
            raise Exception("Super Billy is not implemented yet")
            billy.super() # Not implemented
            billy.weaponCheck(guards, p=WEAPON_PROB)
        else:
            billy.randomStep()
            billy.weaponCheck(guards, p=WEAPON_PROB)

    def guardUpdate(billy, guards):
        if GUARD_LOS:
            for guard in LineOSGuards:
                guard.lineOfSight(billy)
            if TELEPORTER:
                if QUARTILE_ALARMS:
                    for alarm in quartileAlarms:
                        alarm.billyCheck(billy)
                    teleporter.quartileAlarmMove(quartile1, quartile2, quartile3, quartile4)
                else:
                    teleporter.randomStep()
            if KNIGHT:
                knight.randomStep()
        else:
            for guard in Guards:
                guard.randomStep()

    def checkCaught(billy, guards):
        billLoc = billy.location

        for guard in guards:
            if guard.location == billLoc:
                billy.CAUGHT = True

    # Simulation
    #Instantiate Players
    if BILLY:
        billy = p.billy(BORDER)
        if WEAPON:
            billy.weapon = WEAPON
    if PERIMGUARD:
        perimGuard = p.squareGuard(BORDER)
        Guards.append(perimGuard)
        LineOSGuards.append(perimGuard)
    if PATHGUARD:
        pathGuard = p.pathGuard(GUARD_PATH, BORDER) 
        Guards.append(pathGuard)
        LineOSGuards.append(pathGuard)
    if BISHOP:
        bishop = p.bishop(BORDER)
        Guards.append(bishop)
        LineOSGuards.append(bishop)
    if ROOK:
        rook = p.rook(BORDER, CHANGE_IN_PROB)
        Guards.append(rook)
        LineOSGuards.append(rook)
    if KNIGHT:
        knight = p.knight(BORDER)
        Guards.append(knight)
        # No line of sight
    if TELEPORTER:
        teleporter = p.teleporter(BORDER)
        Guards.append(teleporter)
        # No line of sight
    if CENTER_ALARM:
        alarmCenter = p.centerAlarm(ALARM_BORDER, ALARM_CENTER_LOCATION, CENTER_ALARM_TRIGGERED)
    if QUARTILE_ALARMS:
        quartile1 = p.quartileAlarm(QUARTILE_1_LOCATION, QUARTILE_1_TRIGGER)
        quartile2 = p.quartileAlarm(QUARTILE_2_LOCATION, QUARTILE_2_TRIGGER)
        quartile3 = p.quartileAlarm(QUARTILE_3_LOCATION, QUARTILE_3_TRIGGER)
        quartile4 = p.quartileAlarm(QUARTILE_4_LOCATION, QUARTILE_4_TRIGGER)
        quartileAlarms.extend((quartile1, quartile2, quartile3, quartile4))

    while(not(billy.CAUGHT) and not(billy.OutOfBounds)):
        # Alarm Set up
        if CENTER_ALARM:
            if alarmCenter.guardCheck(Guards):
                GUARD_SPRINT = True

        if QUARTILE_ALARMS:
            for alarm in quartileAlarms:
                if alarm.billyCheck(billy):
                    GUARD_SPRINT = True
        
        if GUARD_SPRINT:
            guardUpdate(billy, Guards)
            checkCaught(billy, Guards)
            guardUpdate(billy, Guards)
        else:
            guardUpdate(billy, Guards)

        # Billy Update
        if BILLY_SPRINT:
            billyUpdate(billy, Guards)
            checkCaught(billy, Guards)
            billyUpdate(billy, Guards)
        else:
            billyUpdate(billy, Guards)

        checkCaught(billy, Guards)

    
    #print("Escaped:", billy.OutOfBounds)
   # print("Caught:", billy.CAUGHT)
    
    if billy.CAUGHT:
        return 0
    if billy.OutOfBounds:
        return 1

def main():

    Sims = 10

    if len(argv) > 1:
        SIMULATION_ITERATIONS = int(argv[1])
    else:
        SIMULATION_ITERATIONS = Sims


    escaped = 0
    caught = 0
    for i in range(0, SIMULATION_ITERATIONS):
        x = runSimulation()
        if x == 0:
            caught += 1
        elif x == 1:
            escaped += 1
    print("Caught:", caught, "\nEscaped:", escaped)
    print("\nNumber of Simulations:", SIMULATION_ITERATIONS)

if __name__ == "__main__":
    main()
