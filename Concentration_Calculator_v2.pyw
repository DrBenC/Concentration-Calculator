"""
A simple calculator which imports compound data (name, molar mass, density) and can calculate how much is needed to make up desired concentrations
"""

import glob
import os
import numpy as np
from tkinter import *
from tkinter.ttk import Combobox

#this is used to store the chemical information
class Species(object):
    def __init__(self, name, mass, density):
        self.name = name
        self.mass = mass
        self.density = density

#first we ensure that a species.txt is present - and if not, we create one with two entries (any fewer and numpy freaks out)
def file_check():
    try:
        f = open("species.txt")
    except FileNotFoundError:
        f = open("species.txt", "w+")
        f.write("SodiumChloride,58.44,SOLID")
        f.write("\nPotassiumChloride,74.55,SOLID")
    f.close()

file_check()      

#imports data from species.txt!
def import_data():
    
    #we clear the list for when we add new instances
    del chemicals_list[0:len(chemicals_list)]
    species_info = np.loadtxt("species.txt", dtype=str, delimiter = ",")
      
    for i in species_info:
        n = Species(i[0], i[1], i[2])
        chemicals_list.append(n)

#we declare a list of species objects, and then import data into it
global chemicals_list
chemicals_list = []

import_data()

#begins window
window = Tk()

window.title("Concentration Calculator")
window.geometry("440x340")

#some values have to be declared ahead of usage
vol_var = StringVar()
conc_var = StringVar()
vol_var.set(float(1))
conc_var.set(float(1))
global mass
mass= 0

#this section is for the simple concentration calculations
title_molarity = Label(window, text = "For making a new solution: ", bg = "green", width = 65)
title_molarity.grid(row=1, column =1, columnspan = 5)

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

#this event is triggered when the species combobox (below) is used to select a species
def update_molar_mass(event):
    #picks the species being used currently and compares to all chemicals
    spec_used = combo_species.get()
    for i in chemicals_list:
        if i.name == spec_used:
            #it updates the global density and mass values 
            global density
            density = i.density
            global mass            
            mass = float(i.mass)
            #and it updates a label
            mass_text = "Molar Mass: "+str(mass)+" Da"
            lbl_molar_mass.configure(text=str(mass)+" Da")

#This is the combobox which uses the above function
combo_species = Combobox(window)
combo_species["values"] = [i.name for i in chemicals_list]
combo_species.grid(row = 2, column = 2, padx = 1, sticky = "w")
combo_species.bind("<<ComboboxSelected>>", update_molar_mass)

#this occurs when the 'calculate' button is clicked
def print_mass():
    update_molar_mass
    name_show = combo_species.get()
    volume = float(vol.get())  
    conc_f = float(conc.get())
    moles = conc_f * (volume)

    global mass
    mass_calc = (moles)*float(mass)
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
    global density
    if density == "SOLID":
        lbl_mass.configure(text = " "+str(mass_print)+str(units[units_p])+"g "+str(combo_species.get()))
        
    else:
        density_print = float(density)
        vol_print =round(mass_print/density_print)
        lbl_mass.configure(text = " "+str(mass_print)+str(units[units_p])+"g ("+str(vol_print)+" "+units[units_p+1]+"L ) "+str(name_show))

#finally the calculate button is added
btn_calc = Button(window, text = "Amount Required:", command = print_mass)
btn_calc.grid(row=5, column = 1)

#now we add the section for the dilution calculator

#again, starting with variables we will need later on
conc_final = StringVar()
conc_final.set(float(1))
conc_start = StringVar()
conc_start.set(float(1))
vol_final = StringVar()
vol_final.set(float(1))

#we set out the middle section of the GUI
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

#this is a mess but it works, so screw it
def print_dilution():
    
    volume_2 = float(vol_2.get())
    concen_2 = float(conc_2.get())
    concen_1 = float(conc_entry.get())
    volume_1 = round((volume_2 * concen_2)/concen_1, 2)
    lbl_dilution_show.configure(text = " dilute "+str(volume_1)+" "+str(mag_vol_2.get())+" to a total volume of "+str(volume_2)+" "+str(mag_vol_2.get()))

btn_calc_2 = Button(window, text = "Volume to Dilute:", command = print_dilution)
btn_calc_2.grid(row=10, column = 1)

#final section is adding to the species list!
new_name = StringVar()
new_name.set("Chemical Name")
new_mass = StringVar()
new_mass.set(float(1))
new_density = StringVar()
new_density.set(float(1))
solid = IntVar()

lbl_master_add = Label(window, text="Adding a new chemical to the list: ", bg = "green", width = 65)
lbl_master_add.grid(row=11, column = 1, columnspan = 5)

lbl_name_1 = Label(window, text ="Chemical Name: ")
lbl_name_1.grid(row=12, column = 1, sticky = "w")

name_new = Entry(window, text = new_name)
name_new.grid(row=12, column = 2, sticky = "w")

lbl_mass_new = Label(window, text = "Molar Mass: ")
lbl_mass_new.grid(row = 13, column=1, sticky = "w")

mass_new = Entry(window, text = new_mass)
mass_new.grid(row = 13, column = 2, sticky = "w")

lbl_density_new = Label(window, text = "Density: ")
lbl_density_new.grid(row = 14, column=1, sticky = "w")

density_new = Entry(window, text = new_density)
density_new.grid(row = 14, column = 2, sticky = "w")

density_check = Checkbutton(window, text="Solid", variable=solid).grid(row=12, column=3, sticky ="w")

lbl_density_warning = Label(window, text = "Leave at 1.0 if Solid").grid(row=14, column=3, sticky="w")

lbl_feedback_add = Label(window, text =" ")
lbl_feedback_add.grid(row=15, column = 2, sticky = "w", columnspan = 5)

#this function imports the data in the entry boxes
def add_species():
    name_raw = str(name_new.get())
    name_input = name_raw.replace(",", "")
    
    mass = float(mass_new.get())
    density = float(density_new.get())
    if density == " " or density == "":
        density = 1.0
    solid_new = solid.get()
    
    names_current = [n.name for n in chemicals_list]
    
    if type(name_input) == str and type(mass) == float and name_input not in names_current:
        if type(density) == float and solid_new == False:
            f = open("Species.txt", "a+")
            f.write("\n"+str(name_input)+","+str(mass)+","+str(density))
            f.close()
            lbl_feedback_add.configure(text=name_input+" added to species.txt.")
        if solid_new == True:
            f = open("Species.txt", "a+")
            f.write("\n"+str(name_input)+","+str(mass)+","+"SOLID")
            f.close()
            lbl_feedback_add.configure(text=name_input+" added to species.txt.")
        #here we update everything so it's immediately usable
        import_data()
        update_molar_mass
        combo_species["values"] = [i.name for i in chemicals_list]
    #This should result in nothing user-side.        
    else:
        print("Error")
        

        
        
btn_add_species = Button(window, text = "Add Species", command = add_species)
btn_add_species.grid(row=15, column = 1)

window.mainloop()
