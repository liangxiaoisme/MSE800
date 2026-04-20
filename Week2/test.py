import math

class Operations:

    def Sum(self,a,b): 
     print(f"The sum of the numbers {a} and {b} is: {a+b} ")

    def Minus(self,a,b):
        print(f"The Difference of the {a} and {b} is: {a-b} ")

    def Multiply(self,a,b):
        print(f"The Multiplication of the {a} and {b} is: {a*b} ")    

    def Factorial(self,n):
       result= math.factorial(n)
       print(f"The factorial of {n} is: {result}")

def UserInput():
    x = int(input("Enter first value: "))
    y = int(input("Enter second value: "))
    return x, y

def Funcswitch(obj): #we can write the nickname here 
     while True:    #if this function was method, we use self as an arguments
      print("\n:---Calculator List:-----\n")
      print("1. Sum")
      print("2. Minus")
      print("3. Multiplication")
      print("4. Factorial")
      print("5. Exit\n")
      choice=int(input("Enter your choice:\n"))
      if choice==1:
          a,b=UserInput()
          obj.Sum(a,b)
      
      elif choice==2:
          a,b=UserInput()
          obj.Minus(a,b)
  
      elif choice==3:
          a,b=UserInput()
          obj.Multiply(a,b)
   
      elif choice==4:
          n=int(input("Enter the number to do factorial:\n"))
          obj.Factorial(n)
  
      elif choice==5:
          break    
      
      else:
          print("--ERROR: Invalid Choice")
      
              
obj= Operations()
#obj.Funcinput() #if it is a Method, do this
Funcswitch(obj)   #if it is a Function, do this