from django import forms
from system.models import *
from django.db.models import Q

class AssistanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssistanceForm, self).__init__(*args, **kwargs)
        self.fields["assistance_first_name"].widget.attrs.update(
            {"placeholder": "First Name", "class": "form-control"}
        )

        self.fields["amount_released"].widget.attrs.update(
            {"placeholder": "Amount Released", "class": "form-control"}
        )

        self.fields["assistance_middle_name"].widget.attrs.update(
            {"placeholder": "Middle Name", "class": "form-control"}
        )

        self.fields["request_by"].widget.attrs.update(
            {"placeholder": "Request By", "class": "form-control"}
        )

        self.fields["assistance_last_name"].widget.attrs.update(
            {"placeholder": "Last Name", "class": "form-control"}
        )
        self.fields["suffix"].widget.attrs.update(
            {"placeholder": "Suffix", "class": "form-control"}
        )
        self.fields["type_of_assistance"].widget.attrs.update(
            {"placeholder": "Type of Assistance", "class": "form-control"}
        )
        self.fields["assistance_evidence_first"].widget.attrs.update(
            {"placeholder": "Proof of Evidence 1", "class": "form-control"}
        )
        self.fields["assistance_evidence_second"].widget.attrs.update(
            {"placeholder": "Proof of Evidence 2", "class": "form-control"}
        )

    class Meta:
        model = Assistance
        fields = [
            "request_by",
            "assistance_first_name",
            "assistance_middle_name",
            "assistance_last_name",
            "suffix",
            "amount_released",
            "type_of_assistance",
            "assistance_evidence_first",
            "assistance_evidence_second",
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
        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "First Name", "class": "form-control"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Last Name", "class": "form-control"}
        )
        self.fields["middle_name"].widget.attrs.update(
            {"placeholder": "Middle Name", "class": "form-control"}
        )
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
        self.fields["position"].widget.attrs.update(
            {"placeholder": "Position", "class": "form-control"}
        )
        self.fields["user_id"].label = "Select User"
        self.fields["user_id"].widget.attrs.update(
            {"placeholder": "Select User", "class": "form-control"}
        )
        self.fields["gender"].widget.attrs.update(
            {"placeholder": "Gender", "class": "form-control"}
        )
        self.fields["school_affiliation"].widget.attrs.update(
            {"placeholder": "School Affiliation", "class": "form-control"}
        )

        self.fields["beneficiary"].widget.attrs.update(
            {"placeholder": "Beneficiary", "class": "form-control"}
        )

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
            "first_name",
            "last_name",
            "middle_name",
            "place_of_birth",
            "date_of_birth",
            "address",
            "contact_number",
            "employee_id",
            "position",
            "gender",
            "school_affiliation",
            "beneficiary",
        ]


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields["paid_by"].widget.attrs.update(
            {"placeholder": "Select Employee", "class": "form-control"}
        )
        self.fields["amount"].widget.attrs.update(
            {"placeholder": "Amount Paid", "class": "form-control"}
        )
        self.fields["payment_type"].widget.attrs.update(
            {"placeholder": "Payment Type", "class": "form-control"}
        )

    class Meta:
        model = Payment
        fields = ["paid_by", "amount", "payment_type"]


class UserMembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserMembershipForm, self).__init__(*args, **kwargs)

        user = kwargs.pop('user', None)

        self.fields["first_name"].widget.attrs.update(
            {"placeholder": "First Name", "class": "form-control"}
        )
        self.fields["last_name"].widget.attrs.update(
            {"placeholder": "Last Name", "class": "form-control"}
        )
        self.fields["middle_name"].widget.attrs.update(
            {"placeholder": "Middle Name", "class": "form-control"}
        )
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
        self.fields["position"].widget.attrs.update(
            {"placeholder": "Position", "class": "form-control"}
        )
        
        self.fields["gender"].widget.attrs.update(
            {"placeholder": "Gender", "class": "form-control"}
        )
        self.fields["school_affiliation"].widget.attrs.update(
            {"placeholder": "School Affiliation", "class": "form-control"}
        )

        if user:
            self.fields['beneficiary'].queryset = Beneficiary.objects.filter(Q(user_id=user) & Q(used=False))

        self.fields["beneficiary"].widget.attrs.update(
            {"placeholder": "Beneficiary", "class": "form-control"}
        )

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
            "first_name",
            "last_name",
            "middle_name",
            "place_of_birth",
            "date_of_birth",
            "address",
            "contact_number",
            "employee_id",
            "position",
            "gender",
            "school_affiliation",
            "beneficiary",
        ]


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
        self.fields["assistance_first_name"].widget.attrs.update(
            {"placeholder": "First Name", "class": "form-control"}
        )

        self.fields["assistance_middle_name"].widget.attrs.update(
            {"placeholder": "Middle Name", "class": "form-control"}
        )

        self.fields["assistance_last_name"].widget.attrs.update(
            {"placeholder": "Last Name", "class": "form-control"}
        )
        self.fields["suffix"].widget.attrs.update(
            {"placeholder": "Suffix", "class": "form-control"}
        )
        self.fields["type_of_assistance"].widget.attrs.update(
            {"placeholder": "Type of Assistance", "class": "form-control"}
        )
        self.fields["assistance_evidence_first"].widget.attrs.update(
            {"placeholder": "Proof of Evidence 1", "class": "form-control"}
        )
        self.fields["assistance_evidence_second"].widget.attrs.update(
            {"placeholder": "Proof of Evidence 2", "class": "form-control"}
        )

    class Meta:
        model = Assistance
        fields = [
            "assistance_first_name",
            "assistance_middle_name",
            "assistance_last_name",
            "suffix",
            "type_of_assistance",
            "assistance_evidence_first",
            "assistance_evidence_second",
        ]
