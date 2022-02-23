#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyfirmata import Arduino, util
from time import sleep


# In[2]:


from IPython.display import display, Markdown, clear_output, HTML
import ipywidgets as widgets


# In[3]:


board = Arduino('COM5')


# In[4]:


x_step = 2
x_dir = 5

y_step = 3
y_dir = 6

z_step = 4
z_dir = 7

en_pin = 8

pin_dict = {'x':[x_step, x_dir], 'y':[y_step, y_dir], 'z':[z_step, z_dir]}

# looking at top of motor
clockwise = 0
counterclockwise = 1


# In[ ]:





# In[5]:


""" Moves a single stepper according to arguments 

motor_choice -> str
direction - > int
pulse_pause_time -> float
rotation_steps -> int

"""

def move_stepper(motor_choice, direction, pulse_pause_time, rotation_steps):
    # clean data - lower case dict key
    motor_choice = str.lower(motor_choice)
    
    board.digital[pin_dict[motor_choice][1]].write(direction)
    
    for x in range(rotation_steps):
        board.digital[pin_dict[motor_choice][0]].write(1)
        board.pass_time(pulse_pause_time)
        board.digital[pin_dict[motor_choice][0]].write(0)
        board.pass_time(pulse_pause_time)


# In[6]:


""" Moves multiple steppers according to arguments 
    in an interlaced fashion


motor_args -> array of dicts of the following stucture
    {motor_choice -> str
     direction - > int
     rotation_steps -> int}
pulse_pause_time -> float
interlacing_step_size -> int

"""

def move_multiple_steppers(motor_args, pulse_pause_time, interlacing_step_size):
    # get max steps 
    counter_values = []
    for arg in motor_args:
        counter_values.append(arg["rotation_steps"])
    
    max_steps = max(counter_values)
    
    # while in range of the given pulses
    # while at least one motor still has remaining steps
    while max_steps > 0: 
        # for each motor to be stepped
        for index, arg in enumerate(motor_args):
            # if there are remaining steps for the motor
            if counter_values[index] > 0:
                move_stepper(arg['motor_choice'], arg['direction'], pulse_pause_time, interlacing_step_size)
                counter_values[index] = counter_values[index] - interlacing_step_size
        max_steps = max_steps -1


# In[7]:


##### Init test ######
#move_stepper(step_pin, direction_pin, direction, pulse_pause_time, rotation_steps)
# 200 steps is full rotation

motor_args = [
                {"motor_choice":"X", "direction":0, "rotation_steps": 100},
                {"motor_choice":"y", "direction":1, "rotation_steps": 200},
                {"motor_choice":"z", "direction":0, "rotation_steps": 300}
            ]
pulse_pause_time = .0001
interlacing_step_size = 100

move_multiple_steppers(motor_args, pulse_pause_time, interlacing_step_size)


# In[ ]:





# In[8]:


''' interface components '''

indep_widgets = {"x":[], "y":[], "z":[]}

# iterate through the motors
for motor_item in indep_widgets:

    # which motor checkbox
    motor_checkbox = widgets.Checkbox(
        value=False,
        description = motor_item,
        disabled=False,
        indent=False)
    
    indep_widgets[motor_item].append(motor_checkbox)

    # direction radio buttons
    step_dir = widgets.RadioButtons(
           options=['clockwise', 'counterclock'],
           value='clockwise',
           description=motor_item + ' Direction:')
    
    indep_widgets[motor_item].append(step_dir)
    
    # steps per motor
    motor_steps = widgets.IntText(
       value='200',
       description=motor_item + ' Steps')
    
    indep_widgets[motor_item].append(motor_steps)

    
# same for every motor    
motor_speed = widgets.RadioButtons(
    options=['.1', '.01', '.001', '.0001'],
    description='Pulse Speed:',
    disabled=False,
    value='.0001')

# interlacing step size
interlacing_step = widgets.IntText(
    value='100',
    description='Step Size')

motor_button = widgets.Button(
                description='Run Stepper Motor(s)',
                button_style='Success',
                icon='cog')


# In[ ]:





# In[9]:


''' Interface Layout '''

spacer = widgets.HTML(
    value="<br>",
)

slow_text = widgets.HTML(
    value="<span style='margin-left:85px'>&nbsp;</span>Slow",
)
fast_text = widgets.HTML(
    value="<span style='margin-left:85px; margin-top -205px;'>&nbsp;</span>Fast",
)
interlacing_text = widgets.HTML(
    value="Interlacing Step Size",
)

#### motors independant settings #####
motors_label = widgets.HTML(
    value="Motors",
)

motor_options_widgets = [motors_label]
motors_box_x = widgets.VBox(indep_widgets['x'])
motors_box_y = widgets.VBox(indep_widgets['y'])
motors_box_z = widgets.VBox(indep_widgets['z'])

box_1 = widgets.VBox([motors_label, motors_box_x, motors_box_y, motors_box_z])
box_2 = widgets.VBox([slow_text, motor_speed ,fast_text, spacer, interlacing_text, interlacing_step, spacer, motor_button])

box = widgets.HBox([box_1, box_2])


# In[10]:


# define the button click action
def motor_button_click(arg):
    motor_args = []
    x_args = {}
    y_args = {}
    z_args = {}
    
    # children[0] = motor checkbox
    # children[1] = direction radio buttons
    # children[2] = steps text box
    
    # move_multiple_steppers(motor_args, pulse_pause_time, interlacing_step_size)
    # example motor_args
    # {"motor_choice":"x", "direction":0, "rotation_steps": 100}
    
    #### this section isn't DRY code, but certainly is more convienant :) ####
    #### x ####
    if(motors_box_x.children[0].value == True):
        if(motors_box_x.children[1].value == "clockwise"):
            step_dir_value = 0
        else:
            step_dir_value = 1
        
        step_num = motors_box_x.children[2].value

        x_args = {"motor_choice": "x", "direction": step_dir_value, "rotation_steps": step_num}
        
     #### y ####
    if(motors_box_y.children[0].value == True):
        if(motors_box_y.children[1].value == "clockwise"):
            step_dir_value = 0
        else:
            step_dir_value = 1

        step_num = motors_box_y.children[2].value

        y_args = {"motor_choice": "y", "direction": step_dir_value, "rotation_steps": step_num}

    #### z ####
    if(motors_box_z.children[0].value == True):
        if(motors_box_z.children[1].value == "clockwise"):
            step_dir_value = 0
        else:
            step_dir_value = 1

        step_num = int(motors_box_z.children[2].value)

        z_args = {"motor_choice": "z", "direction": step_dir_value, "rotation_steps": step_num} 

    # move_multiple_steppers(motor_args, pulse_pause_time, interlacing_step_size)
    if len(x_args) > 0:
        motor_args.append(x_args)
            
    if len(y_args) > 0:
        motor_args.append(y_args)
            
    if len(z_args) > 0:
        motor_args.append(z_args)
    
    # set args that apply to all motors
    pulse_pause_time = float(motor_speed.value)
    interlacing_step_size = int(interlacing_step.value)
    
    # run the compiled instructions
    move_multiple_steppers(motor_args, pulse_pause_time, interlacing_step_size)
        
motor_button.on_click(motor_button_click)


# In[11]:


box


# In[ ]:





# In[ ]:




