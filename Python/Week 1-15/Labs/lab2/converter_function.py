def unit_converter(value, input_unit, output_unit):
    if input_unit == "kg":
        base = value * 1
    elif input_unit == "g":
        base = value / 1000
    elif input_unit == "lb":
        base = value / 2.20462
    elif input_unit == "oz":
        base = value / (16*2.20462)
    else:
        print ("Test Failed")
    
    if output_unit == "kg":
        ans = base * 1
    elif output_unit == "g":
        ans = base * 1000
    elif output_unit == "lb":
        ans = base * 2.20462
    elif output_unit == "oz":
        ans = base * (16*2.20462)
    else:
        print ("Test Failed")
    
    return ans

print(unit_converter(1.0, 'kg', 'g'))
print(unit_converter(2, 'kg', 'lb'))
print(unit_converter(35, 'kg', 'oz'))

print(unit_converter(2000, 'g', 'kg'))
print(unit_converter(5, 'g', 'lb'))
print(unit_converter(10, 'g', 'oz'))

print(unit_converter(15, 'lb', 'g'))
print(unit_converter(80, 'lb', 'kg'))
print(unit_converter(120, 'lb', 'oz'))

print(unit_converter(32, 'oz', 'g'))
print(unit_converter(3, 'oz', 'kg'))
print(unit_converter(0.5, 'oz', 'lb'))

print(unit_converter(0.5, 'ou', 'lb'))