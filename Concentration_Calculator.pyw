"""
A simple calculator which imports compound data (name, molar mass, density) and can calculate how much is needed to make up desired concentrations
"""

import glob
import os
import numpy as np
from tkinter import *
from tkinter.ttk import Combobox

#imports data from species.txt
species_info = np.loadtxt("species.txt", dtype=str, delimiter = "\t")

species = [n[0] for n in species_info]
molar_masses = [n[1] for n in species_info]
densities = [n[2] for n in species_info]

if len(species_info) == 0:
    print("No Species.txt found.")

#begins window
window = Tk()

window.title("Moistly Calculator")
window.geometry("440x250")

vol_var = StringVar()
conc_var = StringVar()

global mass
mass= 0

title_molarity = Label(window, text = "For making a new solution: ", bg = "green", width = 65)
title_molarity.grid(row=1, column =1, columnspan = 5)

vol_var.set(float(1))
conc_var.set(float(1))

lbl_spec = Label(window, text="Species: ")
lbl_spec.grid(row = 2, column = 1, sticky = "w")

lbl_conc = Label(window, text="Concentration: ")
lbl_conc.grid(row = 3, column = 1, sticky = "w")

conc = Entry(window, text = conc_var)
conc.grid(row = 3, column = 2, sticky="w")

lbl_conc = Label(window, text="Volume: ")
lbl_conc.grid(row = 4, column = 1, sticky = "w")

vol = Entry(window, text=vol_var)
vol.grid(row = 4, column = 2, sticky="w")

lbl_molar_mass = Label(window)
lbl_molar_mass.grid(row = 2, column = 3)

lbl_mass = Label(window)
lbl_mass.grid(row=5, column = 2, columnspan=4, sticky = "w")

mag_conc = Combobox(window, width=12)
mag_conc["values"] = ["mol", "mmol", "\u03BCmol"]
mag_conc.set("mol")
mag_conc.grid(row = 3, column = 3)

mag_vol = Combobox(window, width=12)
mag_vol["values"] = ["cm\u00B3", "dm\u00B3", "L"]
mag_vol.set("dm\u00B3")
mag_vol.grid(row = 4, column = 3)

#this event is triggered when the species combobox is used to select a species
def update_molar_mass(event):
    spec_used = combo_species.get()
    for spec, mass_l, dens in zip(species, molar_masses, densities):
        if spec == spec_used:
            global density
            density = dens
            mass = float(mass_l)
            global mass_for_calc
            mass_for_calc = mass
            mass_text = "Molar Mass: "+str(mass)+" Da"
            lbl_molar_mass.configure(text=mass)
              
combo_species = Combobox(window)
combo_species["values"] = species
combo_species.grid(row = 2, column = 2, padx = 1, sticky = "w")
combo_species.bind("<<ComboboxSelected>>", update_molar_mass)

#this occurs when the 'calculate' button is clicked
def print_mass():
    
    volume = float(vol.get())  
    conc_f = float(conc.get())
    moles = conc_f * (volume)
    
    mass_calc = (moles)*float(mass_for_calc)
    mass_print = round(mass_calc, 2)
     
    mag_mol_calc = mag_conc.get()
    mag_vol_calc = mag_vol.get()

    #here we use the 'units' inputs by comparing to the SI list    
    units = [" k", " ", " m", " \u03BC" , " n", " p", " f"]  
    units_p = 1

    #the selected magnitudes bump everything up the list!
    if mag_mol_calc == "mol":
        units_p += 0
    elif mag_mol_calc == "mmol":
        units_p += 1
    elif mag_mol_calc == "\u03BCmol":
        units_p += 2

    if mag_vol_calc == "cm\u00B3":
        units_p += 1
    if mag_vol_calc == "dm\u00B3":
        units_p += 0
    if mag_vol_calc == "L":
        units_p += 0

    #solves a problem with overly large numbers observed
    
    while mass_print > 1000:
        mass_print = mass_print / 1000
        units_p += -1

    mass_print = round(mass_print, 2)
    
    #can differentiate between solids and liquid reagents
    if density == "SOLID":
        lbl_mass.configure(text = " "+str(mass_print)+str(units[units_p])+"g "+str(combo_species.get()))
        
    else:
        density_print = float(density)
        vol_print =round(mass_print/density_print)
        lbl_mass.configure(text = " "+str(mass_print)+str(units[units_p])+"g ("+str(vol_print)+" "+units[units_p+1]+"L ) "+str(combo_species.get()))

#finally the calculate button is added
btn_calc = Button(window, text = "Amount Required:", command = print_mass)
btn_calc.grid(row=5, column = 1)

#now we add the section for the dilution calculator
conc_final = StringVar()
conc_final.set(float(1))
conc_start = StringVar()
conc_start.set(float(1))
vol_final = StringVar()
vol_final.set(float(1))

lbl_dilute = Label(window, text="Diluting an existing solution: ", bg = "green", width = 65)
lbl_dilute.grid(row=6, column = 1, columnspan = 5)

lbl_conc_2 = Label(window, text ="Desired Concentration: ")
lbl_conc_2.grid(row=9, column = 1, sticky = "w")

conc_2 = Entry(window, text = conc_final)
conc_2.grid(row=9, column = 2, sticky = "w")

mag_conc_2 = Label(window, width=12, text= "mol dm\u00B3")
mag_conc_2.grid(row= 9, column = 3,  sticky = "w")

lbl_vol_2 = Label(window, text = "Desired Volume: ")
lbl_vol_2.grid(row = 8, column=1, sticky = "w")

vol_2 = Entry(window, text = vol_final)
vol_2.grid(row = 8, column = 2, sticky = "w")

mag_vol_2 = Combobox(window, width=12)
mag_vol_2["values"] = ["L", "mL", "\u03BCL" , "nL"]
mag_vol_2.grid(row= 8, column = 3, sticky = "w")
mag_vol_2.set("mL")

lbl_conc_1 = Label(window, text = "Starting Concentration: ")
lbl_conc_1.grid(row = 7, column=1)

conc_entry = Entry(window, text = conc_start)
conc_entry.grid(row = 7, column = 2, sticky = "w")

mag_conc_1 = Combobox(window, width=12)
mag_conc_1["values"] = ["mol dm\u00B3", "mmol dm\u207B\u00B3", "\u03BCmol dm\u207B\u00B3", "nmol dm\u207B\u00B3", "pmol dm\u207B\u00B3",
                        "g mL\u207B\u00B9", "mg mL\u207B\u00B9", "\u03BCg mL\u207B\u00B9", "ng mL\u207B\u00B9", "pg mL\u207B\u00B9"]
mag_conc_1.grid(row= 7, column = 3, sticky = "w")
mag_conc_1.set("mol dm\u00B3")

def update_conc_2(event):
    mag_conc_2_got = mag_conc_1.get()
    mag_conc_2.configure(text=mag_conc_2_got)
    mag_conc_2.grid(row= 9, column = 3,  sticky = "w")

mag_conc_1.bind("<<ComboboxSelected>>", update_conc_2)

lbl_dilution_show = Label(window)
lbl_dilution_show.grid(rows = 10, column = 2, columnspan = 3, sticky = "w")

def print_dilution():
    volume_2 = float(vol_2.get())
    concen_2 = float(conc_2.get())
    concen_1 = float(conc_entry.get())
    volume_1 = round((volume_2 * concen_2)/concen_1, 2)
    lbl_dilution_show.configure(text = " dilute "+str(volume_1)+" "+str(mag_vol_2.get())+" to a total volume of "+str(volume_2)+" "+str(mag_vol_2.get()))

btn_calc_2 = Button(window, text = "Volume to Dilute:", command = print_dilution)
btn_calc_2.grid(row=10, column = 1)


window.mainloop()
