from django import forms
from .models import Investor, Investment, Withdrawal

# List of countries with phone codes (African countries first, then others, excluding USA)
COUNTRIES_WITH_PHONE_CODES = [
    ('', 'Select Country'),
    ('Algeria (+213)', 'Algeria (+213)'),
    ('Angola (+244)', 'Angola (+244)'),
    ('Benin (+229)', 'Benin (+229)'),
    ('Botswana (+267)', 'Botswana (+267)'),
    ('Burkina Faso (+226)', 'Burkina Faso (+226)'),
    ('Burundi (+257)', 'Burundi (+257)'),
    ('Cabo Verde (+238)', 'Cabo Verde (+238)'),
    ('Cameroon (+237)', 'Cameroon (+237)'),
    ('Central African Republic (+236)', 'Central African Republic (+236)'),
    ('Chad (+235)', 'Chad (+235)'),
    ('Comoros (+269)', 'Comoros (+269)'),
    ('Congo (+242)', 'Congo (+242)'),
    ('DR Congo (+243)', 'DR Congo (+243)'),
    ('Djibouti (+253)', 'Djibouti (+253)'),
    ('Egypt (+20)', 'Egypt (+20)'),
    ('Equatorial Guinea (+240)', 'Equatorial Guinea (+240)'),
    ('Eritrea (+291)', 'Eritrea (+291)'),
    ('Eswatini (+268)', 'Eswatini (+268)'),
    ('Ethiopia (+251)', 'Ethiopia (+251)'),
    ('Gabon (+241)', 'Gabon (+241)'),
    ('Gambia (+220)', 'Gambia (+220)'),
    ('Ghana (+233)', 'Ghana (+233)'),
    ('Guinea (+224)', 'Guinea (+224)'),
    ('Guinea-Bissau (+245)', 'Guinea-Bissau (+245)'),
    ('Ivory Coast (+225)', 'Ivory Coast (+225)'),
    ('Kenya (+254)', 'Kenya (+254)'),
    ('Lesotho (+266)', 'Lesotho (+266)'),
    ('Liberia (+231)', 'Liberia (+231)'),
    ('Libya (+218)', 'Libya (+218)'),
    ('Madagascar (+261)', 'Madagascar (+261)'),
    ('Malawi (+265)', 'Malawi (+265)'),
    ('Mali (+223)', 'Mali (+223)'),
    ('Mauritania (+222)', 'Mauritania (+222)'),
    ('Mauritius (+230)', 'Mauritius (+230)'),
    ('Morocco (+212)', 'Morocco (+212)'),
    ('Mozambique (+258)', 'Mozambique (+258)'),
    ('Namibia (+264)', 'Namibia (+264)'),
    ('Niger (+227)', 'Niger (+227)'),
    ('Nigeria (+234)', 'Nigeria (+234)'),
    ('Rwanda (+250)', 'Rwanda (+250)'),
    ('Sao Tome and Principe (+239)', 'Sao Tome and Principe (+239)'),
    ('Senegal (+221)', 'Senegal (+221)'),
    ('Seychelles (+248)', 'Seychelles (+248)'),
    ('Sierra Leone (+232)', 'Sierra Leone (+232)'),
    ('Somalia (+252)', 'Somalia (+252)'),
    ('South Africa (+27)', 'South Africa (+27)'),
    ('South Sudan (+211)', 'South Sudan (+211)'),
    ('Sudan (+249)', 'Sudan (+249)'),
    ('Tanzania (+255)', 'Tanzania (+255)'),
    ('Togo (+228)', 'Togo (+228)'),
    ('Tunisia (+216)', 'Tunisia (+216)'),
    ('Uganda (+256)', 'Uganda (+256)'),
    ('Zambia (+260)', 'Zambia (+260)'),
    ('Zimbabwe (+263)', 'Zimbabwe (+263)'),
    
    # Major countries from other continents (excluding USA)
    ('Afghanistan (+93)', 'Afghanistan (+93)'),
    ('Argentina (+54)', 'Argentina (+54)'),
    ('Australia (+61)', 'Australia (+61)'),
    ('Austria (+43)', 'Austria (+43)'),
    ('Bangladesh (+880)', 'Bangladesh (+880)'),
    ('Belgium (+32)', 'Belgium (+32)'),
    ('Brazil (+55)', 'Brazil (+55)'),
    ('Canada (+1)', 'Canada (+1)'),
    ('Chile (+56)', 'Chile (+56)'),
    ('China (+86)', 'China (+86)'),
    ('Colombia (+57)', 'Colombia (+57)'),
    ('Cuba (+53)', 'Cuba (+53)'),
    ('Czech Republic (+420)', 'Czech Republic (+420)'),
    ('Denmark (+45)', 'Denmark (+45)'),
    ('Finland (+358)', 'Finland (+358)'),
    ('France (+33)', 'France (+33)'),
    ('Germany (+49)', 'Germany (+49)'),
    ('Greece (+30)', 'Greece (+30)'),
    ('India (+91)', 'India (+91)'),
    ('Indonesia (+62)', 'Indonesia (+62)'),
    ('Iran (+98)', 'Iran (+98)'),
    ('Iraq (+964)', 'Iraq (+964)'),
    ('Ireland (+353)', 'Ireland (+353)'),
    ('Israel (+972)', 'Israel (+972)'),
    ('Italy (+39)', 'Italy (+39)'),
    ('Japan (+81)', 'Japan (+81)'),
    ('Jordan (+962)', 'Jordan (+962)'),
    ('Kazakhstan (+7)', 'Kazakhstan (+7)'),
    ('Kuwait (+965)', 'Kuwait (+965)'),
    ('Lebanon (+961)', 'Lebanon (+961)'),
    ('Malaysia (+60)', 'Malaysia (+60)'),
    ('Mexico (+52)', 'Mexico (+52)'),
    ('Netherlands (+31)', 'Netherlands (+31)'),
    ('New Zealand (+64)', 'New Zealand (+64)'),
    ('Norway (+47)', 'Norway (+47)'),
    ('Oman (+968)', 'Oman (+968)'),
    ('Pakistan (+92)', 'Pakistan (+92)'),
    ('Peru (+51)', 'Peru (+51)'),
    ('Philippines (+63)', 'Philippines (+63)'),
    ('Poland (+48)', 'Poland (+48)'),
    ('Portugal (+351)', 'Portugal (+351)'),
    ('Qatar (+974)', 'Qatar (+974)'),
    ('Russia (+7)', 'Russia (+7)'),
    ('Saudi Arabia (+966)', 'Saudi Arabia (+966)'),
    ('Singapore (+65)', 'Singapore (+65)'),
    ('South Korea (+82)', 'South Korea (+82)'),
    ('Spain (+34)', 'Spain (+34)'),
    ('Sweden (+46)', 'Sweden (+46)'),
    ('Switzerland (+41)', 'Switzerland (+41)'),
    ('Syria (+963)', 'Syria (+963)'),
    ('Thailand (+66)', 'Thailand (+66)'),
    ('Turkey (+90)', 'Turkey (+90)'),
    ('Ukraine (+380)', 'Ukraine (+380)'),
    ('United Arab Emirates (+971)', 'United Arab Emirates (+971)'),
    ('United Kingdom (+44)', 'United Kingdom (+44)'),
    ('Venezuela (+58)', 'Venezuela (+58)'),
    ('Vietnam (+84)', 'Vietnam (+84)'),
    ('Yemen (+967)', 'Yemen (+967)'),
]

class InvestorSignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), label='Confirm Password')
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}), label='Full Name')
    country = forms.ChoiceField(choices=COUNTRIES_WITH_PHONE_CODES, widget=forms.Select(attrs={'class': 'form-select'}), label='Country')
    
    class Meta:
        model = Investor
        fields = ['full_name', 'phone_number', 'country']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number without country code'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = ['amount', 'crypto_type']
        widgets = {
            'amount': forms.NumberInput(attrs={'min': '10', 'step': '0.01'}),
            'crypto_type': forms.Select(attrs={'class': 'form-select'}),
        }

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ['amount', 'wallet_address']
        widgets = {
            'wallet_address': forms.TextInput(attrs={'placeholder': 'Your crypto wallet address'}),
        }
