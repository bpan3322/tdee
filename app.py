from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate bmr
# Men BMR = 88.362 + (13.397 x kg) + (4.799 x cm) - (5.677 x age)
# women BMR = 447.593 + (9.247 x kg) + (3.098 x cm) - (4.330 x age)
def calculate_bmr(weight, height, age, gender):
    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "female":
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Invalid Gender")
    return bmr

# Function to calculate TDEE based off of bmr
# Each activity level has it's own factor as well that we wanna multiply it by
def calculate_tdee(bmr, activity_level):
    activity_factors = {
        'sedentary': 1.2,
        'light':1.375,
        'moderate': 1.55,
        'heavy': 1.725,
        'athlete': 1.9
    }
    if activity_level in activity_factors:
        tdee = bmr * activity_factors[activity_level]
    else:
       raise ValueError("Need to choose one of the activity level options")
    return tdee

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # convert weight and height to float no matter their input
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            age = int(request.form['age'])
            gender = request.form['gender']
            activity_level = request.form['activity_level']

            # Calculate BMR
            bmr = calculate_bmr(weight, height, age, gender)

            # Calculate TDEE
            tdee = calculate_tdee(bmr, activity_level)

            return render_template('results.html', weight=weight, height=height, age=age, gender=gender, activity_level=activity_level, bmr=bmr, tdee=tdee)
        except ValueError as e:
            error = str(e)
            return render_template('index.html', error=error)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
