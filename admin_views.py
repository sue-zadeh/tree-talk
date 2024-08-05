from app import views

@views.route('/admin/dashboard')
def admin_dashboard():
  return "Admin Dashboard"

@views.route('/admin/profile')
def admin_profile():
  return "Admin Profile"