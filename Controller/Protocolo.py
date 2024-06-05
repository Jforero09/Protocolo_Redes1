class Protocolo:
    def __init__(self):
        self.contador_tramas = 0
        self.contador_trama_datos = 1
        self.mensaje_transmitir = []
        self.tramas_enviadas = []
        self.tramas_recibidas = []
        self.delimitador = '10101010'
        self.mensaje_recibido = ''
        self.solicitud_permiso = {
            'delimitador_inicial': '10101010',
            'cof': 0,
            'fin': 0,
            'sol': 1,
            'ctr': 1,
            'per': 0,
            'num': 0,
            'data': '',
            'delimitador_final': '10101010'
        }
        self.permiso_concedido = {
            'delimitador_inicial': '10101010',
            'cof': 0,
            'fin': 0,
            'sol': 0,
            'ctr': 1,
            'per': 1,
            'num': 0,
            'data': '',
            'delimitador_final': '10101010'
        }


    def crear_trama(self, delimitador_inicial, cof, fin, sol, ctr, per, num, data, delimitador_final):
        if delimitador_inicial != self.delimitador or delimitador_final != self.delimitador:
            return "Los delimitadores son incorrectos, deben ser 10101010"
        else:
            return {
                'delimitador_inicial': delimitador_inicial,
                'cof': cof,
                'fin': fin,
                'sol': sol,
                'ctr': ctr,
                'per': per,
                'num': num,
                'data': data,
                'delimitador_final': delimitador_final
            }

    def enviar_trama(self, trama):
        if (trama == self.solicitud_permiso and len(self.tramas_enviadas) == 0):
            print("Enviando solicitud de permiso")
            self.tramas_enviadas.append(trama)
            self.contador_tramas += 1
            mensaje = "Trama " + str(self.contador_tramas) + ": (TX) \nControl, solicitud permiso para transmitir"
            return mensaje
        if (len(self.tramas_recibidas) > 0 and
            self.tramas_recibidas[0] == self.permiso_concedido and
            trama['cof'] == 0 and trama['sol'] == 0 and
            trama['ctr'] == 0 and trama['per'] == 0 and trama['fin'] == 0 and
            trama['data'] == self.mensaje_transmitir[trama['num']-1] and
            trama['num'] == 1):
            print("Enviando trama de datos después de recibir el permiso")
            self.tramas_enviadas.append(trama)
            self.contador_tramas += 1
            mensaje = "Trama " + str(self.contador_tramas) + ": (TX) \nDatos, Trama " + str(self.contador_trama_datos)
            return mensaje
        if (len(self.tramas_enviadas) > 0 and
            self.tramas_enviadas[0] == self.solicitud_permiso and
            trama['cof'] == 0 and trama['sol'] == 0 and trama['ctr'] == 0 and trama['per'] == 0 and trama['fin'] == 0 and
            trama['data'] == self.mensaje_transmitir[trama['num'] - 1] and
            trama['num'] < len(self.mensaje_transmitir) and
            trama['num'] > 1 and
            self.tramas_recibidas[-1]['cof'] == 1 and self.tramas_recibidas[-1]['ctr'] == 1 and
            self.tramas_recibidas[-1]['data'] == self.tramas_enviadas[-1]['data']):
            print("Enviando trama de datos secuenciales")
            self.tramas_enviadas.append(trama)
            self.contador_tramas += 1
            mensaje = "Trama " + str(self.contador_tramas) + ": (TX) \nDatos, Trama " + str(self.contador_trama_datos)
            return mensaje
        if (len(self.tramas_enviadas) > 0 and trama['cof'] == 0 and trama['sol'] == 0 and trama['ctr'] == 0 and trama['per'] == 0 and
            trama['fin'] == 1 and
            trama['data'] == self.mensaje_transmitir[trama['num'] - 1] and
            trama['num'] == len(self.mensaje_transmitir) and
            self.tramas_enviadas[-1]['num'] == trama['num'] - 1):
            print("Enviando trama final")
            self.tramas_enviadas.append(trama)
            self.contador_tramas += 1
            mensaje = "Trama " + str(self.contador_tramas) + ": (TX) \nDatos, Trama " + str(self.contador_trama_datos)
            return mensaje
        if (
            len(self.tramas_enviadas) > 0 and
            trama['fin'] == 1 and trama['ctr'] == 1 and
            trama['cof'] == 0 and trama['sol'] == 0 and trama['per'] == 0 and trama['num'] == 0 and
            trama['data'] == '' and
            self.tramas_enviadas[-1]['num'] == len(self.mensaje_transmitir)):
            self.tramas_enviadas.append(trama)
            self.contador_tramas += 1
            mensaje = "Trama " + str(self.contador_tramas) + ": (TX) \nControl, solicitud para dejar de transmitir"
            return mensaje
        return "Trama incorrecta, Por favor revisar"

    def responder_trama(self, trama):
        count = 1
        if len(self.tramas_enviadas) > 0 and trama == self.permiso_concedido and self.tramas_enviadas[0] == self.solicitud_permiso:
            self.tramas_recibidas.append(trama)
            self.contador_tramas += 1
            mensaje = "Trama " + str(self.contador_tramas) + ": (RX) \nControl, listo para recibir"
            return mensaje
        if (len(self.tramas_enviadas) > 0 and  trama['cof'] == 1 and trama['ctr'] == 1 and
            trama['fin'] == self.tramas_enviadas[-1]['fin'] and
            (trama['sol'], trama['per']) == (0, 0) and
            self.tramas_enviadas[-1]['data'] != '' and
            trama['data'] == self.tramas_enviadas[-1]['data'] and
            trama['num'] == self.tramas_enviadas[-1]['num']):
            self.tramas_recibidas.append(trama)
            self.mensaje_recibido += (trama['data'] + ' ')
            self.contador_tramas += 1
            mensaje = "Trama " + str(self.contador_tramas) + ": (RX) \nControl, Trama " + str(
            self.contador_trama_datos) + " recibida con exito"
            self.contador_trama_datos += 1
            return mensaje
        if (
            len(self.tramas_enviadas) > 0 and
            trama['cof'] == 1 and trama['ctr'] == 1 and
            trama['fin'] == 0 and trama['sol'] == 0 and trama['per'] == 0 and trama['num'] == 0 and trama['data'] == '' and
            self.tramas_enviadas[-1]['fin'] == 1 and self.tramas_enviadas[-1]['ctr'] == 1 and
            self.tramas_enviadas[-1]['cof'] == 0 and self.tramas_enviadas[-1]['sol'] == 0 and
            self.tramas_enviadas[-1]['per'] == 0 and self.tramas_enviadas[-1]['num'] == 0 and
            self.tramas_enviadas[-1]['data'] == ''
        ):
            self.tramas_recibidas.append(trama)
            self.contador_tramas += 1
            mensaje = "Trama " + str(self.contador_tramas) + ": (RX) \nControl, comunicacion finalizada"
            self.tramas_enviadas = []
            self.tramas_recibidas = []
            self.mensaje_recibido = []
            self.mensaje_transmitir = []
            self.mensaje_recibido = ''
            return mensaje
        return "Trama incorrecta, Por favor revisar"

    def dividir_cadena(self, cadena, num_partes):
        partes = cadena.split()

        if len(partes) == num_partes:
            return partes

        if len(partes) < num_partes:
            result = [''] * num_partes
            for i, palabra in enumerate(partes):
                result[i % num_partes] += (palabra + ' ')
            result = [parte.strip() for parte in result]  # Eliminar espacios al final
            return result

        longitud = len(cadena)
        tamaño_parte = longitud // num_partes
        result = [cadena[i * tamaño_parte:(i + 1) * tamaño_parte] for i in range(num_partes - 1)]
        result.append(cadena[(num_partes - 1) * tamaño_parte:])  # Añadir la parte restante
        return result

class Main:
    def __init__(self):
        self.protocolo = Protocolo()

    def ejecutar_pruebas(self):
        self.protocolo.mensaje_transmitir= ['Hola', 'como', 'estas']
        print("Pruba 1: ")
        trama_1 = self.protocolo.crear_trama('10101010',0,0,1,1,0,0,"",'10101010')
        print(trama_1)
        print(self.protocolo.enviar_trama(trama_1))
        print("---------------------------------------------------------------------------")
        trama_2 = self.protocolo.crear_trama('10101010',0,0,0,1,1,0,"",'10101010')
        print(trama_2)
        print(self.protocolo.responder_trama(trama_2))
        print("---------------------------------------------------------------------------")
        trama_3 = self.protocolo.crear_trama('10101010',0,0,0,0,0,1,'Hola','10101010')
        print(trama_3)
        print(self.protocolo.enviar_trama(trama_3))
        print("---------------------------------------------------------------------------")
        trama_4 = self.protocolo.crear_trama('10101010', 1, 0, 0, 1, 0, 1, 'Hola', '10101010')
        print(trama_4)
        print(self.protocolo.responder_trama(trama_4))
        print("---------------------------------------------------------------------------")
        trama_5 = self.protocolo.crear_trama('10101010', 0, 0, 0, 0, 0, 2, 'como', '10101010')
        print(trama_5)
        print(self.protocolo.enviar_trama(trama_5))
        print("---------------------------------------------------------------------------")
        trama_6 = self.protocolo.crear_trama('10101010', 1, 0, 0, 1, 0, 2, 'como', '10101010')
        print(trama_6)
        print(self.protocolo.responder_trama(trama_6))
        print("---------------------------------------------------------------------------")
        trama_7 = self.protocolo.crear_trama('10101010', 0, 1, 0, 0, 0, 3, 'estas', '10101010')
        print(trama_7)
        print(self.protocolo.enviar_trama(trama_7))
        print("---------------------------------------------------------------------------")
        trama_8 = self.protocolo.crear_trama('10101010', 1, 1, 0, 1, 0, 3, 'estas', '10101010')
        print(trama_8)
        print(self.protocolo.responder_trama(trama_8))
        print("---------------------------------------------------------------------------")
        print("Tramas enviadas = " ,self.protocolo.tramas_enviadas)
        print("Tramas recibidas = " ,self.protocolo.tramas_recibidas)
        print("Mensaje recibido = ", self.protocolo.mensaje_recibido)



    def ejecutar_pruebas2(self):
        self.protocolo.mensaje_transmitir = ['Hola', 'mundo', 'esto', 'es', 'prueba']

        print("Prueba 2: ")
        trama_1 = self.protocolo.crear_trama('10101010', 0, 0, 1, 1, 0, 0, '', '10101010')
        print(trama_1)
        print(self.protocolo.enviar_trama(trama_1))
        print("---------------------------------------------------------------------------")

        trama_2 = self.protocolo.crear_trama('10101010', 0, 0, 0, 1, 1, 0, '', '10101010')
        print(trama_2)
        print(self.protocolo.responder_trama(trama_2))
        print("---------------------------------------------------------------------------")

        trama_3 = self.protocolo.crear_trama('10101010', 0, 0, 0, 0, 0, 1, 'Hola', '10101010')
        print(trama_3)
        print(self.protocolo.enviar_trama(trama_3))
        print("---------------------------------------------------------------------------")

        trama_4 = self.protocolo.crear_trama('10101010', 1, 0, 0, 1, 0, 1, 'Hola', '10101010')
        print(trama_4)
        print(self.protocolo.responder_trama(trama_4))
        print("---------------------------------------------------------------------------")

        trama_5 = self.protocolo.crear_trama('10101010', 0, 0, 0, 0, 0, 2, 'mundo', '10101010')
        print(trama_5)
        print(self.protocolo.enviar_trama(trama_5))
        print("---------------------------------------------------------------------------")

        trama_6 = self.protocolo.crear_trama('10101010', 1, 0, 0, 1, 0, 2, 'mundo', '10101010')
        print(trama_6)
        print(self.protocolo.responder_trama(trama_6))
        print("---------------------------------------------------------------------------")

        trama_7 = self.protocolo.crear_trama('10101010', 0, 0, 0, 0, 0, 3, 'esto', '10101010')
        print(trama_7)
        print(self.protocolo.enviar_trama(trama_7))
        print("---------------------------------------------------------------------------")

        trama_8 = self.protocolo.crear_trama('10101010', 1, 0, 0, 1, 0, 3, 'esto', '10101010')
        print(trama_8)
        print(self.protocolo.responder_trama(trama_8))
        print("---------------------------------------------------------------------------")

        trama_9 = self.protocolo.crear_trama('10101010', 0, 0, 0, 0, 0, 4, 'es', '10101010')
        print(trama_9)
        print(self.protocolo.enviar_trama(trama_9))
        print("---------------------------------------------------------------------------")

        trama_10 = self.protocolo.crear_trama('10101010', 1, 0, 0, 1, 0, 4, 'es', '10101010')
        print(trama_10)
        print(self.protocolo.responder_trama(trama_10))
        print("---------------------------------------------------------------------------")

        trama_11 = self.protocolo.crear_trama('10101010', 0, 1, 0, 0, 0, 5, 'prueba', '10101010')
        print(trama_11)
        print(self.protocolo.enviar_trama(trama_11))
        print("---------------------------------------------------------------------------")

        trama_12 = self.protocolo.crear_trama('10101010', 1, 1, 0, 1, 0, 5, 'prueba', '10101010')
        print(trama_12)
        print(self.protocolo.responder_trama(trama_12))
        print("---------------------------------------------------------------------------")

        trama_13 = self.protocolo.crear_trama('10101010', 0, 1, 0, 1, 0, 0, '', '10101010')
        print(trama_13)
        print(self.protocolo.enviar_trama(trama_13))
        print("---------------------------------------------------------------------------")

        trama_14 = self.protocolo.crear_trama('10101010', 1, 0, 0, 1, 0, 0, '', '10101010')
        print(trama_14)
        print(self.protocolo.responder_trama(trama_14))
        print("---------------------------------------------------------------------------")

        print("Tramas enviadas = ", self.protocolo.tramas_enviadas)
        print("Tramas recibidas = ", self.protocolo.tramas_recibidas)
        print("Mensaje recibido = ", self.protocolo.mensaje_recibido)

# Ejecución de la clase Main
if __name__ == "__main__":
    main = Main()
    main.ejecutar_pruebas2()