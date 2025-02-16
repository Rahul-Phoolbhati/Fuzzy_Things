
import matplotlib.pyplot as plt
import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl

# # Define the inputs (antecedents)
# attendance = ctrl.Antecedent(np.arange(0, 101, 1), 'attendance')  # Attendance percentage (0-100)
# assignments = ctrl.Antecedent(np.arange(0, 101, 1), 'assignments') # Average assignment score (0-100)

# # Define the output (consequent)
# grade = ctrl.Consequent(np.arange(0, 101, 1), 'grade')  # Final grade (0-100)

# # Define fuzzy membership functions for inputs
# attendance['low'] = fuzz.trimf(attendance.universe, [0, 0, 50])
# attendance['medium'] = fuzz.trimf(attendance.universe, [25, 50, 75])
# attendance['high'] = fuzz.trimf(attendance.universe, [50, 100, 100])

# assignments['low'] = fuzz.trimf(assignments.universe, [0, 0, 60])
# assignments['medium'] = fuzz.trimf(assignments.universe, [40, 60, 80])
# assignments['high'] = fuzz.trimf(assignments.universe, [60, 100, 100])

# # Define fuzzy membership functions for the output (grade)
# grade['fail'] = fuzz.trimf(grade.universe, [0, 0, 50])
# grade['pass'] = fuzz.trimf(grade.universe, [40, 60, 80])
# grade['good'] = fuzz.trimf(grade.universe, [70, 90, 100])
# grade['excellent'] = fuzz.trimf(grade.universe, [80, 100, 100])

# # Define the rules
# rule1 = ctrl.Rule(attendance['low'] | assignments['low'], grade['fail'])
# rule2 = ctrl.Rule(attendance['medium'] & assignments['medium'], grade['pass'])
# rule3 = ctrl.Rule(attendance['high'] & assignments['high'], grade['excellent'])
# rule4 = ctrl.Rule(attendance['high'] & assignments['medium'], grade['good']) # Good attendance, medium assignments
# rule5 = ctrl.Rule(attendance['medium'] & assignments['high'], grade['good']) # Medium attendance, good assignments


# # Create the control system
# grading_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

# # Create a control system simulation
# grading = ctrl.ControlSystemSimulation(grading_ctrl)

# # Provide inputs (example values - you can change these)
# grading.input['attendance'] = 85  # 85% attendance
# grading.input['assignments'] = 75  # 75 average assignment score

# # Compute the output
# grading.compute()

# # Print the result
# print(f"Predicted grade: {grading.output['grade']:.2f}")

# # # Visualize (optional - uncomment to see the membership functions)
# # attendance.view()
# # assignments.view()
# # grade.view()
# # grading.view()  # Can be cluttered, better to view individual membership functions

# # Visualize (Corrected)
# attendance.view()
# plt.savefig("attendance.png")  # Save to attendance.png

# assignments.view()
# plt.savefig("assignments.png")

# grade.view()
# plt.savefig("grade.png")# View the grade membership functions

# # Inspect input and output values for the simulation
# print("Inputs to the fuzzy system:")
# print(grading.input)
# print("Output of the fuzzy system:")
# print(grading.output)

# # If you want to see the *rules* and how they were applied (more advanced)
# # You can explore the 'graded' object (the ControlSystemSimulation) further
# # But this is often more complex than just viewing the inputs/outputs.
# # For example:
# #print(grading.rules) # to see the rules
# #print(grading.rulebase) # to see how the rules are applied (numerical)


def trimf(x, params):
    """Triangular membership function."""
    a, b, c = params
    if x <= a or x >= c:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)

def fuzzify(value, membership_functions):
    """Fuzzify a crisp value using membership functions."""
    fuzzified_values = {}
    for name, func in membership_functions.items():
        fuzzified_values[name] = func(value)
    return fuzzified_values

def apply_rules(fuzzified_inputs, rules):
    """Apply fuzzy rules to fuzzified inputs."""
    fuzzy_output = {}
    for rule_antecedent, rule_consequent in rules.items():
        antecedent_terms = rule_antecedent.split(" AND ")  # Split into individual conditions
        antecedent_value = 1  # Initialize with 1 (AND logic)
        for term in antecedent_terms:
            term_parts = term.split(" OR ")  # Check for OR within the AND
            or_value = 0
            for or_term in term_parts:
                input_name, fuzzy_set = or_term.split(" is ")
                or_value = max(or_value, fuzzified_inputs[input_name][fuzzy_set])
            antecedent_value = min(antecedent_value, or_value)

        for consequent_set in rule_consequent.split(" OR "):  # Handle multiple consequents
            if consequent_set not in fuzzy_output:
                fuzzy_output[consequent_set] = 0
            fuzzy_output[consequent_set] = max(fuzzy_output[consequent_set], antecedent_value)

    return fuzzy_output


# def defuzzify_centroid(fuzzy_output, universe):
#     """Defuzzify using the centroid method (simplified)."""
#     numerator = 0
#     denominator = 0
#     for fuzzy_set, membership in fuzzy_output.items():
#         # A very simplified centroid: assume membership is constant across the set
#         # In reality, you'd integrate over the membership function
#         # For simplicity, we just use the midpoint of the set's range
#         set_range = universe[fuzzy_set]
#         midpoint = (set_range[0] + set_range[1]) / 2  # Simplified midpoint
#         numerator += membership * midpoint
#         denominator += membership
#     if denominator == 0:  # Handle cases where no rules fire
#         return 0  # Or another appropriate default
#     return numerator / denominator

def defuzzify_centroid(fuzzy_output, universe):
    """Defuzzify using the centroid method (more accurate)."""
    numerator = 0
    denominator = 0

    for fuzzy_set, membership in fuzzy_output.items():
        # Get the range for this fuzzy set from the universe
        set_range = universe[fuzzy_set]
        # More accurate centroid: integrate (approximated)
        # We'll approximate the integral by sampling points within the range
        num_samples = 100  # Number of points to sample (adjust for accuracy/speed)
        sample_points = np.linspace(set_range[0], set_range[1], num_samples)
        for x in sample_points:
            # We assume the membership is constant over the sampled range for this point
            numerator += membership * x  # x is the value on the universe of discourse
            denominator += membership

    if denominator == 0:  # Handle cases where no rules fire
        return 0  # Or another appropriate default
    return numerator / denominator
# Example usage:

# 1. Define Membership Functions
attendance_mf = {
    "low": lambda x: trimf(x, [0, 0, 50]),
    "medium": lambda x: trimf(x, [25, 50, 75]),
    "high": lambda x: trimf(x, [50, 100, 100]),
}

assignments_mf = {
    "low": lambda x: trimf(x, [0, 0, 60]),
    "medium": lambda x: trimf(x, [40, 60, 80]),
    "high": lambda x: trimf(x, [60, 100, 100]),
}

grade_mf = {
    "fail": lambda x: trimf(x, [0, 0, 50]),
    "pass": lambda x: trimf(x, [40, 60, 80]),
    "good": lambda x: trimf(x, [70, 90, 100]),
    "excellent": lambda x: trimf(x, [80, 100, 100]),
}

# Define the universe of discourse (simplified ranges)
attendance_universe = {"low": [0, 50], "medium": [25, 75], "high": [50, 100]}
assignments_universe = {"low": [0, 60], "medium": [40, 80], "high": [60, 100]}
grade_universe = {"fail": [0, 50], "pass": [40, 80], "good": [70, 90], "excellent": [80, 100]}

# 2. Define Rules (using strings for simplicity)
rules = {
    "attendance is low OR assignments is low": "fail",
    "attendance is medium AND assignments is medium": "pass",
    "attendance is high AND assignments is high": "excellent",
    "attendance is high AND assignments is medium": "good",
    "attendance is medium AND assignments is high": "good",
}

# 3. Get Inputs
attendance_input = 85
assignments_input = 75

# 4. Fuzzify Inputs
fuzzified_attendance = fuzzify(attendance_input, attendance_mf)  # Fuzzify attendance separately
fuzzified_assignments = fuzzify(assignments_input, assignments_mf) # Fuzzify assignments separately

fuzzified_inputs = {  # Create the combined dictionary with correct structure
    "attendance": fuzzified_attendance,
    "assignments": fuzzified_assignments,
}
# 5. Apply Rules
fuzzy_output = apply_rules(fuzzified_inputs, rules)

# 6. Defuzzify Output
grade = defuzzify_centroid(fuzzy_output, grade_universe)

# 7. Print Result
print(f"Predicted grade: {grade:.2f}")

def plot_membership_function(universe, mf_dict, title):
    """Plots membership functions for a given variable."""
    x_values = np.linspace(min(universe.values())[0], max(universe.values())[1], 100)  # Common x-axis
    plt.figure()  # Create a new figure for each variable
    for name, func in mf_dict.items():
        y_values = [func(x) for x in x_values]
        plt.plot(x_values, y_values, label=name)

    plt.xlabel(title)
    plt.ylabel("Membership Degree")
    plt.title(f"Membership Functions for {title}")
    plt.legend()
    plt.grid(True)
    # plt.savefig(f"{title}.png") # Save the plot
    plt.show() # Show the plot


plot_membership_function(attendance_universe, attendance_mf, "Attendance")
plot_membership_function(assignments_universe, assignments_mf, "Assignments")
plot_membership_function(grade_universe, grade_mf, "Grade")

