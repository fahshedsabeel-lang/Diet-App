
def calculate_bmr(age,weight,height,gender,activity_level="1.2"):
    bmr=0
    if gender=="male":
        bmr=(10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        (10 * weight) + (6.25 * height) - (5 * age) - 161
    # return round(bmr)

    tdee=bmr*float(activity_level)
    return bmr

# res=calculate_bmr(28,80,180,"male")

# print(res)