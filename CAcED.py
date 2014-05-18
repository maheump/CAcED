# -*- coding: utf-8

                                     # THRESHOLD FOR CONSCIOUSSNESS ACCESS AND ERROR DETECTION #
                                                         # Maxime Maheu #
                                                       # (C)opyright 2014 #

######################################################### IMPORT MODULES ##########################################################

#### Import pygame modules
import pygame
from pygame.locals import *
#### Import mathematical modules
import random
import datetime

####################################################### DEFINE PARAMETERS #########################################################

'''(W, H) = (1024, 768)'''

gray = [127, 127, 127]
black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
blue = [0, 0, 255]

SOAs_list = [16, 33, 50, 66, 83, 100, 116, 133, 'NaN'] # ms
number_of_trials_per_SOA = 1#5
SOAs = number_of_trials_per_SOA*SOAs_list
random.shuffle(SOAs)

number_of_training_trials = 0#10
number_of_trials = len(SOAs)

target_duration = 16 # ms
mask_duration = 200 # ms
interstimuli_timelaps = 1000 # ms

####################################################### DEFINE FUNCTIONS ##########################################################

def wait(duration):
    t0 = pygame.time.get_ticks()
    #### Wait until reaching the "duration" threshold
    while True:
        t = pygame.time.get_ticks() - t0
        if duration > 0 and t > duration: return

def draw_text(text, position, letters_size):
    #### Providing a simple function to display words and letters
    font = pygame.font.Font(None, letters_size)
    image = font.render(text, 1, black)
    size = image.get_size()
    window.blit(image, [position[0] - size[0]/2, position[1] - size[1]/2])
    return

def draw_fixation_cross():
    #### Display a simple fixation cross at the center of the screen
    pygame.draw.line(window, black, [W/2, H/2 - 5], [W/2, H/2 + 5], 3)
    pygame.draw.line(window, black, [W/2 - 5, H/2], [W/2 + 5, H/2], 3)
    return

def break_screen():
    #### Display instructions during inter-blocks break
    window.fill(gray)
    draw_text(u"PAUSE", [W/2, H/2 - 300], 30)
    draw_text(u"Faîtes une pause d'une ou deux minute(s).", [W/2, H/2], 30)
    draw_text(u"Appuyez sur ESPACE quand vous êtes prêt(e).", [W/2, H/2 + 300], 30)
    pygame.display.flip()
    #### Clear the events from the queue
    pygame.event.clear()
    #### Wait until press on spacebar
    while True:
        for ev in pygame.event.get():            
            if (ev.type == KEYDOWN) and (ev.key == K_SPACE): return

def create_file():
    #### Print title and copyright
    print 'THRESHOLD FOR CONSCIOUSSNESS ACCESS AND ERROR DETECTION'
    print '[Copyright 2014 (C) Maxime Maheu]'
    subject_number = str(datetime.datetime.today().day) + '-' + str(datetime.datetime.today().month)
    print 'Subject number:', subject_number
    #### Get initials and put them in capital letters
    subject_initials = raw_input('Subject initials: ')
    subject_initials = subject_initials.upper()
    #### Get subject age, genre and handedness
    subject_age = 'NaN'
    while (subject_age == 'NaN') or (subject_age <= 0):
        subject_age = raw_input('Subject age: ')
    subject_genre = 'NaN'
    while subject_genre not in ('M', 'F'):
        subject_genre = raw_input('Subject genre ([M]ale or [F]emale): ')
        subject_genre = subject_genre.upper()
    subject_handedness = 'NaN'
    while subject_handedness not in ['L', 'R']:
        subject_handedness = raw_input('Subject handedness ([L]eft or [R]ight): ')
        subject_handedness = subject_handedness.upper()
    recording_file_name = 'CAcED_' + subject_initials + '_' + str(subject_number) + '_' + subject_genre + subject_age + subject_handedness  + '_' + 'DATA' + '.dat'
    #### Record headings in this file
    output_file = open(recording_file_name, 'a')
    print >> output_file, 'SUBJECT_INITIALS', 'SUBJECT_NUMBER', 'TRIAL', 'TRIAL_TYPE', 'SOA', 'DIGIT_DISPLAY', 'DIGIT_ANSWER', 'DIGIT_CORRECTION', 'DIGIT_RT', 'VISIBILITY_ANSWER', 'VISIBILITY_RT', 'ERROR_ANSWER', 'ERROR_RT'
    output_file.close()
    return subject_initials, subject_number, recording_file_name, output_file

def display_instructions(training):
    instructions = [u"Dans certains des essais que vous allez voir, un chiffre va apparaître",
                    u"sur l'écran puis très rapidement être caché par des lettres.",
                    u"Essayez d'être le(la) plus attentif(ve) possible à ce chiffre",
                    u"car vous serez par la suite interrogé sur le chiffre en question.",
                    u"Attention dans certains des essais aucun chiffre n'est affiché."]
    window.fill(gray)
    #### Display items type (i.e. training or not)
    if training == 0: draw_text((str(number_of_trials) + " " + u"ESSAIS DIVISÉS EN 2 BLOCKS"), [W/2, H/2 - 300], 30)
    elif training == 1: draw_text((str(number_of_training_trials) + " " + u"ESSAIS D'ENTRAINEMENT"), [W/2, H/2 - 300], 30)
    #### Walk back in the instructions list to fully display the type I instruction on the top of the screen
    lign = len(instructions) - 1
    vertical_position = H/2 - 30
    while lign >= 0:
        draw_text(instructions[lign], [W/2, vertical_position], 30)
        lign -= 1
        vertical_position -= 30
    instructions = [u"Après la présentation de l'essai, il vous sera d'abord demandé de rapporter le chiffre. Si vous",
                    u"n'avez pas eu le temps d'identifier le chiffre ou si vous pensez qu'aucun chiffre n'était affiché,",
                    u"choisissez un chiffre au hasard. Vous devrez par la suite dire si vous pensez qu'un chiffre était présent",
                    u"ou non (Vu ou Pas vu). Finalement vous devrez dire si vous pensez avoir fait une erreur dans",
                    u"votre rapport (Correct ou Erreur). Ainsi, si vous avez eu conscience qu'il y avait un chiffre mais,",
                    u"du fait de sa durée trop brève, n'avez pas pû l'identifier, il vous suffira (1) de rapporter un chiffre",
                    u"au hasard, puis (2) stipuler avoir vu un chiffre et enfin (3) dire que vous avez fait une erreur !"]
    lign = 0
    vertical_position = H/2 + 30
    #### Walk in the consigns list to fully display the metacognitive consign on the back of the screen
    while lign <= (len(instructions) - 1):
        draw_text(instructions[lign], [W/2, vertical_position], 30)
        lign += 1
        vertical_position += 30
    #### Display instructions to begin the task
    draw_text(u"Appuyez sur ESPACE quand vous êtes prêt(e).", [W/2, H/2 + 300], 30)
    #### Display all these instructions
    pygame.display.flip()
    #### Clear the events from the queue
    pygame.event.clear()
    #### Check the events and begin the task when spacebar is pressed
    while True:
        for ev in pygame.event.get():            
            if (ev.type == KEYDOWN) and (ev.key == K_SPACE): return

def crowding(SOA):
    if SOA != 'NaN': trial_type = 1
    elif SOA == 'NaN': trial_type = 0
    #### Define distance from the screen center and the 2 possibles positions
    eccentricity = 200
    positions = [[W/2, H/2 - eccentricity], [W/2, H/2 + eccentricity]]
    #### Define the letters and their spacings
    letters = ['E','M']
    vertical_spacing = 50
    horizontal_spacing = 43
    #### 
    digit_target_list = [1, 2, 3, 4, 6, 7, 8, 9]
    digit_target = digit_target_list[random.randint(0, (len(digit_target_list) - 1))]
    if trial_type == 0: digit_target = 'NaN'
    #### Get two letters to create the mask
    flankers = [letters[0], letters[1]]
    #### Randomly choose a stimulus position among the four possibles
    choosen_position = random.choice(positions)
    #### Draw the target
    window.fill(gray)
    if trial_type == 1: draw_text(str(digit_target), [choosen_position[0], choosen_position[1]], 100)
    pygame.display.flip()
    t0 = pygame.time.get_ticks()
    wait(target_duration)
    window.fill(gray)
    draw_fixation_cross()
    pygame.display.flip()
    #### Wait during SOA
    if SOA != 'NaN':
        t = pygame.time.get_ticks() - t0
        while t < SOA:
            t = pygame.time.get_ticks() - t0
    elif SOA == 'NaN':
        temp = random.choice([50, 66, 83, 100, 116, 133])
        t = pygame.time.get_ticks() - t0
        while t < temp:
            t = pygame.time.get_ticks() - t0
    #### Draw the mask
    draw_text(flankers[0], [choosen_position[0] - horizontal_spacing, choosen_position[1]], 100)
    draw_text(flankers[0], [choosen_position[0] + horizontal_spacing, choosen_position[1]], 100)
    draw_text(flankers[1], [choosen_position[0], choosen_position[1] - vertical_spacing], 100)
    draw_text(flankers[1], [choosen_position[0], choosen_position[1] + vertical_spacing], 100)
    pygame.display.flip()
    wait(mask_duration)
    return trial_type, digit_target

def display_dichotomic_choice(first_possibility, second_possibility, first_possibility_poistion, second_possibility_position):
    draw_text(first_possibility, first_possibility_poistion, 100)
    draw_text(second_possibility, second_possibility_position, 100)
    return

def digit_judgment():
    digit_answer = 'NaN'
    digit_RT = 'NaN'
    window.fill(gray)
    draw_text('1', [W/2 - 400, H/2], 100)
    draw_text('2', [W/2 - 300, H/2], 100)
    draw_text('3', [W/2 - 200, H/2], 100)
    draw_text('4', [W/2 - 100, H/2], 100)
    draw_text('5', [W/2, H/2], 100)
    draw_text('6', [W/2 + 100, H/2], 100)
    draw_text('7', [W/2 + 200, H/2], 100)
    draw_text('8', [W/2 + 300, H/2], 100)
    draw_text('9', [W/2 + 400, H/2], 100)
    pygame.display.flip()
    t0 = pygame.time.get_ticks()
    #### Clear the events from the queue
    pygame.event.clear()
    #### Get answer with right keys
    while (digit_answer == 'NaN') and ((pygame.time.get_ticks() - t0) <= 10000):
        for ev in pygame.event.get():            
            if ev.type == KEYDOWN:
                if ev.key == K_1: digit_answer = 1
                if ev.key == K_2: digit_answer = 2
                if ev.key == K_3: digit_answer = 3
                if ev.key == K_4: digit_answer = 4
                if ev.key == K_5: digit_answer = 5
                if ev.key == K_6: digit_answer = 6
                if ev.key == K_7: digit_answer = 7
                if ev.key == K_8: digit_answer = 8
                if ev.key == K_9: digit_answer = 9
    #### If answer is given before 2 s, record it (and the RT) then provide feedback (only for the answer)
    if (pygame.time.get_ticks() - t0) <= 10000:
        digit_RT = (pygame.time.get_ticks() - t0)
        feedbackpos = [-450, -350, -250, -150, -50, 50, 150, 250, 350]
        pygame.draw.rect(window, red, pygame.Rect(W/2 + feedbackpos[digit_answer - 1], H/2 - 50, 100, 100), 5)
        pygame.display.flip()
    #### If confidence is given after 2 s, display a warning message
    elif (pygame.time.get_ticks() - t0) > 10000:
        window.fill(gray)
        draw_text('Trop lent !', [W/2, H/2], 100)
        pygame.display.flip()
    wait(interstimuli_timelaps)
    return digit_answer, digit_RT

def visibility_judgment():
    visibility_answer = 'NaN'
    visibility_RT = 'NaN'
    window.fill(gray)
    display_dichotomic_choice('Vu', 'Pas vu', [W/2, H/2 - 200], [W/2, H/2 + 200])
    pygame.display.flip()
    t0 = pygame.time.get_ticks()
    #### Clear the events from the queue
    pygame.event.clear()
    #### Get answer with right keys
    while (visibility_answer == 'NaN') and ((pygame.time.get_ticks() - t0) <= 10000):
        for ev in pygame.event.get():            
            if ev.type == KEYDOWN:
                if ev.key == K_UP: visibility_answer = 1
                elif ev.key == K_DOWN: visibility_answer = 0
    #### If answer is given before 2 s, record it (and the RT) then provide feedback (only for the answer)
    if (pygame.time.get_ticks() - t0) <= 10000:
        visibility_RT = (pygame.time.get_ticks() - t0)
        feedbackpos = [150, -250]
        pygame.draw.rect(window, red, pygame.Rect(W/2 - 120, H/2 + feedbackpos[visibility_answer], 240, 100), 5)
        pygame.display.flip()
    #### If confidence is given after 2 s, display a warning message
    elif (pygame.time.get_ticks() - t0) > 10000:
        window.fill(gray)
        draw_text('Trop lent !', [W/2, H/2], 100)
        pygame.display.flip()
    wait(interstimuli_timelaps)
    return visibility_answer, visibility_RT

def error_judgment():
    error_answer = 'NaN'
    error_RT = 'NaN'
    window.fill(gray)
    display_dichotomic_choice('Correct', "Erreur", [W/2, H/2 - 200], [W/2, H/2 + 200])
    pygame.display.flip()
    t0 = pygame.time.get_ticks()
    #### Clear the events from the queue
    pygame.event.clear()
    #### Get answer with right keys
    while (error_answer == 'NaN') and ((pygame.time.get_ticks() - t0) <= 10000):
        for ev in pygame.event.get():            
            if ev.type == KEYDOWN:
                if ev.key == K_UP: error_answer = 1
                elif ev.key == K_DOWN: error_answer = 0
    #### If answer is given before 2 s, record it (and the RT) then provide feedback (only for the answer)
    if (pygame.time.get_ticks() - t0) <= 10000:
        error_RT = (pygame.time.get_ticks() - t0)
        feedbackpos = [150, -250]
        pygame.draw.rect(window, red, pygame.Rect(W/2 - 150, H/2 + feedbackpos[error_answer], 300, 100), 5)
        pygame.display.flip()
    #### If confidence is given after 2 s, display a warning message
    elif (pygame.time.get_ticks() - t0) > 10000:
        window.fill(gray)
        draw_text('Trop lent !', [W/2, H/2], 100)
        pygame.display.flip()
    wait(interstimuli_timelaps)
    return error_answer, error_RT

######################################################### LAUNCH PROGRAM ##########################################################

try:
    subject_initials, subject_number, recording_file_name, output_file = create_file()
    
    pygame.init()
    '''window = pygame.display.set_mode([W, H], DOUBLEBUF)'''
    window = pygame.display.set_mode([1024, 768], FULLSCREEN | DOUBLEBUF | HWSURFACE)
    W, H = window.get_size()

    #### Mask the cursor during all the experiment
    pygame.mouse.set_visible(False)

    training = 1
    training_trial = 1
    trial = 1
    while (trial <= number_of_trials) or (training_trial <= number_of_training_trials):
        if ((trial == 1) and (training == 0)) or ((training_trial == 1) and (training == 1)): display_instructions(training)  
        
        if training == 0: SOA = SOAs[trial - 1]
        if training == 1: SOA = SOAs_list[random.randint(0, (len(SOAs_list) - 1))]
        
        window.fill(gray)
        draw_fixation_cross()
        pygame.display.flip()
        wait(interstimuli_timelaps)
        
        trial_type, digit_target = crowding(SOA)
        
        digit_answer, digit_RT = digit_judgment()
        
        if digit_answer != 'NaN':
            
            if digit_target == digit_answer: digit_correction = 1
            if digit_target != digit_answer: digit_correction = 0
                
            visibility_answer, visibility_RT = visibility_judgment()
            
            if visibility_answer != 'NaN': error_answer, error_RT = error_judgment()
            if visibility_answer == 'NaN': (error_answer, error_RT) = ('NaN', 'NaN')
                
        if digit_answer == 'NaN': (digit_correction, visibility_answer, visibility_RT, error_answer, error_RT) = ('NaN', 'NaN', 'NaN', 'NaN', 'NaN')
        
        '''visibility_answer, visibility_RT = visibility_judgment()
        
        if visibility_answer != 'NaN':        
        
            if visibility_answer == 1:
                digit_answer, digit_RT = digit_judgment()
                if digit_answer != 'NaN': error_answer, error_RT = error_judgment()
                elif digit_answer == 'NaN': (error_answer, error_RT) = ('NaN', 'NaN')
                    
            if visibility_answer == 0:
                (digit_answer, digit_RT, error_answer, error_RT) = ('NaN', 'NaN', 'NaN', 'NaN')
        
            if digit_target == digit_answer: digit_correction = 1
            if digit_target != digit_answer: digit_correction = 0
                
        if visibility_answer == 'NaN':
                    (digit_answer, digit_RT, error_answer, error_RT, digit_correction) = ('NaN', 'NaN', 'NaN', 'NaN', 'NaN')'''
        
        if training == 0:
            output_file = open(recording_file_name, 'a')
            print >> output_file, subject_initials, subject_number, trial, trial_type, SOA, digit_target, digit_answer, digit_correction, digit_RT, visibility_answer, visibility_RT, error_answer, error_RT
            output_file.close()
        
        if trial == (number_of_trials/2): break_screen()
                        
        if training == 0: trial += 1
        if training == 1: training_trial += 1
            
        if training_trial > number_of_training_trials: training = 0

finally:
    try: output_file.close()
    except: pass
    pygame.quit()
