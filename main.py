from sympy import *

# first step is to determine the number of spans on the beam
number_of_supports = int(input("number of supports? "))
number_of_internal_joints = int(input("number of internal joints? "))
number_of_nodes = number_of_supports + number_of_internal_joints
number_of_spans = number_of_nodes - 1


# create a class to store the properties of each node, then create functions that will calculate each property
class Node:
    def __init__(self, settlement, angular_displacement, equilibrium_equation):
        self.settlement = settlement
        self.angular_displacement = angular_displacement
        self.equilibrium_equation = equilibrium_equation


# store all the nodes in a list, and make everything node an instance of the class 'Node'
beam_nodes = []
settlement_variable = ""
angular_displacement_variable = ""
equilibrium_equation_variable = ""
for i in range(number_of_nodes):
    beam_nodes.append("")
    beam_nodes[i] = Node(settlement_variable, angular_displacement_variable, equilibrium_equation_variable)

# make all the unknown angular displacements sympy symbols, and store them in a list, first and last are always = 0
list_of_unknown_angular_displacements = []
first_node = "A"
for i in range(number_of_nodes):
    if i != 0 and i != number_of_nodes - 1:
        beam_nodes[i].angular_displacement = symbols(f"Theta_{first_node}")
        list_of_unknown_angular_displacements.append(beam_nodes[i].angular_displacement)
    else:
        beam_nodes[i].angular_displacement = symbols(f"Theta_{first_node}")
        beam_nodes[i].angular_displacement = 0

    first_node = chr(ord(first_node) + 1)


# create a class to store the properties of each span, then create functions that will calculate each property
class Span:
    def __init__(self, left_fem, right_fem, span_length, load, loading_condition, cord_rotation, left_moment,
                 right_moment, left_slope_deflection_equation, right_slope_deflection_equation):
        self.left_fem = left_fem
        self.right_fem = right_fem
        self.span_length = span_length
        self.load = load
        self.loading_condition = loading_condition
        self.cord_rotation = cord_rotation
        self.left_moment = left_moment
        self.right_moment = right_moment
        self.left_slope_deflection_equation = left_slope_deflection_equation
        self.right_slope_deflection_equation = right_slope_deflection_equation


# store all the nodes in a list, and make everything node an instance of the class 'Node'
beam_spans = []
left_fem_variable = ""
right_fem_variable = ""
span_length_variable = ""
load_variable = ""
loading_condition_variable = ""
cord_rotation_variable = ""
left_moment_variable = ""
right_moment_variable = ""
left_slope_deflection_equation_variable = ""
right_slope_deflection_equation_variable = ""
for i in range(number_of_spans):
    beam_spans.append("")
    beam_spans[i] = Span(left_fem_variable, right_fem_variable, span_length_variable, load_variable,
                         loading_condition_variable, cord_rotation_variable, left_moment_variable,
                         right_moment_variable, left_slope_deflection_equation_variable,
                         right_slope_deflection_equation_variable)

# the parameters needed for the FEM calculation are gotten from user
print("Key words for loading condition:"
      "\nNo loading on span (none)"
      "\nPoint load at center (P_C)"
      "\nPoint load at distance 'a' from left end and 'b' from the right end (P_X)"
      "\nTwo equal point loads, spaced at 1/3 of the total length from each other (P_C_2)"
      "\nThree equal point loads, spaced at 1/4 of the total length from each other (P_C_3)"
      "\nUniformly distributed load over the whole length (UDL)"
      "\nUniformly distributed load over half of the span (UDL/2)"
      "\nVariably distributed load, with highest point on the right end (VDL_R)"
      "\nVariably distributed load, with highest point on the left end (VDL_L)"
      "\nVariably distributed load, with highest point at the center (VDL_C)")
for i in range(number_of_spans):
    beam_spans[i].loading_condition = input(f"what is the nature of loading on span {i + 1}? ")
    beam_spans[i].span_length = float(input(f"what is the length of span {i + 1}? "))
    beam_spans[i].load = float(input(f"what is the magnitude of loading on the span {i + 1}? "))

    if beam_spans[i].loading_condition == 'P_C':
        beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length) / 8
        beam_spans[i].left_fem = -1 * beam_spans[i].right_fem
    elif beam_spans[i].loading_condition == 'P_X':
        a = int(input("distance from point load to the right end joint"))
        b = beam_spans[i].span_length - a
        beam_spans[i].right_fem = (beam_spans[i].load * b * a * a) / (beam_spans[i].span_length *
                                                                      beam_spans[i].span_length)

        beam_spans[i].left_fem = (beam_spans[i].load * b * b * a) / (beam_spans[i].span_length *
                                                                     beam_spans[i].span_length)
    elif beam_spans[i].loading_condition == 'P_C_2':
        beam_spans[i].right_fem = (2 * beam_spans[i].load * beam_spans[i].span_length) / 9
        beam_spans[i].left_fem = -1 * beam_spans[i].right_fem
    elif beam_spans[i].loading_condition == 'P_C_3':
        beam_spans[i].right_fem = (15 * beam_spans[i].load * beam_spans[i].span_length) / 48
        beam_spans[i].left_fem = -1 * beam_spans[i].right_fem
    elif beam_spans[i].loading_condition == 'UDL':
        beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 12
        beam_spans[i].left_fem = -1 * beam_spans[i].right_fem
    elif beam_spans[i].loading_condition == 'UDL/2':
        beam_spans[i].right_fem = (5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 192
        beam_spans[i].left_fem = -1 * (11 * beam_spans[i].load * beam_spans[i].span_length *
                                       beam_spans[i].span_length) / 192
    elif beam_spans[i].loading_condition == 'VDL_R':
        beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 20
        beam_spans[i].left_fem = -1 * (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30
    elif beam_spans[i].loading_condition == 'VDL_L':
        beam_spans[i].right_fem = (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 30
        beam_spans[i].left_fem = -1 * (beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 20
    elif beam_spans[i].loading_condition == 'VDL_C':
        beam_spans[i].right_fem = (5 * beam_spans[i].load * beam_spans[i].span_length * beam_spans[i].span_length) / 96
        beam_spans[i].left_fem = -1 * beam_spans[i].right_fem
    elif beam_spans[i].loading_condition == "none":
        beam_spans[i].right_fem = 0
        beam_spans[i].left_fem = 0
        print("No loading on span")


# Make all the end span moments sympy symbols, and store them in a list of unknown end moments
list_of_unknown_end_moments = []
left_end = "a"
right_end = "b"
for i in range(number_of_spans):
    beam_spans[i].left_moment, beam_spans[i].right_moment = symbols(f"M{left_end}{right_end} M{right_end}{left_end}")
    left_end = chr(ord(left_end) + 1)
    right_end = chr(ord(right_end) + 1)
    list_of_unknown_end_moments.append(beam_spans[i].left_moment)
    list_of_unknown_end_moments.append(beam_spans[i].right_moment)

# next is to get the value of the support settlements
settlement_on_beam = input("Is there any settlement on the beam (yes) or (no)? ")
if settlement_on_beam != "yes":
    print("No settlement on beam")
    for node in range(number_of_nodes):
        beam_nodes[node].settlement = 0
else:
    settlement_positions = []
    for i in range(number_of_nodes):
        position = int(input("input the first settlement position: "))
        while position != "":
            settlement_positions.append(position)
            position = int(input("input the first settlement position: "))

        for node in range(number_of_nodes):
            if node in settlement_positions:
                beam_nodes[i].settlement = int(input(f"value of settlement at position {node}?: "))
            else:
                beam_nodes[i].settlement = 0

# next is to determine the value of the cord rotation for each span
for i in range(number_of_spans):
    beam_spans[i].cord_rotation = (
            (beam_nodes[i + 1].settlement - beam_nodes[i].settlement) / beam_spans[i].span_length)

# for the slope deflection equations, we need to check if the first and last nodes are fixed
first_node_fixed = input("is first node fixed? (yes) or (no): ")
last_node_fixed = input("is last node fixed? (yes) or (no): ")

# next is to express the two slope deflection equations for each span, and store them in a list
list_of_slope_deflection_equations = []
for i in range(number_of_spans):
    if i == 0 and first_node_fixed == "no":
        beam_spans[i].left_slope_deflection_equation = 0
        beam_spans[i].right_slope_deflection_equation = \
            Eq(
                (((3 * (beam_nodes[i + 1].angular_displacement - beam_spans[i].cord_rotation)) / beam_spans[
                    i].span_length)
                 + beam_spans[i].right_fem), beam_spans[i].right_moment
            )

    elif i == number_of_spans - 1 and last_node_fixed == "no":
        beam_spans[i].left_slope_deflection_equation = \
            Eq(
                (((3 * (beam_nodes[i].angular_displacement - beam_spans[i].cord_rotation)) / beam_spans[i].span_length)
                 + beam_spans[i].left_fem), beam_spans[i].left_moment
            )
        beam_spans[i].right_slope_deflection_equation = 0

    else:
        beam_spans[i].left_slope_deflection_equation = Eq((((2 * (
                (2 * beam_nodes[i].angular_displacement) + beam_nodes[i + 1].angular_displacement - (
                 3 * beam_spans[i].cord_rotation))) / beam_spans[i].span_length) + beam_spans[i].left_fem),
                                                          beam_spans[i].left_moment)
        beam_spans[i].right_slope_deflection_equation = Eq((((2 * (
                (2 * beam_nodes[i + 1].angular_displacement) + beam_nodes[i].angular_displacement - (
                 3 * beam_spans[i].cord_rotation))) / beam_spans[i].span_length) + beam_spans[i].right_fem),
                                                           beam_spans[i].right_moment)

    list_of_slope_deflection_equations.append(beam_spans[i].left_slope_deflection_equation)
    list_of_slope_deflection_equations.append(beam_spans[i].right_slope_deflection_equation)

# next is to define the equilibrium equations, and store it in a list
list_of_equilibrium_equations = []
for i in range(number_of_nodes):
    if i != 0 and i != number_of_nodes - 1:
        beam_nodes[i].equilibrium_equation = Eq(beam_spans[i - 1].right_moment + beam_spans[i].left_moment, 0)
    else:
        beam_nodes[i].equilibrium_equation = 0

    list_of_equilibrium_equations.append(beam_nodes[i].equilibrium_equation)

# store the equations and the unknowns in lists
equations = list_of_slope_deflection_equations + list_of_equilibrium_equations
unknowns = list_of_unknown_end_moments + list_of_unknown_angular_displacements

# next is to solve all the equations for the unknowns
solution = solve(tuple(equations), tuple(unknowns))

print(solution)


# make code work with settlement
# make code work for beams with cantilever
# make code work for frames
# make code work for beams and frames with point moment
