# -*- coding: utf-8 -*-
"""Author: Payton Dunning
    Last Date Modified: 12/9/2020
    Script for modifying CC3D XML Files.    
"""
import xml.etree.ElementTree as ET

#sphereTest XML File: C:\Users\Temp\Desktop\BioChem Research\Newer Simulations\sphereTest\SphereTest\Simulation\SphereTest.xml
#Blobby XML File: C:\Users\Temp\Desktop\BioChem Research\Newer Simulations\sphereTest\SphereTest\Simulation\Blobby.xml

def test1():
    print("Hello World")
    
    tree = ET.parse(r"C:\Users\Temp\Desktop\BioChem Research\Newer Simulations\sphereTest\SphereTest\Simulation\SphereTest.xml")
    root = tree.getroot()
    #stringRoot = ET.fromstring()
    
    print(root)
    print(root.attrib)
    #Returns iterator for every child element in the XML file.
    '''iterator = root.iter()
    for x in iterator:
        print(x)
    '''
    
    iterator1 = root.iter()
    
    #for temp in root.iter():
    #    print(temp.text)
    potts = root.find('Potts')
    temp = potts.find('Temperature')
    print(temp.text)
    temp.text = "10"
    tree.write(r"C:\Users\Temp\Desktop\BioChem Research\Newer Simulations\Blobby\Simulation\Blobby.xml")
    #temp = root.find('Temperature')
    #temp.set(50)
    #potts = root.find('Potts')
    #root.set('Temperature', 50)
    #temp = potts.get('Temperature')
    #print(temp)
    #potts.set('Temperature', 50)

def tempMod(rootArg, treeArg):
    #print("Temp Mod")
    potts = rootArg.find('Potts')
    temp = potts.find('Temperature')
    tempText = temp.text
    
    print("Temperature is currently set to %s" %(tempText))
    print("Enter new Temperature setting: ")
    newTemp = input()
    
    temp.text = newTemp
    treeArg.write(r"C:\Users\Temp\Desktop\BioChem Research\Newer Simulations\Blobby\Simulation\Blobby.xml")


def stepMod(rootArg):
    print("Step Mod")
    
def neighborMod(rootArg):
    print("Order Mod")

def dimensionMod(rootArg):
    print("Dimension Mod")
    
def test2():
   print("Welcome to XML Modder!")
   print("By default, Blobby.xml is the xml file we'll be modifying")
   print("Don't worry, you can select a different XML file to modify later!")
   
   tree = ET.parse(r"C:\Users\Temp\Desktop\BioChem Research\Newer Simulations\Blobby\Simulation\Blobby.xml")
   root = tree.getroot()
   
   print("For now, please select a CC3D XML file element to modify from the following list:")
   print("To modify Temperature, enter 'temp'")
   print("To modify Steps, enter 'steps'")
   print("To modify NeighborOrder, enter 'order'")
   print("To modify Dimensions, enter 'dimensions")
   print("Enter 'exit' at any time to quit.")
   
   userSelect = input()
   
   while(userSelect != "exit"):
       #print("While Iteration Check")
       
       if(userSelect == "temp"):
           tempMod(root, tree)

       elif(userSelect == "steps"):
            stepMod(root)
       elif(userSelect == "order"):
            neighborMod(root)
       elif(userSelect == "dimensions"):
            dimensionMod(root)
       else:
            print("Invalid Input, please select from the previously listed options.")
       print("Enter next input: ")
       userSelect = input()
test2()