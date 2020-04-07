frase = input("Ingrese una palabra o frase: ")

frase_set = set(frase)
frase_set.discard(" ")

caracteres = []

print()

for chara in frase_set:
	cant_apariciones = frase.count(chara)
	caracteres.append((chara, cant_apariciones))

caracteres_primos = []
	
for elem in caracteres:
	print("La cantidad de veces que aparece la letra ", elem[0], " es de ", elem[1])
	if (elem[1] > 1):
		divisor = 2
		es_primo = True
		while (es_primo) and (divisor < elem[1]):
			if (elem[1] % divisor) == 0:
				es_primo = False
			divisor += 1
		if (es_primo):
			caracteres_primos.append(elem)

print()

for chara_primo in caracteres_primos:
	print("El caracter %s ha aparecido %s veces y, por lo tanto, es primo." % (chara_primo[0], chara_primo[1]))
