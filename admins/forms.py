from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:

        model = Product
        fields = '__all__'

        labels = {
            'name' : 'Name',
            'price' : 'Price',
            'images1' : 'Image1',
            'images2' : 'Image2',
            'images3' : 'Image3',
            'ram' : 'Ram',
            'storage' : 'Storage',
            'camara' : 'Camara',
            'battery' : 'Battery',
            'processor' : 'Processor',
            'display' : 'Display',
            'stock' : 'Stock',
            'brand' : 'Brand',
            'date' : 'Date',
        }
    
    def __init__(self, *args ,**kwargs):
        super(ProductForm, self).__init__(*args ,**kwargs)

        self.fields['name'].widget.attrs.update(
            {'class':'form-control'})

        self.fields['price'].widget.attrs.update(
            {'class':'form-control'})
            
        self.fields['ram'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['storage'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['camara'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['battery'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['processor'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['display'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['images1'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['images2'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['images3'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['stock'].widget.attrs.update(
            {'class':'form-control'})
        
        self.fields['brand'].widget.attrs.update(
            {'class':'form-control'})
        
# class Productf(forms.ModelForm):
#     img1=forms.ImageField(widget=forms.FileInput,)
#     img2=forms.ImageField(widget=forms.FileInput,)
#     img3=forms.ImageField(widget=forms.FileInput,)
#     class Meta:
#         model=Product
#         fields = ('img1','img2','img3')
#         exclude = ('')        
            


#  form-control-lg py-1 rounded