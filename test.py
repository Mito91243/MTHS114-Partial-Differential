# TESTING THE PDE INPUT

#from sympy import symbols, Function, Eq, sympify, solve




"""
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
x, y = parse_key_input(key_input)


for j in np.arange(x_start_for_loop, x_end_for_loop+h, h):
 for i in np.arange(t_start_for_loop, t_end_for_loop+k, k):
  print("!!!!")
  if j != x_start and j != x_end:       
    i = round(i,2)
    j = round(j,2)
    print("11")
    if grid_dict[j,i] == 0:
       temp_key = (j,i)
       print("1")
       evaluated_pde = evaluate_pde_at_key(temp_key, h, k)
       print("2")
       updates_dict[j, i] = solve(evaluated_pde,x)
       print("3")
       grid_dict.update(updates_dict)
       print("4")
"""






# TESTING THE INITIAL CONDITIONS
"""
from sympy import symbols, lambdify, sympify

# Define symbols for sympy
x, t = symbols('x t')

def create_functions_from_user_inputs():
    # Ask for the number of initial conditions
    num_conditions = int(input("Enter the number of initial conditions: "))

    # Dictionary to store the functions for each condition
    condition_functions = {}

    for _ in range(num_conditions):
        # Prompt the user to enter the condition
        user_input = input("Enter the initial condition (e.g., 'U(x,0) = x*5', 'U(2,t) = t**3', 'U(x,1) = 4'): ").strip()

        # Parse the condition
        condition, expression = user_input.split('=')
        condition = condition.strip()
        expression = expression.strip()

        # Determine the variable and point/value in the condition
        if 'x' in condition:
            point, _ = condition.split(',')
            point = point.strip('u( ')
            if point == 'x':
                # Variable is x, and the condition is at a specific t value
                at_value = float(condition.split(',')[1].strip(' )'))
                func = lambdify(x, sympify(expression), modules=['numpy'])
                condition_functions[('x', at_value)] = func
            else:
                # Condition at a specific x value
                func = lambdify(t, sympify(expression), modules=['numpy'])
                condition_functions[('x', float(point))] = func
        elif 't' in condition:
            point, ttt = condition.split(',')
            ttt = ttt.strip(' )')
            if ttt == 't':
                # Variable is t, and the condition is at a specific x value
                at_value = float(condition.split(',')[0].strip('u( '))
                func = lambdify(t, sympify(expression), modules=['numpy'])
                condition_functions[(at_value, 't')] = func
            else:
                # Condition at a specific t value
                func = lambdify(x, sympify(expression), modules=['numpy'])
                condition_functions[(float(point), 't')] = func

    return condition_functions

# Create functions from user inputs
user_defined_functions = create_functions_from_user_inputs()

for key, func in user_defined_functions.items():
    if key[0] == 'x':
        # Test with some x value, for example x = 2
        test_value = 2
        print(f"Initial condition at x = {key[1]}, test_value = {test_value}: u = {func(test_value)}")
    elif key[1] == 't':
        # Test with some t value, for example t = 2
        test_value = 2
        print(f"Initial condition at t = {key[0]}, test_value = {test_value}: u = {func(test_value)}")

        """













"""

# Define the finite difference expressions using SymPy
def uxx(key):
    if key == 0:
       return x
    
    return (grid_dict(key[0]+h, key[1]) - 2*grid_dict(key[0], key[1]) + grid_dict(key[0]-h, key[1])) / h**2

def utt(key):
    if key == 0:
       return x
       
    return (grid_dict(key[0], key[1]+k) - 2*grid_dict(key[0], key[1]) + grid_dict(key[0], key[1]-k)) / k**2

def ux(key):
    if key == 0:
       return x
    
    if difference_type == "FD":
     return (grid_dict(key[0]+h, key[1]) - grid_dict(key[0], key[1])) / h
    elif difference_type == "BD":
     return (grid_dict(key[0]+h, key[1]) - grid_dict(key[0]-h, key[1])) / h
    elif difference_type == "CD":
     return (grid_dict(key[0]+h, key[1]) - grid_dict(key[0]-h, key[1])) / h*2
    
def ut(key):
    if key == 0:
       return x

    if difference_type == "FD":
     return (grid_dict(key[0], key[1]+k) - grid_dict(key[0], key[1])) / k
    elif difference_type == "BD":
     return (grid_dict(key[0], key[1]) - grid_dict(key[0], key[1]-k)) / k
    elif difference_type == "CD":
     return (grid_dict(key[0], key[1]+k) - grid_dict(key[0], key[1]-k)) / k*2



# Function to create a PDE using finite difference formulas
def create_pde(user_pde_input):
    # Parse the user input
    lhs_term = user_pde_input.split('=')[0].strip()
    rhs_term = user_pde_input.split('=')[1].strip()

    # Handle the left hand side of the pde as a general expression
    lhs_expr = sympify(lhs_term, locals={'u': grid_dict(x, t) if grid_dict(x,t) != 0 else x, 'ux': ux(key), 'ut': ut(key),'utt': utt(key),'uxx': uxx(key)})

    # Handle the right-hand side of the PDE as a general expression
    rhs_expr = sympify(rhs_term, locals={'u': grid_dict(x, t) if grid_dict(x,t) != 0 else x, 'ux': ux(key), 'ut': ut(key),'utt': utt(key),'uxx': uxx(key)})

    # Create the PDE as an equation
    pde = Eq(lhs_expr, rhs_expr)

    return pde

# Example PDE input from the user
pde_input = input("Enter PDE: ")

# Create the finite difference PDE
fd_pde = create_pde(pde_input)

"""

"""
if difference_type == "CD":
   #Expand the grid 1 point in each direction
   x_start_for_loop_temp = x_start_for_loop - h
   x_end_for_loop_temp = x_end_for_loop + h
   t_start_for_loop_temp = t_start_for_loop - k
   t_end_for_loop_temp = t_end_for_loop + k

   #for i in np.arange(x_start_for_loop_temp, x_end_for_loop_temp+h, h):
      #val = grid_dict[i+h,t_start_for_loop+k] - user_defined_function(i)*2*k
      #grid_dict[i,t_start_for_loop_temp] = val
      #print(f"At x: {i} , At y: {t_start_for_loop} , Value is {val}")
      

   #determine which point in the grid has only 1 unkown
   for i in np.arange(x_start_for_loop, x_end_for_loop+h, h):
    for j in np.arange(t_start_for_loop, t_end_for_loop+k, k_CD):
       
       c = 0

       val_left = grid_dict[i-h,j]
       val_right = grid_dict[i+h,j] 
       val_up = grid_dict[i,j+k] 
       val_down = grid_dict[i,j-k] 
       
       if grid_dict[i-h,j] == 0:
          c += 1
       if grid_dict[i+h,j]  == 0:
          c += 1
       if grid_dict[i,j+k]  == 0:
          c += 1
       if grid_dict[i,j-k] == 0:
          c += 1
"""
    # For loop on all thegrod of you find no points that has only 1 0 around it You know you will create the imaginary
    # For loop starts from inside the grid . aka don't include any boundary points
    # The points next to any boundary are always the ones needed
    #? Cirteria to which boundary should i move into?
    # I think you should look for it depending on the pde. maybe a little helper function to look for uxx or utt in the pde
    # Then depedning on the wanted point if we need its left or right i should go for left boundary or right boundary or top or down
    # 
    
   #Look at pde equation and determine points that you will need utt / uxx tells you will need 1 above , 1 below , 1 right , 1 left
   #? How to know the differnce between when i need imaginary points and when i don't ?
   #Depending on required point determine if you will go left <-- or top or bottom
   #Depending on the direction where you find a point that only has 1 X and all others in the pde equation are available
   #Get the 3 imaginary points on the axis you went in the direction of
   #Make for loop to go from the
   

 # BASMAGHA LE TA7T
 # Instead of getting the point relative to other just change the final formula in the pde
 # u(i,j-k) = u(i,j+k) - 2*k*u(i,j)
 # utt = 2*k*u(i,j) / k**2

 # BASMAGHA LE Shmal
 # Instead of getting the point relative to other just change the final formula in the pde
 # u(i-h,j) = u(i+h,j) - 2*h*u(i,j)
 # uxx = 2*h*u(i,j) / h**2
