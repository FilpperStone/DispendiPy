from cgitb import text
import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import random
import os
from tkinter import messagebox
from tkinter import simpledialog, Toplevel
from turtle import distance
import customtkinter 
from customtkinter import CTkCheckBox, CTkSwitch
from customtkinter import *
from customtkinter.windows.widgets import CTkLabel, CTkOptionMenu
import datetime
from datetime import date
import csv  # Import the csv module
import requests
import sys
import shutil
#Comando per buildare: cd DispendiPY, python -m PyInstaller --onefile --hidden-import=requests DispendiPy.py -i icona.ico -n "Dispendi" -w
def aggiungi():
    print("Workin'")
    if not loaded:
        folder_name = filedialog.askdirectory(initialdir = os.path , title = "Seleziona la cartella")

        direzioni_file = os.path.join(folder_name, "atleti.txt")
        atleta=athletewindow()
        atleti.append(atleta)
        if not os.path.exists(folder_name):
           messagebox.showerror("Errore", "La cartella non esiste.")
           return  # Usciamo dalla funzione se la cartella non esiste

        with open(direzioni_file, "w") as f:
            for item in atleti:
                f.write(item)  # Scriviamo ogni elemento della lista su una nuova riga
            #with open(direzioni_file, "a") as f:
                #f.write("\n")
        load()
    else:
        atleta=athletewindow()
        atleti.append(str(atleta)+"\n")
        for i in atleti:
            print(i)
        update_combobox()
        
    

def folderwindow():
    global folder_name_var

    folder_window_open=True
    # Crea una finestra per inserire il nome della cartella
    folder_window = CTkInputDialog(title="Nome della Cartella", text="Cartella:")
    folder_window.focus()
    folder_name=folder_window.get_input()

def athletewindow():
    global athletewindow_open
    athletewindow_open=True
    # Crea una finestra per inserire il nome della cartella
    atleta_box = customtkinter.CTkInputDialog(text="Inserisci l'atleta:", title="Atleti")
    atleta=atleta_box.get_input()

    return atleta

def load():
    global folder_name, loaded, atleti, coefficienti  # Assuming atleti and coefficienti are global lists

    folder_name = filedialog.askdirectory(initialdir=os.path, title="Seleziona la cartella")
    atleta_file = os.path.join(folder_name, "atleti.txt")

    if os.path.exists(atleta_file):
        with open(atleta_file, "r") as f:
            atleti.clear()
            coefficienti.clear()  # Clear both lists
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) == 2:  # Ensure each row has two elements
                    atleti.append(row[0].strip())  # Append the athlete name, removing whitespace
                    coefficienti.append(row[1].strip())  # Append the coefficient, removing whitespace

        update_combobox()  # Assuming this function updates the comboboxes
        Combo2.configure(state='readonly')
        Combo3.configure(state='readonly')
        loaded = True

    else:
        messagebox.showerror("Errore", "La cartella o i file non esistono.")
        
def rollback():
    global folder_name, loaded, Output, turns
    atleti.clear()
    distanza_entry.delete(0, END)
    tempo_entry.delete(0, END)
    loaded=False
    turns=False
    folder_name=""

def update_combobox():
    Combo2.configure(values=atleti)
    Combo3.configure(values=atleti)

def delete():
    # Crea una nuova finestra per la cancellazione
    global delete_window
    delete_window = CTkToplevel(root)
    delete_window.title("Cancella valori")

    # Aggiungi etichette e checkbox per i valori di direzioni
    for i, x in enumerate(atleti):
        label = CTkLabel(delete_window, text=x)
        label.grid(row=i, column=0, sticky="w")
        delete_var_a = BooleanVar()
        delete_checkbox_a = CTkCheckBox(delete_window, variable=delete_var_a)
        delete_checkbox_a.grid(row=i, column=1, sticky="e")
        selectedA_delete.append(delete_var_a)

    # Aggiungi un pulsante per confermare la cancellazione
    confirm_button = CTkButton(delete_window, text="Conferma cancellazione", command=confirm_deletion)
    confirm_button.grid(row=len(atleti) + 1, column=0, columnspan=4)

def confirm_deletion():
    global delete_window, selectedA_delete
    # Rimuovi gli elementi selezionati da direzioni e strutture
    updated_atleti = [atleti[i] for i, var in enumerate(selectedA_delete) if not var.get()]

    # Aggiorna direzioni e strutture con gli elementi non cancellati
    atleti.clear()
    atleti.extend(updated_atleti)

    # Chiudi la finestra di cancellazione
    delete_window.destroy()

#modificare dopo
def save():
    global dispendio, distanza, folder_name_var, Combo1, Combo2

    # Ottieni i valori delle variabili StringVar
    folder_name = folder_name_var.get().strip()
    atleta_var = Combo2.get().strip()
    
    # Rimuovi i caratteri non validi dal nome del file
    atleta_var = atleta_var.replace('\n', '').replace('\r', '')

    print("Creazione del file...")

    # Costruisci il percorso del file
    file_path=filedialog.askdirectory(initialdir = os.path , title = "Seleziona la cartella")
    file_path = os.path.join(file_path, atleta_var + ".txt")

    try:
        # Scrivi nel file
        with open(file_path, "a") as f:
            f.write(f"{date.today()}\n")
            f.write(f"{dispendio}\n")
            f.write(f"{distanza.get()}\n")
            f.write(f"{Combo1.get()}\n")
        print(f"File salvato correttamente in {file_path}")
    except OSError as e:
        print(f"Errore nella scrittura del file: {e}")

def calculate():
  global dispendio 
  for widget in mainframe.winfo_children():
       if isinstance(widget, Label):
           widget.pack_forget()
  if tempofed == tempo:

    dispendio = 100
  else:
    temptempo=tempo.get()
    temptempo=int(temptempo)
    temptempofed=tempofed.get()
    temptempofed=int(temptempofed)
    dispendio = temptempo - temptempofed
    dispendio = 100 - (dispendio / temptempofed * 100)

    CTkLabel(mainframe, text=dispendio).grid(column=2, row=6, sticky=W)

def calculateC():
    global coeffwindow, media2000, colpi2000
    coeffwindow=CTkToplevel(root)
    coeffwindow.title("Calcola il coefficiente")
    coeffwindow.lift()  # Bring the window to the front
    coeffwindow.focus_force()  # Force focus on the window
    
    colpi2000=StringVar()
    media2000=StringVar()
    CTkLabel(coeffwindow, text="Media").grid(column=0, row=1, sticky=(W))
    media_entry=CTkEntry(coeffwindow, width=7, textvariable=media2000)
    media_entry.grid(column=1, row=1, sticky=(W, E))
    
    CTkLabel(coeffwindow, text="Colpi").grid(column=0, row=2, sticky=(W))
    media_entry=CTkEntry(coeffwindow, width=7, textvariable=colpi2000)
    media_entry.grid(column=1, row=2, sticky=(W, E))

    

    endButton=CTkButton(coeffwindow, text="Calcola", command=windowdestroy).grid(column=1, row=3, sticky=(W, E))
    coeffwindow.after(10, lambda: coeffwindow.focus())  # Ensure the window is focused after it's fully initialized
def windowdestroy():
    if Combo3.get() in atleti:
        index=atleti.index(Combo3.get())
    coefficienti[index]=media2000+colpi2000
    #coefficienti[index]=media2000.get()+colpi2000.get()
    CoeffTextLabel.configure(text=coefficienti[index])
    coeffwindow.destroy()
        
    

    

def addbutton(c, r, Btext, funzione):
    CTkButton(mainframe, text=Btext, command=funzione).grid(column=c, row=r, sticky=(W, E))
    
def saveathletes():
    athlete_files=os.path.join(folder_name, "atleti.txt")
    with open() as f:
        for i in atleti:
            f.write(i)

def segmented_button_callback(value):
    if value=="Salva":
        save()
    elif value=="Carica":
        load()
    elif value=="aggiungi":
       aggiungi()
    elif value=="Cancella":
        delete()
    elif value=="Reset": 
        rollback()
    elif value=="Chiudi": 
        root.destroy()
    segmented_button.set(None)


def show_splash_screen(update_info):
    splash = Toplevel()
    splash.title("Controllo Aggiornamenti")
    splash.geometry("300x200")
    splash.overrideredirect(True)  # Rimuove il bordo della finestra

    Label(splash, text="Benvenuto in DispendiPy", font=("Arial", 14)).pack(pady=10)
    Label(splash, text=update_info, wraplength=280, font=("Arial", 10)).pack(pady=10)

    splash.after(10000, splash.destroy)  # Chiude lo splash screen dopo 10 secondi

def check_for_update():
    try:
        # Recupera i dati della release più recente da GitHub
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        
        release_info = response.json()
        latest_version = release_info["tag_name"]
        print(release_info["tag_name"])
        if latest_version > CURRENT_VERSION:
            update_info = f"Nuova versione disponibile: {latest_version}\nVersione corrente: {CURRENT_VERSION}"
            show_splash_screen(update_info)

            update_prompt = messagebox.askyesno("Aggiornamento Disponibile", f"È disponibile una nuova versione ({latest_version}). Vuoi aggiornare?")
            
            if update_prompt:
                asset_name = next((asset["name"] for asset in release_info["assets"] if asset["name"].endswith(".exe")), None)
                
                if asset_name:
                    download_update(latest_version, asset_name)
                else:
                    messagebox.showerror("Errore", "Impossibile trovare il file di aggiornamento.")
        else:
            print("Nessun aggiornamento disponibile.")
    
    except requests.RequestException as e:
        print(f"Errore durante il controllo degli aggiornamenti: {e}")

def download_update(latest_version, asset_name):
    try:
        download_url = GITHUB_DOWNLOAD_URL.format(tag=latest_version, asset_name=asset_name)
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        update_file_path = os.path.join(os.path.dirname(sys.executable), asset_name)
        
        with open(update_file_path, "wb") as update_file:
            shutil.copyfileobj(response.raw, update_file)
        
        # Sostituzione dell'eseguibile corrente
        current_executable = sys.executable
        os.replace(update_file_path, current_executable)
        
        messagebox.showinfo("Aggiornamento completato", "L'aggiornamento è stato installato con successo. Riavvia l'applicazione.")
        sys.exit(0)  # Chiude l'applicazione corrente
    
    except Exception as e:
        print(f"Errore durante il download dell'aggiornamento: {e}")
        messagebox.showerror("Errore di aggiornamento", "Si è verificato un errore durante il download dell'aggiornamento.")

root = CTk()
root.title("Calcolo dei dispendi")
root.resizable(True, True)
atleta=StringVar()
selectedA=[]
selectedS=[]
atleti=[]
coefficienti=[]
imbarcazioni=["1", "2x", "2-", "2+", "4x", "4-", "4+", "8"]
selectedA_delete = []
selectedS_delete = []
direzione_bool=BooleanVar(value=False)
struttura_bool=BooleanVar(value=False)
turns=BooleanVar(value=False)
loaded=BooleanVar(value=False)
folder_window_open=BooleanVar()
turn_window_open=BooleanVar()
folder_name_var=StringVar()
mainframe = CTkFrame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("400x300")
athlete_window=BooleanVar()
GITHUB_API_URL = "https://api.github.com/repos/FilpperStone/DispendiPy/releases/latest"
GITHUB_DOWNLOAD_URL = "https://github.com/FilpperStone/DispendiPy/releases/download/{tag}/{asset_name}"
CURRENT_VERSION = "V1.0.1"  # La versione attuale del programma


mainframe = customtkinter.CTkFrame(root)
mainframe.grid(column=0, row=0, sticky=(customtkinter.N, customtkinter.W, customtkinter.E, customtkinter.S))
mainframe.grid(column=0, row=0, sticky=(customtkinter.N, customtkinter.W, customtkinter.E, customtkinter.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=2)
mainframe.columnconfigure(3, weight=2)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=1)
mainframe.rowconfigure(2, weight=1)
mainframe.rowconfigure(3, weight=1)
mainframe.rowconfigure(4, weight=1)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
check_for_update()
tabs=CTkTabview(master=mainframe)
tabs.grid(column=2, row=1, sticky=(W, E))
coefftab=tabs.add("Coefficiente")
dispetab=tabs.add("Dispendi")
tabs.set("Coefficiente")

Combo1 = CTkComboBox(dispetab, state='readonly')  # Set combobox to read-only
Combo1.grid(column=2, row=2, sticky=(W, E))
Combo1.configure(values=imbarcazioni)

Combo2 = CTkComboBox(dispetab, state='disabled')  # Set combobox to read-only
Combo2.grid(column=2, row=1, sticky=(W, E))

Combo3 = CTkComboBox(coefftab, state='disabled')  # Set combobox to read-only
Combo3.grid(column=2, row=1, sticky=(W, E))

CTkLabel(dispetab, text="Distanza:").grid(column=1, row=3, sticky=W)
distanza=StringVar()
distanza_entry=CTkEntry(dispetab, width=7, textvariable=distanza)
distanza_entry.grid(column=2, row=3, sticky=(W, E))

CTkLabel(dispetab, text="Tempo:").grid(column=1, row=4, sticky=W)
tempo=StringVar()
tempo_entry=CTkEntry(dispetab, width=7, textvariable=tempo)
tempo_entry.grid(column=2, row=4, sticky=(W, E))

CTkLabel(dispetab, text="Tempo Federale:").grid(column=1, row=5, sticky=W)
tempofed=StringVar()
tempofed_entry=CTkEntry(dispetab, width=7, textvariable=tempofed)
tempofed_entry.grid(column=2, row=5, sticky=(W, E))
segmented_button = customtkinter.CTkSegmentedButton(
    mainframe,
    values=["Salva", "Carica", "aggiungi", "Cancella", "Reset", "Chiudi"],
    command=segmented_button_callback
)
segmented_button.grid(column=1, row=0, columnspan=6, sticky=(customtkinter.W, customtkinter.E), padx=5, pady=5)
segmented_button.grid_propagate(False)
CTkLabel(dispetab, text="Atleta:").grid(column=1, row=1, sticky=W)
CTkLabel(coefftab, text="Atleta:").grid(column=1, row=1, sticky=W)
CTkLabel(dispetab, text="Imbarcazione:").grid(column=1, row=2, sticky=W)
CTkLabel(coefftab, text="Coefficiente:").grid(column=1, row=2, sticky=W)
# Creazione di un CTkFrame come CoeffLabel e CTkLabel figlia per il testo del coefficiente
CoeffLabel = CTkFrame(coefftab)
CoeffLabel.grid(column=2, row=2, sticky=(customtkinter.W, customtkinter.E, customtkinter.S, customtkinter.N))

# Label all'interno del frame per mostrare il valore del coefficiente
CoeffTextLabel = CTkLabel(CoeffLabel, text="")
CoeffTextLabel.grid(column=0, row=0, sticky=W)

coeffbutton=CTkButton(coefftab, text="Calcola", command=calculateC)
coeffbutton.grid(column=3, row=2, sticky=(W, E))
CTkLabel(dispetab, text="Dispendio:").grid(column=1, row=6, sticky=W)
CTkButton(dispetab, text="Calcola", command=calculate).grid(column=1, row=7, sticky=(W, E))

#ttk.Button(mainframe, text="Reset", command=rollback).grid(column=3, row=1, sticky=(W, E))
#ttk.Button(mainframe, text="Cancella", command=delete).grid(column=2, row=1, sticky=(W, E))

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

def on_enter(event):
    distanza_text = distanza.get().strip()
    tempo_text = tempo.get().strip()
    tempofed_text = tempofed.get().strip()
    folder_text = folder_name_var.get().strip()


    calculate()
    

# Funzione per aggiornare il coefficiente in base alla selezione della Combo3
def update_coefficient(event):
    # Ottieni l'indice dell'atleta selezionato
    print("Workin")
    if Combo3.get() in atleti:
        selected_index=atleti.index(Combo3.get())
    
    if selected_index != -1:  # Verifica che ci sia una selezione valida
        CoeffTextLabel.configure(text=coefficienti[selected_index])

# Imposta il callback sulla Combo3 per l'evento di selezione
Combo3.bind("<<ComboboxSelected>>", update_coefficient)

root.bind("<Return>", on_enter)

root.mainloop()

'''
def show_splash_screen(update_info):
    """Mostra uno splash screen con le informazioni sugli aggiornamenti."""
    splash = Toplevel()
    splash.title("Controllo Aggiornamenti")
    splash.geometry("300x200")
    splash.overrideredirect(True)  # Rimuove il bordo della finestra

    Label(splash, text="Benvenuto in DispendiPy", font=("Arial", 14)).pack(pady=10)
    Label(splash, text=update_info, wraplength=280, font=("Arial", 10)).pack(pady=10)

    splash.after(10000, splash.destroy)  # Chiude lo splash screen dopo 3 secondi

def check_for_update():
    try:
        # Recupera i dati della release più recente da GitHub
        response = requests.get(GITHUB_API_URL.format(user="FilpperStone", repo="DispendiPy"))
        response.raise_for_status()
        
        release_info = response.json()
        latest_version = release_info["tag_name"]

        if latest_version > CURRENT_VERSION:
            # Mostra uno splash screen con le informazioni sugli aggiornamenti
            update_info = f"Nuova versione disponibile: {latest_version}\nVersione corrente: {CURRENT_VERSION}"
            show_splash_screen(update_info)

            # Dopo lo splash screen, chiede all'utente se desidera aggiornare
            update_prompt = messagebox.askyesno("Aggiornamento Disponibile", f"È disponibile una nuova versione ({latest_version}). Vuoi aggiornare?")
            
            if update_prompt:
                asset_name = next((asset["name"] for asset in release_info["assets"] if asset["name"].endswith(".exe")), None)
                
                if asset_name:
                    download_update(latest_version, asset_name)
                else:
                    messagebox.showerror("Errore", "Impossibile trovare il file di aggiornamento.")
        else:
            messagebox.showerror("Nessun aggiornamento disponibile.", "Procedere")
            print("Nessun aggiornamento disponibile.")
    
    except requests.RequestException as e:
        print(f"Errore durante il controllo aggiornamenti: {e}")

def download_update(new_version, asset_name):
    try:
        # Costruisce l'URL per scaricare l'asset della release
        download_url = GITHUB_DOWNLOAD_URL.format(user="FilpperStone", repo="DispendiPy", tag=new_version, asset_name=asset_name)
        
        # Percorso temporaneo per salvare il file scaricato
        temp_file = "DispendiPy_nuovo.exe"
        
        # Effettua il download del file
        with requests.get(download_url, stream=True) as response:
            response.raise_for_status()
            with open(temp_file, "wb") as f:
                shutil.copyfileobj(response.raw, f)
        
        # Rinomina l'eseguibile attuale e sostituisce con quello nuovo
        os.rename(sys.argv[0], f"{sys.argv[0]}.old")  # Rinominare il vecchio eseguibile
        shutil.move(temp_file, sys.argv[0])  # Sposta il nuovo eseguibile nel percorso originale
        
        messagebox.showinfo("Aggiornamento Completato", "Aggiornamento completato con successo! Riavvio dell'applicazione.")
        os.execv(sys.argv[0], sys.argv)  # Riavvia il programma con la nuova versione
    
    except Exception as e:
        print(f"Errore durante il download dell'aggiornamento: {e}")
'''