import zipfile
import os
import shutil
import re

def clean_docx(source_path, dest_path):
    if not os.path.exists(source_path):
        print(f"Error: {source_path} does not exist.")
        return False
    
    # Crea una copia temporanea o di destinazione
    shutil.copy2(source_path, dest_path)
    
    temp_dir = "temp_docx_unzip"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Estrai il file docx
        with zipfile.ZipFile(dest_path, 'r') as z:
            z.extractall(temp_dir)
            
        # Percorso del documento principale
        doc_xml_path = os.path.join(temp_dir, "word", "document.xml")
        if os.path.exists(doc_xml_path):
            with open(doc_xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Creiamo un corpo di documento Word standard con i capitoli del Masterfile
            # che utilizza gli stili esistenti (come 'heading 1', 'heading 2', ecc.)
            # Per non corrompere l'XML di Word, possiamo fare una sostituzione conservativa del testo principale.
            # Invece di rimuovere tutto l'XML, cerchiamo i tag <w:t> (testo) e li sostituiamo con dei segnaposto generici
            # o con la struttura del Masterfile.
            
            # Sostituiamo in modo intelligente i testi specifici di "Damiani" con dei segnaposto.
            content = content.replace("Damiani", "[GRUPPO CLIENTE]")
            content = content.replace("DAMIANI", "[GRUPPO CLIENTE]")
            content = content.replace("2024", "[FY_RIFERIMENTO]")
            content = content.replace("Valenza", "[SEDE_CAPOGRUPPO]")
            
            with open(doc_xml_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
        # Ricompatta il file docx
        os.remove(dest_path)
        with zipfile.ZipFile(dest_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, temp_dir)
                    z.write(file_path, arc_name)
                    
        print(f"Successfully generated clean SBNP Template Word: {dest_path}")
        return True
    except Exception as e:
        print(f"Error during cleaning: {e}")
        return False
    finally:
        # Pulisci cartella temporanea
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    source = "C:/Users/luca.consalter/Desktop/Pilota/Damiani MF  FY 24 draft.docx"
    dest = "C:/Users/luca.consalter/Desktop/Pilota/SBNP_Masterfile_Template_4.0.docx"
    clean_docx(source, dest)
