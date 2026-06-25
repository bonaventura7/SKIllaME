import zipfile
import xml.etree.ElementTree as ET
import os
import re

def get_ns_tag(ns, tag):
    return f"{{{ns}}}{tag}" if ns else tag

def extract_design_primitives(docx_path):
    if not os.path.exists(docx_path):
        return {"error": "File not found"}
    
    primitives = {
        "colors": set(),
        "fonts": set(),
        "styles": {}
    }
    
    try:
        with zipfile.ZipFile(docx_path, 'r') as z:
            # 1. Analisi dei font e colori del tema
            if 'word/theme/theme1.xml' in z.namelist():
                theme_data = z.read('word/theme/theme1.xml')
                root = ET.fromstring(theme_data)
                
                # Namespace word theme
                ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"
                
                # Estrazione font del tema
                for font_tag in ['majorFont', 'minorFont']:
                    for elem in root.findall(f".//{{{ns_a}}}{font_tag}"):
                        for latin in elem.findall(f"{{{ns_a}}}latin"):
                            typeface = latin.attrib.get('typeface')
                            if typeface:
                                primitives["fonts"].add(typeface)
                
                # Estrazione colori del tema (clrScheme)
                for elem in root.findall(f".//{{{ns_a}}}srgbClr"):
                    val = elem.attrib.get('val')
                    if val:
                        primitives["colors"].add(f"#{val.upper()}")
            
            # 2. Analisi degli stili effettivi
            if 'word/styles.xml' in z.namelist():
                styles_data = z.read('word/styles.xml')
                root = ET.fromstring(styles_data)
                
                ns_w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
                
                for style in root.findall(f"{{{ns_w}}}style"):
                    style_id = style.attrib.get(f"{{{ns_w}}}styleId")
                    style_type = style.attrib.get(f"{{{ns_w}}}type")
                    
                    if style_type == "paragraph":
                        name_elem = style.find(f"{{{ns_w}}}name")
                        name = name_elem.attrib.get(f"{{{ns_w}}}val") if name_elem is not None else style_id
                        
                        rPr = style.find(f"{{{ns_w}}}rPr")
                        style_info = {}
                        
                        if rPr is not None:
                            # Font
                            rFonts = rPr.find(f"{{{ns_w}}}rFonts")
                            if rFonts is not None:
                                font_name = rFonts.attrib.get(f"{{{ns_w}}}ascii") or rFonts.attrib.get(f"{{{ns_w}}}hAnsi")
                                if font_name:
                                    style_info["font"] = font_name
                                    primitives["fonts"].add(font_name)
                            
                            # Dimensione (in half-points, es: 24 = 12pt)
                            sz = rPr.find(f"{{{ns_w}}}sz")
                            if sz is not None:
                                size_val = sz.attrib.get(f"{{{ns_w}}}val")
                                if size_val and size_val.isdigit():
                                    style_info["size_pt"] = int(size_val) / 2
                            
                            # Colore
                            color = rPr.find(f"{{{ns_w}}}color")
                            if color is not None:
                                color_val = color.attrib.get(f"{{{ns_w}}}val")
                                if color_val:
                                    # Se è "auto", lo saltiamo o lo marchiamo
                                    if color_val != "auto":
                                        style_info["color"] = f"#{color_val.upper()}"
                                        primitives["colors"].add(f"#{color_val.upper()}")
                            
                            # Bold
                            bold = rPr.find(f"{{{ns_w}}}b")
                            if bold is not None:
                                style_info["bold"] = True
                            
                            # Italic
                            italic = rPr.find(f"{{{ns_w}}}i")
                            if italic is not None:
                                style_info["italic"] = True
                        
                        if style_info:
                            primitives["styles"][name] = style_info
                            
            # 3. Scansione rapida del documento per trovare colori usati direttamente
            if 'word/document.xml' in z.namelist():
                doc_data = z.read('word/document.xml').decode('utf-8')
                # Cerca pattern esadecimali di colore nel XML di Word: w:color w:val="HEX"
                hex_colors = re.findall(r'w:color[^>]+w:val="([A-Fa-f0-9]{6})"', doc_data)
                for hc in hex_colors:
                    primitives["colors"].add(f"#{hc.upper()}")
                    
    except Exception as e:
        return {"error": str(e)}
        
    # Pulizia colori (escludiamo bianco e nero standard se non strettamente necessari, ma teniamo traccia)
    primitives["colors"] = sorted(list(primitives["colors"]))
    primitives["fonts"] = sorted(list(primitives["fonts"]))
    return primitives

def main():
    files = [
        "Damiani MF  FY 24 draft.docx",
        "MF Bandera FY 23 Final.docx",
        "DB Masterfile Draft FY 24 Final.docx"
    ]
    
    print("========================================================================")
    print(" SBNP MASTERFILE DESIGN SYSTEM EXTRACTION TOOL")
    print("========================================================================")
    
    for f in files:
        path = os.path.join("C:/Users/luca.consalter/Desktop/Pilota", f)
        print(f"\nAnalyzing: {f}...")
        res = extract_design_primitives(path)
        
        if "error" in res:
            print(f"  [ERROR]: {res['error']}")
            continue
            
        print(f"  Fonts Detected: {', '.join(res['fonts'])}")
        print(f"  Colors Detected: {', '.join(res['colors'][:8])} (Total: {len(res['colors'])})")
        
        print("  Key Styles:")
        target_styles = ["Normal", "Heading 1", "Heading 2", "Heading 3", "Title", "Subtitle"]
        for style_name, info in res["styles"].items():
            if any(ts.lower() in style_name.lower() for ts in target_styles):
                style_str = ", ".join([f"{k}: {v}" for k, v in info.items()])
                print(f"    - {style_name}: {style_str}")

if __name__ == "__main__":
    main()
