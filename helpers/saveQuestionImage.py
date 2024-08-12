import matplotlib.pyplot as plt
import math

def calculate_third_side(base=None, height=None, hypotenuse=None):
    if base is not None and height is not None:
        hypotenuse = math.sqrt(base ** 2 + height ** 2)
    elif base is not None and hypotenuse is not None:
        height = math.sqrt(hypotenuse ** 2 - base ** 2)
    elif height is not None and hypotenuse is not None:
        base = math.sqrt(hypotenuse ** 2 - height ** 2)
    return int(base), int(height), int(hypotenuse)

def save_right_triangle(user_base=None, user_height=None, user_hypotenuse=None, question_number=1):
    base, height, hypotenuse = calculate_third_side(user_base, user_height, user_hypotenuse)
    folder_dir = "images"

    plt.figure()
    plt.plot([0, base], [0, 0], 'k')  # Base
    plt.plot([0, 0], [0, height], 'k')  # Height
    plt.plot([base, 0], [0, height], 'k')  # Hypotenuse

    plt.text(base / 2, -(0.15 * height) , f'{base} cm' if user_base else '', ha='center', fontsize=20)
    plt.text(-(0.30 * base), height / 2, f'{height} cm' if user_height else '', va='center', fontsize=20)
    plt.text((0.60 * base), (0.60 * height), f'{hypotenuse} cm' if user_hypotenuse else '', ha='center', fontsize=20)

    plt.xlim(-1, base + 1)
    plt.ylim(-1, height + 1)
    plt.axis('off')
    path = f'{folder_dir}/right_triangle_0_{question_number}.png'
    plt.savefig(path)  # Save as image
    plt.close()
    return path