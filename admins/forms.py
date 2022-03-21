from django import forms
from .models import Banner, Product


class ProductForm(forms.ModelForm):
    class Meta:

        model = Product
        fields = '__all__'
        exclude = ['product_off']

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
        

class BannerForm(forms.ModelForm):
    class Meta:
        model=Banner
        fields = '__all__'  
        exclude = ['status']
            
    def __init__(self, *args ,**kwargs):
        super(BannerForm, self).__init__(*args ,**kwargs)

        self.fields['image'].widget.attrs.update(
            {'class':'form-control','id':'id_images1'})


#  form-control-lg py-1 rounded