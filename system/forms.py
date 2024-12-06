from django import forms
from system.models import *
from .models import Membership, Beneficiary


class LedgerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LedgerForm, self).__init__(*args, **kwargs)
        for field_name, field_instance in self.fields.items():
            field_instance.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Ledger
        fields = "__all__"
        widgets = {
            "transaction_date": forms.DateInput(
                {
                    "type": "date",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 2,
                }
            ),
        }
        exclude = ["recorded_by"]


class UpdateMembershipInforDependentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(UpdateMembershipInforDependentsForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["my_dependents"].queryset = Dependents.objects.filter(
                related_to_member=user.membership
            )
            self.fields["beneficiary"].queryset = Beneficiary.objects.filter(
                user_id=user.membership
            )

        self.fields["my_dependents"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Select Dependents",
            }
        )
        self.fields["beneficiary"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Select Beneficiary",
            }
        )

    class Meta:
        model = Membership
        fields = ["my_dependents", "beneficiary"]


class UpdateDependentsForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(UpdateDependentsForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["my_dependents"].queryset = Dependents.objects.filter(
                related_to_member=user
            )
        self.fields["my_dependents"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Membership
        fields = ["my_dependents"]


class DependentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DependentForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Dependents
        fields = "__all__"


class MyDependentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyDependentForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Dependents
        fields = (
            "dependent_first_name",
            "dependent_last_name",
            "dependent_middle_name",
            "dependent_last_name",
            "relationship_to_member",
            "suffix",
            "gender",
        )
        exclude = [
            "related_to_member",
        ]



class SchoolYearForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SchoolYearForm, self).__init__(*args, **kwargs)
        self.fields["start_year"].widget.attrs.update({"class": "form-control"})
        self.fields["end_year"].widget.attrs.update({"class": "form-control"})
        self.fields["primary_school_year"].widget.attrs.update({"class": "form-check-input"})

    class Meta:
        model = SchoolYear
        fields = '__all__'
        widgets = {
            'start_year': forms.DateInput({'type':'date'}),
            'end_year': forms.DateInput({'type':'date'})
        }


class ExpenseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields["amount"].widget.attrs.update({"class": "form-control"})
        self.fields["expense_type"].widget.attrs.update({"class": "form-control"})
        self.fields["school_year"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = Expenses
        fields = [
            "amount",
            "expense_type",
            "school_year"
        ]


class AssistanceReleaseStatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssistanceReleaseStatusForm, self).__init__(*args, **kwargs)
        self.fields["amount_released"].widget.attrs.update({"class": "form-control"})
        self.fields["released_status"].widget.attrs.update(
            {"class": "form-check-input"}
        )

    class Meta:
        model = Assistance
        fields = [
            "amount_released",
            "released_status",
        ]
        widget = {"amount_released": forms.TextInput(attrs={"class": "form-control"})}


class AssistanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssistanceForm, self).__init__(*args, **kwargs)

        if "released_status" in self.fields:
            self.fields["released_status"].widget.attrs.update(
                {"class": "form-check-input"}
            )

        self.fields["request_by"].widget.attrs.update(
            {"placeholder": "Request By", "class": "form-control"}
        )

        self.fields["suffix"].widget.attrs.update(
            {"placeholder": "Suffix", "class": "form-control"}
        )
        self.fields["type_of_assistance"].widget.attrs.update(
            {"placeholder": "Type of Assistance", "class": "form-control"}
        )
        self.fields["assistance_evidence_first"].widget.attrs.update(
            {"placeholder": "Medical Certificate", "class": "form-control"}
        )
        self.fields["assistance_evidence_second"].widget.attrs.update(
            {"placeholder": "Hospital Billing", "class": "form-control"}
        )

        self.fields["death_cert"].widget.attrs.update(
            {"placeholder": "Death Certificate", "class": "form-control"}
        )

        self.fields["amount_released"].widget.attrs.update(
            {"placeholder": "Amount Applied", "class": "form-control"}
        )

        self.fields["assistance_evidence_first"].label = "Medical Certificate"
        self.fields["assistance_evidence_second"].label = "Hospital Billing"
        self.fields["death_cert"].label = "Death Certificate"

    class Meta:
        model = Assistance
        fields = [
            "request_by",
            "suffix",
            "amount_released",
            "type_of_assistance",
            "assistance_evidence_first",
            "assistance_evidence_second",
            "death_cert",
            "released_status",
        ]


class BeneficiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BeneficiaryForm, self).__init__(*args, **kwargs)
        self.fields["beneficiary_first_name"].widget.attrs.update(
            {"placeholder": "First Name", "class": "form-control"}
        )
        self.fields["beneficiary_middle_name"].widget.attrs.update(
            {"placeholder": "Middle Name", "class": "form-control"}
        )
        self.fields["beneficiary_last_name"].widget.attrs.update(
            {"placeholder": "Last Name", "class": "form-control"}
        )
        self.fields["suffix"].widget.attrs.update(
            {"placeholder": "Suffix", "class": "form-control"}
        )
        self.fields["relationship"].widget.attrs.update(
            {"placeholder": "Relationship", "class": "form-control"}
        )
        self.fields["date_of_birth"].widget.attrs.update(
            {"placeholder": "Date of Birth", "class": "form-control"}
        )
        self.fields["proof"].widget.attrs.update(
            {"placeholder": "Proof of Evidence", "class": "form-control"}
        )

        self.fields["proof"].label = "Birth Certificate"

        self.fields["user_id"].label = "Beneficiary User"

        self.fields["user_id"].widget.attrs.update(
            {"placeholder": "Belong to", "class": "form-control"}
        )

    class Meta:
        model = Beneficiary
        widgets = {
            "date_of_birth": forms.DateInput(
                {
                    "type": "date",
                }
            )
        }
        fields = [
            "user_id",
            "beneficiary_first_name",
            "beneficiary_middle_name",
            "beneficiary_last_name",
            "suffix",
            "relationship",
            "date_of_birth",
            "proof",
        ]


class MembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MembershipForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )
            field.widget.is_required = True

    class Meta:
        model = Membership
        widgets = {
            "date_of_birth": forms.DateInput(
                {
                    "type": "date",
                }
            )
        }
        fields = [
            "user_id",
            "place_of_birth",
            "date_of_birth",
            "school_year",
            "address",
            "contact_number",
            "employee_id",
            "position",
            "gender",
            "school_affiliation",
        ]
        exclude = ["beneficiary"]


class AddRelativesMembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddRelativesMembershipForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )
            field.widget.is_required = True

    class Meta:
        model = Membership
        fields = [
            "my_dependents",
            "beneficiary",
        ]

class AddMyRelativesMembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        beneficiary_queryset = kwargs.pop('beneficiary_queryset', None)
        dependents_queryset = kwargs.pop('dependents_queryset', None)
        super(AddMyRelativesMembershipForm, self).__init__(*args, **kwargs)
        
        if beneficiary_queryset is not None:
            self.fields['beneficiary'].queryset = beneficiary_queryset
        if dependents_queryset is not None:
            self.fields['my_dependents'].queryset = dependents_queryset

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )
            field.widget.is_required = True

    class Meta:
        model = Membership
        fields = [
            "my_dependents",
            "beneficiary",
        ]


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {"class": "form-control", "placeholder": field.label}
            )
            field.widget.is_required = True

    class Meta:
        model = Payment
        fields = ["paid_by","school_year", "amount", "payment_type"]


class UserMembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)

        super(UserMembershipForm, self).__init__(*args, **kwargs)

        self.fields["place_of_birth"].widget.attrs.update(
            {"placeholder": "Place of Birth", "class": "form-control"}
        )
        self.fields["date_of_birth"].widget.attrs.update(
            {"placeholder": "Date of Birth", "class": "form-control"}
        )
        self.fields["address"].widget.attrs.update(
            {"placeholder": "Address", "class": "form-control"}
        )
        self.fields["contact_number"].widget.attrs.update(
            {"placeholder": "Contact Number", "class": "form-control"}
        )
        self.fields["employee_id"].widget.attrs.update(
            {"placeholder": "Employee ID", "class": "form-control"}
        )
        self.fields["school_year"].widget.attrs.update(
            {"placeholder": "School Year", "class": "form-control"}
        )
        self.fields["position"].widget.attrs.update(
            {"placeholder": "Position", "class": "form-control"}
        )
        self.fields["gender"].widget.attrs.update(
            {"placeholder": "Gender", "class": "form-control"}
        )
        self.fields["school_affiliation"].widget.attrs.update(
            {"placeholder": "School Affiliation", "class": "form-control"}
        )

    class Meta:
        model = Membership
        widgets = {
            "date_of_birth": forms.DateInput(
                {"type": "date"},
            )
        }
        fields = [
            "place_of_birth",
            "date_of_birth",
            "address",
            "contact_number",
            "employee_id",
            "position",
            "gender",
            "school_year",
            "school_affiliation",
        ]
        exclude = [
            "beneficiary",
        ]


class ViewUserMembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        field_attrs = {
            "place_of_birth": "Place of Birth",
            "date_of_birth": "Date of Birth",
            "address": "Address",
            "contact_number": "Contact Number",
            "employee_id": "Employee ID",
            "position": "Position",
            "gender": "Gender",
            "school_affiliation": "School Affiliation",
            "beneficiary": "Beneficiary",
        }

        for field_name, placeholder in field_attrs.items():
            self.fields[field_name].widget.attrs.update(
                {"placeholder": placeholder, "class": "form-control"}
            )

        self.fields["my_dependents"].widget.attrs.update(
            {
                "placeholder": "Dependents",
                "class": "form-control",
                "disabled": "disabled",
            }
        )

        if user:
            self.fields["beneficiary"].queryset = Beneficiary.objects.filter(
                user_id=user, used=False
            )

            self.fields["my_dependents"].queryset = Dependents.objects.filter(
                related_to_member=user
            )

    class Meta:
        model = Membership
        fields = [
            "place_of_birth",
            "date_of_birth",
            "address",
            "contact_number",
            "employee_id",
            "position",
            "gender",
            "school_affiliation",
            "beneficiary",
            "my_dependents",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }


class UserBeneficiaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserBeneficiaryForm, self).__init__(*args, **kwargs)
        self.fields["beneficiary_first_name"].widget.attrs.update(
            {"placeholder": "First Name", "class": "form-control"}
        )
        self.fields["beneficiary_middle_name"].widget.attrs.update(
            {"placeholder": "Middle Name", "class": "form-control"}
        )
        self.fields["beneficiary_last_name"].widget.attrs.update(
            {"placeholder": "Last Name", "class": "form-control"}
        )
        self.fields["suffix"].widget.attrs.update(
            {"placeholder": "Suffix", "class": "form-control"}
        )
        self.fields["relationship"].widget.attrs.update(
            {"placeholder": "Relationship", "class": "form-control"}
        )
        self.fields["date_of_birth"].widget.attrs.update(
            {"placeholder": "Date of Birth", "class": "form-control"}
        )
        self.fields["proof"].widget.attrs.update(
            {"placeholder": "Proof of Evidence", "class": "form-control"}
        )
        self.fields["proof"].label = "Birth Certificate"

    class Meta:
        model = Beneficiary
        widgets = {
            "date_of_birth": forms.DateInput(
                {
                    "type": "date",
                }
            )
        }
        fields = [
            "beneficiary_first_name",
            "beneficiary_middle_name",
            "beneficiary_last_name",
            "suffix",
            "relationship",
            "date_of_birth",
            "proof",
        ]


class UserAssistanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserAssistanceForm, self).__init__(*args, **kwargs)
        self.fields["suffix"].widget.attrs.update(
            {"placeholder": "Suffix", "class": "form-control"}
        )
        self.fields["type_of_assistance"].widget.attrs.update(
            {"placeholder": "Type of Assistance", "class": "form-control"}
        )
        self.fields["assistance_evidence_first"].widget.attrs.update(
            {"placeholder": "Medical Certificate", "class": "form-control"}
        )
        self.fields["assistance_evidence_first"].label = "Medical Certificate"
        self.fields["assistance_evidence_second"].label = "Hospital Billing"
        self.fields["death_cert"].label = "Death Certificate"

        self.fields["assistance_evidence_second"].widget.attrs.update(
            {"placeholder": "Hospital Billing", "class": "form-control"}
        )
        self.fields["death_cert"].widget.attrs.update(
            {"placeholder": "Death Certificate", "class": "form-control"}
        )

    class Meta:
        model = Assistance
        fields = [
            "suffix",
            "type_of_assistance",
            "assistance_evidence_first",
            "assistance_evidence_second",
            "death_cert",
        ]
