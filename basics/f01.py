# this program calculates the area of a rectangle given its length and width
def calculate_area_of_rectangle(length, width):
    if length < 0 or width < 0:
        raise ValueError("Length and width must be non-negative.")
    return length * width   

if __name__ == "__main__":
    try:
        length = float(input("Enter the length of the rectangle: "))
        width = float(input("Enter the width of the rectangle: "))
        area = calculate_area_of_rectangle(length, width)
        print(f"The area of the rectangle is {area}")
    except ValueError as e:
        print(f"Error: {e}")

