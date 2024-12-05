from django.db import models
from authentication.models import AuthUser
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class SchoolYear(models.Model):
    start_year = models.DateField(help_text="Start Year")
    end_year = models.DateField(help_text="End Year")
    primary_school_year = models.BooleanField(
        default=False, help_text="Toggle if primary school year"
    )

    def __str__(self) -> str:
        return f"School Year {self.start_year.year} - {self.end_year.year}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["primary_school_year"],
                condition=Q(primary_school_year=True),
                name="unique_primary_school_year",
                violation_error_message="Only one school year should be specified as primary school year, please try again.",
            )
        ]
        verbose_name = "School year"
        verbose_name_plural = "School years"


class Ledger(models.Model):
    transaction_date = models.DateField()
    description = models.TextField(max_length=255)
    school_year_transaction = models.ForeignKey(
        SchoolYear,
        related_name="school_year_transaction",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    amount = models.FloatField()
    transaction_type = models.CharField(
        max_length=255,
        choices=[
            ("Debit", "Debit"),
            ("Credit", "Credit"),
        ],
    )
    date_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Ledger for {self.transaction_date}- ₱ {self.amount}"

    class Meta:
        verbose_name = "Ledger"
        verbose_name_plural = "Ledgers"


class Dependents(models.Model):

    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    RELATIONSHIP_TYPE = (
        ("Daughter", "Daughter"),
        ("Son", "Son"),
        ("Spouse", "Spouse"),
        ("Father", "Father"),
        ("Mother", "Mother"),
    )
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
            f"{self.dependent_first_name} {self.dependent_last_name}"
            if self.suffix
            else f"{self.dependent_first_name} {self.dependent_last_name}"
        )

    def __str__(self) -> str:
        return self.get_full_name_of_dependent()
    

    class Meta:
        verbose_name = "Dependent"
        verbose_name_plural = "Dependents"


class Assistance(models.Model):

    ASSISTANCE_TYPE = [
        ("Death", "Death"),
        ("Hospitalization", "Hospitalization"),
    ]
    school_year = models.ForeignKey(
        SchoolYear,
        related_name="assistance_school_year",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    request_by = models.ForeignKey(
        "Membership",
        on_delete=models.CASCADE,
        help_text="The name of the member who requested the assistance",
    )
    id = models.AutoField(primary_key=True)
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
        decimal_places=2,
        help_text="Amount applied in assistance",
    )
    date_released = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.request_by} assistance for {self.type_of_assistance}"

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
            f"{self.beneficiary_first_name} {self.beneficiary_last_name}"
        )
    
    def get_full_name(self):
        return f"{self.beneficiary_first_name} {self.beneficiary_last_name}"

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
        ("Dapiawan CES", "Dapiawan CES"),
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
    place_of_birth = models.CharField(max_length=50, help_text="Place of birth")
    date_of_birth = models.DateField(help_text="Date of birth")
    address = models.CharField(max_length=100, help_text="Address of the employee")
    contact_number = models.CharField(
        max_length=11, help_text="Contact number of the employee", unique=True,
    )
    employee_id = models.CharField(
        max_length=50, help_text="Employee ID of the employee", unique=True,
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
    my_dependents = models.ManyToManyField(
        Dependents,
        blank=True,
        help_text="Select dependent of the employee, select multiple.",
    )
    membership_status = models.BooleanField(
        default=False, help_text="Membership status of the employee"
    )

    school_year = models.ForeignKey(
        SchoolYear, related_name="membership_school_year", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.user_id.first_name} {self.user_id.last_name}"

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
    school_year = models.ForeignKey(
        SchoolYear,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="expense_school_year",
    )
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
    school_year = models.ForeignKey(
        SchoolYear, blank=True, null=True, on_delete=models.CASCADE
    )
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


@receiver(post_save, sender=Payment)
def handle_payment_post_save(sender, instance, created, **kwargs):
    if created:
        current_date = timezone.now().date()
        description = f"Recorded payment {instance.payment_type} with amount of {instance.amount} paid by Member #{instance.paid_by.user_id.id}"
        get_school_year = SchoolYear.objects.get(primary_school_year=True)
        create_transaction_ledger = Ledger.objects.create(
            transaction_date=current_date,
            description=description,
            amount=instance.amount,
            transaction_type="Credit",
            school_year_transaction=get_school_year,
        )
        create_transaction_ledger.save()


@receiver(post_save, sender=Assistance)
def handle_payment_post_save(sender, instance, created, **kwargs):
    if created:
        current_date = timezone.now().date()
        description = f"Cash assistance recorded {instance.type_of_assistance} with amount of {instance.amount_released} to Member #{instance.request_by.user_id.id}"
        get_school_year = SchoolYear.objects.get(primary_school_year=True)
        create_transaction_ledger = Ledger.objects.create(
            transaction_date=current_date,
            description=description,
            amount=instance.amount_released,
            transaction_type="Debit",
            school_year_transaction=get_school_year,
        )
        create_transaction_ledger.save()


@receiver(post_save, sender=Expenses)
def handle_payment_post_save(sender, instance, created, **kwargs):
    if created:
        current_date = timezone.now().date()
        description = f"Expense recorded {instance.expense_type} with amount of {instance.amount}"
        get_school_year = SchoolYear.objects.get(primary_school_year=True)
        create_transaction_ledger = Ledger.objects.create(
            transaction_date=current_date,
            description=description,
            amount=instance.amount,
            transaction_type="Debit",
            school_year_transaction=instance.school_year,
        )
        create_transaction_ledger.save()


