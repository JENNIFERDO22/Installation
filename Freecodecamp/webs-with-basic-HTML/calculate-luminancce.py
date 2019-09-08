import math

# Link to the article: https://www.w3.org/TR/WCAG20-TECHS/G17.html

luminance = []

for i in range(2):
    print("Enter the RGB values")
    r = input("red ")
    g = input("green ")
    b = input("yellow ")

    r = int(r)
    g = int(g)
    b = int(b)

    r = r / 255
    b = b / 255
    g = g/255

    if r <= 0.03928:
        red = r/12.92
    else:
        red = math.pow(((r + 0.055)/1.055), 2.4)

    if g <= 0.03928:
        green = g/12.92
    else:
        green = math.pow(((g + 0.055)/1.055), 2.4)

    if b <= 0.03928:
        blue = b /12.92
    else:
        blue = math.pow(((b + 0.055)/1.055), 2.4)

    l = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    luminance.append(l)

ratio = (luminance[0]+0.05) / (luminance[1] + 0.05)
if ratio < 1:
    ratio = 1 / ratio

print("Ratio:", ratio)


