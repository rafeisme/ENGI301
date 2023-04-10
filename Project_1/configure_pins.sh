#!/bin/bash
# --------------------------------------------------------------------------
# Combination Lock - Configure Pins
# --------------------------------------------------------------------------
# License:   
# Copyright 2020 Erik Welsh
# Updated 2023 Rafe Neathery
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation 
# and/or other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COls -PYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# --------------------------------------------------------------------------
# 
# Configure pins for Kerbal Controller:
#   - I2C1 & I2C2
#   - Buttons and Switches
#   - LEDs (Red / Green / Stage)
#   - Display
# 
# --------------------------------------------------------------------------

# I2C for LED Bars
#Orange
config-pin P1_26 i2c #SDA 
config-pin P1_28 i2c #SCL
#Blue
config-pin P2_09 i2c #SCL
config-pin P2_11 i2c #SDA

# Buttons/Switches:
#Brake - p2 2
#Lights - p2 4
#Gear - p2 6
#Action Group 1 - p2 8
#Action Group 2 - p2 10
#Action Group 3 - p2 17
#Action Group 4 - p2 18
#Action Group 5 - p2 19
#Action Group 6 - p2 20
#Action Group 7 - p2 22
#time warp stop - p2 28
#Time warp slow down - p2 30
#time warp increase - p2 32
#ABORT - p2 24
#Stage - p2 34
#SAS Toggle - P2 25
#RCS Toggle - P2 27
#Docking Mode - P2 29
#Map Mode - P2 31

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

# LEDs

#config-pin P1_31 gpio #Red
#config-pin P1_03 gpio #Green
#stage
config-pin P1_03 gpio

#Display
#RS - P1_4
#E - P1_6
#D0 - P1_31
#D1 - P1_34
#D2 - P1_35
#D3 - P2_33
#D4 - P1_8
#D5 - P1_10
#D6 - P1_12
#D7 - P1_29

config-pin P1_04 gpio
config-pin P1_06 gpio
config-pin P1_31 gpio
config-pin P1_34 gpio
config-pin P1_35 gpio
config-pin P1_33 gpio
config-pin P1_08 gpio
config-pin P1_10 gpio
config-pin P1_12 gpio
config-pin P1_29 gpio


#Pots - no need to configure
#Joystick 1 x - P1_19
#Joystick 1 y - P1_21
#Joystick 2 x - P1_23
#Joystick 2 y - P1_25
#Display Mode - P1_27
#SAS Mode - P2_36
#Throttle - P1_2 3.3 VOLTS
#config-pin P1_02 AIN

