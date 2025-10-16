import os, shutil

# 
base = r"C:\Users\Saleh\clien"

#  
folders = {
    "data": (".xlsx", ".xls"),
    "scripts": (".py",),
    "images": (".png", ".jpg", ".jpeg")
}

# 
for f in folders:
    os.makedirs(os.path.join(base, f), exist_ok=True)

# 
for filename in os.listdir(base):
    path = os.path.join(base, filename)
    if os.path.isfile(path):
        ext = os.path.splitext(filename)[1].lower()
        for folder, exts in folders.items():
            if ext in exts:
                dest = os.path.join(base, folder, filename)
                shutil.move(path, dest)
                print(f"✅ Déplacé : {filename} → {folder}")
                break
