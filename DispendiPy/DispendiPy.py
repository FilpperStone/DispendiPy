from cgitb import text
from shlex import join
from sqlite3 import Row
import tkinter
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import random
import os
from tkinter import messagebox
from tkinter import simpledialog, Toplevel
from turtle import distance, update
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
import ctypes
import traceback
import subprocess
import time

#Comando per buildare: cd DispendiPY, python -m PyInstaller --onefile --hidden-import=requests DispendiPy.py -i icona.ico -n "Dispendi" -w
def aggiungi():
    print("Workin'")
    if not loaded:
        folderwindow()

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
    global folder_name, loaded

    folder_window_open=True
    # Crea una finestra per inserire il nome della cartella
    folder_name = filedialog.askdirectory(initialdir = os.path , title = "Seleziona la cartella")
    loaded = True

def athletewindow():
    global athletewindow_open
    athletewindow_open=True
    # Crea una finestra per inserire il nome della cartella
    atleta_box = customtkinter.CTkInputDialog(text="Inserisci l'atleta:", title="Atleti")
    atleta=atleta_box.get_input()

    return atleta

def load():
    global folder_name, loaded, atleti, coefficienti  # Assuming atleti and coefficienti are global lists

    folderwindow()
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

    atleta_var = Combo2.get().strip()
    
    # Rimuovi i caratteri non validi dal nome del file
    atleta_var = atleta_var.replace('\n', '').replace('\r', '')

    print("Creazione del file...")

    # Costruisci il percorso del file
    if not loaded:
        folderwindow()
    file_path = os.path.join(folder_name, atleta_var + ".txt")

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

def settings():
    global loaded
    settings_window = CTkToplevel(root)
    settings_window.title("Impostazioni")
    settings_window.lift()  # Porta la finestra in primo piano
    settings_window.focus_force()  # Forza il focus sulla finestra
    
    # Crea le tab nel tabview
    settingstabs = customtkinter.CTkTabview(settings_window)
    settingstabs.grid(column=1, row=1, sticky="WENS")
    infotab=settingstabs.add("Informazioni")
    foldertab=settingstabs.add("Cartelle")
    resettab=settingstabs.add("Reset")
    feedbacktab=settingstabs.add("Feedback")
    settingstabs.set("Informazioni")
    
    # Crea un frame per contenere i check_button e versionLabel
    check_frame = customtkinter.CTkFrame(infotab)
    check_frame.grid(column=1, row=1, sticky="WENS")
    
    # Aggiungi elementi al frame
    versionLabel = customtkinter.CTkLabel(check_frame, text="Versione attuale: " + CURRENT_VERSION)
    versionLabel.grid(column=0, row=0, sticky="W", padx=5, pady=5)
    
    check_button = customtkinter.CTkButton(check_frame, text="Controllo Aggiornamenti", command=check_for_update)
    check_button.grid(column=0, row=1, sticky="W", padx=5, pady=5)
    
    if update_available:  # e.g., if CURRENT_VERSION < latest_version
        updateLabel = customtkinter.CTkLabel(infotab, text="Aggiornamento disponibile: " + latest_version)
        updateLabel.grid(column=0, row=2, sticky="W", padx=5, pady=5)
        
        update_button = customtkinter.CTkButton(infotab, text="Aggiorna", command=download_update)
        update_button.grid(column=0, row=3, sticky="W", padx=5, pady=5)
        
    folder_label=CTkLabel(foldertab, text=" Selezionare la cartella")
    folder_label.grid(column=0, row=4, sticky=(W, E))
    if loaded:
        print(loaded)
        folder_label.configure(text=folder_name)
    folder_button=CTkButton(foldertab, text="Sfoglia", command=lambda: browse(folder_label))
    folder_button.grid(column=1, row=4, sticky="ENS")

    
    # Assicura che la finestra abbia il focus dopo l'inizializzazione
    settings_window.after(10, lambda: settings_window.focus())


def browse(label):
    print("Here we are")
    folderwindow()
    label.configure(text=folder_name)
    
def segmented_button_callback(value):
    if value=="Salva":
        save()
    elif value=="Carica":
        load()
    elif value=="aggiungi":
       aggiungi()
    elif value=="Cancella":
        delete()
    elif value=="Impostazioni":
        settings()
    elif value=="Chiudi": 
        root.destroy()
    segmented_button.set(None)


def check_for_update():
    global update_info, latest_version, update_available
    try:
        # Recupera i dati della release più recente da GitHub
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        
        release_info = response.json()
        latest_version = release_info["tag_name"]
        print(release_info["tag_name"])
        if latest_version > CURRENT_VERSION:
            update_info = f"Nuova versione disponibile: {latest_version}\nVersione corrente: {CURRENT_VERSION}"
            update_available=True
            update_prompt = messagebox.askyesno("Aggiornamento Disponibile", f"È disponibile una nuova versione ({latest_version}). Vuoi aggiornare?")
            
            if update_prompt:
                asset_name = next((asset["name"] for asset in release_info["assets"] if asset["name"].endswith(".exe")), None)
                
                if asset_name:
                    file_path=os.path.join(working_dir, "update.txt")
                    with open(file_path, "a") as f:
                        f.write(f"{latest_version}\n")
                        f.write(f"{asset_name}\n")
                    subprocess.Popen(updater, shell=False)
                    #download_update(latest_version, asset_name)
                    #update_prompt = messagebox.askyesno("Aggiornamento Disponibile", f"È disponibile una nuova versione ({latest_version}). Vuoi aggiornare?")
                    sys.exit(0)
                else:
                    messagebox.showerror("Errore", "Impossibile trovare il file di aggiornamento.")
        else:
            print("Nessun aggiornamento disponibile.")
            update_available=False
            #if os.path.exists(new_executable):
             #   time.sleep(3)
                #os.remove(old_executable)
    
    except requests.RequestException as e:
        print(f"Errore durante il controllo degli aggiornamenti: {e}")

GITHUB_DOWNLOAD_URL = "https://github.com/your_repo/releases/download/{tag}/{asset_name}"

def download_update(latest_version, asset_name):
    try:
        # URL per il download
        download_url = GITHUB_DOWNLOAD_URL.format(tag=latest_version, asset_name=asset_name)
        response = requests.get(download_url, stream=True)
        response.raise_for_status()



        # Scarica il nuovo eseguibile in un file temporaneo
        with open(temp_executable, "wb") as temp_file:
            shutil.copyfileobj(response.raw, temp_file)

        # Rinomina l'eseguibile corrente
        if os.path.exists(new_executable):
            os.rename(new_executable, old_executable)

        # Sposta il nuovo file nella posizione corretta
        shutil.move(temp_executable, new_executable)
        
        #executable_dir=os.path.join(os.path.dirname(new_executable), new_executable)
        #os.chdir(updaterdir)
        #print(os.getcwd())
        #os.system(f"python {updater}")
        os.system(updater)
      
        #process.wait()
        # Notifica l'utente del successo
        #messagebox.showinfo("Aggiornamento completato", "L'aggiornamento è stato installato con successo. Riavvia l'applicazione.")

        # Chiudi l'applicazione
        #sys.exit(0)

    except Exception as e:
        messagebox.showerror("Errore di aggiornamento", f"Si è verificato un errore durante l'aggiornamento: {e}")

def mostra_permessi(path):
    print(f"Permessi per: {path}")
    print(f"    Lettura: {'Sì' if os.access(path, os.R_OK) else 'No'}")
    print(f"    Scrittura: {'Sì' if os.access(path, os.W_OK) else 'No'}")
    print(f"    Esecuzione: {'Sì' if os.access(path, os.X_OK) else 'No'}")

def mostra_permessi_avanzati(path):
    print(f"Permessi avanzati per {path}: {oct(os.stat(path).st_mode)[-3:]}")
    print(f"Scrittura: {'Sì' if os.access(path, os.W_OK) else 'No'}")

def test_permessi_scrittura(path):
    test_file = os.path.join(path, "test_write_permissions.txt")
    try:
        with open(test_file, "w") as f:
            f.write("Test di scrittura riuscito.")
        print(f"Scrittura riuscita: {test_file}")
        os.remove(test_file)  # Rimuove il file di test
    except Exception as e:
        print(f"Errore di scrittura: {e}")

def check_admin_permissions():
    """Controlla se il programma è in esecuzione come amministratore"""
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False
    return is_admin

def restart_as_admin():
    """Riavvia il programma come amministratore se non ha i permessi elevati"""
    if not check_admin_permissions():
        print("Questo programma richiede i permessi di amministratore per funzionare correttamente.")
        try:
            # Riavvia il programma come amministratore
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit()  # Termina l'istanza corrente
        except Exception as e:
            print(f"Errore nell'elevazione dei permessi: {e}")
            sys.exit(1)  # Termina il programma in caso di errore




CURRENT_VERSION = "V1.1.0"  # La versione attuale del programma
root = CTk()
root.title("Calcolo dei dispendi "+CURRENT_VERSION)
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
folder_name=StringVar()
mainframe = CTkFrame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("400x300")
athlete_window=BooleanVar()
update_available=BooleanVar(value=False)
GITHUB_API_URL = "https://api.github.com/repos/FilpperStone/DispendiPy/releases/latest"
GITHUB_DOWNLOAD_URL = "https://github.com/FilpperStone/DispendiPy/releases/download/{tag}/{asset_name}"

# Percorsi
current_executable = sys.executable
working_dir = os.path.dirname(current_executable)
temp_executable = os.path.join(working_dir, "temp_new_Dispendi.exe")
old_executable = os.path.join(working_dir, "Dispendi-old.exe")
new_executable = str(current_executable)
updater = os.path.join(os.path.dirname(current_executable), "Updater.exe")
 
#restart_as_admin()

# Controlla i permessi sulla directory corrente
#mostra_permessi(os.getcwd())

# Controlla i permessi sulla cartella Downloads
#mostra_permessi(os.path.expanduser(os.getcwd()))

#mostra_permessi_avanzati(os.getcwd())

#test_permessi_scrittura(os.path.expanduser(os.getcwd()))

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
    values=["Salva", "Carica", "aggiungi", "Cancella", "Impostazioni", "Chiudi"],
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
CoeffTextLabel = CTkLabel(CoeffLabel, text=" ")
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
    atleta_selezionato = Combo3.get()
    
    if atleta_selezionato in atleti:
        selected_index = atleti.index(atleta_selezionato)
        
        # Aggiorna il testo di CoeffTextLabel con il valore del coefficiente corrispondente
        CoeffTextLabel.configure(text=coefficienti[selected_index])
    else:
        # Pulisce il testo se non è stato selezionato un atleta valido
        CoeffTextLabel.configure(text="")

# Imposta il callback sulla Combo3 per l'evento di selezione
Combo3.bind("<<ComboboxSelected>>", update_coefficient)

root.bind("<Return>", on_enter)

root.mainloop()

