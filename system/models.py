from django.db import models
from authentication.models import AuthUser


class Dependents(models.Model):

    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    RELATIONSHIP_TYPE = (("Daughter", "Daughter"), ("Son", "Son"))
    related_to_member = models.ForeignKey(
        "Membership", on_delete=models.CASCADE, null=True, blank=True
    )
    dependent_first_name = models.CharField(
        max_length=50, help_text="The first name of the dependent"
    )
    dependent_middle_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="The middle name of the dependent",
    )
    dependent_last_name = models.CharField(
        max_length=100, help_text="The last name of the dependent"
    )
    suffix = models.CharField(
        max_length=10, blank=True, null=True, help_text="The suffix of the dependent"
    )
    gender = models.CharField(
        max_length=10, choices=GENDER, help_text="The gender of the dependent"
    )
    relationship_to_member = models.CharField(
        max_length=50,
        help_text="The relationship to the member",
        choices=RELATIONSHIP_TYPE,
    )

    date_added = models.DateTimeField(
        auto_now_add=True, help_text="The date added to the relationship"
    )

    def get_full_name_of_dependent(self):
        return (
            f"{self.dependent_first_name} {self.dependent_middle_name} {self.dependent_last_name}"
            if self.suffix
            else f"{self.dependent_first_name} {self.dependent_last_name}"
        )

    def __str__(self) -> str:
        return self.get_full_name_of_dependent()


class Assistance(models.Model):

    ASSISTANCE_TYPE = [
        ("Death", "Death"),
        ("Hospitalization", "Hospitalization"),
    ]

    request_by = models.ForeignKey(
        "Membership",
        on_delete=models.CASCADE,
        help_text="The name of the member who requested the assistance",
    )
    id = models.AutoField(primary_key=True)
    assistance_first_name = models.CharField(
        max_length=50, help_text="The first name of the employee"
    )
    assistance_middle_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="The middle name of the employee",
    )
    assistance_last_name = models.CharField(
        max_length=100, help_text="The last name of the employee"
    )
    suffix = models.CharField(
        max_length=10, blank=True, null=True, help_text="The suffix of the employee"
    )
    type_of_assistance = models.CharField(
        max_length=50, choices=ASSISTANCE_TYPE, help_text="Choose type of assistance"
    )
    assistance_status = models.BooleanField(
        default=False, help_text="Assistance status"
    )
    assistance_evidence_first = models.ImageField(
        upload_to="assistance/proof/",
        blank=True,
        null=True,
        help_text="Upload medical certification",
    )
    assistance_evidence_second = models.ImageField(
        upload_to="assistance/proof/",
        blank=True,
        null=True,
        help_text="Upload hospital certificate",
    )
    death_cert = models.ImageField(
        upload_to="assistance/proof/",
        blank=True,
        null=True,
        help_text="Upload death certificate",
    )
    released_status = models.BooleanField(
        default=False, help_text="Release status of the assistance"
    )
    amount_released = models.DecimalField(
        max_digits=10,
        default=0.00,
        decimal_places=2,
        help_text="Amoutnt to be released by the assistance",
    )
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

    user_id = models.ForeignKey(
        "Membership",
        related_name="beneficiary_membership",
        on_delete=models.CASCADE,
        help_text="Select related user to the beneficiary",
    )
    id = models.AutoField(primary_key=True)
    beneficiary_first_name = models.CharField(
        max_length=50, help_text="First name of the beneficiary"
    )
    beneficiary_middle_name = models.CharField(
        max_length=50, blank=True, help_text="Middle name of the beneficiary, optional."
    )
    beneficiary_last_name = models.CharField(
        max_length=50, help_text="Last name of the beneficiary"
    )
    suffix = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Suffix of the beneficiary, optional",
    )
    relationship = models.CharField(
        max_length=50, choices=RELATIONSHIP, help_text="Relationship to the beneficiary"
    )
    date_of_birth = models.DateField(help_text="Date of Birth of the beneficiary")
    proof = models.ImageField(
        upload_to="beneficiary/proof/",
        help_text="Upload birth certificate of the beneficiary",
    )
    used = models.BooleanField(default=False, help_text="Whether used as a beneficiary")

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
        ("ISAL", "ISAL"),
        ("ALIVE", "ALIVE"),
        ("Teacher 1", "Teacher 1"),
        ("Teacher 2", "Teacher 2"),
        ("Teacher 3", "Teacher 3"),
        ("MS Teacher 1", "MS Teacher 1"),
        ("MS Teacher 2", "MS Teacher 2"),
        ("MS Teacher 3", "MS Teacher 3"),
        ("School Head", "School Head"),
    ]

    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    SCHOOL_AFFILIATION = [
        ("Dapiawan CES", "Dapiowan CES"),
        ("Datu Pendililang ES", "Datu Pendililang ES"),
        ("Madia IS", "Madia IS"),
        ("Elian ES", "Elian ES"),
        ("Gawang ES", "Gawang ES"),
        ("Kitango ES", "Kitango ES"),
        ("Kitapok ES", "Kitapok ES"),
        ("Datu Kogia ES", "Datu Kogia ES"),
        ("Dimaukom Utto ES", "Dimaukom Utto ES"),
        ("Dimaukom ES", "Dimaukom ES"),
    ]

    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(
        AuthUser,
        on_delete=models.CASCADE,
        help_text="Employee who want to be a member",
        limit_choices_to={"user_type": "Employee"},
        unique=True,
    )
    first_name = models.CharField(max_length=50, help_text="Employee first name")
    middle_name = models.CharField(
        max_length=50, blank=True, help_text="Employee middle name"
    )
    last_name = models.CharField(max_length=50, help_text="Employee last name")
    place_of_birth = models.CharField(max_length=50, help_text="Place of birth")
    date_of_birth = models.DateField(help_text="Date of birth")
    address = models.CharField(max_length=100, help_text="Address of the employee")
    contact_number = models.CharField(
        max_length=20, help_text="Contact number of the employee"
    )
    employee_id = models.CharField(
        max_length=50, help_text="Employee ID of the employee"
    )
    position = models.CharField(
        max_length=50, choices=POSITION, help_text="Position of the employee"
    )
    gender = models.CharField(
        max_length=20, choices=GENDER, help_text="Gender of the employee"
    )
    school_affiliation = models.CharField(
        max_length=100,
        choices=SCHOOL_AFFILIATION,
        help_text="School affiliation of the employee",
    )
    beneficiary = models.OneToOneField(
        Beneficiary,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="Select beneficiary of the employee, select only one.",
    )
    membership_status = models.BooleanField(
        default=False, help_text="Membership status of the employee"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "membership"
        verbose_name = "Membership"
        verbose_name_plural = "Membership"


class Expenses(models.Model):
    EXPENSE_TYPE = (
        ("Claims", "Claims"),
        ("District Activities", "District Activities"),
        ("Visitors Fund", "Visitors Fund"),
    )

    expense_type = models.CharField(max_length=255, choices=EXPENSE_TYPE)
    amount = models.FloatField(help_text="Amount of Expenses")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.expense_type

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        db_table = "expenses"


class Payment(models.Model):

    PAYMENT_TYPE = [
        ("Membership", "Membership Fee"),
        ("Delegation Pay", "Delegation Pay"),
        ("Trust Fund", "Trust Fund"),
        ("Visitors Fund", "Visitors Fund"),
    ]

    id = models.AutoField(primary_key=True)
    paid_by = models.ForeignKey(
        Membership,
        related_name="payment_name",
        on_delete=models.CASCADE,
        limit_choices_to={"user_id__user_type": "Employee"},
        help_text="Employee who paid",
    )
    amount = models.FloatField(help_text="Amount employee paid")
    payment_type = models.CharField(
        max_length=50,
        choices=PAYMENT_TYPE,
        help_text="Payment type made by the employee",
    )
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Paid by {self.paid_by.user_id.get_full_name()}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "payment"
