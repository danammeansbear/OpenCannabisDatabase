# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:31:29 2020

@author: adam
"""


# my_states.py
import time
from time import sleep

from state import State

class Plants_healthy(State):
    """
    The state which indicates that there are limited device capabilities.
    """
    print("plants healthy")

    def on_event(self, event):
        if event == 'Needs_Nitrogen':
            return Nitrogen_Solution_pump()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

        return self

# Start of our states
class ObservingState(State):
    """
    The state which indicates that there are limited device capabilities.
    """
    print("cameras looking")
    def on_event(self, event):
        if event == 'Needs_Nitrogen':
            return Nitrogen_Solution_pump()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

        return self


class Nitrogen_Solution_pump(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """
    print("nitrogen pump on")
    def on_event(self, event):
        if event == 'done_pumping':
            return ObservingState()
        elif event == 'Needs_Nitrogen':
            return Done_Pumping()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

        return self

class Light_On(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """
    
    time.sleep(30)
    print("light is on")
    def on_event(self, event):
        if event == 'Light_On':
            return Light_Off()
        elif event == 'Needs_Nitrogen':
            return Nitrogen_Solution_pump()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

        return self

class Light_Off(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """
    print("now the light has recieved the off signal")
    time.sleep(10)
    

    def on_event(self, event):
        if event == 'Light_Off':
            return ObservingState()
        elif event == 'Needs_Nitrogen':
            return Nitrogen_Solution_pump()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

        return self

class Release_Valve_On_10_seconds(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        if event == 'Release_Valve_On_10_seconds':
            return Done_Pumping()
        elif event == 'Needs_Nitrogen':
            return Nitrogen_Solution_pump()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

        return self

class Done_Pumping(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        if event == 'Done_Pumping':
            return ObservingState()
        elif event == 'Needs_Nitrogen':
            return Nitrogen_Solution_pump()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

        return self

class Water_Pump_On_10_seconds(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        if event == 'Water_Pump_On_10_seconds':
            return Done_Pumping()
        elif event == 'Needs_Nitrogen':
            return Nitrogen_Solution_pump()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

        return self

class Phosphorus_Solution_Pump(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        if event == 'Phosphorus_Solution_Pump':
            return Done_Pumping()
        elif event == 'Needs_Nitrogen':
            return Nitrogen_Solution_pump()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

        return self


class Potasium_Solution_Pump(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """

    def on_event(self, event):
        if event == 'Phosphorus_Solution_Pump':
            return Done_Pumping()
        elif event == 'Needs_Nitrogen':
            return Nitrogen_Solution_pump()
        elif event == 'Needs_Potasium':
            return Potasium_Solution_Pump()
        elif event == 'Needs_phosphorus':
            return Phosphorus_Solution_Pump()
        elif event == 'Needs_Water':
            return Water_Pump_On_10_seconds()
        elif event == 'Needs_Light':
            return Light_On()
        elif event == 'Needs_Darnkess':
            return Light_Off()
        elif event == 'Needs_Less_water':
            return Release_Valve_On_10_seconds()
        elif event == 'Plants_Healthy':
            print("plants healthy for now..")
            time.sleep(5)
            return ObservingState()

    #End of our states.