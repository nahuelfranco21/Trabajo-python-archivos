import csv
import sys
import os

TOMATE = "T"
BROCOLI = "B"
ZANAHORIA = "Z"
LECHUGA = "L"

ARCHIVO_PEDIDOS = "pedidos.csv"
ARCHIVO_CLIENTES = "clientes.csv"
ARCHIVO_AUXILIAR = "auxiliar.csv"
MODO_LECTURA = "r"
MODO_ESCRITURA = "a"
SEPARADOR = ";"
MODO_ESCRITURA_MODIFICAR = "w"
MODO_ESCRITURA_ELIMINAR = "w"

ID_PEDIDO = 0
VERDURA = 1
CANTIDAD = 2

CANT_ARGUMENTOS_AGREGAR = 5
CANT_ARGUMENTOS_MODIFICAR = 5
CANT_ARGUMENTOS_ELIMINAR = 3
MIN_CANT_ARGUMENTOS_LISTAR = 2
MAX_CANT_ARGUMENTOS_LISTAR = 3

AGREGAR = "agregar"
MODIFICAR = "modificar"
ELIMINAR = "eliminar"
LISTAR = "listar"

#Pre: 
#Post: Verifica que la cantidad de argumentos de la linea de comandos sea incorrecta devuelve true si lo es
def argumentos_invalidos(longitud_1 , longitud_2):
	return (len(sys.argv) < longitud_1 or len(sys.argv) > longitud_2)

#Pre: tiene que existir el archivo
#Post: Devuelve el id del ultimo pedido
def ultimo_id():

	try:
		pedidos = open(ARCHIVO_PEDIDOS, MODO_LECTURA)
		reader = csv.reader(pedidos, delimiter=SEPARADOR)
	except:
		print("No se pudo abrir el archivo")
		return

	id_final = 0

	for linea in reader:
		id_final = int(linea[ID_PEDIDO])

	pedidos.close()

	return id_final

#Pre: tiene que existir el archivo
#Post: se encargar de buscar un id especifico, si lo encuentra devuelve true
def buscar_id_en_archivo(id_del_pedido: int):

	try:
		clientes = open(ARCHIVO_CLIENTES, MODO_LECTURA)
	except:
		print("No se pudo abrir el archivo")
		return

	reader = csv.reader(clientes, delimiter=SEPARADOR)

	for buscar_id in reader:
		if (id_del_pedido == int(buscar_id[ID_PEDIDO])):
			clientes.close()
			return True

	clientes.close()
	return False

#Pre:
#Post: Se crea el archivo y guarda los datos ingresados
def agregar_a_pedidos(cantidad_verduras: int, tipo_verdura: str, nombre: str):

	vector_verduras = [TOMATE,BROCOLI,ZANAHORIA,LECHUGA]

	try:
		pedidos = open(ARCHIVO_PEDIDOS, MODO_ESCRITURA)
	except:
		print("No se pudo abrir el archivo.")
		return

	numero_id = ultimo_id()
	numero_id += 1

	escribir_pedidos = csv.writer(pedidos,delimiter = SEPARADOR)

	if(cantidad_verduras > 0 and tipo_verdura in vector_verduras):
		vector = [numero_id,tipo_verdura,cantidad_verduras]
		escribir_pedidos.writerow(vector)
		print("Se agrego con exito!")
	else:
		print("Ingresaste mal un dato, fijate")

	pedidos.close()

#Pre:
#Post: Se gaurdar los datos tales como el id y el nombre al archivo de clientes
def agregar_a_clientes(tipo_verdura: str ,nombre: str):

	vector_verduras = [TOMATE,LECHUGA,ZANAHORIA,BROCOLI]

	try:
		clientes = open(ARCHIVO_CLIENTES, MODO_ESCRITURA)
	except:
		print("No se pudo abrir el archivo.")
		return

	id_final = ultimo_id()
	if(tipo_verdura in vector_verduras and id_final > 0):
		escribir_clientes = csv.writer(clientes,delimiter = SEPARADOR)
		vector = [id_final,nombre]
		escribir_clientes.writerow(vector)

	clientes.close()

#Pre:
#Post: Se agregan los datos a los archivos
def agregar():

	if (argumentos_invalidos(CANT_ARGUMENTOS_AGREGAR,CANT_ARGUMENTOS_AGREGAR)):
		print("Error, le erraste en la cantidad de argumentos")
		return 0

	cantidad_verduras = int(sys.argv[2])
	tipo_verdura = str(sys.argv[3])
	nombre = str(sys.argv[4])

	agregar_a_pedidos(cantidad_verduras,tipo_verdura,nombre)
	agregar_a_clientes(tipo_verdura,nombre)

#Pre: 
#Post: El archivo necesita cumplir ciertas reglas para modificarse, si se cumplen, se modifica lo correspondiente
def modificar_pedidos(id_del_pedido: int, cantidad_verduras: int, tipo_verdura: str):

	vector_verduras = [TOMATE,BROCOLI,ZANAHORIA,LECHUGA]

	try:
		pedidos = open(ARCHIVO_PEDIDOS, MODO_LECTURA)
	except:
		print("No se pudo abrir el archivo de pedidos.")
		return

	try:
		auxiliar = open(ARCHIVO_AUXILIAR, MODO_ESCRITURA_MODIFICAR)
	except:
		pedidos.close()
		print("No se pudo abrir el archivo auxiliar.")
		return

	leer_pedidos = csv.reader(pedidos, delimiter = SEPARADOR)
	escribir_en_auxiliar = csv.writer(auxiliar, delimiter = SEPARADOR)

	for linea in leer_pedidos:
		if(int(linea[ID_PEDIDO]) == id_del_pedido and cantidad_verduras > 0 and tipo_verdura in vector_verduras):
			if(tipo_verdura == linea[VERDURA]):
				nueva_cantidad = cantidad_verduras
				vector_nuevo = [id_del_pedido,tipo_verdura,nueva_cantidad]
				escribir_en_auxiliar.writerow(vector_nuevo)
			else:
				vector = [id_del_pedido,tipo_verdura,cantidad_verduras]
				escribir_en_auxiliar.writerow(linea)
				escribir_en_auxiliar.writerow(vector)
		else:
			escribir_en_auxiliar.writerow(linea)

	pedidos.close()
	auxiliar.close()

	os.rename(ARCHIVO_AUXILIAR,ARCHIVO_PEDIDOS)

#Pre: Necesito la cantidad de argumentos correspondientes
#Post: Modifica el archivo correspondiente
def modificar_archivos():

	if (argumentos_invalidos(CANT_ARGUMENTOS_MODIFICAR,CANT_ARGUMENTOS_MODIFICAR)):
		print("Error, le erraste en la cantidad de argumentos")
		return 0

	id_del_pedido = int(sys.argv[2])
	cantidad_verduras = int(sys.argv[3])
	tipo_verdura = str(sys.argv[4])

	id_buscado = buscar_id_en_archivo(id_del_pedido)

	if(id_buscado):
		modificar_pedidos(id_del_pedido, cantidad_verduras, tipo_verdura)
		print("Se pudo modificar con exito!")
	else:
		print("No se pudo modificar, fijate capaz ingresaste mal el id")

#Pre: TIene que existir el id ingresado
#Post: Elimina el pedido segun el id
def eliminar_en_pedidos(id_del_pedido: int):

	try:
		pedidos = open(ARCHIVO_PEDIDOS, MODO_LECTURA)
	except:
		print("No se pudo abrir el archivo de pedidos.")
		return

	try:
		auxiliar = open(ARCHIVO_AUXILIAR, MODO_ESCRITURA_ELIMINAR)
	except:
		pedidos.close()
		print("No se pudo abrir el archivo auxiliar.")
		return

	leer_pedidos = csv.reader(pedidos, delimiter = SEPARADOR)
	escribir_en_auxiliar = csv.writer(auxiliar, delimiter = SEPARADOR)

	for linea in leer_pedidos:
		if(int(linea[ID_PEDIDO]) != id_del_pedido):
			escribir_en_auxiliar.writerow(linea)

	pedidos.close()
	auxiliar.close()

	os.rename(ARCHIVO_AUXILIAR,ARCHIVO_PEDIDOS)

#Pre: Tiene que existir el id ingresado
#Post: Elimina el pedido segun el id
def eliminar_en_clientes(id_del_pedido: int):

	try:
		clientes = open(ARCHIVO_CLIENTES, MODO_LECTURA)
	except:
		print("No se pudo abrir el archivo de pedidos.")
		return

	try:
		auxiliar = open(ARCHIVO_AUXILIAR, MODO_ESCRITURA_ELIMINAR)
	except:
		clientes.close()
		print("No se pudo abrir el archivo auxiliar.")
		return

	leer_clientes = csv.reader(clientes, delimiter = SEPARADOR)
	escribir_en_auxiliar = csv.writer(auxiliar, delimiter = SEPARADOR)

	for linea in leer_clientes:
		if(int(linea[ID_PEDIDO]) != id_del_pedido):
			escribir_en_auxiliar.writerow(linea)

	clientes.close()
	auxiliar.close()

	os.rename(ARCHIVO_AUXILIAR,ARCHIVO_CLIENTES)

#Pre: 
#Post: Se encarga de eliminar lo indicado de ambos archivos
def eliminar():

	if (argumentos_invalidos(CANT_ARGUMENTOS_ELIMINAR,CANT_ARGUMENTOS_ELIMINAR)):
		print("Error pibe, le erraste a la cantidad de argumentos")
		return 0

	id_del_pedido = int(sys.argv[2])

	id_buscado = buscar_id_en_archivo(id_del_pedido)

	if (len(sys.argv) == 3 and id_buscado):
		eliminar_en_clientes(id_del_pedido)
		eliminar_en_pedidos(id_del_pedido)
		print("Se elimino correctamente")
	else:
		print("No existe el ID que ingresaste")
		return

#Pre: El archivo tiene que estar creado y con informacion
#Post: Lista los pedidos de todos los archivos
def listar_todos_pedidos():

	try:
		pedidos = open(ARCHIVO_PEDIDOS, MODO_LECTURA)
	except:
		print("No se pudo abrir el archivo")


	lectura = csv.reader(pedidos,delimiter=SEPARADOR)
	print("Aca va la lista de todos los pedidos:\n")
	for linea in lectura:
		print(f"Numero id: {linea[ID_PEDIDO]}, El tipo de verdura es: {linea[VERDURA]} y la cantidad es: {linea[CANTIDAD]}")

	pedidos.close()

#Pre: Tiene que existir el id ingresado
#Post: Lista los datos segun el id
def listar_por_id(id_buscado: int):

	try:
		pedidos = open(ARCHIVO_PEDIDOS, MODO_LECTURA)
		lectura = csv.reader(pedidos,delimiter=SEPARADOR)
	except:
		print("No se pudo abrir el archivo")

	print("Aca va la lista de todos los pedidos con ese id:\n")
	for linea in lectura:
		if (id_buscado == int(linea[ID_PEDIDO])):
			print(f"Numero id: {linea[ID_PEDIDO]}, El tipo de verdura es: {linea[VERDURA]} y la cantidad son: {linea[CANTIDAD]}")

	pedidos.close()

#Pre:
#Post: dependiendo la cantidad de argumentos lista toda la informacion, o segun su ID
def listar():

	if (argumentos_invalidos(MIN_CANT_ARGUMENTOS_LISTAR,MAX_CANT_ARGUMENTOS_LISTAR)):
		print("Error pibe, le erraste a la cantidad de argumentos")
		return 0

	id_del_pedido = int(sys.argv[2])

	id_a_buscar = buscar_id_en_archivo(id_del_pedido)

	if (len(sys.argv) == 3 and id_a_buscar):
		listar_por_id(id_del_pedido)
	elif (len(sys.argv) == 2):
		listar_todos_pedidos()
	else:
		print("No existe el ID ingresado")


def main():
	palabra = str(sys.argv[1])

	if (palabra == AGREGAR):
		agregar()
	elif (palabra == MODIFICAR):
		modificar_archivos()
	elif (palabra == ELIMINAR):
		eliminar()
	elif (palabra == LISTAR):
		listar()
	else:
		print("Ingresaste mal la palabra")
		return 0

if __name__ == "__main__":
	main()