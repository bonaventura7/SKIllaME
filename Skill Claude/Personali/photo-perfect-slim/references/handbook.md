# 📚 photo-perfect Handbook

> Riferimento unico caricato **on-demand**. L'agente usa il TOC sotto per saltare alla
> sezione esatta (`grep -A 200 "^## §"` oppure leggere solo l'ancora richiesta).

## 📑 TOC (jump anchors)

| Quando l'utente parla di…              | Vai a sezione      |
|----------------------------------------|--------------------|
| Vinted, vestiti usati, marketplace     | [§1 Vinted](#-1-vinted-playbook) |
| Prodotti e-commerce, sfondo bianco     | [§2 Product](#-2-product-shot)   |
| Ritocco generico, esposizione, denoise | [§3 Retouch](#-3-general-retouch)|
| Colori sballati, WB, fedeltà colore    | [§4 Color](#-4-color-fidelity)   |
| Diagnostica problema specifico         | [§5 Troubleshoot](#-5-troubleshoot)|

---

## § 1 Vinted playbook

### Principi base (tutte le categorie)
1. Luce diffusa (finestra, no sole diretto) o softbox a 45°.
2. Sfondo neutro uniforme (bianco / grigio chiaro / beige).
3. Formato 1:1, min 800×800, ideale 1200×1200, max 20 MB.
4. 4–8 foto consigliate per inserzione.
5. **Onestà visuale**: mostra difetti reali (ToS Vinted).
6. No persone riconoscibili, no bambini.
7. No watermark, testo, logo di brand su sfondo.

### Set per categoria (recipes)

| Categoria | Foto consigliate (in ordine) | Preset skill |
|---|---|---|
| Maglione / T-shirt | front_flat → back_flat → label_close → detail_texture → defects | `vinted-clothing` |
| Jeans | front_flat → back_flat → waist_label → hem_detail → fabric_close | `vinted-clothing` |
| Vestito / Abito | front_hanger → back_hanger → label_close → detail_pattern | `vinted-clothing` |
| Giacca / Cappotto | front_flat → back_flat → lining → label_close → zipper_detail | `vinted-clothing` |
| Scarpe | side_pair → top_pair → sole_pair → heel_detail → label_inside | `vinted-shoes` |
| Borsa / Accessorio | front → back → inside → label_logo → hardware_close | `vinted-accessory` |

### Tip professionali
- **Vestiti**: stira prima di scattare (o preset wrinkle_reduce subtle); gruccia spessa di legno mai metallo sottile.
- **Jeans**: mostra SEMPRE etichetta interna W/L → riduce resi.
- **Giacche**: la fodera interna è molto richiesta su Vinted.
- **Scarpe**: la suola va mostrata onestamente (usura visibile = trust ↑).
- **Borse**: primo piano nitido di logo + hardware = anti-contraffazione.

### Compliance tecnica (riassunto)
| Parametro | Valore |
|---|---|
| Formato | JPG q92 |
| Color space | sRGB obbligatorio |
| Dim. min / consigliata | 800² / 1200² |
| Peso max | 20 MB |
| EXIF GPS | rimuovere (privacy) |
| Filtri creativi | vietati |

---

## § 2 Product shot

### Setup luce ideale
- 2 softbox 45° sopra prodotto (rapporto 1:1.5)
- 1 riflettore bianco opposto alla luce principale
- Polarizzatore se prodotto lucido (vetro/metallo)
- 5500K uniforme, no mix tungsteno+LED

### Composizione
| Regola | Valore |
|---|---|
| Padding | 10–15% (Amazon: min 85% riempimento) |
| Centratura | asse verticale |
| Angolo | 3/4 (15–30°) preferito |
| Crop | 1:1 standard, 4:5 social portrait |

### Trappola del "bianco puro" #FFFFFF
Bruciare lo sfondo a 255 perde i bordi del prodotto (aloni). **Tecnica corretta**: scatta su grigio #E5E5E5 sottoesposto -1 stop, poi porta a 250-252 con maschera del soggetto. La skill lo fa automaticamente con preset `product-white`.

### Ombre — quale scegliere
1. **Natural** — ombra reale del set.
2. **Drop shadow** (default skill): opacità 15-25%, blur 25-35px, offset Y +8/+12.
3. **Reflection** — per bottiglie/cosmetici lucidi.
4. **No shadow** — solo illustrazioni o packaging trasparente.

### Categorie speciali
| Tipo | Note |
|---|---|
| Gioielli / vetro / orologi | Light tent obbligatorio. HDR 3 scatti -1/0/+1 |
| Cibo confezionato | Etichetta + scadenza leggibili |
| Elettronica | Cavi avvolti in scatto separato; schermo spento o UI neutra |
| Tessili (lenzuola, asciugamani) | Piega "hotel style", luce radente per texture |

### Specifiche piattaforme (cheat sheet)
| Piattaforma | Min dim | Sfondo | Note |
|---|---|---|---|
| Amazon main | 1000² | #FFFFFF puro | min 85% frame, no testo |
| eBay | 500² | bianco consigliato | fino 24 foto |
| Shopify | 2048² | flessibile | 1:1 preferito |
| Etsy | 2000² | flessibile | lifestyle ok |
| Vinted | 800² | neutro | vedi §1 |
| Instagram | 1080² | flessibile | shopping tags |

---

## § 3 General retouch

### Ordine operazioni (NON CAMBIARE)
```
1. Lens correction (se EXIF lo permette)
2. White Balance
3. Esposizione + recupero highlights/shadows
4. Contrasto locale (CLAHE su L di LAB)
5. Saturazione & Vibrance
6. Denoise          ← PRIMA dello sharpening
7. Sharpening (unsharp mask)
8. Crop & resize
9. Compressione + strip EXIF
```

### Soglie "safe" (no over-process)
| Parametro | Min | Sweet spot | Max sano |
|---|---|---|---|
| Saturazione | 0.95 | 1.05 | 1.15 |
| Vibrance | 0.95 | 1.07 | 1.20 |
| Contrasto | 0.95 | 1.06 | 1.15 |
| Esposizione EV | -1.0 | auto | +1.0 |
| Unsharp amount | 0.3 | 0.5–0.7 | 1.0 |
| Unsharp radius | 0.8 | 1.0–1.2 | 1.8 |
| Denoise (h) | 0 | 3–7 | 12 |

Oltre max → look HDR finto, plastica, perdita dettaglio.

### Algoritmi (per debug/tuning)
- **Grey-World WB** — assume media scena = grigio. Fallisce su scene mono-colore (erba/mare).
- **Auto Exposure** — luma BT.601, target 128, cap ±35%.
- **CLAHE** — tile 8×8, clipLimit 2.0, solo canale L (no shift colore).
- **fastNlMeans** — patch-based, preserva bordi meglio del Gaussian.
- **Unsharp Mask** — amplifica contrasto locale ai bordi.

### Quale preset usare
```
vestito da rivendere   → vinted-clothing
prodotto e-commerce    → product-white
ritratto               → portrait-natural
foto tutti i giorni    → general-enhance
foto vecchia/danneggiata → restore-old
```

---

## § 4 Color fidelity

### Color space — regole d'oro
| Contesto | Color space | Bit |
|---|---|---|
| Web / Social / Marketplace | **sRGB** | 8 |
| Stampa pro | AdobeRGB / ProPhoto | 16 |
| Cinema | Rec.709 / DCI-P3 | 10+ |

**Mai** AdobeRGB su Vinted: browser converte male → colori spenti.

### Temperatura colore
| Sorgente | K |
|---|---|
| Candela | 1500-2000 |
| Tungsteno casa | 2700-3000 |
| Alba/tramonto | 3000-4000 |
| Daylight | 5500-6500 ✅ |
| Nuvoloso | 6500-7500 |
| Ombra | 8000-10000 |

Target output sempre 5500K.

### Metodi WB della skill
1. `auto-grey-world` (default) — veloce, fallisce su scene mono-colore.
2. `auto-faces` — calibra sui toni pelle (portrait).
3. Picker manuale `--wb-pick X,Y`.
4. Grey card / colorchecker — workflow pro, max fedeltà.

### Test di fedeltà (built-in)
```python
mean_r, mean_g, mean_b = img.mean(axis=(0,1))
# entro ±15% l'uno dall'altro → ok
if abs(mean_r/mean_g - 1) > 0.15: warn("dominante colore")
```

### Compliance marketplace
- Saturazione prodotto MAX 1.10.
- Non correggere usura reale (es. ingiallimento bianco vintage).
- No filtri Instagram.
- sRGB embedded sempre.

---

## § 5 Troubleshoot

| Sintomo | Causa | Fix |
|---|---|---|
| Aloni biancastri ai bordi | Sharpening troppo | abbassa `unsharp.amount` o aumenta threshold |
| Cielo a chiazze | Denoise + JPG basso | denoise più leggero, q≥92 |
| Skin tones gialli | WB grey-world su scena calda | preset `portrait-natural` o WB manuale |
| Colori "lavati" | sRGB → AdobeRGB sbagliato | forza sRGB |
| Banding gradienti | JPG q basso o 8bit | q≥90 o PNG 16bit |
| Scontorno sbagliato | rembg confuso (sfondo simile soggetto) | Livello 3 (AI) o GrabCut manuale |
| Output > 20 MB | qualità troppo alta | la skill ricomprime auto a q88/85/82/78 |
| "no bg engine" warning | Manca rembg+onnxruntime | `pip install rembg onnxruntime` |
| "cv2 missing" warning | Manca OpenCV | `pip install opencv-python` (CLAHE/denoise saltati) |
| OPENROUTER_API_KEY mancante | AI cloud non configurato | export var o usa solo livelli 1-2 |
