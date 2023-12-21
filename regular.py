# -----------------------------------------------------------
# Givens
  # Uxx - u = 4Utt
  # Point
  # X axis & Y axis
  # Initial Condition
  # Boundary Condition
  # B.D or C.D or F.D
  # Mesh size H & K (horizontal & Vertical Step)
  # PDE Equation

# Steps 
  # Draw The Region (When not given)
  # Draw the grid using Delta_X and Delta_Y ** (Givens)
  # Apply Initial and boundary conditions to the shape
  #    -> If 2 boundary conditions meet we take average at the meeeting point
  # Will be Given Uy to X or Ux to Y function like Uy(x,1) = x
  # Retrieve from formula sheet the corresponding equation according to the Given
  # If no B.D or C.D or F.D is given retrieve the C.D
  # Get each point
  # Retrieve the Uxx or Uyy from formula sheet
  # Use these points in the equivalent pde equation to get the U
# -----------------------------------------------------------


import numpy as np
from sympy import symbols, lambdify, sympify

# Define symbols for sympy
x, t = symbols('x t')


# Ask for the range of x and t
x_input = input("Enter the x-axis range (start and end) separated by space, use 'inf' for infinity: ")
t_input = input("Enter the t-axis range (start and end) separated by space, use 'inf' for infinity: ")

# Function to handle 'inf' input
def parse_input(input_string):
    start, end = input_string.split()
    if start.lower() == 'inf':
        start = float('inf')
    else:
        start = float(start)
    if end.lower() == 'inf':
        end = float('inf')
    else:
        end = float(end)
    return start, end

# Parse the input ranges
x_start, x_end = parse_input(x_input)
t_start, t_end = parse_input(t_input)

# Based on the ranges, ask for the boundary conditions
# Inf checks for boundary enteries
# Convert sympy expressions to functions that can be used for calculations

#******************************************************************************** Read Boundaries and Convert To Function ********************************************************************************

if not np.isinf(x_start):
 boundary_condition_x_start_expr = input(f"Enter the boundary condition u({x_start}, t): ")
 boundary_condition_x_start_sympy = lambdify(t, boundary_condition_x_start_expr)

 
if not np.isinf(x_end):
 boundary_condition_x_end_expr = input(f"Enter the boundary condition u({x_end}, t): ")
 boundary_condition_x_end_sympy = lambdify(t, boundary_condition_x_end_expr)


if not np.isinf(t_start):
 boundary_condition_t_start_expr = input(f"Enter the boundary condition u(x, {t_start}): ")
 boundary_condition_t_start_sympy = lambdify(x, boundary_condition_t_start_expr)


if not np.isinf(t_end):
 boundary_condition_t_end_expr = input(f"Enter the boundary condition u(x, {t_end}): ")
 boundary_condition_t_end_sympy = lambdify(x, boundary_condition_t_end_expr)


# Convert the user input strings into sympy expressions

def boundary_condition_x_start(t_val):
    return boundary_condition_x_start_sympy(t_val)

def boundary_condition_x_end(t_val):
    return boundary_condition_x_end_sympy(t_val)

def boundary_condition_t_start(t_val):
    return boundary_condition_t_start_sympy(t_val)

def boundary_condition_t_end(t_val):
    return boundary_condition_t_end_sympy(t_val)


#******************************************************************************** Initial Condition ********************************************************************************


def create_function_from_user_input():
    # Prompt the user to enter the equation or a number
    user_input = input("Enter the expression (e.g., 'x**2', '5 + t') or a number: ").strip()

    # Check if the input is just a number
    if user_input.replace('.', '', 1).isdigit():
        # If it's just a number, create a function that always returns this number
        value = float(user_input)
        return lambda var: value  # var is a dummy variable, the function always returns 'value'
    
    # If the input is not just a number, proceed to check if it's in terms of 'x' or 't'
    variable = None
    if 'x' in user_input:
        variable = x
    elif 't' in user_input:
        variable = t
    else:
        raise ValueError("The input must be an expression in terms of 'x' or 't', or just a number.")

    # Parse the user input into a sympy expression
    expression = sympify(user_input, evaluate=False)

    # Create a callable function from the sympy expression
    func = lambdify(variable, expression, modules=['numpy'])

    return func

# Create the function from user input
user_defined_function = create_function_from_user_input()



#******************************************************************************** Mesh Creation and Case Handling for BD ********************************************************************************

h = float(input("Enter H step: "))
k = float(input("Enter K step: "))
difference_type = input("Enter Difference Type: ")
x_low = []
x_up = []
t_left = []
t_right = []


#If BD we no upper limit aka t_start = -inf 
#Make the k = -k so the step is in negative and make sure the t_end will be negtaive
if difference_type == 'BD' and np.isinf(t_start) and t_end == 0:
    k = -k  # make k negative for the backward step
    t_start_for_loop = 0  # start from 0 for the loop
    t_end_for_loop = -5 * abs(k)  # end at a large negative number for the loop
else:
    t_start_for_loop = t_start if not np.isinf(t_start) else 0
    t_end_for_loop = t_end if not np.isinf(t_end) else 5 * k
    
x_start_for_loop = 0 if x_start == float('-inf') else x_start
x_end_for_loop = 5*h if x_end == float('inf') else x_end

grid_dict = {}
for i in np.arange(t_start_for_loop, t_end_for_loop+k, k):
   for j in np.arange(x_start_for_loop, x_end_for_loop+h, h):
      grid_dict[round(j,2),round(i,2)] = 0


# Helper Function to handle corner values
def update_value(x, y):

  if x == x_start and y == t_end or y == t_end and x == x_end or x == x_start and y == t_start or x == x_end and y == t_end:
    key = (x,y)
    existing_value = grid_dict[key]
    if y == t_start:
        average_value = (existing_value + boundary_condition_t_start(x)) / 2
        grid_dict[key] = average_value
    else: 
        average_value = (existing_value + boundary_condition_t_end(x)) / 2
        grid_dict[key] = average_value





# Example usage to test the boundary conditions
# The if before each for loop just so we can ignore a boundary if given an infinity in a certain axis
if not np.isinf(t_start):
  for i in np.arange(x_start_for_loop, x_end_for_loop+h, h):
    i = round(i,2)
    grid_dict[i,t_start] = round(boundary_condition_t_start(i),5)
    


if not np.isinf(t_end):
  for i in np.arange(x_start_for_loop, x_end_for_loop+h, h):
    i = round(i,2)
    grid_dict[i,t_end] = round(boundary_condition_t_end(i),5)


if not np.isinf(x_start):
  for i in np.arange(t_start_for_loop, t_end_for_loop+k, k):
   i = round(i,2)
   grid_dict[x_start,i] = round(boundary_condition_x_start(i),5)
   update_value(x_start,i)



if not np.isinf(x_end):
  for i in np.arange(t_start_for_loop, t_end_for_loop+k , k):
   i = round(i,2)
   grid_dict[x_end,i] = round(boundary_condition_x_end(i),5)
   update_value(x_end,i)


for key, value in grid_dict.items():
    print(f"Key: {key}, Value: {value}")


#******************************************************************************** Formulas ********************************************************************************
# If grid is in the -Y direction get the correct K again
if k < 0:
  k = -k


#************************************************** Backward ************************************************** 

if difference_type == "BD":
# Temporary dictionary for updates
 updates_dict = {}

 def backward_diff(key, k, func):
   val_boundary = grid_dict[key]
   val = val_boundary - (k * func(key[0]))
   updates_dict[(key[0], key[1]-k)] = val
   print(f"At x: {key[0]} , At y: {key[1]-k} , Value is {val}")


 # Calculate backward differences but store them in updates_dict
 for key, value in list(grid_dict.items()):
    #Check which is bigger the upper or lower boundary
    if t_end > t_start:
        #if we are on the upper boundary
        if key[1] == t_end:
            if key[0] != x_start and key[0] != x_end:      
                backward_diff(key, k, user_defined_function)
 # Now apply the updates to grid_dict
 grid_dict.update(updates_dict)

#************************************************** Backward ************************************************** 


#************************************************** Forward ************************************************** 

# Forward Difference Formula
"""def forward_diff(x,t,value):
   LHS = ()/k


# FORWARD DIFFERENCE IMPLEMENTATION
for key, value in grid_dict.items():
    if key[0] == t_start:
       if not key == (x_start,t_start) or not key == (x_start , t_end):
          forward_diff(key[0],0,grid_dict[key])          
"""

#************************************************** Forward ************************************************** 


#************************************************** Central ************************************************** 

if difference_type == "CD":
# Temporary dictionary for updates
 updates_dict = {}

 def Central_diff(key, k, func):
   val_boundary = grid_dict[key]
   val = val_boundary - (k * func(key[0]))
   updates_dict[(key[0], key[1]-k)] = val
   #print(f"At x: {key[0]} , At y: {key[1]} , Value is {val}")


 # Calculate backward differences but store them in updates_dict
 for key, value in list(grid_dict.items()):
    #Check which is bigger the upper or lower boundary
    if t_end > t_start:
        #if we are on the upper boundary
        if key[1] == t_end:
            if key[0] != x_start and key[0] != x_end:      
                Central_diff(key, k, user_defined_function)
 # Now apply the updates to grid_dict
 grid_dict.update(updates_dict)

#************************************************** Central ************************************************** 


#******************************************************************************** Tasks ********************************************************************************
#* Implement Forward Diffrence and Central Difference
#* Finish the Backward Difference Equation
#* Take input point from user
#* Take input pde from user