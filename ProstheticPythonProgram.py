#Import Libraries

import RPi.GPIO as GPIO
import time
import sys
import math
import matplotlib.pyplot as plt
import pylab

#Set up GPIO Mode
GPIO.setmode(GPIO.BCM) #this is to turn the motor
GPIO.setwarnings(False) #gets ride of warnings to remove any errors

#Set up pins
MotorA = 12 #defines DC motor by using necessary pins
motADir = 5

#Set pin modes
GPIO.setup(MotorA,GPIO.OUT)
GPIO.setup(motADir,GPIO.OUT)#GPIO Numbering

#PWM
freq = 60 #chosen value
pwmMotA = GPIO.PWM(MotorA,freq)

def main_menu():   
    print ("Welcome,")
    print ("Please choose the menu you want to start:") #prints out all the choices for the subprograms and the integrated bonus (subprogram4)
    print ("1. Subprogram 1")
    print ("2. Subprogram 2")
    print ("3. Subprogram 3")
    print ("4. Subprogram 4")
    print ("5. Exit from program")
    while True:
        try:
            choice = int(input("Please enter your selection:  ")) #asks user to enter selection
            if choice== 1:
                SubProgram1()
                break
            elif choice== 2:
                SubProgram2()
                break
            elif choice== 3:
                SubProgram3()
                break
            elif choice== 4:
                SubProgram4()
            elif choice== 5:
                break #breaks the loop and stops the program
            else:
                print ("You have entered an invalid choice. Please try again.")
                main_menu()
        except ValueError:
            print ("You have entered an invalid choice. Please try again.")
            main_menu()
    exit
    

def SubProgram1():
    while True:
       try:
           otherTeamNumber = int(input("What is the team number you will be testing?"))
       except ValueError: # just catch the exceptions you know!
           print ('That\'s not a number!')
       else:
           if 1 <= otherTeamNumber <= 23:
               break                       # this is faster
           else:
               print ('Out of range. Try again')
               SubProgram1()
    Time= int(input("How many seconds do you want it to rotate? "))
    inFile= input("File name:")
    copiedFile= open(inFile,'r') #opens file and reads
    Team_List = []
    for line in copiedFile:
        Team_List.append(line.split(' ')) #creates a nested list by splitting by a space
    copiedFile.close()
    preTeamList = [[s.strip() for s in nested] for nested in Team_List] #just makes a list with int/float values
    subTeamList1= [int(i[0]) for i in preTeamList]  #creates sublists for store values as int and float using list comprehension
    subTeamList2 = [float(i[1]) for i in preTeamList]
    TeamList = [list(a) for a in zip(subTeamList1, subTeamList2)] #nested list
    for i in TeamList:
        for i[0] in i:
            if i[0]== otherTeamNumber:
                input_Speed= i[1] #searchs the first index which corresponds to user input
    inputSpeedx= input_Speed
    inputSpeed= round(inputSpeedx,3)
    gearRatio= 5.625 #necessary units
    output_Speed= inputSpeed/(gearRatio*60)
    outputSpeed= round(output_Speed,3) #rounds the value
    maxSpeed= 17/6 #max speed in RPS of the motor
    SpeedFactor = 10 #sets up speed factor to more 'visible output'
    speed= (outputSpeed*SpeedFactor/maxSpeed)*100
    pwmMotA.start(speed) #starts the motor
    GPIO.output(motADir,1)
    time.sleep(Time) #this is how long the motor will turn for
    pwmMotA.ChangeDutyCycle(0) #the motor stops
    print ("The team number you have chosen is " +str(otherTeamNumber)) #the printed values
    print ("The input speed is " +str(input_Speed))
    print ("The corresponding output speed is " +str(outputSpeed))
    print ("The gear ratio used for this calculation is " +str(gearRatio))
    anykey= input("Would you like to:\n1. Re-Run\n2. Return to Main Menu\n") #asks if the user wants to re-run the program or go back to main menu
    if anykey== "Re-Run" or anykey == "1":
        SubProgram1() #runs subprogram1 again
    if anykey== "Return to Main Menu" or anykey == "2":
        main_menu() #goes back to main menu

def SubProgram2():
#request user to enter certain values
    print ("The starting position can either be fully open or fully closed.") #prints out two possible scenarios for starting position
    startPos = 0
    while True:
        try:
            startPos = int(input("Enter -1 for fully Open or 1 for fully Closed: "))
        except ValueError: # just catch the exceptions you know!
           print ('Thats not a number!')
        else:
            if startPos == -1 or startPos== 1:
                break
            else:
               print ('Invalid entry. Try again.') #if the number entered is not in the options
               SubProgram2()
    numRot = float(input("Enter the number of desired rotations for the motor: ")) #asks for number of rotations
    numIncrements = int(input("Enter the number of increments: "))


    #define constants
    maxDegree= 506.25 #the amount it needs to move to move 90 based on our gear ratio of 5.625
    Angle=0 #starting angle
    thumbLength=70.5 #length of the thumb
    fingerLength= 70.5 #length of the finger
        
    #list of things to record all the necessary output values
    directionMotor=[]
    motorAngle=[]
    angleFinger=[]
    angleThumb=[]
    posFinger=[]
    posThumb=[]
    posFingerx= []
    posFingery= []
    posThumbx= []
    posThumby= []

    #set up the cartesian grid for the graph
    fig1= plt.figure(1, figsize = (8.5,11)) #defining the size of the image
    axes = plt.gca()
    pylab.axvline(linewidth=0.5, color = 'k') #plotting the x axis
    pylab.axhline(linewidth=0.5, color = 'k')# plotting the y axis
    axes.set_xlim([-130,130]) #setting x axis limit
    axes.set_ylim([-130,130]) #setting y axis limit
    rectangleX = [-70, -70, -40, -40, -70] #x coordinates for rectangle
    rectangleY = [-80, -50, -50, -80, -80] #y coordinates for rectangle
    plt.plot(rectangleX, rectangleY, 'o', color= 'r') #plotting the functional workspace
    plt.plot(rectangleX, rectangleY, '-', color= 'r', label= 'Function Workspace')
    
    #begin for-loop in range of number of increments
    for inc in range (numIncrements):
        inc += 1
        deltaAngle=startPos*numRot*360/numIncrements #find the change in angle based on the increment 

    #direction of motor rotation depending on the sign of delta angle
        if deltaAngle>0:
            motorDirection=("Clockwise") #prints out necessary direction
            directionMotor.append(motorDirection)
        else:
            motorDirection=("Counter-Clockwise")
            directionMotor.append(motorDirection)

        changedAngle=Angle + deltaAngle #calculating the new value of the angle
    #angle of motor rotation relative to the starting position
        if abs(changedAngle)>maxDegree: #using all three possible conditions for the change in angle and computes relevant values
            Angle=round(startPos*(2*maxDegree)-(Angle+deltaAngle), 3) #sets constraints for the motion of the motor from not moving past 90 deg of motion
            startPos=-startPos
            motorAngle.append(Angle)
        elif changedAngle<0:
            Angle=round(startPos*(Angle+deltaAngle),3)
            startPos= -startPos
            motorAngle.append(Angle)
        else:
            Angle+=round(deltaAngle,3)
            motorAngle.append(Angle)
            
    #forefinger and thumb angles relative to the starting position
        if startPos==-1 or startPos==1:
            FingerAngle=round((Angle/maxDegree)*90,3) #using the ratio of the angle of the motor and the max angle to find the angle of the finger/thumb
            thumbAngle=round((Angle/maxDegree)*90,3)
            angleFinger.append(FingerAngle)
            angleThumb.append(thumbAngle)

        else:
            None #if an invalid entry is inputted

    #forefinger position relative to the origin
        fingerPosx=round(-70.5 * math.cos(FingerAngle*math.pi/180)-55,2) #using the shift in position based on the mounting bracket
        fingerPosy=round(-70.5 * math.sin(FingerAngle*math.pi/180),2) #using cos for y coordinate and sin for x coordinate
        fingerPos=(fingerPosx,fingerPosy)
        posFingerx.append(fingerPosx) #creating lists for x and y coordinates
        posFingery.append(fingerPosy)
        posFinger.append(fingerPos)
        
        
    #thumb position relative to the origin
        if thumbAngle <= 25: #20 since the is the shift we chose for our thumb
            alpha = 25 - thumbAngle
            thumbPosx = round(-70.5 * math.sin(alpha*math.pi/180),3) #using cos for y coordinate and sin for x coordinate
            thumbPosy = round(-27.5 - 70.5 * math.cos(alpha*math.pi/180),3) #using round function for a 'cleaner' output
            thumbPos = (thumbPosx, thumbPosy)
            posThumbx.append(thumbPosx)
            posThumby.append(thumbPosy)
            posThumb.append(thumbPos)

        else:
            alpha = thumbAngle - 25
            thumbPosx = round(-70.5 * math.sin(alpha*math.pi/180),3) #takes in consideration if the angle is different based on the starting position
            thumbPosy = round(-27.5 - 70.5 * math.cos(alpha*math.pi/180),3)
            thumbPos = (thumbPosx, thumbPosy)
            posThumbx.append(thumbPosx)
            posThumby.append(thumbPosy)
            posThumb.append(thumbPos)
            
        
        print("\nIncrement:", str(inc)) #PRINT PRINT PRINT
        print("The direction the motor is spinning is:", motorDirection)
        print("The angle relative from the starting position is "  + str(Angle))
        print("The angle of the forefinger from the starting position is "+str(FingerAngle))
        print("The angle of the thumb from the starting position is "+str(thumbAngle))             
        print("The position of the finger tip relative to the starting position: ", fingerPos)
        print("The position of the thumb tip relative to the starting position: ", thumbPos)

        plt.plot(posThumbx, posThumby, '.', color= 'g') #plotting all the data calculated from the for loop based on increments
        plt.plot(posFingerx, posFingery, '.', color= 'b')


    with open('WritingtoFile3.0.txt', 'w') as file: 
        for i in range(len(posThumb)): #uses any list since their length will be the same based on the increments
            d=str(directionMotor[i])
            ptx=str(posThumbx[i])
            pty=str(posThumby[i])
            pfx=str(posFingerx[i])
            pfy=str(posFingery[i])
            af= str(angleFinger[i])
            at= str(angleThumb[i])
            aa= str(motorAngle[i])
            file.write(d + "|") 
            file.write(aa + "|")
            file.write(af + "|")
            file.write(at + "|")
            file.write(pfx + "|")
            file.write(pfy + "|")
            file.write(ptx + "|")
            file.write('{}\n'.format(pty)) #adding a new line after each incremental data
    file.close()

    plt.ylabel('Position of the Fingers (y)') #relevant labels
    plt.xlabel('Position of the Fingers (x)')
    pylab.legend(loc='upper left') #position of the legend
    plt.grid(True)
    plt.show() #shows the actual graph
    
    anykey= input("Would you like to:\n1. Re-Run\n2. Return to Main Menu\n") #asks user to re-run the program or return to main menu
    if anykey== "Re-Run" or anykey== '1':
        SubProgram2()
    elif anykey== "Return to Main Menu" or anykey== '2':
        main_menu()

    


def SubProgram3():
    score = 0
#Give user option of continue or exit quiz
    print("Welcome to the DP-2 Quiz")
    begin = input("Would you like to begin?\n(a) Yes\n(b) No\n")
    if begin == "a" or begin == "Yes" or begin == "yes":#If user chooses yes, subprogram 3 will continue
        print("Good luck!\nIf hand moves an increment to close position answer is correct.\nIf hand moves an increment to open position answer is incorrect")
    else:
        print("Try again next time")#If the following condition is not met, returns to main menu
        main_menu()
    
    #Input Speed and gear ratio with output speed
    inputSpeed = 33.75
    gearRatio = 5.625 #Necessary units
    outputSpeed = inputSpeed/(gearRatio*60)
    maxSpeed = 17/6
    speedFactor = 10 #Multiply outputSpeed by speed factor to make speed of motor more visible
    speed = (outputSpeed*speedFactor/maxSpeed)*100

    #Ask User questions, if condition is met motor will move

    q1 = input("How many weeks is the DP-2 Project?\n(a) 4 weeks\n(b) 5 weeks\n(c) 6 weeks\n\n") #Condition is met if user inputs correct answer
    if q1 == "b" or q1 == "B":
       pwmMotA.start(speed)#Correct answer will rotate motor forward
       GPIO.output(motADir,1)#motor rotates forward
       time.sleep(4)#motor runs for 4 seconds
       pwmMotA.ChangeDutyCycle(0)#motor stops
       score = score + 1#Correct answer will increase score by 1
           
    else:
         pwmMotA.start(speed)#Wrong answer will rotate motor backwards
         GPIO.output(motADir,0)#motor rotates backwards
         time.sleep(4)#motor runs for 4 seconds 
         pwmMotA.ChangeDutyCycle(0)#motor stops
        
#User is asked the following questions following the same if and else statements
    q2 = input("The point-of-contact between the forefinger-tip and thumb-tip is required to lie within a:\n(a) 15x15mm 2D functional workspace\n(b) 25x25mm 2D functional workspace\n(c) 30x30mm 2D functional worksspace\n\n")
    if q2 == "c" or q2 == "C":
        pwmMotA.start(speed)
        GPIO.output(motADir,1)
        time.sleep(4)
        pwmMotA.ChangeDutyCycle(0)
        score = score + 1

    else:
        pwmMotA.start(speed)
        GPIO.output(motADir,0)
        time.sleep(4)
        pwmMotA.ChangeDutyCycle(0)

    q3 = input("How much is the Preliminary Assembly Milestone worth?\n(a) 5%\n(b) 10%\n(c) 15%\n\n")
    if q3 == "b" or q3 == "B":
        pwmMotA.start(speed)
        GPIO.output(motADir,1)
        time.sleep(4)
        pwmMotA.ChangeDutyCycle(0)
        score = score + 1

    else:
        pwmMotA.start(speed)
        GPIO.output(motADir,0)
        time.sleep(4)
        pwmMotA.ChangeDutyCycle(0) 

    q4 = input("An external feedback loop at the end of the design process involving user feedback is known as:\n(a) Validation\n(b) Verification\n(c) Criticism\n\n")
    if q4 == "a" or q4 == "A":
        pwmMotA.start(speed)
        GPIO.output(motADir,1)
        time.sleep(4)
        pwmMotA.ChangeDutyCycle(0)
        score = score + 1

    else:
        pwmMotA.start(speed)
        GPIO.output(motADir,0)
        time.sleep(4)
        pwmMotA.ChangeDutyCycle(0)

    q5 = input("EWB is a Canadian charity that applies engineering to humanitarian work in Africa. What does EWB stand for?\n(a) Engineers With Borders\n(b) Engineers Without Borders\n(c) Engineers With Blessings\n\n")
    if q5 == "b" or q5 == "B":
        pwmMotA.start(speed)
        GPIO.output(motADir,1)
        time.sleep(4)
        pwmMotA.ChangeDutyCycle(0)
        score = score + 1

    else:
        pwmMotA.start(speed)
        GPIO.output(motADir,0)
        time.sleep(4)
        pwmMotA.ChangeDutyCycle(0)

    print("\n\n\nThanks for playing, you got " + str(score) +"/5 right!") #Score of user is inputed as a string
    
    anykey= input("\nWould you like to:\n1. Play Again\n2. Return to Main Menu\n\n") #asks if the user wants to re-run the program or go back to main menu
    if anykey== "Play Again" or anykey == "1": #If user meets condition program returns to subprogram 3
        SubProgram3()
    if anykey== "Return to Main Menu" or anykey =="2": #If user meets condition, program returns to main menu
        main_menu()


def SubProgram4():
    while True:
        try:
            anykey= input('Hello, you have chosen to view the Integrated Bonus component. Are you ready to begin? Enter 1 to continue or 2 to go back to main menu. ') #asks user to continue with program or go back to main menu 
        except ValueError: # just catch the exceptions you know!
            print ('That\'s not valid!')
        else:
            if anykey== '1':
               break  # this is faster
            elif anykey== '2':
                main_menu
            else:
               print ('Out of range. Try again') #value out of range and restarts program
               SubProgram4()
    maxspeed= 17/6 #max speed of motor in RPS
    speed= (0.5625/maxspeed)*100 #% speed of the motor that displays desired output
    pwmMotA.start(speed) #motor moves in one direction and fingers close
    GPIO.output(motADir,1)
    time.sleep(1.5)
    GPIO.output(motADir,0)#motor moves back to starting position and rotates in the opposite direction
    time.sleep(1.5)
    GPIO.output(motADir,1)#repeats the same action twice
    time.sleep(1.5)
    GPIO.output(motADir,0)
    time.sleep(1.5)
    pwmMotA.ChangeDutyCycle(0) #stops the motor after 2 cycles
    meme= input("Would you like to re-run this program or go back to the main menu?\n1. Re-Run\n2. Main Menu \n") #asks user to re-run the program or go back to main menu
    if meme== '1' or meme== "Re-Run":
        SubProgram4()
    if meme== '2'or meme== "Main Menu":
        main_menu()
#Main Program
main_menu()


