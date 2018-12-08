'''
    File name: controller.py
    Author: Maxime FELICI, Meggan ESCARTEFIGUE, Mohamed Anis BEN MAHMOUD, Zeineb LAKNECH
    Python Version: 2.7
    This class handles calls to the gphoto2 software
'''


try:
    import Tkinter as Tk # python 2
except ModuleNotFoundError:
    import tkinter as Tk # python 3

import subprocess
from os import listdir


class Controller:
    def __init__(self, model):
        self.model = model
        p = subprocess.Popen("rm -Rf tmp", stdout=subprocess.PIPE, shell=True) #Delete tmp directory
        (output, err) = p.communicate()
        p = subprocess.Popen("mkdir tmp", stdout=subprocess.PIPE, shell=True) #Create empty tmp directory
        (output, err) = p.communicate()
        self.default_tmp_path = "tmp/" #TODO change with temp dir on Linux like /tmp

    def get_iso(self):
        iso_list = []
        p = subprocess.Popen("gphoto2 --get-config=/main/imgsettings/iso", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        end_line = output.find("END")
        choice_line = output.find("Choice")
        sub_chain = output[choice_line:end_line]
        print("sub chain : " + sub_chain)

        while len(sub_chain)>10:
            sub_chain=sub_chain[sub_chain.find(" ")+1:len(sub_chain)]
            sub_chain=sub_chain[sub_chain.find(" ")+1:len(sub_chain)]
            iso = sub_chain[0:sub_chain.find("\n")]
            sub_chain = sub_chain[sub_chain.find("\n")+1:len(sub_chain)]
            try:
                if int(iso)>51200:
                    break
            except ValueError : print("")
            iso_list.append(iso)

        print iso_list
        return iso_list

    def set_iso(self, selected_iso):
        command = "gphoto2 --set-config=/main/imgsettings/iso=" + selected_iso
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()


    def get_aperture(self):
        aperture_list = []
        p = subprocess.Popen("gphoto2 --get-config=/main/capturesettings/f-number", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()

        end_line = output.find("END")
        choice_line = output.find("Choice")
        sub_chain = output[choice_line:end_line]
        print("sub chain : " + sub_chain)

        while len(sub_chain)>10:
            sub_chain=sub_chain[sub_chain.find(" ")+1:len(sub_chain)]
            sub_chain=sub_chain[sub_chain.find(" ")+1:len(sub_chain)]
            aperture = sub_chain[0:sub_chain.find("\n")]
            sub_chain = sub_chain[sub_chain.find("\n")+1:len(sub_chain)]
            aperture_list.append(aperture)

        print aperture_list
        return aperture_list


        def set_aperture(self, selected_aperture):
            command = "gphoto2 --set-config=/main/capturesettings/f-number=" + selected_aperture
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()

    def refresh_live_view_pictures(self, dir):
        if self.model != None:
            allfiles = listdir(dir)
            imgfiles = []

            print allfiles

            for file in allfiles:
                if file.lower().endswith('.png') or file.lower().endswith('.jpg'):
                    imgfiles.append(file)
            self.model.set_live_view_pictures(imgfiles)
            print imgfiles

    def take_picture(self):
        #TODO: set the output file
        #TODO: temp dir: self.default_tmp_path+"/img1.jpg"
        cmd = "gphoto2 --capture-image-and-download --filename tmp/"


        allfiles = listdir(self.default_tmp_path)
        imgfiles = []

        print allfiles

        for file in allfiles:
            if file.lower().endswith('.png') or file.lower().endswith('.jpg'):
                imgfiles.append(file)

        nb = len(imgfiles)

        cmd = cmd + str(nb+1) + ".png"


        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()

        self.refresh_live_view_pictures(self.default_tmp_path)

        rtrn = str(nb+1) + ".png"

        return rtrn #TODO: return the name

    def info_function(self):
        pass
