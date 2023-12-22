# TESTING THE PDE INPUT

from sympy import symbols, Function, Eq, sympify

# Define symbols
x, t, h, k = symbols('x t h k')
u = Function('u')

difference_type = "FD"
# Define the finite difference expressions using SymPy
def uxx():
    return (u(x+h, t) - 2*u(x, t) + u(x-h, t)) / h**2

def utt():
    return (u(x, t+k) - 2*u(x, t) + u(x, t-k)) / k**2

def ux():
    if difference_type == "FD":
     return (u(x+h, t) - u(x, t)) / h
    elif difference_type == "BD":
     return (u(x+h, t) - u(x-h, t)) / h
    elif difference_type == "CD":
     return (u(x+h, t) - u(x-h, t)) / h*2
    
def ut():
    if difference_type == "FD":
     return (u(x, t+k) - u(x, t)) / k
    elif difference_type == "BD":
     return (u(x, t) - u(x, t-k)) / k
    elif difference_type == "CD":
     return (u(x, t+k) - u(x, t-k)) / k*2



# Function to create a PDE using finite difference formulas
def create_pde(user_pde_input):
    # Parse the user input
    lhs_term = user_pde_input.split('=')[0].strip()
    rhs_term = user_pde_input.split('=')[1].strip()

    sympy_locals = {
        'u': u(x, t),
        'uxx': uxx(),
        'utt': utt(),
        'ux': ux(),
        'ut': ut()
    }

    # Handle the left hand side of the pde as a general expression
    lhs_expr = sympify(lhs_term, locals=sympy_locals)

    # Handle the right-hand side of the PDE as a general expression
    rhs_expr = sympify(rhs_term, locals=sympy_locals)

    # Create the PDE as an equation
    pde = Eq(lhs_expr, rhs_expr)

    return pde

# Example PDE input from the user
pde_input = input("Enter PDE: ")

# Create the finite difference PDE
fd_pde = create_pde(pde_input)

def evaluate_pde_at_key(pde, grid_dict, key, h_val, k_val):
    # Substitute the key into the PDE
    pde_substituted = pde.subs({x: key[0], t: key[1], h: h_val, k: k_val})

    # Evaluate the PDE using the grid dictionary
    pde_evaluated = pde_substituted.subs({u(x, t): grid_dict.get(key, 0)})

    return pde_evaluated


# Example grid dictionary and key
grid_dict = {(1, 1): 3, (1.2, 1): 4, (0.8, 1): 2, (1, 1.2): 5, (1, 0.8): 1}
key = (1, 1)
h_val = 2
k_val = 2

# Evaluate the PDE at the key
evaluated_pde = evaluate_pde_at_key(fd_pde, grid_dict, key, h_val, k_val)

print("Evaluated PDE at key:", evaluated_pde)







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