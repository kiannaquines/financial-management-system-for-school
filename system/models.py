from django.db import models
from authentication.models import AuthUser


class Assistance(models.Model):

    ASSISTANCE_TYPE = [
        ("Death", "Death"),
        ("Hospitalization", "Hospitalization"),
    ]

    request_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    assistance_first_name = models.CharField(max_length=50)
    assistance_middle_name = models.CharField(max_length=50)
    assistance_last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    type_of_assistance = models.CharField(max_length=50, choices=ASSISTANCE_TYPE)
    assistance_status = models.BooleanField(default=False)
    assistance_evidence_first = models.ImageField(upload_to="assistance/proof/")
    assistance_evidence_second = models.ImageField(upload_to="assistance/proof/")
    amount_released = models.DecimalField(max_digits=10, default=0.00, decimal_places=2)
    date_released = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.assistance_first_name} {self.assistance_last_name} {self.suffix}"

    class Meta:
        verbose_name = "Assistance"
        verbose_name_plural = "Assistances"
        db_table = "assistance"


class Beneficiary(models.Model):

    RELATIONSHIP = [
        ("Mother", "Mother"),
        ("Father", "Father"),
        ("Child", "Child"),
        ("Spouse", "Spouse"),
    ]

    user_id = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    beneficiary_first_name = models.CharField(max_length=50)
    beneficiary_middle_name = models.CharField(max_length=50, blank=True)
    beneficiary_last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP)
    date_of_birth = models.DateField()
    proof = models.ImageField(upload_to="beneficiary/proof/")
    used = models.BooleanField(default=True)

    def __str__(self) -> str:
        return (
            f"{self.beneficiary_first_name} {self.beneficiary_last_name} {self.suffix}"
        )

    class Meta:
        verbose_name = "Benefeciary"
        verbose_name_plural = "Beneficiaries"
        db_table = "benefeciary"


class Membership(models.Model):

    POSITION = [
        ("Teacher 1", "Teacher 1"),
        ("Teacher 2", "Teacher 2"),
        ("Teacher 3", "Teacher 3"),
        ("Teacher 4", "Teacher 4"),
        ("Teacher 5", "Teacher 5"),
        ("Principal", "Principal"),
        ("ADAS", "ADAS"),
    ]

    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    SCHOOL_AFFILIATION = [
        ("Dapiowan Central ES", "Dapiowan Central ES"),
        ("Datu Pendililang ES", "Datu Pendililang ES"),
        ("Madia ES", "Madia ES"),
        ("Elian ES", "Elian ES"),
        ("Gawang ES", "Gawang ES"),
        ("Kitango ES", "Kitango ES"),
        ("Kitapok ES", "Kitapok ES"),
        ("Datu Kogia ES", "Datu Kogia ES"),
        ("Dimaukon Utto ES", "Dimaukon Utto ES"),
        ("Dimankom ES", "Dimankom ES"),
    ]

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    place_of_birth = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    employee_id = models.CharField(max_length=50)
    position = models.CharField(max_length=50, choices=POSITION)
    gender = models.CharField(max_length=20, choices=GENDER)
    school_affiliation = models.CharField(max_length=100, choices=SCHOOL_AFFILIATION)
    beneficiary = models.ManyToManyField(Beneficiary,blank=True)
    membership_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "membership"
        verbose_name = "Membership"
        verbose_name_plural = "Membership"


class Payment(models.Model):

    PAYMENT_TYPE = [
        ("Membership", "Membership Fee"),
        ("Delegation Pay", "Delegation Pay"),
        ("Trust Fund", "Trust Fund"),
        ("Visitors Fund", "Visitors Fund"),
    ]

    id = models.AutoField(primary_key=True)
    paid_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    amount = models.FloatField()
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Paid by {self.paid_by.username}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "payment"
