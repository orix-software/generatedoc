#!/usr/bin/python3
# -*- coding: utf8 -*-
# Initial version : from ch376lib

from __future__ import print_function

from pprint import pprint

import fileinput
import sys

def transform(content):
    line_out_all = ''
    #
    # Configuration
    #
    var_types = {
        '.addr': 'unsigned int',
        '.byte': 'char',
        '.byt': 'char',
        '.word': 'int',
        '.dword': 'double',
        '.res': 'char',
        '.asciiz': 'const char'
        }

    extern_is_fn = True
    #macro_dcl = 'inline macro'
    macro_dcl = '#define'
    # equ_dcl = '#define'
    equ_dcl = 'const char'

    #
    # Pas de modifications au delÃ  de cette limite
    #
    def_bloc = False
    def_cbloc = False

    # TESTS
    def_chrisbloc = False

    def_struct = False
    struct_name = ''
    def_proc = False
    proc_name = ''
    def_macro = False


    last_label = ''
    line_out = ''
    lines = content.splitlines()
    for line in lines:
        line_out = ''
        line = line.rstrip()

        #if fileinput.isfirstline():
        #    fname = fileinput.filename()
        #    print('\n'.join(['/**', ' * @file '+fname, '*/']))

        if line:
            inst = line.split()
            nb_inst = len(inst)

            line_out = ''

            # pprint(inst)
            if def_bloc:
                if inst[0] == ';;':
                    def_bloc = False
                    line_out = ''.join(inst[1:])

                else:
                    line_out = line[1:]

                    # Au cas oÃ¹ il manque un ' ' entre le ';' et le commentaire
                    #if len(inst[0]) > 1 and inst[0][1] == ';':
                    #    line_out += inst[0][1:]
                    #    print('----', line)

                    #if nb_inst > 1:
                    #    line_out += ' '.join(inst[1:])

            elif def_cbloc:
                line_out = ''

                if inst[0] == '*/':
                    def_cbloc = False

            elif def_chrisbloc:
                line_out = ''

                if len(line) > 1:
                    line_out = ''

                if inst[0] == ';' and nb_inst > 1 and inst[1][:2] == '==':
                    def_chrisbloc = False
                    line_out = ''

            elif def_proc:
                if inst[0] == '.endproc':
                    def_proc = False

                    proc_name = ''
                    line_out = '\n'

                elif inst[0] == ';;@bug':
                    line_out = '!!! bug "' + ' '.join(inst[1:]) + '"'

                elif inst[0] == ';;@proto':
                    line_out = '## '+ ' '.join(inst[1:])
                    line_out = line_out + '\n'

                elif inst[0] == ';;@brief':
                    line_out = '***Description***\n\n'+ ' '.join(inst[1:])
                    line_out = line_out + '\n'

                elif ';;@input' in inst[0]:
                    if def_input_found == False:
                        line_out = '***Input***\n\n'
                        def_input_found == True
                    else:
                        line_out = ""

                    if inst[0] == ';;@inputPARAM':
                        param = inst[0] .split('_')
                        line_out = line_out + '*' +  param[1] +' : '+inst[1] +' ' + ' '.join(inst[2:])

                elif inst[0] == ';;@param':
                    line_out = '* '+ '*'+inst[1] +'* ' + ' '.join(inst[2:])

                elif inst[0] == ';;@returns':
                    line_out = '***Returns***\n\n'+ '' + inst[1] +' ' + ' '.join(inst[2:])

                # Appel Ã  une fonction
                elif inst[0].lower() == 'jsr':
                    line_out = ''

                # [--- TEST
                # DÃ©claration d'une zone mÃ©moire
                elif last_label and inst[0] in var_types:
                    if inst[0] in ['.byte', '.byt']:

                        line_out = ''

                        var_len = inst[1].count(',') + 1
                        if var_len > 1:
                            line_out += ''

                        line_out += ''

                    elif inst[0] == '.word':
                        line_out = var_types['.word'] + ' ' + last_label

                        var_len = inst[1].count(',')+1
                        if var_len > 1:
                            line_out += ''

                        line_out += ''

                    elif inst[0] == '.addr':
                        line_out = var_types['.addr'] + ' ' + last_label

                        var_len = inst[1].count(',')+1
                        if var_len > 1:
                            line_out += ''

                        line_out += ''

                    elif inst[0] == '.dword':
                        line_out = var_types['.dword']+' ' + last_label

                        var_len = inst[1].count(',') + 1
                        if var_len > 1:
                            line_out += ''

                        line_out += ''

                    elif inst[0] == '.res':
                        line_out = ''

                    elif inst[0] == '.asciiz':
                        init = ' '.join(inst[1:])
                        # -2 Ã  cause des "",  +1 Ã  cause du \00 final
                        var_len = len(init) - 2 + 1
                        line_out = ''

                    else:
                        line_out = ''

                    last_label = ''

                elif nb_inst == 1:
                    # Label?
                    # Pas d'espace avant un label
                    if not line[0] in [' ', '.', ';', '@', '\t']:
                        if inst[0][-1] == ':':
                            last_label = inst[0][:-1]
                            line_out = ''

                        else:
                            last_label = inst[0]
                            line_out = ''
                # --]
                else:
                    # On ne prend rien en compte dans la fonction
                    # TODO: Ajouter la prise en charge des variables et les dÃ©clarer privÃ©es?
                    #Â line_out = '????: '+line
                    if line[0] !=';':
                        last_label = ''

                    line_out = ''

            elif def_struct:
                if inst[0] == '.endstruct':
                    def_struct = False

                    line_out = ''

                else:
                    # Traitement des membres de la structure
                    if nb_inst >= 2 and inst[1].lower() in var_types:
                        inst[1] = inst[1].lower()
                        cmnt = ''

                        if inst[1] in ['.byte', '.byt']:
                            line_out = ''

                            if nb_inst > 3:
                                cmnt = ' '.join(inst[3:])

                        elif inst[1] == '.word':
                            line_out = ''

                            if nb_inst > 3:
                                cmnt = ' '.join(inst[3:])

                        elif inst[1] == '.addr':
                            line_out = ''

                            if nb_inst > 3:
                                cmnt = ' '.join(inst[3:])

                        elif inst[1] == '.dword':
                            line_out = ''

                            if nb_inst > 3:
                                cmnt = ' '.join(inst[3:])

                        elif inst[1] == '.res':
                            # VÃ©rifier  si inst[3] == ';' au cas oÃ¹?

                            line_out = ''

                            if nb_inst > 4:
                                cmnt = ' '.join(inst[4:])

                        else:
                            line_out = ''

                        if line_out and cmnt:
                            # line_out = '/** '+cmnt+' */ '+line_out
                            line_out += ''

            elif def_macro:
                line_out = ''
                if inst[0] == '.endmacro':
                    def_macro = False

                    if macro_dcl !='#define':
                        line_out = ''

            else:
                if inst[0] == ';;':
                    def_bloc = True

                    line_out = ''
                    if nb_inst >=2:
                        if inst[1] == '/**':
                            inst[1] = ''

                        line_out += ''

                elif inst[0] in ['/*', '/**']:
                    def_cbloc = True
                    #line_out = line

                elif inst[0] == ';' and nb_inst > 1 and inst[1][:2] == '==':
                    def_chrisbloc = True
                    line_out = ''

                elif inst[0] == '.proc':
                    def_proc = True
                    def_input_found = False
                    def_returns_found = False

                    # Ne prend pas en compte un Ã©ventuel commentaire sur la ligne .proc
                    # TODO: Ajouter un @brief pour le prendre en compte?
                    proc_name = inst[1]
                    if not proc_name[0] == '_':
                        #line_out = "## " + proc_name + '\n'
                    #else:
                        def_proc = False


                elif inst[0] == '.struct':
                    def_struct = True

                    # Ne prend pas en compte un Ã©ventuel commentaire sur la ligne .proc
                    # TODO: Ajouter un @brief pour le prendre en compte?
                    struct_name = inst[1]

                    #line_out = 'typedef struct {'

                elif inst[0] == ';;@param':
                    line_out = ''

                elif inst[0] == '.macro':
                    def_macro = True

                    #line_out = macro_dcl + ' ' + inst[1] +'('

                    if nb_inst > 2:
                        if macro_dcl != '#define':
                            line_out += ''
                        else:
                            line_out += ''

                    line_out += ''
                    if macro_dcl != '#define':
                        line_out += ''

                elif inst[0] == '.define':
                    # ATTENTION: un commentaire Ã  la fin de la ligne peut poser problÃ¨me
                    if nb_inst > 3 and inst[3] == ';':
                        line_out = ''
                        line_out += ''

                    else:
                        line_out = ''

                elif inst[0] == '.include':
                    # Pas de prise en compte d'un Ã©ventuel commentaire en fin de ligne
                    # TODO: A prende en compte?
                    line_out = ''

                elif inst[0] == '.tag':
                    line_out = '%s %s;' % (inst[1], last_label)

                elif inst[0] == '.import':
                    if extern_is_fn:
                        line_out = ''

                    else:
                        line_out = ''


                # DÃ©claration d'une zone mÃ©moire
                elif last_label and inst[0].lower() in var_types:
                    inst[0] = inst[0].lower()
                    if inst[0] in ['.byte', '.byt']:

                        line_out = ''

                        var_len = inst[1].count(',')+1
                        if var_len > 1:
                            line_out += ''

                        line_out += ''

                    elif inst[0] == '.word':
                        line_out = var_types['.word']+' '+last_label

                        var_len = inst[1].count(',')+1
                        if var_len > 1:
                            line_out += ''

                        line_out += ''

                    elif inst[0] == '.addr':
                        line_out = var_types['.addr']+' '+last_label

                        var_len = inst[1].count(',')+1
                        if var_len > 1:
                            line_out += ''

                        line_out += ''

                    elif inst[0] == '.dword':
                        line_out = var_types['.dword']+' '+last_label

                        var_len = inst[1].count(',')+1
                        if var_len > 1:
                            line_out += ''

                        line_out += ''

                    elif inst[0] == '.res':
                        line_out = ''


                    elif inst[0] == '.asciiz':
                        init = ' '.join(inst[1:])
                        # -2 Ã  cause des "",  +1 Ã  cause du \00 final
                        var_len = len(init)-2+1
                        line_out = var_types['.asciiz']+' %s[%s] = %s;' % (last_label, var_len, init)

                    else:
                        line_out = ''

                    last_label = ''

                elif nb_inst == 1:
                    # Label?
                    # Pas d'espace avant un label
                    if not line[0] in [' ', '.', ';', '@', '\t']:
                        if inst[0][-1] == ':':
                            last_label = inst[0][:-1]
                            line_out = ''

                        else:
                            last_label = inst[0]
                            line_out = ''


                elif nb_inst >= 3:
                    # DÃ©claration d'une variable / label
                    if inst[1] in ['=', ':=']:
                        if nb_inst > 3 and inst[3] == ';':
                            line_out = ''

                            if equ_dcl == '#define':
                                line_out += ''
                            else:
                                line_out += ''

                        else:
                            if equ_dcl == '#define':
                                line_out = ''
                            else:
                                line_out = ''

                    #elif inst[1] == ':=':
                    #    if nb_inst > 3 and inst[3] == ';':
                    #        line_out = '/** ' + ' '.join(inst[4:]) + ' */ '
                    #        line_out += '#define ' + inst[0] + ' ' + inst[2]

                    #    else:
                    #        line_out = '#define '+inst[0] + ' ' + ' '.join(inst[2:])

                    elif inst[1] == ';':
                        if inst[0][-1] == ':':
                            last_label = inst[0][:-1]
                        else:
                            last_label = inst[0]

                        # Ne marche pas, il faudrait connaitre la ligne suivante
                        # pour savoir si le commentaire se rapporte Ã  elle
                        # line_out = '/** ' + ' '.join(inst[2:]) + ' */'

                    else:
                        line_out = ''

                    if inst[0][0] not in ['.', ';']:
                        last_label = ''

                else:
                    #Â line_out = '????: '+line
                    if line[0] !=';':
                        last_label = ''
                    line_out = ''
        line_out_all += line_out
    return line_out_all



path_to_file = ""
filename = ""


if len(sys.argv) != 3:
    filename = fileinput.input()
    line_out = transform(filename)
else:
    filename = sys.argv[1]
    path_to_file = sys.argv[2]

    try:
        with open(filename, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filename}' n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    line_out = transform(content)

if len(line_out) != 0:
    if path_to_file != "":
        try:
        # Écriture de "toto" dans le fichier spécifié
            with open(path_to_file, 'w') as file:
                file.write(line_out)
                print(f"'Write into  : {path_to_file}")
        except Exception as e:
            print(f"Write error : {e}")
            sys.exit(1)
    else:
        print(line_out)


