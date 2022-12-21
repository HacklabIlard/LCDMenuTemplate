from machine import Pin,SPI,PWM
import framebuf
import utime
import os
import math

import modlcd

# ============ Start of Drive Code ================
#  == Copy and paste into your code ==
BL = 13  # Pins used for display screen
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

def colour(R,G,B):
# Get RED value
    rp = int(R*31/255) # range 0 to 31
    if rp < 0: rp = 0
    r = rp *8
# Get Green value - more complicated!
    gp = int(G*63/255) # range 0 - 63
    if gp < 0: gp = 0
    g = 0
    if gp & 1:  g = g + 8192
    if gp & 2:  g = g + 16384
    if gp & 4:  g = g + 32768
    if gp & 8:  g = g + 1
    if gp & 16: g = g + 2
    if gp & 32: g = g + 4
# Get BLUE value       
    bp =int(B*31/255) # range 0 - 31
    if bp < 0: bp = 0
    b = bp *256
    colour = r+g+b
    return colour


'''
Adjustable font for the WaveShare 1.3" IPS LCD Display Module for Raspberry Pi Pico (240x240)
                         Tony Goodhew 17th Aug 2021
           Modified from code by Les Wright 2021 V 1.1 for Pimoroni Pico Display                  
              https://forums.pimoroni.com/t/pico-display-and-fonts/16194/18
'''
#ASCII Character Set
cmap = ['00000000000000000000000000000000000', #Space
        '00100001000010000100001000000000100', #!
        '01010010100000000000000000000000000', #"
        '01010010101101100000110110101001010', ##
        '00100011111000001110000011111000100', #$
        '11001110010001000100010001001110011', #%
        '01000101001010001000101011001001101', #&
        '10000100001000000000000000000000000', #'
        '00100010001000010000100000100000100', #(
        '00100000100000100001000010001000100', #)
        '00000001001010101110101010010000000', #*
        '00000001000010011111001000010000000', #+
        '000000000000000000000000000000110000100010000', #,
        '00000000000000011111000000000000000', #-
        '00000000000000000000000001100011000', #.
        '00001000010001000100010001000010000', #/
        '01110100011000110101100011000101110', #0
        '00100011000010000100001000010001110', #1
        '01110100010000101110100001000011111', #2
        '01110100010000101110000011000101110', #3
        '00010001100101011111000100001000010', #4
        '11111100001111000001000011000101110', #5
        '01110100001000011110100011000101110', #6
        '11111000010001000100010001000010000', #7
        '01110100011000101110100011000101110', #8
        '01110100011000101111000010000101110', #9
        '00000011000110000000011000110000000', #:
        '01100011000000001100011000010001000', #;
        '00010001000100010000010000010000010', #<
        '00000000001111100000111110000000000', #=
        '01000001000001000001000100010001000', #>
        '01100100100001000100001000000000100', #?
        '01110100010000101101101011010101110', #@
        '00100010101000110001111111000110001', #A
        '11110010010100111110010010100111110', #B
        '01110100011000010000100001000101110', #C
        '11110010010100101001010010100111110', #D
        '11111100001000011100100001000011111', #E
        '11111100001000011100100001000010000', #F
        '01110100011000010111100011000101110', #G
        '10001100011000111111100011000110001', #H
        '01110001000010000100001000010001110', #I
        '00111000100001000010000101001001100', #J
        '10001100101010011000101001001010001', #K
        '10000100001000010000100001000011111', #L
        '10001110111010110101100011000110001', #M
        '10001110011010110011100011000110001', #N
        '01110100011000110001100011000101110', #O
        '11110100011000111110100001000010000', #P
        '01110100011000110001101011001001101', #Q
        '11110100011000111110101001001010001', #R
        '01110100011000001110000011000101110', #S
        '11111001000010000100001000010000100', #T
        '10001100011000110001100011000101110', #U
        '10001100011000101010010100010000100', #V
        '10001100011000110101101011101110001', #W
        '10001100010101000100010101000110001', #X
        '10001100010101000100001000010000100', #Y
        '11111000010001000100010001000011111', #Z
        '01110010000100001000010000100001110', #[
        '10000100000100000100000100000100001', #\
        '00111000010000100001000010000100111', #]
        '00100010101000100000000000000000000', #^
        '00000000000000000000000000000011111', #_
        '11000110001000001000000000000000000', #`
        '00000000000111000001011111000101110', #a
        '10000100001011011001100011100110110', #b
        '00000000000011101000010000100000111', #c
        '00001000010110110011100011001101101', #d
        '00000000000111010001111111000001110', #e
        '00110010010100011110010000100001000', #f
        '000000000001110100011000110001011110000101110', #g
        '10000100001011011001100011000110001', #h
        '00100000000110000100001000010001110', #i
        '0001000000001100001000010000101001001100', #j
        '10000100001001010100110001010010010', #k
        '01100001000010000100001000010001110', #l
        '00000000001101010101101011010110101', #m
        '00000000001011011001100011000110001', #n
        '00000000000111010001100011000101110', #o
        '000000000001110100011000110001111101000010000', #p
        '000000000001110100011000110001011110000100001', #q
        '00000000001011011001100001000010000', #r
        '00000000000111110000011100000111110', #s
        '00100001000111100100001000010000111', #t
        '00000000001000110001100011001101101', #u
        '00000000001000110001100010101000100', #v
        '00000000001000110001101011010101010', #w
        '00000000001000101010001000101010001', #x
        '000000000010001100011000110001011110000101110', #y
        '00000000001111100010001000100011111', #z
        '00010001000010001000001000010000010', #{
        '00100001000010000000001000010000100', #|
        '01000001000010000010001000010001000', #}
        '01000101010001000000000000000000000' #}~
]


def printchar(letter,xpos,ypos,size,charupdate,c):
    origin = xpos
    charval = ord(letter)
    #print(charval)
    index = charval-32 #start code, 32 or space
    #print(index)
    character = cmap[index] #this is our char...
    rows = [character[i:i+5] for i in range(0,len(character),5)]
    #print(rows)
    for row in rows:
        #print(row)
        for bit in row:
            #print(bit)
            if bit == '1':
                LCD.pixel(xpos,ypos,c)
                if size==2:
                    LCD.pixel(xpos,ypos+1,c)
                    LCD.pixel(xpos+1,ypos,c)
                    LCD.pixel(xpos+1,ypos+1,c)
                if size == 3:
                    LCD.pixel(xpos,ypos,c)
                    LCD.pixel(xpos,ypos+1,c)
                    LCD.pixel(xpos,ypos+2,c)
                    LCD.pixel(xpos+1,ypos,c)
                    LCD.pixel(xpos+1,ypos+1,c)
                    LCD.pixel(xpos+1,ypos+2,c)
                    LCD.pixel(xpos+2,ypos,c)
                    LCD.pixel(xpos+2,ypos+1,c)
                    LCD.pixel(xpos+2,ypos+2,c)
            xpos+=size
        xpos=origin
        ypos+=size
    if charupdate == True:
        LCD.show()


def delchar(xpos,ypos,size,delupdate):
    if size == 1:
        charwidth = 5
        charheight = 9
    if size == 2:
        charwidth = 10
        charheight = 18
    if size == 3:
        charwidth = 15
        charheight = 27
    c =colour(0,0,0) # Colour of background
    LCD.fill_rect(xpos,ypos,charwidth,charheight,c) #xywh
    if delupdate == True:
        LCD.show()


def printstring(string,xpos,ypos,size,charupdate,strupdate,c):   
    if size == 1:
        spacing = 8
    if size == 2:
        spacing = 14
    if size == 3:
        spacing = 18
    for i in string:
        printchar(i,xpos,ypos,size,charupdate,c)
        xpos+=spacing
    if strupdate == True:
        LCD.show()
# =============End of Characters section ===============


def ring(cx,cy,r,cc):   # Draws a circle - with centre (x,y), radius, colour 
    for angle in range(91):  # 0 to 90 degrees in 2s
        y3=int(r*math.sin(math.radians(angle)))
        x3=int(r*math.cos(math.radians(angle)))
        LCD.pixel(cx-x3,cy+y3,cc)  # 4 quadrants
        LCD.pixel(cx-x3,cy-y3,cc)
        LCD.pixel(cx+x3,cy+y3,cc)
        LCD.pixel(cx+x3,cy-y3,cc)




    
def game():
   
    LCD.fill(colour(40,40,40))
    LCD.show()
    
    running = True # Loop control
    # =========== Main loop ===============
    while(running):
        if keyA.value() == 0:        
            print("A")
        
        if(keyB.value() == 0):
            print("B")
                       
        if(keyX.value() == 0):
            print("X")
            
        if(keyY.value() == 0):
            print("Y")
        
        # Move UP
        if(up.value() == 0):
            print("UP")
 
            
        # Move DOWN        
        if(down.value() == 0):
            print("DOWN")

            
        # Move LEFT    
        if(left.value() == 0):
            print("LEFT")
           
            
        # Move RIGHT
        if(right.value() == 0):
            print("RIGHT")

        # CONTROL
        if(ctrl.value() == 0):
            print("CTRL")
                       
        LCD.show()
        if (keyA.value() == 0) and (keyY.value() == 0): # Halt looping?
            # Background colour - dark grey
            LCD.fill(colour(40,40,40))
            LCD.show()
            running = False
            
        utime.sleep(.15) # Debounce delay - reduce multiple button reads


# =========== Main ============

if __name__=='__main__':
    pwm = PWM(Pin(BL)) # Screen Brightness
    pwm.freq(1000)
    pwm.duty_u16(32768) # max 65535 - mid value

    LCD = modlcd.LCD_1inch3()
    # Background colour - dark grey
    LCD.fill(colour(40,40,40))
    LCD.show()

    # Define pins for buttons and Joystick
    keyA = Pin(15,Pin.IN,Pin.PULL_UP) # Normally 1 but 0 if pressed
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)
    keyX = Pin(19,Pin.IN,Pin.PULL_UP)
    keyY= Pin(21,Pin.IN,Pin.PULL_UP)

    up = Pin(2,Pin.IN,Pin.PULL_UP)
    down = Pin(18,Pin.IN,Pin.PULL_UP)
    left = Pin(16,Pin.IN,Pin.PULL_UP)
    right = Pin(20,Pin.IN,Pin.PULL_UP)
    ctrl = Pin(3,Pin.IN,Pin.PULL_UP)

    # Draw background, frame, title and instructions
    LCD.rect(0,0,240,240,LCD.red) # Red edge
    # White Corners
    LCD.pixel(1,1,LCD.white)     # LT
    LCD.pixel(0,239,LCD.white)   # LB
    LCD.pixel(239,0,LCD.white)   # RT
    LCD.pixel(239,239,LCD.white) # RB
    LCD.show()

    # ======= Menu ==============

    m = 0
    yellow = colour(255,255,0)
    blue = colour(0,0,255)
    running = True
    while running:
        c = colour(255,0,0) 
        printstring("DEMO",17,10,3,0,0,c)
        c = yellow
        if m == 0:
            c = blue
        printstring("Menu0",35,50,2,0,0,c)
        
        c = yellow
        if m == 1:
            c = blue
        printstring("Menu1",35,80,2,0,0,c)

        c = yellow
        if m == 2:
            c = blue
        printstring("Menu2",35,110,2,0,0,c)

        c = yellow
        if m == 3:
            c = blue
        printstring("Quit",35,170,2,0,0,c)
        
        LCD.show()
        
        # Check joystick UP/DOWN/CTRL
        if(up.value() == 0):
            m = m - 1
            if m < 0:
                m = 0
                
        elif(down.value() == 0):
            m = m + 1
            if m > 3:
                m = 3
                           
        elif(ctrl.value() == 0):
            if(m == 3): # Exit loop and HALT program
                running = False
            if(m == 2):
                print("menu2")            
            if(m == 1):
                print("menu1")
            if(m == 0):
                game()
                print("menu0")
                


    # Finish
    LCD.fill(0)
    for r in range(10):
        ring(120,120,60+r,colour(255,255,0))
    LCD.text("Halted", 95, 115, colour(255,0,0))
    LCD.show()
    # Tidy up
    utime.sleep(3)
    LCD.fill(0)
    LCD.show()

