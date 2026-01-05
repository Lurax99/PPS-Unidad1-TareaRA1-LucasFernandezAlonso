# lavadero.py

# SIMULACIÓN LAVADERO

# Esta clase modela el funcionamiento de un túnel de lavado de coches
# utilizando una máquina de estados. Cada fase del lavado se representa
# mediante una constante numérica, y el sistema avanza de fase de forma
# controlada.

class Lavadero:

    """
    Esta clase representa un lavadero automático de coches.
    
    La idea principal es modelar el proceso completo de lavado como
    una secuencia de estados (fases), avanzando de uno a otro según
    las opciones elegidas por el cliente.
    """

    # FASES DEL LAVADO

    # Cada fase se representa con un número.
    # Usamos constantes para que el código sea
    # más fácil de leer y entender.

    FASE_INACTIVO = 0          # No hay ningún coche
    FASE_COBRANDO = 1          # Se está cobrando al cliente
    FASE_PRELAVADO_MANO = 2    # Se limpia el coche a mano antes
    FASE_ECHANDO_AGUA = 3      # Se moja el coche con agua
    FASE_ENJABONANDO = 4       # Se aplica jabón
    FASE_RODILLOS = 5          # El coche pasa por los rodillos
    FASE_SECADO_AUTOMATICO = 6 # Secado con aire
    FASE_SECADO_MANO = 7       # Secado manual
    FASE_ENCERADO = 8          # Encerado final

    def __init__(self):
        
        """
        CONSTRUCTOR
        
        Este método se ejecuta automáticamente
        cuando se crea un lavadero nuevo.
        
        Aquí dejamos todo preparado para empezar:
        - El lavadero está vacío
        - No se ha ganado dinero
        - No hay servicios seleccionados
        """
      
        self.__ingresos = 0.0
        self.__fase = self.FASE_INACTIVO
        self.__ocupado = False

        # Servicios del lavado actual (al principio ninguno)
        self.__prelavado_a_mano = False
        self.__secado_a_mano = False
        self.__encerado = False

        # Funcion destructor
        self.terminar()

    # PROPIEDADES (SOLO LECTURA)
    # Estas funciones permiten consultar el estado
    # del lavadero sin modificarlo.

    @property
    def fase(self):
        # Devuelve el número de la fase actual
        return self.__fase

    @property
    def ingresos(self):
        # Devuelve el dinero total ganado
        return self.__ingresos

    @property
    def ocupado(self):
        # Indica si hay un coche dentro del lavadero
        return self.__ocupado
    
    @property
    def prelavado_a_mano(self):
        # Indica si el cliente pidió prelavado manual
        return self.__prelavado_a_mano

    @property
    def secado_a_mano(self):
        # Indica si el cliente pidió secado manual
        return self.__secado_a_mano

    @property
    def encerado(self):
        # Indica si el cliente pidió encerado
        return self.__encerado

    # FINALIZAR LAVADO

    def terminar(self):
        """
        TERMINAR
        
        Este método se llama cuando el lavado termina.
        Deja el lavadero listo para el siguiente coche.
        """

        self.__fase = self.FASE_INACTIVO
        self.__ocupado = False
        self.__prelavado_a_mano = False
        self.__secado_a_mano = False
        self.__encerado = False
    
    # INICIAR UN LAVADO
    
    def hacerLavado(self, prelavado_a_mano, secado_a_mano, encerado):
        """
        Inicia un nuevo ciclo de lavado, validando reglas de negocio.
        
        :raises RuntimeError: Si el lavadero está ocupado (Requisito 3).
        :raises ValueError: Si se intenta encerar sin secado a mano (Requisito 2).
        """
        if self.__ocupado:
            raise RuntimeError("No se puede iniciar un nuevo lavado mientras el lavadero está ocupado")
        
        if not secado_a_mano and encerado:
            raise ValueError("No se puede encerar el coche sin secado a mano")
        
        # Se coloca la fase inicial (aún no ha empezado el proceso real)
        self.__fase = self.FASE_INACTIVO

        # Se marca el lavadero como ocupado
        self.__ocupado = True
        
        # Se guardan las opciones elegidas por el cliente
        # dentro del objeto lavadero
        self.__prelavado_a_mano = prelavado_a_mano
        self.__secado_a_mano = secado_a_mano
        self.__encerado = encerado
        
    # COBRAR EL LAVADO

    def _cobrar(self):
        """
        Calcula y añade los ingresos según las opciones seleccionadas (Requisitos 4-8).
        Precio base: 5.00€ (Implícito, 5.00€ de base + 1.50€ de prelavado + 1.00€ de secado + 1.20€ de encerado = 8.70€)
        """
        coste_lavado = 5.00     # Precio base

        # Si hay prelavado manual, se suma su coste
        if self.__prelavado_a_mano:
            coste_lavado += 1.50
       
        # Si hay secado manual, se suma su coste
        if self.__secado_a_mano:
            coste_lavado += 1.20

        # Si hay encerado, se suma su coste
        if self.__encerado:
            coste_lavado += 1.00

        # Se suma el dinero ganado
        self.__ingresos += coste_lavado
        return coste_lavado

    # AVANZAR DE FASE

    def avanzarFase(self):

        """
        Cada vez que se llama a este método, el lavadero
        avanza a la siguiente fase del proceso de lavado.
        """
        # Si no hay ningún coche en el lavadero, no se hace nada
        
        if not self.__ocupado:
            return

        # FASE 0 → INACTIVO
        # Aquí se cobra al cliente
        
        if self.__fase == self.FASE_INACTIVO:
            coste_cobrado = self._cobrar()
            self.__fase = self.FASE_COBRANDO
            print(f" (COBRADO: {coste_cobrado:.2f} €) ", end="")

        # FASE 1 → COBRANDO
        # Se decide si hay prelavado o se pasa directamente al agua
        
        elif self.__fase == self.FASE_COBRANDO:
            if self.__prelavado_a_mano:
                self.__fase = self.FASE_PRELAVADO_MANO
            else:
                self.__fase = self.FASE_ECHANDO_AGUA 
        
        # FASE 2 → PRELAVADO A MANO

        elif self.__fase == self.FASE_PRELAVADO_MANO:
            self.__fase = self.FASE_ECHANDO_AGUA
        
        # FASE 3 → ECHANDO AGUA

        elif self.__fase == self.FASE_ECHANDO_AGUA:
            self.__fase = self.FASE_ENJABONANDO

        # FASE 4 → ENJABONANDO

        elif self.__fase == self.FASE_ENJABONANDO:
            self.__fase = self.FASE_RODILLOS
        
        # FASE 5 → RODILLOS
        # Después de los rodillos se decide el tipo de secado

        elif self.__fase == self.FASE_RODILLOS:
            if self.__secado_a_mano:
                self.__fase = self.FASE_SECADO_AUTOMATICO 
            else:
                self.__fase = self.FASE_SECADO_MANO
        
        # FASES FINALES → SE TERMINA EL LAVADO

        elif self.__fase == self.FASE_SECADO_AUTOMATICO:
            self.terminar()
        
        elif self.__fase == self.FASE_SECADO_MANO:
            self.terminar() 
        
        elif self.__fase == self.FASE_ENCERADO:
            self.terminar() 

        # SEGURIDAD: ESTADO NO VÁLIDO
        # Si el número de fase no coincide con ninguno conocido,
        # algo va mal y se lanza un error.

        else:
            raise RuntimeError(f"Estado no válido: Fase {self.__fase}. El lavadero va a estallar...")

    # IMPRIMIR FASE

    def imprimir_fase(self):
        """
        Muestra por pantalla el nombre de la fase actual.
        Traduce el número de fase (0, 1, 2...) a un texto entendible.
        """
        fases_map = {
            self.FASE_INACTIVO: "0 - Inactivo",
            self.FASE_COBRANDO: "1 - Cobrando",
            self.FASE_PRELAVADO_MANO: "2 - Haciendo prelavado a mano",
            self.FASE_ECHANDO_AGUA: "3 - Echándole agua",
            self.FASE_ENJABONANDO: "4 - Enjabonando",
            self.FASE_RODILLOS: "5 - Pasando rodillos",
            self.FASE_SECADO_AUTOMATICO: "6 - Haciendo secado automático",
            self.FASE_SECADO_MANO: "7 - Haciendo secado a mano",
            self.FASE_ENCERADO: "8 - Encerando a mano",
        }
        
        # Se imprime la fase actual usando el diccionario
        print(fases_map.get(self.__fase, f"{self.__fase} - En estado no válido"), end="")

    # IMPRIMIR ESTADO

    def imprimir_estado(self):
        """
        Muestra por pantalla el estado completo del lavadero.
        Es útil para depurar y entender qué está pasando.
        """
        print("----------------------------------------")
        print(f"Ingresos Acumulados: {self.ingresos:.2f} €")
        print(f"Ocupado: {self.ocupado}")
        print(f"Prelavado a mano: {self.prelavado_a_mano}")
        print(f"Secado a mano: {self.secado_a_mano}")
        print(f"Encerado: {self.encerado}")
        print("Fase: ", end="")
        # Se delega la impresión de la fase a su método específico
        self.imprimir_fase()
        print("\n----------------------------------------")
        
    # METODO DE PRUEBAS

    def ejecutar_y_obtener_fases(self, prelavado, secado, encerado):
        """
        Ejecuta un ciclo completo de lavado y devuelve una lista
        con todas las fases por las que ha pasado el lavadero.
        Este método se usa para pruebas unitarias.
        """

        # Se inicia un lavado con las opciones indicadas
        self.hacerLavado(prelavado, secado, encerado)

        # Lista que guardará las fases visitadas
        fases_visitadas = [self.fase]

        # Mientras el lavadero esté ocupado, se avanza de fase
        while self.ocupado:
            # Usamos un límite de pasos para evitar bucles infinitos en caso de error
            if len(fases_visitadas) > 15:
                raise Exception("Bucle infinito detectado en la simulación de fases.")
            self.avanzarFase()
            fases_visitadas.append(self.fase)

        return fases_visitadas