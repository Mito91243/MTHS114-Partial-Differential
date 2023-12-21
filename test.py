# TESTING THE PDE INPUT

"""
from sympy import symbols, Function, Eq, sympify

# Define symbols
x, t, h, k = symbols('x t h k')
u = Function('u')

# Define the finite difference expressions using SymPy
def uxx(u, x, t, h):
    return (u(x+h, t) - 2*u(x, t) + u(x-h, t)) / h**2

def uyy(u, x, t, k):
    return (u(x, t+k) - 2*u(x, t) + u(x, t-k)) / k**2

# Function to create a PDE using finite difference formulas
def create_fd_pde(user_pde_input):
    # Parse the user input
    lhs_terms = user_pde_input.split('=')[0].split('+')
    rhs_term = user_pde_input.split('=')[1].strip()

    # Initialize the left-hand side of the PDE
    lhs_expr = 0

    # Add each term to the left-hand side expression
    for term in lhs_terms:
        term = term.strip()
        if term == 'uxx':
            lhs_expr += uxx(u, x, t, h)
        elif term == 'uyy':
            lhs_expr += uyy(u, x, t, k)
        elif term == 'u' or term == 'uxt':
            lhs_expr += u(x, t)

    # Handle the right-hand side of the PDE
    if rhs_term == 'u':
        rhs_expr = u(x, t)
    else:
        # If the term is a multiple of 'u', like '2*u'
        coeff, _ = rhs_term.split('*')
        rhs_expr = sympify(coeff) * u(x, t)

    # Create the PDE as an equation
    pde = Eq(lhs_expr, rhs_expr)

    return pde

# Example PDE input from the user
user_pde_input = input("Enter PDE: ")

# Create the finite difference PDE
fd_pde = create_fd_pde(user_pde_input)

# Print the PDE
print(fd_pde)
"""





# TESTING THE INITIAL CONDITIONS

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
