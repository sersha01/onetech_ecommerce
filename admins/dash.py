rams = ['','1GB','2GB','4GB','6GB','8GB']
roms = ['16GB','32GB','64GB','128GB','256GB']
for ram in rams:
    for rom in roms:
        print("""
        form"""+rom[:-2]+ram[:-2]+""" = ProductForm(request.POST, request.FILES)
        if form"""+rom[:-2]+ram[:-2]+""".is_valid():
            form"""+rom[:-2]+ram[:-2]+""".save()
            return redirect('products')""")