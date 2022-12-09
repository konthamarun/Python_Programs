a=[]
n=int(input("Enter number of elements:"))
for i in range(1,n+1):
    b=int(input("Enter element:"))
    a.append(b)
print(a)
a.sort()

print(" first Largest element is:",a[n-1])
print("second Largest element is:",a[n-2])
