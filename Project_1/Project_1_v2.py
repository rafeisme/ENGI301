"""
--------------------------------------------------------------------------
PocketKerbal
--------------------------------------------------------------------------
License:   
Copyright 2023 - Rafe Neathery
Built on framework of combo_lock code by Erik Welsh

This is a cobs encode and decode script created by cmcqueen. 
https://github.com/cmcqueen/cobs-python/blob/main/python3/cobs/cobs/_cobs_py.py

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use the following hardware components to recieve and send information to Kerbal Space Program:  
  - HT16K33 Display
  - Button
  - Red LED
  - Green LED
  - Potentiometer (analog input)

Requirements:
UPDATE ME LATER
  - Hardware:
    - When locked:   Red LED is on; Green LED is off; Servo is "closed"; Display is unchanged
    - When unlocked: Red LED is off; Green LED is on; Servo is "open"; Display is "----"
    - Display shows value of potentiometer (raw value of analog input divided by 8)
    - Button
      - Waiting for a button press should allow the display to update (if necessary) and return any values
      - Time the button was pressed should be recorded and returned
    - User interaction:
      - Needs to be able to program the combination for the “lock”
        - Need to be able to input three values for the combination to program or unlock the “lock”
      - Combination lock should lock when done programming and wait for combination input
      - If combination is unsuccessful, the lock should go back to waiting for combination input
      - If combination was successful, the lock should unlock
        - When unlocked, pressing button for less than 2s will re-lock the lock; greater than 2s will allow lock to be re-programmed

Uses:
  - Libraries developed in class

"""
import time

import serial

import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

import Adafruit_BBIO.GPIO as GPIO

#from array import array

from cobs import cobs

import array         as arr

import ht16k33       as HT16K33
import button        as BUTTON
import potentiometer as POT
import led           as LED
import Joystick      as JOYSTICK
#import LCD           as DISPLAY
# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

POT_DIVIDER        = 8       # Divider used to help reduce potentiometer granularity

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

#port = '/dev/ttyGS0'
        
    #com = serial.Serial(port,115200,timeout=5)
#comSerial = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=2, stopbits=serial.STOPBITS_ONE)

class PocketKerbal():
    """ PocketKerbal """
    reset_time     = None
    button         = None
    stage_led        = None
    potentiometer_throt  = None
    potentiometer_SAS = None
    potentiometer_display = None
    joystickL       =None
    joystickR       =None
    display        = None
    debug          = None
    stage_state     = None
    #cob            = None
    
    def __init__(self, reset_time=2.0, button="P2_1", 
                       stage_led="P1_3",
                       potentiometer_throt="P1_02",potentiometer_display="P1_27",potentiometer_SAS="P2_36",joystickL=1,joystickR=2, cob = None,
                       i2c_bus=1, i2c_address=0x70):
        """ Initialize variables and set up display """

        self.reset_time     = reset_time
        self.button         = BUTTON.Button(button)
        #self.stage_led        = LED.LED(stage_led)
        self.potentiometer_throt  = POT.Potentiometer(potentiometer_throt)
        self.potentiometer_display  = POT.Potentiometer(potentiometer_display)
        self.potentiometer_SAS  = POT.Potentiometer(potentiometer_SAS)
        self.joystickL      = JOYSTICK.Joystick(joystickL)
        self.joystickR      = JOYSTICK.Joystick(joystickR)
        self.display        = HT16K33.HT16K33(i2c_bus, i2c_address)
        #self.lcd            = DISPLAY.LCD()
       # self.cob            = COB.Cobs(cob)
        self.debug          = True
        
        lcd_rs = digitalio.DigitalInOut(board.P1_4)
        lcd_en = digitalio.DigitalInOut(board.P1_6)
        lcd_d7 = digitalio.DigitalInOut(board.P1_29)
        lcd_d6 = digitalio.DigitalInOut(board.P1_12)
        lcd_d5 = digitalio.DigitalInOut(board.P1_10)
        lcd_d4 = digitalio.DigitalInOut(board.P1_8)
        lcd_d3 = digitalio.DigitalInOut(board.P1_33)
        lcd_d2 = digitalio.DigitalInOut(board.P1_35)
        lcd_d1 = digitalio.DigitalInOut(board.P1_34)
        lcd_d0 = digitalio.DigitalInOut(board.P1_31)
    
        lcd_columns = 16
        lcd_rows = 2
        
        #self._setup()
    
    def _setup(self):
        """Setup the hardware components."""

        # Initialize Display
        #self.set_display_dash()
        
        """
        setup gpio pins
        config-pin P2_02 gpio
        config-pin P2_04 gpio
        config-pin P2_06 gpio
        config-pin P2_08 gpio
        config-pin P2_10 gpio
        config-pin P2_17 gpio
        config-pin P2_18 gpio
        config-pin P2_19 gpio
        config-pin P2_20 gpio
        config-pin P2_22 gpio
        config-pin P2_24 gpio
        config-pin P2_25 gpio
        config-pin P2_27 gpio
        config-pin P2_28 gpio
        config-pin P2_29 gpio
        config-pin P2_30 gpio
        config-pin P2_31 gpio
        config-pin P2_32 gpio
        config-pin P2_34 gpio
        
        """
        GPIO.setup("P2_2", GPIO.IN)
        GPIO.setup("P2_4", GPIO.IN)
        GPIO.setup("P2_6", GPIO.IN)
        GPIO.setup("P2_8", GPIO.IN)
        GPIO.setup("P2_10", GPIO.IN)
        GPIO.setup("P2_17", GPIO.IN)
        GPIO.setup("P2_18", GPIO.IN)
        GPIO.setup("P2_19", GPIO.IN)
        GPIO.setup("P2_20", GPIO.IN)
        GPIO.setup("P2_22", GPIO.IN)
        GPIO.setup("P2_24", GPIO.IN)
        GPIO.setup("P2_25", GPIO.IN)
        GPIO.setup("P2_27", GPIO.IN)
        GPIO.setup("P2_28", GPIO.IN)
        GPIO.setup("P2_29", GPIO.IN)
        GPIO.setup("P2_30", GPIO.IN)
        GPIO.setup("P2_31", GPIO.IN)
        GPIO.setup("P2_32", GPIO.IN)
        GPIO.setup("P2_34", GPIO.IN)

        # Button / LEDs / Potentiometer
        #GPIO.setup("P1_3", GPIO.OUT)
        #   - All initialized by libraries when instanitated

    # End def
    
    def init(self):
        
        return False

    
    def HandshakekRPC(self):
        
        import krpc
        conn = krpc.connect(name='Hello World', address="192.168.7.1")
        vessel = conn.space_center.active_vessel
        print(vessel.name)
        return True
        
    #End def

    def run(self):
       
        self._setup()
        #HANDSHAKE
        self.message("Connecting...")
        
        import krpc
        conn = krpc.connect(name='Hello World', address="192.168.7.1")
        vessel = conn.space_center.active_vessel
        print(vessel.name)
            
        self.message("Connected!")
            
        stage_state =  GPIO.input("P2_34")  
        """
        if(debug == True):
            self.ReadControls()
            self.DebugDisplay()
            self.WriteLCD()
        else:
        """
        while(1):
            #self.Set_Display(vessel,conn)
            self.Controls(vessel)
       

    # End def

    
    def message(self, msg):
        
                
        lcd_rs = digitalio.DigitalInOut(board.P1_4)
        lcd_en = digitalio.DigitalInOut(board.P1_6)
        lcd_d7 = digitalio.DigitalInOut(board.P1_29)
        lcd_d6 = digitalio.DigitalInOut(board.P1_12)
        lcd_d5 = digitalio.DigitalInOut(board.P1_10)
        lcd_d4 = digitalio.DigitalInOut(board.P1_8)
        lcd_d3 = digitalio.DigitalInOut(board.P1_33)
        lcd_d2 = digitalio.DigitalInOut(board.P1_35)
        lcd_d1 = digitalio.DigitalInOut(board.P1_34)
        lcd_d0 = digitalio.DigitalInOut(board.P1_31)
    
        lcd_columns = 16
        lcd_rows = 2
        
        #lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d0, lcd_d1, lcd_d2, lcd_d3, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
        lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
        lcd.message = msg
        
    #End def
    
    def Set_Display(self,vessel,conn):
        
        raw_disp = self.potentiometer_display.get_value() 
        disp_val = int(raw_disp // 682)
        if disp_val == 0:
            msg1 = str(conn.get_call(getattr, vessel.flight(), 'g_force'))
            #msg2 = str(conn.get_call(getattr, vessel.flight(), 'mach'))
            msg2 = ""
            msg = "G-Force = " + msg1 + "G's" + "\n" + "Mach Number = " + msg2
            self.message(msg)
        elif disp_val == 1:
            msg1 = str(conn.get_call(getattr, vessel.flight(), 'mean_altitude'))
            #msg2 = str(conn.get_call(getattr, vessel.flight(), 'surface_altitude'))
            msg2 = ""
            msg = "Mean Alt = " + msg1 + "\n" + "Surf Alt = " + msg2
            self.message(msg)
        elif disp_val == 2:
            msg1 = str(conn.get_call(getattr, vessel.orbit, 'speed'))
            #msg1 = srt()
            #msg2 = str(conn.get_call(getattr, vessel.orbit, 'period'))
            msg2 = ""
            msg = "Speed = " + msg1 + "\n" + "Period = " + msg2
            self.message(msg)
        elif disp_val == 3:
            msg1 = str(conn.get_call(getattr, vessel.orbit, 'apoapsis_altitude'))
            #msg2 = str(conn.get_call(getattr, vessel.orbit, 'periapsis_altitude'))
            msg2 = ""
            msg = "Apoapsis = " + msg1 + "\n" + "Periapsis = " + msg2
            self.message(msg)
        elif disp_val == 4:
            msg1 = str(conn.get_call(getattr, vessel.orbit, 'time_to_apoapsis'))
            #msg2 = str(conn.get_call(getattr, vessel.orbit, 'time_to_periapsis'))
            msg2 = ""
            msg = "Time to Apo = " + msg1 + "\n" + "Time to Peri = " + msg2
            self.message(msg)
        elif disp_val == 5:
            msg1 = str(conn.get_call(getattr, vessel.orbit, 'eccentricity'))
            #msg2 = str(conn.get_call(getattr, vessel.orbit, 'inclination'))
            msg2 = ""
            msg = "Eccentricity = " + msg1 + "\n" + "Inclination = " + msg2
            self.message(msg)
        
    
    #End def
    
    def Controls(self,vessel):
        
        """
        #Get Throttle
        raw_throttle = self.potentiometer_throt.get_value()
        throttle_val = raw_throttle / 2048
        vessel.control.throttle = throttle_val
       """
        
        #Get Stage
        """
        if stage_state == 0:
            if GPIO.input("P2_34") > stage_state:
                stage_state = GPIO.input("P2_34")
                vessel.control.activate_next_stage()
        else:
            if GPIO.input("P2_34") < stage_state:
                stage_state = GPIO.input("P2_34")
                vessel.control.activate_next_stage()
        """
        
        if vessel.control.stage_lock == False:
            #self.stage_led.on()
            #GPIO.output("P1_3", self.GPIO.HIGH)
            if  GPIO.input("P2_34") == 0:
                vessel.control.activate_next_stage()
                time.sleep(0.75)
        #else:
            #self.stage_led.off()
            # GPIO.output("P1_3", self.GPIO.LOW)


        
        """
        #Check Brakes
        if  GPIO.input("P2_2") > 0:
            vessel.control.brakes = False
        else:
            vessel.control.brakes = True
            
        #Check Lights
        if  GPIO.input("P2_4") > 0:
            vessel.control.lights = False
        else:
            vessel.control.lights = True
            
        #Check Gear
        if  GPIO.input("P2_6") > 0:
            vessel.control.gear = False
        else:
            vessel.control.gear = True
                
        #Update Action Groups
        if  GPIO.input("P2_8") > 0:
            vessel.control.set_action_group(1,False)
        else:
            vessel.control.set_action_group(1,True)
            
        if  GPIO.input("P2_10") > 0:
            vessel.control.set_action_group(2,False)
        else:
            vessel.control.set_action_group(2,True)
            
        if  GPIO.input("P2_17") > 0:
            vessel.control.set_action_group(3,False)
        else:
            vessel.control.set_action_group(3,True)
            
        if  GPIO.input("P2_18") > 0:
            vessel.control.set_action_group(4,False)
        else:
            vessel.control.set_action_group(4,True)
            
        if  GPIO.input("P2_19") > 0:
            vessel.control.set_action_group(5,False)
        else:
            vessel.control.set_action_group(5,True)
            
        if  GPIO.input("P2_20") > 0:
            vessel.control.set_action_group(6,False)
        else:
            vessel.control.set_action_group(6,True)
            
        if  GPIO.input("P2_22") > 0:
            vessel.control.set_action_group(7,False)
        else:
            vessel.control.set_action_group(7,True)
        
        #Check SAS and set mode
        if  GPIO.input("P2_25") > 0:
            vessel.control.sas = False
        else:
            vessel.control.sas = True
            raw_sas = self.potentiometer_SAS.get_value() #0-4095
            print(raw_sas)
            sas_val = int(raw_sas // 409)
            print(sas_val)
            if sas_val == 0:
                vessel.control.sas_mode = vessel.control.sas_mode.stability_assist
            elif sas_val == 1:
                try:
                    vessel.control.sas_mode = vessel.control.sas_mode.manuever
                except RuntimeError:
                    print('Could not set SAS Mode - Manuever')
                    vessel.control.sas_mode = vessel.control.sas_mode.stability_assist
            elif sas_val == 2:
                try:
                    vessel.control.sas_mode = vessel.control.sas_mode.prograde
                except RuntimeError:
                    print('Could not set SAS Mode - Prograde')
                    vessel.control.sas_mode = vessel.control.sas_mode.stability_assist
            elif sas_val == 3:
                try:
                    vessel.control.sas_mode = vessel.control.sas_mode.retrograde
                except RuntimeError:
                    print('Could not set SAS Mode - Retrograde')
                    vessel.control.sas_mode = vessel.control.sas_mode.stability_assist
            elif sas_val == 4:
                vessel.control.sas_mode = vessel.control.sas_mode.normal
            elif sas_val == 5:
                vessel.control.sas_mode = vessel.control.sas_mode.anti_normal
            elif sas_val == 6:
                vessel.control.sas_mode = vessel.control.sas_mode.radial
            elif sas_val == 7:
                vessel.control.sas_mode = vessel.control.sas_mode.anti_radial
            elif sas_val == 8:
                try:
                    vessel.control.sas_mode = vessel.control.sas_mode.target
                except RuntimeError:
                    print('Could not set SAS Mode - Target')
                    vessel.control.sas_mode = vessel.control.sas_mode.stability_assist
            elif sas_val == 9:
                try:
                    vessel.control.sas_mode = vessel.control.sas_mode.anti_target
                except RuntimeError:
                    print('Could not set SAS Mode - Anti_target')
                    vessel.control.sas_mode = vessel.control.sas_mode.stability_assist
            else:
                vessel.control.sas_mode = vessel.control.sas_mode.stability_assist
         
        #Check RCS
        if  GPIO.input("P2_27") > 0:
            vessel.control.rcs = False
        else:
            vessel.control.rcs = True
            
        #ABORT
        if  GPIO.input("P2_24") > 0:
            vessel.control.abort = False
        else:
            vessel.control.abort = True
            
        #Docking Mode
        #tbd
        
        #Map Mode
        #Tbd
        
        #Time Warp Controls
        #Time Warp Stop
        if  GPIO.input("P2_28") == 0:
           rails_warp_factor = 0
         
        
        """
        
        #Yaw
        raw_yaw = self.joystickL.get_value(0) #0-4095
        yaw_val = (raw_yaw / 2048) - 1
        vessel.control.yaw = yaw_val
        
        #Pitch
        raw_pitch = self.joystickL.get_value(1) #0-4095
        pitch_val = (raw_pitch / 2048) - 1
        vessel.control.pitch = pitch_val
        
        #Roll
        raw_roll = self.joystickR.get_value(0) #0-4095
        roll_val = (raw_roll / 2048) - 1
        vessel.control.roll = roll_val
        
        #Forward
        raw_ford = self.joystickR.get_value(1) #0-4095
        ford_val = (raw_ford / 2048) - 1
        vessel.control.forward = ford_val
    
    #End def

    def cleanup(self):
        """Cleanup the hardware components."""
        
        # Set Display to something fun to show program is complete
        #self.display.text("DEAD")
        self.message("That did\n NOT work")
        

        # Clean up hardware
        # self.button.cleanup()
        #self.red_led.cleanup()
        #self.green_led.cleanup()
        #self.potentiometer.cleanup()

    # End def

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")
    
    project1 = PocketKerbal()
    
  #  print('\nStatus -> ',comSerial) 
    
    try:
        # Handshake
        project1.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        project1.cleanup()

    print("Program Complete")
