from django import forms
from .models import Lend, Maintenance, Asset



class LendForm(forms.ModelForm):
    id = forms.ModelChoiceField(queryset=Asset.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Lend
        fields = ['asset', 'quantity', 'id']
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(LendForm, self).__init__(*args, **kwargs)
        self.fields['asset'].queryset = Asset.objects.all()

        if 'asset' in self.data:
            try:
                asset_id = int(self.data.get('asset'))
                self.fields['id'].queryset = Asset.objects.filter(id=asset_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['id'].queryset = self.instance.asset.id_set.all()



class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['asset', 'quantity', 'is_fixed']
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_fixed': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

class AddAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'total_quantity']  # Exclude 'available_quantity' and 'unique_id'
        widgets = {
            'name': forms.Select(choices=Asset.ASSET_CHOICES, attrs={'class': 'form-control'}),
            'total_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class ReturnAssetForm(forms.ModelForm):
    quantity_good = forms.IntegerField(min_value=0, label='Quantity in Good Condition', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    quantity_bad = forms.IntegerField(min_value=0, label='Quantity in Bad Condition', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Lend
        fields = ['returned_date', 'condition']
        widgets = {
            'returned_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'condition': forms.Select(choices=[('Good', 'Good'), ('Bad', 'Bad')], attrs={'class': 'form-control'}),
        }
