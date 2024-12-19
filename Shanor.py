import random

# Paramètres 
p = 88667  
g = 70322  
q = 1031
t= 10
# Secret 
a =755

k = random.randint(0, q - 1)
b = pow(g, k, p) #on a le b un nombre calcue par alice et envoyé a bob

print("b =", b)

# Vérificateur choisit un défi aléatoire (bob), puit l'enoie a alice
r = random.randint(a, pow(2, t))

# Envoi du défi au prouveur
print("r =", r)

# Calcul de la réponse d'alice apres le defie de Bob
c = (k + a*r) % q

# Envoi de la réponse au vérificateur
print("La valeur de C est ", c)


alpha = pow(g,-a,p) #calucle de alpha pour la verfication
print("la valeur de alpha est ",alpha)
verif_b = pow(g, c, p)*pow(alpha,r,p) % p #verification de la preuve par bob
print (verif_b) #puis on va comparer les deux résultats
if verif_b == b:
    print("La preuve est valide !")
else:
    print("La preuve est invalide.")
	
