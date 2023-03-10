import zipfile
import os

# Name der ZIP-Datei
zip_name = "meine_dateien.zip"

# Liste der Dateien, die Sie packen möchten
datei_liste = ["datei1.txt", "datei2.txt", "ordner/datei3.txt"]

# Öffnen Sie die ZIP-Datei im Schreibmodus
with zipfile.ZipFile(zip_name, "w") as zip:
    # Schleife durch die Datei-Liste und fügen Sie jede Datei zur ZIP-Datei hinzu
    for datei in datei_liste:
        # Erstellen Sie den relativen Pfad der Datei
        rel_pfad = os.path.relpath(datei)
        # Fügen Sie die Datei zur ZIP-Datei hinzu
        zip.write(datei, rel_pfad)

print("Dateien erfolgreich gepackt!")
