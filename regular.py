# Check for symmetry (for both regular) With 3 methods
#   -> Around X , Y or X=Y
#   -> Boundary Condition Same
#   -> Check PDE substitute with point to the left and point to the right and get the same answer
# Write PDE equation in a discrete form using finite difference formuala
# Substitute for each point (the symmetry check part)
# Solve the obtained Linear system of equations



# REGULAR
#  Import Regular Boundaries Formula Sheet
#  If not mentioned Use Central Difference as mentioned
#  Given Equation Uxx and Uyy
#  If given Ux or Uy use Central difference as defualt unless mentioned


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


# Tips
  # Boundary Conditions are like 
  # U(0,t) = 2t
  # U(1,t) = t
  # U(x,0) = 7
  # But the equation you use to get the number from the Formula Sheet
  # Looks like Ut(x,0) = x^2
  # We retrieve the function from Formula sheet and equate it to X^2 for example



import numpy as np
from sympy import symbols, lambdify

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

if not np.isinf(x_start):
 boundary_condition_x_start_expr = input(f"Enter the boundary condition u({x_start}, t): ")
 boundary_condition_x_start_sympy = lambdify(t, boundary_condition_x_start_expr)

 
if not np.isinf(x_end):
 boundary_condition_x_end_expr = input(f"Enter the boundary condition u({x_end}, t): ")
 boundary_condition_x_end_sympy = lambdify(t, boundary_condition_x_end_expr)


if not np.isinf(t_start):
 boundary_condition_t_start_expr = input(f"Enter the boundary condition u(x, {t_start}): ")
 boundary_condition_t_start_sympy = lambdify(t, boundary_condition_t_start_expr)


if not np.isinf(t_end):
 boundary_condition_t_end_expr = input(f"Enter the boundary condition u(x, {t_end}): ")
 boundary_condition_t_end_sympy = lambdify(t, boundary_condition_t_end_expr)


initial_condition_expr = input("Enter the initial condition: ")

# Convert the user input strings into sympy expressions
initial_condition_sympy = lambdify(x, initial_condition_expr)

def boundary_condition_x_start(t_val):
    return boundary_condition_x_start_sympy(t_val)

def boundary_condition_x_end(t_val):
    return boundary_condition_x_end_sympy(t_val)

def boundary_condition_t_start(t_val):
    return boundary_condition_t_start_sympy(t_val)

def boundary_condition_t_end(t_val):
    return boundary_condition_t_end_sympy(t_val)


def initial_condition(x_val):
    return initial_condition_sympy(x_val)

h = float(input("Enter H step: "))
k = float(input("Enter K step: "))

x_low = []
x_up = []
t_left = []
t_right = []


# If t_start is -inf, replace it with 0 for the boundary condition loop
# Handle the inf loops to just substitute for 5 points at max
t_start_for_loop = 0 if t_start == float('-inf') else t_start
t_end_for_loop = 5*k if t_end == float('inf') else t_end
x_start_for_loop = 0 if x_start == float('-inf') else x_start
x_end_for_loop = 5*h if x_end == float('inf') else x_end

# Example usage to test the boundary conditions
if not np.isinf(t_start):
  for i in np.arange(x_start_for_loop, x_end_for_loop+h, h):
    print(f"Boundary condition at u({i:.2f}, {t_start}):", "{:.2f}".format(boundary_condition_t_start(i)))
    x_low.append(boundary_condition_t_start(i))

print('*'*80)

if not np.isinf(t_end):
  for i in np.arange(x_start_for_loop, x_end_for_loop+h, h):
    print(f"Boundary condition at u({i:.2f}, {t_end}):", "{:.2f}".format(boundary_condition_t_end(i)))
    x_up.append(boundary_condition_t_end(i))

print('*'*80)

if not np.isinf(x_start):
  for i in np.arange(t_start_for_loop, t_end_for_loop+k, k):
   print(f"Boundary condition at u({x_start} , {i:.2f}):", "{:.2f}".format(boundary_condition_x_start(i)))
   t_left.append(boundary_condition_x_start(i))

print('*'*80)

if not np.isinf(x_end):
  for i in np.arange(t_start_for_loop, t_end_for_loop+k , k):
   print(f"Boundary condition at u({x_end} , {i:.2f}):", "{:.2f}".format(boundary_condition_x_end(i)))
   t_right.append(boundary_condition_x_end(i))




#print('*'*80)

#print(x_low)

#print('*'*80)

#print(t_left)

print('*'*80)

#print(t_right)

# Know which boundary equation to use  