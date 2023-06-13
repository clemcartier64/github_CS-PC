'''
Mariotte Mélanie
Réalisez un script montrant l’utilisation d’un tube anonyme (pipe) entre deux processus
12/05/2023
'''
#sort text | grep toto | wc -l #indique le nombre de fois que le mot 'toto' apparaît dans le fichier 'texte'

#cat fichier | wc
'''
import os,sys
(dfr,dfw) = os.pipe()
pid = os.fork()
if pid == 0: 
    os.close(dfw)
    os.dup2(dfr,0)
    os.close(dfr)
    os.execlp("wc", "wc")
else: 
    os.close(dfr)
    os.dup2(dfw,1)
    os.close(dfw)
    os.execlp("cat", "cat", "text") 
sys.exit(0)
'''

#sort < fichier | grep chaine | tail –n 5 > sortie
import os, sys

(r_sort_grep, w_sort_grep) = os.pipe()
(r_grep_tail, w_grep_tail) = os.pipe()

pid = os.fork()
if pid == 0 :
    sortie = os.open("sortie", os.O_WRONLY | os.O_CREAT, 0o64)

    os.dup2(sortie, 1)
    os.close(sortie)

    os.close(w_grep_tail)
    os.close(w_sort_grep)
    os.close(r_sort_grep)

    os.dup2(r_grep_tail , 0)
    os.close(r_grep_tail)
    os.execlp("tail", "tail", "-n 5")
else:
    pid2 = os.fork()
    if pid2 == 0 :
        os.dup2(r_sort_grep,0)
        os.close(r_sort_grep)
        
        os.dup2(w_grep_tail,1)
        os.close(w_grep_tail)

        os.close(r_grep_tail)
        os.close(w_sort_grep)

        os.execlp("grep", "grep", "chaine")
    else:
        fic = os.open("text", os.O_RDONLY)
        os.dup2(fic,0)
        os.close(fic)

        os.close(r_sort_grep)

        os.close(r_grep_tail)
        os.close(w_grep_tail)

        os.dup2(w_sort_grep, 1)
        os.close(w_sort_grep)

        os.execlp("sort", "sort")



