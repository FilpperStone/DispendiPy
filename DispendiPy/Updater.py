#!/usr/bin/python
# -*- coding: latin-1 -*-
import os
#import psutil
import sys
import shutil
import subprocess
import requests
import customtkinter 
from customtkinter import *
from tkinter import messagebox



'''def close_parent_process():
    PROCNAME = "Dispendi-old.exe"

    for proc in psutil.process_iter():
        # check whether the process name matches
        print(proc.name())
        if proc.name() == PROCNAME:
            proc.kill()
            open_new_executable()'''
def open_new_executable():
    workingdir = os.path.join(os.getcwd(), "Dispendi.exe")
    subprocess.Popen(workingdir, shell=True)
    
def download_update():
    try:
        file_path=os.path.join(os.path.dirname(this_executable), "update.txt")
        with open(file_path) as f:
            latest_version=f.readline().strip()
            print(latest_version)
            asset_name=f.readline().strip()
            print(asset_name)

        # URL per il download
        download_url = GITHUB_DOWNLOAD_URL.format(tag=latest_version, asset_name=asset_name)
        print(download_url)
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
        #close_parent_process
        open_new_executable()
    except Exception as e:
        messagebox.showerror("Errore di aggiornamento", f"Si è verificato un errore durante l'aggiornamento: {e}")


print("Updater running")
GITHUB_API_URL = "https://api.github.com/repos/FilpperStone/DispendiPy/releases/latest"
GITHUB_DOWNLOAD_URL = "https://github.com/FilpperStone/DispendiPy/releases/download/{tag}/{asset_name}"
this_executable=sys.executable
current_executable = os.path.join(os.path.dirname(this_executable), "Dispendi.exe")
temp_executable = os.path.join(os.path.dirname(this_executable), "temp_new_Dispendi.exe")
old_executable = os.path.join(os.path.dirname(this_executable), "Dispendi-old.exe")
new_executable = current_executable

root = CTk()
root.title("Aggiornamento in corso")
root.resizable(True, True)
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

progressbar = customtkinter.CTkProgressBar(mainframe, orientation="horizontal")

download_update()