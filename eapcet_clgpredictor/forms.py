from django import forms

class ClgPredictorForm(forms.Form):
    gender_choices = (
        ("M","Male"),
        ('F',"Female"),
        ("O","Others"),
    )
    category_choices = [
        ("OC","OC"),
        ("BC-A","BC-A"),
        ("BC-B","BC-B"),
        ("BC-C","BC-C"),
        ("BC-D","BC-D"),
        ("BC-E","BC-E"),
        ("SC","SC"),
        ("ST","ST"),
        ("GEN_EWS","GEN_EWS"),
        ("PWD","PWD")
    ]

    AP_EAPCET_RANK = forms.IntegerField(widget=forms.TextInput)
    Gender = forms.ChoiceField(choices = gender_choices,widget = forms.RadioSelect)
    category = forms.ChoiceField(choices=category_choices)