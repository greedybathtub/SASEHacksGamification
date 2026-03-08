import os

def get_points(user_file):

    if not os.path.exists(user_file):
        return 0

    with open(user_file, "r") as f:
        for line in f:
            if line.startswith("PointsEarned:"):
                return int(line.replace("PointsEarned:", "").strip())

    return 0


def add_points(user_file, amount):

    points = get_points(user_file)
    points += amount

    lines = []

    if os.path.exists(user_file):
        with open(user_file, "r") as f:
            lines = f.readlines()

    updated = False

    for i, line in enumerate(lines):
        if line.startswith("PointsEarned:"):
            lines[i] = f"PointsEarned:{points}\n"
            updated = True
            break

    if not updated:
        lines.append(f"PointsEarned:{points}\n")

    with open(user_file, "w") as f:
        f.writelines(lines)

    return points