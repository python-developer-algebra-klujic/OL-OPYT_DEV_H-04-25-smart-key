import customtkinter as ctk
import random

# -----------------------------
# POMOĆNE FUNKCIJE (iz tvog koda)
# -----------------------------
def cezar_enkripcija(tekst: str, pomak: int) -> str:
    """
    Cezarova enkripcija nad stringom (samo A-Z), s pomakom.
    """
    rezultat = ""
    for slovo in tekst:
        ascii_code = ord(slovo)
        if 65 <= ascii_code <= 90:
            slovo = chr(((ascii_code - 65 + pomak) % 26) + 65)
        rezultat += slovo
    return rezultat


def enigma(poruka: str, rotori, reflektor, rotori_pomak, rotori_pocetne_pozicije, ploca_s_utikacima_postavke) -> str:
    """
    Enigma simulator (po uzoru na tvoj kod).
    - rotori: tuple npr. ('I','II','III')
    - reflektor: 'B' ili 'C'
    - rotori_pomak: string npr. 'CBS' (3 slova)
    - rotori_pocetne_pozicije: string npr. 'NBA' (3 slova)
    - ploca_s_utikacima_postavke: string npr. 'AT BS DE ...'
    """
    kriptirana_poruka = ""
    abeceda = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Konfiguracija rotora (Wikipedia)
    rotor_I = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    rotor_I_zarez = "Q"
    rotor_II = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    rotor_II_zarez = "E"
    rotor_III = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    rotor_III_zarez = "V"
    rotor_IV = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    rotor_IV_zarez = "J"
    rotor_V = "VZBRGITYUPSDNHLXAWMJQOFECK"
    rotor_V_zarez = "Z"

    rotor_dict = {
        "I": rotor_I,
        "II": rotor_II,
        "III": rotor_III,
        "IV": rotor_IV,
        "V": rotor_V,
    }
    rotor_zarezi_dict = {
        "I": rotor_I_zarez,
        "II": rotor_II_zarez,
        "III": rotor_III_zarez,
        "IV": rotor_IV_zarez,
        "V": rotor_V_zarez,
    }

    reflektor_tip_B = {
        "A": "Y", "Y": "A",
        "B": "R", "R": "B",
        "C": "U", "U": "C",
        "D": "H", "H": "D",
        "E": "Q", "Q": "E",
        "F": "S", "S": "F",
        "G": "L", "L": "G",
        "I": "P", "P": "I",
        "J": "X", "X": "J",
        "K": "N", "N": "K",
        "M": "O", "O": "M",
        "T": "Z", "Z": "T",
        "V": "W", "W": "V",
    }
    reflektor_tip_C = {
        "A": "F", "F": "A",
        "B": "V", "V": "B",
        "C": "P", "P": "C",
        "D": "J", "J": "D",
        "E": "I", "I": "E",
        "G": "O", "O": "G",
        "H": "Y", "Y": "H",
        "K": "R", "R": "K",
        "L": "Z", "Z": "L",
        "M": "X", "X": "M",
        "N": "W", "W": "N",
        "Q": "T", "T": "Q",
        "S": "U", "U": "S",
    }
    reflektor_dict = reflektor_tip_B if reflektor == "B" else reflektor_tip_C

    # Odabir rotora prema postavkama
    rotor_A = rotor_dict[rotori[0]]
    rotor_B = rotor_dict[rotori[1]]
    rotor_C = rotor_dict[rotori[2]]

    rotor_A_zarez = rotor_zarezi_dict[rotori[0]]
    rotor_B_zarez = rotor_zarezi_dict[rotori[1]]
    rotor_C_zarez = rotor_zarezi_dict[rotori[2]]

    rotor_A_pocetno_slovo = rotori_pocetne_pozicije[0]
    rotor_B_pocetno_slovo = rotori_pocetne_pozicije[1]
    rotor_C_pocetno_slovo = rotori_pocetne_pozicije[2]

    rotor_A_pomak_postavke = abeceda.index(rotori_pomak[0])
    rotor_B_pomak_postavke = abeceda.index(rotori_pomak[1])
    rotor_C_pomak_postavke = abeceda.index(rotori_pomak[2])

    rotor_A = cezar_enkripcija(rotor_A, rotor_A_pomak_postavke)
    rotor_B = cezar_enkripcija(rotor_B, rotor_B_pomak_postavke)
    rotor_C = cezar_enkripcija(rotor_C, rotor_C_pomak_postavke)

    # Rotacija stringa rotora ovisno o pomaku (kao u tvom kodu)
    if rotor_A_pomak_postavke > 0:
        rotor_A = rotor_A[26 - rotor_A_pomak_postavke:] + rotor_A[:26 - rotor_A_pomak_postavke]
    if rotor_B_pomak_postavke > 0:
        rotor_B = rotor_B[26 - rotor_B_pomak_postavke:] + rotor_B[:26 - rotor_B_pomak_postavke]
    if rotor_C_pomak_postavke > 0:
        rotor_C = rotor_C[26 - rotor_C_pomak_postavke:] + rotor_C[:26 - rotor_C_pomak_postavke]

    # Plugboard dict
    ploca_s_utikacima = ploca_s_utikacima_postavke.upper().split()
    ploca_s_utikacima_dict = {}
    for kombinacija in ploca_s_utikacima:
        if len(kombinacija) == 2:
            a, b = kombinacija[0], kombinacija[1]
            ploca_s_utikacima_dict[a] = b
            ploca_s_utikacima_dict[b] = a

    poruka = poruka.upper()

    for slovo in poruka:
        kriptirano_slovo = slovo

        # Zakretanje rotora (samo kad je slovo A-Z)
        if slovo in abeceda:
            rotor_zakret_okidac = False

            # desni rotor se uvijek zakreće
            if rotor_C_pocetno_slovo == rotor_C_zarez:
                rotor_zakret_okidac = True
            rotor_C_pocetno_slovo = abeceda[(abeceda.index(rotor_C_pocetno_slovo) + 1) % 26]

            # srednji rotor ako je okidač
            if rotor_zakret_okidac:
                rotor_zakret_okidac = False
                if rotor_B_pocetno_slovo == rotor_B_zarez:
                    rotor_zakret_okidac = True
                rotor_B_pocetno_slovo = abeceda[(abeceda.index(rotor_B_pocetno_slovo) + 1) % 26]

                # lijevi rotor ako se dogodio okidač na srednjem
                if rotor_zakret_okidac:
                    rotor_A_pocetno_slovo = abeceda[(abeceda.index(rotor_A_pocetno_slovo) + 1) % 26]
        else:
            # Ako nije slovo, samo ga proslijedimo (nema enkripcije)
            kriptirana_poruka += kriptirano_slovo
            continue

        # Plugboard 1
        if slovo in ploca_s_utikacima_dict:
            kriptirano_slovo = ploca_s_utikacima_dict[slovo]

        pomak_A = abeceda.index(rotor_A_pocetno_slovo)
        pomak_B = abeceda.index(rotor_B_pocetno_slovo)
        pomak_C = abeceda.index(rotor_C_pocetno_slovo)

        # Naprijed kroz rotore (desni -> srednji -> lijevi)
        pozicija = abeceda.index(kriptirano_slovo)
        slovo_na_rotoru = rotor_C[(pozicija + pomak_C) % 26]
        pozicija = abeceda.index(slovo_na_rotoru)
        kriptirano_slovo = abeceda[(pozicija - pomak_C + 26) % 26]

        pozicija = abeceda.index(kriptirano_slovo)
        slovo_na_rotoru = rotor_B[(pozicija + pomak_B) % 26]
        pozicija = abeceda.index(slovo_na_rotoru)
        kriptirano_slovo = abeceda[(pozicija - pomak_B + 26) % 26]

        pozicija = abeceda.index(kriptirano_slovo)
        slovo_na_rotoru = rotor_A[(pozicija + pomak_A) % 26]
        pozicija = abeceda.index(slovo_na_rotoru)
        kriptirano_slovo = abeceda[(pozicija - pomak_A + 26) % 26]

        # Reflektor
        if kriptirano_slovo in reflektor_dict:
            kriptirano_slovo = reflektor_dict[kriptirano_slovo]

        # Nazad kroz rotore (lijevi -> srednji -> desni) bez reflektora
        pozicija = abeceda.index(kriptirano_slovo)
        slovo_na_rotoru = abeceda[(pozicija + pomak_A) % 26]
        pozicija = rotor_A.index(slovo_na_rotoru)
        kriptirano_slovo = abeceda[(pozicija - pomak_A + 26) % 26]

        pozicija = abeceda.index(kriptirano_slovo)
        slovo_na_rotoru = abeceda[(pozicija + pomak_B) % 26]
        pozicija = rotor_B.index(slovo_na_rotoru)
        kriptirano_slovo = abeceda[(pozicija - pomak_B + 26) % 26]

        pozicija = abeceda.index(kriptirano_slovo)
        slovo_na_rotoru = abeceda[(pozicija + pomak_C) % 26]
        pozicija = rotor_C.index(slovo_na_rotoru)
        kriptirano_slovo = abeceda[(pozicija - pomak_C + 26) % 26]

        # Plugboard 2
        if kriptirano_slovo in ploca_s_utikacima_dict:
            kriptirano_slovo = ploca_s_utikacima_dict[kriptirano_slovo]

        kriptirana_poruka += kriptirano_slovo

    return kriptirana_poruka


# -----------------------------
# CUSTOMTKINTER GUI
# -----------------------------
def normalize_3letters(s: str) -> str:
    s = (s or "").strip().upper()
    s = "".join([c for c in s if c.isalpha()])
    return s[:3]


def validate_plugboard(s: str) -> str:
    # dozvoli slova i razmake; sve ostalo izbaci (jednostavno)
    raw = (s or "").upper()
    allowed = []
    for ch in raw:
        if ch.isalpha() or ch.isspace():
            allowed.append(ch)
    return "".join(allowed)


def on_encrypt():
    try:
        r1 = rotor_1_var.get()
        r2 = rotor_2_var.get()
        r3 = rotor_3_var.get()
        ref = reflector_var.get()

        pomak = normalize_3letters(rotor_shift_var.get())
        poc = normalize_3letters(rotor_pos_var.get())
        plug = validate_plugboard(plugboard_var.get())

        if len(pomak) != 3 or len(poc) != 3:
            raise ValueError("Pomak i početne pozicije moraju imati točno 3 slova (A-Z).")

        msg = input_textbox.get("1.0", "end").strip()
        if not msg:
            raise ValueError("Upiši poruku za kriptiranje.")

        out = enigma(
            poruka=msg,
            rotori=(r1, r2, r3),
            reflektor=ref,
            rotori_pomak=pomak,
            rotori_pocetne_pozicije=poc,
            ploca_s_utikacima_postavke=plug
        )

        output_textbox.configure(state="normal")
        output_textbox.delete("1.0", "end")
        output_textbox.insert("1.0", out)
        output_textbox.configure(state="disabled")

        status_label.configure(text="OK: poruka kriptirana.")

    except Exception as e:
        status_label.configure(text=f"Greška: {e}")


def on_reset_defaults():
    rotor_1_var.set("I")
    rotor_2_var.set("II")
    rotor_3_var.set("III")
    reflector_var.set("B")
    rotor_shift_var.set("CBS")
    rotor_pos_var.set("NBA")
    plugboard_var.set("AT BS DE FM IR KN LZ OW PV XY")
    status_label.configure(text="Postavke vraćene na default.")


# UI setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Enigma Simulator (CustomTkinter)")
app.geometry("980x560")

app.grid_columnconfigure(0, weight=0)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# Lijevi panel - postavke
left = ctk.CTkFrame(app, corner_radius=16)
left.grid(row=0, column=0, sticky="ns", padx=14, pady=14)

ctk.CTkLabel(left, text="ENIGMA POSTAVKE", font=("Arial", 18, "bold")).pack(pady=(14, 10))

rotors_frame = ctk.CTkFrame(left)
rotors_frame.pack(fill="x", padx=12, pady=(6, 10))

ctk.CTkLabel(rotors_frame, text="Rotori (L, S, D):").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 4))

rotor_1_var = ctk.StringVar(value="I")
rotor_2_var = ctk.StringVar(value="II")
rotor_3_var = ctk.StringVar(value="III")

opts = ["I", "II", "III", "IV", "V"]

row = ctk.CTkFrame(rotors_frame, fg_color="transparent")
row.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 10))

ctk.CTkOptionMenu(row, variable=rotor_1_var, values=opts, width=80).pack(side="left", padx=(0, 8))
ctk.CTkOptionMenu(row, variable=rotor_2_var, values=opts, width=80).pack(side="left", padx=(0, 8))
ctk.CTkOptionMenu(row, variable=rotor_3_var, values=opts, width=80).pack(side="left")

reflector_var = ctk.StringVar(value="B")
ctk.CTkLabel(left, text="Reflektor:").pack(anchor="w", padx=12)
ctk.CTkOptionMenu(left, variable=reflector_var, values=["B", "C"], width=120).pack(anchor="w", padx=12, pady=(0, 10))

rotor_shift_var = ctk.StringVar(value="CBS")
rotor_pos_var = ctk.StringVar(value="NBA")
plugboard_var = ctk.StringVar(value="AT BS DE FM IR KN LZ OW PV XY")

ctk.CTkLabel(left, text="Pomak rotora (3 slova):").pack(anchor="w", padx=12)
ctk.CTkEntry(left, textvariable=rotor_shift_var, width=220).pack(anchor="w", padx=12, pady=(0, 10))

ctk.CTkLabel(left, text="Početne pozicije (3 slova):").pack(anchor="w", padx=12)
ctk.CTkEntry(left, textvariable=rotor_pos_var, width=220).pack(anchor="w", padx=12, pady=(0, 10))

ctk.CTkLabel(left, text="Ploča s utikačima (npr. AT BS ...):").pack(anchor="w", padx=12)
ctk.CTkEntry(left, textvariable=plugboard_var, width=300).pack(anchor="w", padx=12, pady=(0, 14))

btn_row = ctk.CTkFrame(left, fg_color="transparent")
btn_row.pack(fill="x", padx=12, pady=(0, 12))

ctk.CTkButton(btn_row, text="Default", command=on_reset_defaults, width=120).pack(side="left", padx=(0, 8))
ctk.CTkButton(btn_row, text="Kriptiraj ▶", command=on_encrypt, width=160).pack(side="left")

status_label = ctk.CTkLabel(left, text="", text_color="#bbbbbb", wraplength=320, justify="left")
status_label.pack(anchor="w", padx=12, pady=(6, 12))

# Desni panel - poruka i rezultat
right = ctk.CTkFrame(app, corner_radius=16)
right.grid(row=0, column=1, sticky="nsew", padx=(0, 14), pady=14)
right.grid_rowconfigure(2, weight=1)
right.grid_columnconfigure(0, weight=1)

ctk.CTkLabel(right, text="PORUKA", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 6))
input_textbox = ctk.CTkTextbox(right, height=120)
input_textbox.grid(row=1, column=0, sticky="ew", padx=14)
input_textbox.insert("1.0", "UPISI PORUKU OVDJE")

ctk.CTkLabel(right, text="KRIPTIRANI TEKST", font=("Arial", 16, "bold")).grid(row=2, column=0, sticky="w", padx=14, pady=(14, 6))
output_textbox = ctk.CTkTextbox(right)
output_textbox.grid(row=3, column=0, sticky="nsew", padx=14, pady=(0, 14))
output_textbox.configure(state="disabled")

# Enter = kriptiraj (praktično za predavanje)
app.bind("<Return>", lambda e: on_encrypt())

app.mainloop()
