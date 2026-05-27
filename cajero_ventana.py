import tkinter as tk
from tkinter import messagebox, ttk
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict

# ═══════════════════════════════════════════════════════
# CLASES BASE (LOGICA DE NEGOCIO - SE MANTIENE POO)
# ═══════════════════════════════════════════════════════

class CuentaBancaria(ABC):
    def __init__(self, numero_cuenta: str, titular: str, saldo: float = 0):
        self._numero_cuenta = numero_cuenta
        self._titular = titular
        self._saldo = saldo
        self._historial: List[Dict] = []

    @abstractmethod
    def calcular_comision(self, monto: float) -> float:
        pass

    @abstractmethod
    def get_tipo_cuenta(self) -> str:
        pass

    def depositar(self, monto: float) -> bool:
        if monto > 0:
            self._saldo += monto
            self._registrar_transaccion("DEPÓSITO", monto)
            return True
        return False

    def retirar(self, monto: float) -> bool:
        comision = self.calcular_comision(monto)
        total_a_restar = monto + comision

        if total_a_restar <= self._saldo:
            self._saldo -= total_a_restar
            self._registrar_transaccion("RETIRO", -monto, f"Comisión: ${comision:,.0f}")
            return True
        return False

    def _registrar_transaccion(self, tipo: str, monto: float, detalle: str = ""):
        self._historial.append(
            {"fecha": datetime.now(), "tipo": tipo, "monto": monto, "detalle": detalle}
        )

    @property
    def saldo(self) -> float: return self._saldo

    @property
    def numero_cuenta(self) -> str: return self._numero_cuenta

    @property
    def titular(self) -> str: return self._titular

    def get_historial(self) -> List[Dict]: return self._historial.copy()


class CuentaAhorros(CuentaBancaria):
    _tasa_interes = 0.05
    def calcular_comision(self, monto: float) -> float: return 0.0
    def get_tipo_cuenta(self) -> str: return "Ahorros 💰"


class CuentaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta: str, titular: str, saldo: float = 0, limite_sobregiro: float = 500000):
        super().__init__(numero_cuenta, titular, saldo)
        self._limite_sobregiro = limite_sobregiro

    def calcular_comision(self, monto: float) -> float: return monto * 0.02
    def get_tipo_cuenta(self) -> str: return "Corriente 🏦"

    def retirar(self, monto: float) -> bool:
        comision = self.calcular_comision(monto)
        total_a_restar = monto + comision
        if total_a_restar <= (self._saldo + self._limite_sobregiro):
            self._saldo -= total_a_restar
            self._registrar_transaccion("RETIRO", -monto, f"Comisión: ${comision:,.0f} | Sobregiro")
            return True
        return False


class CuentaNomina(CuentaBancaria):
    def __init__(self, numero_cuenta: str, titular: str, saldo: float = 0, empresa: str = ""):
        super().__init__(numero_cuenta, titular, saldo)
        self._empresa = empresa

    def calcular_comision(self, monto: float) -> float: return 0.0
    def get_tipo_cuenta(self) -> str: return "Nómina 💼"


class Usuario:
    def __init__(self, nombre: str, pin: str):
        self._nombre = nombre
        self._pin = pin
        self._cuentas: Dict[str, CuentaBancaria] = {}

    def agregar_cuenta(self, cuenta: CuentaBancaria):
        self._cuentas[cuenta.numero_cuenta] = cuenta

    def verificar_pin(self, pin_ingresado: str) -> bool:
        return pin_ingresado == self._pin

    def listar_cuentas(self) -> List[CuentaBancaria]:
        return list(self._cuentas.values())

    @property
    def nombre(self) -> str: return self._nombre


# ═══════════════════════════════════════════════════════
# INTERFAZ GRÁFICA (GUI con Tkinter)
# ═══════════════════════════════════════════════════════

class CajeroGrafico(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cajero Automático Avanzado POO")
        self.geometry("500x600")
        self.config(bg="#f0f2f5")
        self.resizable(False, False)

        # Estado del cajero
        self._usuarios: Dict[str, Usuario] = {}
        self._usuario_actual: Usuario = None
        self._cuenta_seleccionada: CuentaBancaria = None

        self._inicializar_usuarios_demo()
        
        # Contenedor principal para cambiar de pantallas (Frames)
        self.contenedor = tk.Frame(self, bg="#f0f2f5")
        self.contenedor.pack(fill="both", expand=True, padx=20, pady=20)

        # Mostrar pantalla de Login al iniciar
        self.mostrar_pantalla_login()

    def _inicializar_usuarios_demo(self):
        # Clonamos tu base de datos demo original
        u1 = Usuario("Juan Pérez", "1234")
        u1.agregar_cuenta(CuentaAhorros("001", "Juan Pérez", 1000000))
        self._usuarios["001"] = u1

        u2 = Usuario("María García", "5678")
        u2.agregar_cuenta(CuentaCorriente("002", "María García", 2000000, 500000))
        u2.agregar_cuenta(CuentaAhorros("003", "María García", 500000))
        self._usuarios["002"] = u2

        u3 = Usuario("Carlos López", "9999")
        u3.agregar_cuenta(CuentaNomina("004", "Carlos López", 750000, "Tech Corp"))
        self._usuarios["004"] = u3

        u4 = Usuario("Hector Benavides", "5555")
        u4.agregar_cuenta(CuentaNomina("005", "Hector Benavides", 22000000, "Tech Corp"))
        self._usuarios["005"] = u4

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    # ─── PANTALLA 1: AUTENTICACIÓN ──────────────────────────
    def mostrar_pantalla_login(self):
        self.limpiar_contenedor()

        # Título
        lbl_titulo = tk.Label(self.contenedor, text="🏦 BANCO POO", font=("Arial", 22, "bold"), bg="#f0f2f5", fg="#1a73e8")
        lbl_titulo.pack(pady=30)

        # Inputs
        tk.Label(self.contenedor, text="Número de Cuenta:", font=("Arial", 11), bg="#f0f2f5").pack(anchor="w", pady=5)
        txt_cuenta = tk.Entry(self.contenedor, font=("Arial", 12), bd=2, relief="groove")
        txt_cuenta.pack(fill="x", pady=5)

        tk.Label(self.contenedor, text="PIN de Seguridad:", font=("Arial", 11), bg="#f0f2f5").pack(anchor="w", pady=5)
        txt_pin = tk.Entry(self.contenedor, font=("Arial", 12), bd=2, relief="groove", show="*")
        txt_pin.pack(fill="x", pady=5)

        # Nota ayuda demo
        lbl_ayuda = tk.Label(self.contenedor, text="Demo: Cuenta '001' PIN '1234' o '002' PIN '5678'", font=("Arial", 9, "italic"), bg="#f0f2f5", fg="gray")
        lbl_ayuda.pack(pady=15)

        def ejecutar_login():
            n_cuenta = txt_cuenta.get().strip()
            pin = txt_pin.get().strip()

            if n_cuenta in self._usuarios:
                usuario = self._usuarios[n_cuenta]
                if usuario.verificar_pin(pin):
                    self._usuario_actual = usuario
                    # Seleccionamos la primera cuenta del usuario por defecto
                    self._cuenta_seleccionada = usuario.listar_cuentas()[0]
                    self.mostrar_pantalla_principal()
                else:
                    messagebox.showerror("Error", "PIN incorrecto.")
            else:
                messagebox.showerror("Error", "La cuenta no existe.")

        btn_ingresar = tk.Button(self.contenedor, text="Ingresar Seguro", font=("Arial", 12, "bold"), bg="#1a73e8", fg="white", bd=0, cursor="hand2", command=ejecutar_login)
        btn_ingresar.pack(fill="x", pady=20, ipady=8)

    # ─── PANTALLA 2: MENÚ PRINCIPAL Y OPERACIONES ───────────
    def mostrar_pantalla_principal(self):
        self.limpiar_contenedor()

        # Encabezado de bienvenida
        lbl_bienvenida = tk.Label(self.contenedor, text=f"Hola, {self._usuario_actual.nombre} 👋", font=("Arial", 16, "bold"), bg="#f0f2f5", fg="#333")
        lbl_bienvenida.pack(anchor="w", pady=(10, 0))

        # Selector de Cuentas (Polimorfismo visible)
        lbl_selector = tk.Label(self.contenedor, text="Seleccione cuenta a operar:", font=("Arial", 10), bg="#f0f2f5", fg="gray")
        lbl_selector.pack(anchor="w", pady=(10, 2))

        cuentas_usuario = self._usuario_actual.listar_cuentas()
        nombres_cuentas = [f"{c.get_tipo_cuenta()} - N° {c.numero_cuenta}" for c in cuentas_usuario]
        
        cb_cuentas = ttk.Combobox(self.contenedor, values=nombres_cuentas, state="readonly", font=("Arial", 11))
        # Seleccionar la cuenta que está activa en el estado
        idx_actual = cuentas_usuario.index(self._cuenta_seleccionada)
        cb_cuentas.current(idx_actual)
        cb_cuentas.pack(fill="x", pady=5)

        # Panel de visualización de Saldo Dinámico
        frame_saldo = tk.Frame(self.contenedor, bg="white", bd=1, relief="solid")
        frame_saldo.pack(fill="x", pady=15, ipady=15)

        lbl_txt_saldo = tk.Label(frame_saldo, text="SALDO DISPONIBLE", font=("Arial", 9, "bold"), bg="white", fg="gray")
        lbl_txt_saldo.pack()

        lbl_monto_saldo = tk.Label(frame_saldo, text=f"${self._cuenta_seleccionada.saldo:,.2f}", font=("Arial", 22, "bold"), bg="white", fg="#2e7d32")
        lbl_monto_saldo.pack()

        # Cambiar de cuenta dinámicamente mediante el combobox
        def cambiar_cuenta_activa(event):
            self._cuenta_seleccionada = cuentas_usuario[cb_cuentas.current()]
            self.mostrar_pantalla_principal() # Refrescar la pantalla

        cb_cuentas.bind("<<ComboboxSelected>>", cambiar_cuenta_activa)

        # Sección de Transacciones Rápidas
        lbl_ops = tk.Label(self.contenedor, text="Operaciones Monetarias", font=("Arial", 11, "bold"), bg="#f0f2f5", fg="#333")
        lbl_ops.pack(anchor="w", pady=5)

        tk.Label(self.contenedor, text="Monto ($):", font=("Arial", 10), bg="#f0f2f5").pack(anchor="w")
        txt_monto = tk.Entry(self.contenedor, font=("Arial", 14), bd=2, relief="groove")
        txt_monto.pack(fill="x", pady=5)

        def accion_depositar():
            try:
                monto = float(txt_monto.get())
                if self._cuenta_seleccionada.depositar(monto):
                    messagebox.showinfo("Éxito", f"Depósito exitoso de ${monto:,.2f}")
                    self.mostrar_pantalla_principal()
                else:
                    messagebox.showwarning("Atención", "Monto inválido.")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido.")

        def accion_retirar():
            try:
                monto = float(txt_monto.get())
                if self._cuenta_seleccionada.retirar(monto):
                    messagebox.showinfo("Éxito", f"Retiro exitoso de ${monto:,.2f}\n(Revisa las comisiones si aplican)")
                    self.mostrar_pantalla_principal()
                else:
                    messagebox.showerror("Fondos Insuficientes", "No tienes fondos suficientes o has superado el límite de sobregiro.")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número válido.")

        # Botones de Acción de Dinero
        frame_botones_moneda = tk.Frame(self.contenedor, bg="#f0f2f5")
        frame_botones_moneda.pack(fill="x", pady=10)

        btn_dep = tk.Button(frame_botones_moneda, text="📥 Depositar", font=("Arial", 11, "bold"), bg="#2e7d32", fg="white", bd=0, cursor="hand2", command=accion_depositar)
        btn_dep.pack(side="left", fill="x", expand=True, padx=(0, 5), ipady=8)

        btn_ret = tk.Button(frame_botones_moneda, text="📤 Retirar", font=("Arial", 11, "bold"), bg="#c62828", fg="white", bd=0, cursor="hand2", command=accion_retirar)
        btn_ret.pack(side="right", fill="x", expand=True, padx=(5, 0), ipady=8)

        # Botones de información de cuenta e historial
        btn_detalles = tk.Button(self.contenedor, text="📊 Ver Detalles Técnicos de Cuenta", font=("Arial", 10), bg="#e0e0e0", bd=0, cursor="hand2", command=self._mostrar_popup_detalles)
        btn_detalles.pack(fill="x", pady=5, ipady=5)

        btn_historial = tk.Button(self.contenedor, text="📜 Ver Historial de Movimientos", font=("Arial", 10), bg="#e0e0e0", bd=0, cursor="hand2", command=self._mostrar_popup_historial)
        btn_historial.pack(fill="x", pady=5, ipady=5)

        # Botón Salir Seguro
        btn_salir = tk.Button(self.contenedor, text="🚪 Cerrar Sesión Segura", font=("Arial", 10, "bold"), bg="#37474f", fg="white", bd=0, cursor="hand2", command=self.mostrar_pantalla_login)
        btn_salir.pack(fill="x", pady=(20, 0), ipady=6)

    # ─── VENTANAS EMERGENTES (POPUPS DE INFORMACIÓN) ───────
    def _mostrar_popup_detalles(self):
        c = self._cuenta_seleccionada
        detalles = f"Tipo de Cuenta: {c.get_tipo_cuenta()}\n"
        detalles += f"Número de Cuenta: {c.numero_cuenta}\n"
        detalles += f"Titular: {c.titular}\n"
        detalles += f"Saldo Interno: ${c.saldo:,.2f}\n"

        # Aplicación de Polimorfismo / Inspección de subtipos
        if isinstance(c, CuentaAhorros):
            detalles += f"Tasa de Interés: {c._tasa_interes * 100:.1f}% anual\n"
        elif isinstance(c, CuentaCorriente):
            detalles += f"Límite de Sobregiro Disponible: ${c._limite_sobregiro:,.2f}\n"
            detalles += "Nota: Esta cuenta cobra 2% de comisión por retiro."
        elif isinstance(c, CuentaNomina):
            detalles += f"Empresa Vinculada: {c._empresa}\n"
            detalles += "Beneficio: Retiros sin costo de comisión de nómina."

        messagebox.showinfo("Detalles de Abstracción", detalles)

    def _mostrar_popup_historial(self):
        historial_ventana = tk.Toplevel(self)
        historial_ventana.title("Historial de Cuenta")
        historial_ventana.geometry("450x350")
        
        txt_area = tk.Text(historial_ventana, font=("Courier", 10), padhorizontal=10, padvertical=10)
        txt_area.pack(fill="both", expand=True)

        historial = self._cuenta_seleccionada.get_historial()
        if not historial:
            txt_area.insert("1.0", "No existen movimientos registrados en esta cuenta.")
        else:
            encabezado = f"{'FECHA':<12} {'TIPO':<10} {'MONTO':>12}\n" + "-"*40 + "\n"
            txt_area.insert("1.0", encabezado)
            for t in reversed(historial):
                fecha = t["fecha"].strftime("%d/%m %H:%M")
                monto = f"${t['monto']:,.0f}"
                linea = f"{fecha:<12} {t['tipo']:<10} {monto:>12}\n"
                if t["detalle"]:
                    linea += f"   > {t['detalle']}\n"
                txt_area.insert("end", linea)
        
        txt_area.config(state="disabled") # Bloquear escritura


# ═══════════════════════════════════════════════════════
# PUNTO DE ENTRADA DE LA GUI
# ═══════════════════════════════════════════════════════
if __name__ == "__main__":
    app = CajeroGrafico()
    app.mainloop()