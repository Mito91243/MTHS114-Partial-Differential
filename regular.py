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
from sympy import symbols, lambdify, sympify, solve, Function, Eq

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
      grid_dict[round(j,2),round(i,2)] = None


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





#******************************************************************************** Formulas ********************************************************************************
# If grid is in the -Y direction get the correct K again
if k < 0:
  k = -k


#************************************************** Backward ************************************************** 

if difference_type == "BD":
# Temporary dictionary for updates
 updates_dict = {}

 def backward_diff(key):
   val_boundary = grid_dict[key]
   val = val_boundary - (k * user_defined_function(key[0]))
   updates_dict[key[0], round(key[1]-k,2)] = val
   #print(f"At x: {key[0]} , At y: {key[1]-k} , Value is {val}")


 # Calculate backward differences but store them in updates_dict
 for key, value in list(grid_dict.items()):
    #Check which is bigger the upper or lower boundary
    if t_end > t_start:
        #if we are on the upper boundary
        if key[1] == t_end:
            if key[0] != x_start and key[0] != x_end:      
                backward_diff(key)
 # Now apply the updates to grid_dict
 grid_dict.update(updates_dict)

#************************************************** Backward ************************************************** 


#************************************************** Forward ************************************************** 

if difference_type == "FD":
# Temporary dictionary for updates
 updates_dict = {}

 def forward_diff(key):
   val_boundary = grid_dict[key]
   val = val_boundary + (k * user_defined_function(key[0]))
   updates_dict[key[0], round(key[1]+k,2)] = val
   #print(f"At x: {key[0]} , At y: {round(key[1]+k,2)} , Value is {val}")


 # Calculate backward differences but store them in updates_dict
 for key, value in list(grid_dict.items()):
    #if we are on the upper boundary
        if key[1] == t_start:
            if key[0] != x_start and key[0] != x_end:      
                forward_diff(key)
 
 # Now apply the updates to grid_dict
 grid_dict.update(updates_dict)

#************************************************** Forward ************************************************** 

#************************************************** PDE ************************************************** 
 
h_val, k_val = symbols('h k')
u = Function('u')

# Handle if the pde equation has different difference formula from the Inital condition
difference_type_pde = input("Enter PDE Difference Type (None if not mentioned): ")
difference_type_pde = "CD" if difference_type_pde == "None" else difference_type_pde


# Define the finite difference expressions as functions
def uxx():
    #TO BE TESTED
    return (u(x+h_val, t) - 2*u(x, t) + u(x-h_val, t)) / h_val**2

def utt():
    #TO BE TESTED
    if difference_type == "CD":
       return ((2*u(x, t+k_val)) - (2*u(x, t)) - (2*k*u(x, t))) / k_val**2
    return (u(x, t+k_val) - 2*u(x, t) + u(x, t-k_val)) / k_val**2

def ux():
    if difference_type_pde == "FD":
     return (u(x+h_val, t) - u(x, t)) / h_val
    elif difference_type_pde == "BD":
     return (u(x+h_val, t) - u(x-h_val, t)) / h_val
    elif difference_type_pde == "CD":
     return (u(x+h_val, t) - u(x-h_val, t)) / h_val*2
    
def ut():
    if difference_type_pde == "FD":
     return (u(x, t+k_val) - u(x, t)) / k_val
    elif difference_type_pde == "BD":
     return (u(x, t) - u(x, t-k_val)) / k_val
    elif difference_type_pde == "CD":
     return (u(x, t+k_val) - u(x, t-k_val)) / k_val*2



# Function to create a PDE using finite difference formulas
def create_pde(user_pde_input):
    # Parse the user input
    lhs_term = user_pde_input.split('=')[0].strip()
    rhs_term = user_pde_input.split('=')[1].strip()

#Dictionary of what each letter in pde equation equates to as a function
    sympy_locals = {
        'u': u(x, t),
        'uxx': uxx(),
        'utt': utt(),
        'ux': ux(),
        'ut': ut(),
        #'uxt' : uxt()
    }

    # Handle the left hand side of the pde as a general expression
    lhs_expr = sympify(lhs_term, locals=sympy_locals)

    # Handle the right-hand side of the PDE as a general expression
    rhs_expr = sympify(rhs_term, locals=sympy_locals)

    # Create the PDE as an equation
    pde = Eq(lhs_expr, rhs_expr)
    print(pde)
    return pde

# Example PDE input from the user
pde_input = input("Enter PDE: ")

# Create the finite difference PDE
fd_pde = create_pde(pde_input)

def evaluate_pde_at_key(key, h, k):
    # Substitute the key into the PDE
    x_val, t_val = key

    # Create a dictionary of all terms that need to be substituted
    subs_dict = {
       #replace with x if we are at a point in the grid that has value 0 aka unkown value
        u(x, t): x if grid_dict.get((x_val, t_val), 0) == None else grid_dict.get((x_val, t_val), 0),
        u(x+h_val, t): x if grid_dict.get((round(x_val+h,2), t_val), 0) == None else grid_dict.get((round(x_val+h,2), t_val), 0),
        u(x-h_val, t): x if grid_dict.get((round(x_val-h,2), t_val), 0) == None else grid_dict.get((round(x_val-h,2), t_val), 0),
        u(x, t+k_val): x if grid_dict.get((x_val, round(t_val+k,2)), 0) == None else grid_dict.get((x_val, round(t_val+k,2)), 0),
        u(x, t-k_val): x if grid_dict.get((x_val, round(t_val-k,2)), 0) == None else grid_dict.get((x_val, round(t_val-k,2)), 0),
        h_val: h,
        k_val: k
        # Add more substitutions for other terms if needed
    }

    # Substitute the finite difference expressions into the PDE
    pde_evaluated = fd_pde.subs(subs_dict)

    return pde_evaluated


# Evaluate the PDE at the wanted key
# TASK: FOR LOOP GOES HERE TO CALCULATE ALL GRID WITH GIVEN PDE
# Helper Function to use when interpereting the key input
def parse_key_input(user_input):
    # Split the input by comma
    x_str, y_str = user_input.split(',')

    # Convert the split strings into numbers
    x_val = float(x_str.strip())
    y_val = float(y_str.strip())

    return x_val, y_val

# Prompt the user for the key
key_input = input("Enter the point coordinates (format 'x, y'): ")

# Parse the user input
xx, yy = parse_key_input(key_input)
kkey = (round(xx,2),round(yy,2))

# Handle the
k_temp = k
if(t_start_for_loop > t_end_for_loop):
    k_temp = -k

if difference_type != "CD":
 for i in np.arange(x_start_for_loop, x_end_for_loop+h, h):
  for j in np.arange(t_start_for_loop, t_end_for_loop+k, k_temp):
   if round(i,2) != x_start and round(i,2) != x_end and round(j,2) != t_start and round(j,2) != t_end:       
    i = round(i,2)
    j = round(j,2)
    print(f"X: {i} Y: {j} Value: {grid_dict[i,j]}")
    if grid_dict[i,j] != 0:
       temp_key = (i,j)
       evaluated_pde = evaluate_pde_at_key(temp_key, h, k)
       # Store in a temp value to extract it as int from list 
       temp_list = solve(evaluated_pde,x)
       #Based on what type of Difference we are working on how to store value
       if difference_type == "FD":
         if len(temp_list) > 0:
          updates_dict[i, round(j+k,2)] = temp_list[0]
       else:
        if len(temp_list) > 0:
         updates_dict[i, round(j-k,2)] = temp_list[0]
    
       grid_dict.update(updates_dict)


# Now apply the updates to grid_dict
if difference_type == "CD":
  updates_dict = {}
  for i in np.arange(x_start_for_loop, x_end_for_loop+h, h):
    for j in np.arange(t_start_for_loop, t_start_for_loop+k, k_temp):
        i = round(i,2)
        j = round(j,2)
        if round(i,2) != x_start and round(i,2) != x_end:
            temp_key = (i,j)
            evaluated_pde = evaluate_pde_at_key(temp_key, h, k)
            print(evaluated_pde)
            # Store in a temp value to extract it as int from list 
            temp_list = solve(evaluated_pde,x)
            #Based on what type of Difference we are working on how to store value

            print(f"X: {i} Y: {j+k} Value: {temp_list}")
            grid_dict[i, round(j+k,2)] = temp_list[0]


    for i in np.arange(x_start_for_loop, x_end_for_loop+h, h):
        i = round(i,2)
        j = round(t_start_for_loop+k,2)
        if round(i,2) != x_start and round(i,2) != x_end:
            temp_key = (i,j)
            evaluated_pde = evaluate_pde_at_key(temp_key, h, k)
            print(evaluated_pde)
            # Store in a temp value to extract it as int from list 
            temp_list = solve(evaluated_pde,x)
            #Based on what type of Difference we are working on how to store value

            print(f"X: {i} Y: {j+k} Value: {temp_list}")
            if len(temp_list) > 0:
             grid_dict[i, round(j+k,2)] = temp_list[0]


#TESTNG
print(f"at x: {kkey[0]} at y: {kkey[1]} value is: {grid_dict[kkey[0],kkey[1]]}")
#print(f"at x: {round(kkey[0]+h,2)} at y: {kkey[1]} value is: {grid_dict[round(kkey[0]+h,2),round(kkey[1],2)]}")
#print(f"at x: {kkey[0]-h} at y: {kkey[1]} value is: {grid_dict[round(kkey[0]-h,2),kkey[1]]}")
#print(f"at x: {kkey[0]} at y: {kkey[1]+k} value is: {grid_dict[kkey[0],round(kkey[1]+k,2)]}")
#print(f"at x: {kkey[0]} at y: {kkey[1]-k} value is: {grid_dict[kkey[0],round(kkey[1]-k,2)]}")

#************************************************** PDE ************************************************** 

 


