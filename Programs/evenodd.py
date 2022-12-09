
import pdb
def check(n):
    if (n < 2):
        return (n % 2 == 0)
    return (check(n - 2))

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    pdb.set_trace()
    n = int(input("Enter number:"))
    if (check(n) == True):
        print("Number is even!")
    else:
        print("Number is odd!")