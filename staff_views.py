from app import app

@app.route('/staff/home')
def staff_dashboard():
  return "Staff Dashboard"
@app.route('/staff/profile')
def staff_profile():
  return "Staff Profile"