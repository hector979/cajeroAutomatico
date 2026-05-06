#!/usr/bin/env python3
# _#_ coding: utf-8 _#_
"""
🏛🏛 CAJERO AUTOMÁTICO - Version con POO
Autor: [Tu nombre]
Fecha: 2026
Características: Herencia, Polimorfismo, Encapsulamiento,Abstracción
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict




#================================
# CLASES BASE (AABSTRACTAS)
class CuentaBancaria(ABC):
    def __init__(self, numero_cuenta: str, titular: str, saldo: float = 0):
        self._numero_cuenta = numero_cuenta #Encapsulamiento
        self._titular = titular
        self._saldo = saldo
        self._historial1: List [Dict] = []

    @abstractmethod
    def calcular_comision(self) -> float:
        """ Metodo abstracto: Cada tipo de cuenta tendrá su propia comisión."""
        pass

    @abstractmethod
    def get_tipo_cuenta(self) -> str:
        """ Retorna el tipo de cuenta (polimorfismo)."""
        pass

    def depositar(self,monto: float) -> bool:
        """ Metodo concreto heredado por todas las cuentas."""
        if monto > 0:
            self._saldo += monto
            self._registrar_transaccion("DEPOSITO", monto)
            return True 
        return False

    def retirar(self,monto: float) -> bool:
        """ Metodo que puede ser sobreescrito (polimorfismo)."""
        comision = self.calcular_comision(monto)
        total_a_restar = monto + comision
        
        if total_a_restar <= self._saldo:
            self._saldo -= total_a_restar
            self._registrar_transaccion("RETIRO", monto)
            return True
        return False
    


   
        

