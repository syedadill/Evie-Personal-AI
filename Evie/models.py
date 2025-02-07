# models.py
from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     date_of_birth = models.DateField(blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     email = models.EmailField( blank=True, null=True)
#     nationality = models.CharField(max_length=50, blank=True, null=True)
#     languages_spoken = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username}'s Profile"
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Each user gets ONE profile
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    languages_spoken = models.CharField(max_length=255, blank=True, null=True)

    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    institution_name = models.CharField(max_length=255, blank=True, null=True)
    specialty = models.CharField(max_length=255, blank=True, null=True)
    degree = models.CharField(max_length=255, blank=True, null=True)
    education_address = models.CharField(max_length=255, blank=True, null=True)
    education_city = models.CharField(max_length=100, blank=True, null=True)
    education_state = models.CharField(max_length=100, blank=True, null=True)
    education_zip_code = models.CharField(max_length=20, blank=True, null=True)
    education_country = models.CharField(max_length=100, blank=True, null=True)
    education_achievements = models.TextField(blank=True, null=True)

    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    work_address = models.CharField(max_length=255, blank=True, null=True)
    work_city = models.CharField(max_length=100, blank=True, null=True)
    work_state = models.CharField(max_length=100, blank=True, null=True)
    work_zip_code = models.CharField(max_length=20, blank=True, null=True)
    work_country = models.CharField(max_length=100, blank=True, null=True)
    supervisor_name = models.CharField(max_length=255, blank=True, null=True)
    supervisor_phone = models.CharField(max_length=20, blank=True, null=True)
    supervisor_email = models.EmailField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    work_achievements = models.TextField(blank=True, null=True)

    family_name = models.CharField(max_length=255, blank=True, null=True)
    family_relationship = models.CharField(max_length=100, blank=True, null=True)
    family_birthday = models.DateField(blank=True, null=True)
    family_notes = models.TextField(blank=True, null=True)
    family_phone = models.CharField(max_length=20, blank=True, null=True)
    family_email = models.EmailField(blank=True, null=True)

    car_make = models.CharField(max_length=100, blank=True, null=True)
    car_model = models.CharField(max_length=100, blank=True, null=True)
    car_year = models.IntegerField(blank=True, null=True)
    vin = models.CharField(max_length=100, blank=True, null=True)
    licence_plate = models.CharField(max_length=100, blank=True, null=True)
    date_purchased = models.DateField(blank=True, null=True)
    odometer_at_purchase = models.IntegerField(blank=True, null=True)
    total_purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    financed_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    real_estate_type = models.CharField(max_length=100, blank=True, null=True)
    real_estate_sq_ft = models.IntegerField(blank=True, null=True)
    real_estate_lot_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    real_estate_address = models.CharField(max_length=255, blank=True, null=True)
    real_estate_city = models.CharField(max_length=100, blank=True, null=True)
    real_estate_state = models.CharField(max_length=100, blank=True, null=True)
    real_estate_zip_code = models.CharField(max_length=20, blank=True, null=True)
    real_estate_country = models.CharField(max_length=100, blank=True, null=True)
    real_estate_year_built = models.IntegerField(blank=True, null=True)

    mortgage_real_estate = models.CharField(max_length=255, blank=True, null=True)
    financial_institution = models.CharField(max_length=255, blank=True, null=True)
    mortgage_monthly_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mortgage_notes = models.TextField(blank=True, null=True)
    mortgage_start_date = models.DateField(blank=True, null=True)
    mortgage_period = models.CharField(max_length=100, blank=True, null=True)
    property_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    down_percent = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mortgage_down_payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mortgage_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    apr = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    upfront_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    blood_type = models.CharField(max_length=5, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)

    travel_destination = models.CharField(max_length=255, blank=True, null=True)
    travel_date_start = models.DateField(blank=True, null=True)
    travel_date_end = models.DateField(blank=True, null=True)
    travel_notes = models.TextField(blank=True, null=True)

    membership_type = models.CharField(max_length=100, blank=True, null=True)
    membership_company = models.CharField(max_length=255, blank=True, null=True)
    membership_number = models.CharField(max_length=100, blank=True, null=True)
    membership_status = models.CharField(max_length=100, blank=True, null=True)
    membership_notes = models.TextField(blank=True, null=True)

    preference_type = models.CharField(max_length=100, blank=True, null=True)
    favorite_item = models.CharField(max_length=255, blank=True, null=True)

    celebration_event = models.CharField(max_length=255, blank=True, null=True)
    celebration_person = models.CharField(max_length=255, blank=True, null=True)
    celebration_date = models.DateField(blank=True, null=True)
    first_event_date = models.DateField(blank=True, null=True)
    celebration_notes = models.TextField(blank=True, null=True)

    insurance_type = models.CharField(max_length=100, blank=True, null=True)
    insurance_provider = models.CharField(max_length=255, blank=True, null=True)
    policy_number = models.CharField(max_length=100, blank=True, null=True)
    insurance_start_date = models.DateField(blank=True, null=True)
    insurance_end_date = models.DateField(blank=True, null=True)
    premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coverage_details = models.TextField(blank=True, null=True)
    linked_asset = models.CharField(max_length=255, blank=True, null=True)
    insurance_notes = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
class PDFUpload(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
