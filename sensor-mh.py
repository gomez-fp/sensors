import mh_z19

while True:
    
    x1 = mh_z19.read_all()
    x = x1['co2']
    x = x - 100
    print(x1)
    print("co2 = ", x)
