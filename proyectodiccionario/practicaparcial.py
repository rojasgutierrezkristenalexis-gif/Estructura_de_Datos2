class Nodo:
    def __init__(self,valor):
        self._raiz=valor
        self._izq=None
        self._der=None
    @property
    def raiz(self):
        return self._raiz
    @raiz.setter
    def raiz(self,valor):
        self._raiz=valor
    @property
    def izq(self):
        return self._izq
    @izq.setter
    def izq(self,valor):
        self._izq=valor
    @property
    def der(self):
        return self._der
    @der.setter
    def der(self,valor):
        self._der=valor
class arbol:
    def __init__(self):
        self.val=None
    def altura(self,nodo) :
        if nodo is None :
            return -1
        return 1+max(self.altura(nodo.izq),self.altura(nodo.der))
    def _balance(self,nodo) :
        if nodo is None :
            return 0
        return self.altura(nodo.der)-self.altura(nodo.izq)
    def rotar_izq(self,nodo):
        y=nodo.der
        aux=y.izq
        y.izq=nodo
        nodo.der=aux 
        return y 
    def rota_der(self,nodo) :
        y=nodo.izq
        t2=y.der
        y.der=nodo
        nodo.izq=t2
        return y
        
    def encontrar_minimo(self,nodo):
        actual=nodo
        while actual and actual.izq is  not None :
            actual=actual.izq 
        return actual
        
        
            
    def insertar(self,valor):
        self.val=self._insertar_privado(self.val,valor)
        
    def _insertar_privado(self,nodo,valor):
        if not nodo  :
            return Nodo(valor)
        if valor > nodo.raiz :
            nodo.der=self._insertar_privado(nodo.der,valor)
        elif valor < nodo.raiz :
            nodo.izq=self._insertar_privado(nodo.izq,valor)
        else:
            print ('intentas meter un numero repetido')
            return nodo
        #balanceo 
        balance=self._balance(nodo)
        if balance > 1 and valor > nodo.der.raiz:
            return self.rotar_izq(nodo)
        
        if balance < -1 and  valor < nodo.izq.raiz:
            
            return self.rota_der(nodo)
        
        if balance > 1 and valor < nodo.der.raiz :
            nodo.der=self.rota_der(nodo.der)
            return self.rotar_izq(nodo)

        if balance < -1 and valor > nodo.izq.raiz :
            nodo.izq=self.rotar_izq(nodo.izq)
            return self.rota_der(nodo)
        
        return nodo
        
    def eliminar(self,valor):
        self.val=self._eliminar_privado(self.val,valor)
        
    def _eliminar_privado(self,nodo,valor) :
        if nodo is None :
            return None
        if valor > nodo.raiz :
            nodo.der = self._eliminar_privado(nodo.der,valor)
    
        elif valor < nodo.raiz :
            nodo.izq = self._eliminar_privado(nodo.izq,valor)
            
        else :
            if nodo.izq is None :
                return nodo.der
            elif nodo.der is None :
                return  nodo.izq
            else :
                sucesor=self.encontrar_minimo(nodo.der)
                nodo.raiz = sucesor.raiz
                nodo.der=self._eliminar_privado(nodo.der,sucesor.raiz)
                
                
        #balanceo 
        balance=self._balance(nodo)
        if balance < -1 and self._balance(nodo.izq) <= 0 :
            return self.rota_der(nodo)
    
        if balance > 1 and self._balance( nodo.der) >= 0 :
            return self.rotar_izq(nodo)
        
        if balance < -1 and self._balance(nodo.izq) > 0 :
            nodo.izq=self.rotar_izq(nodo.izq)
            return self.rota_der(nodo)
        
        if balance > 1 and self._balance(nodo.der) < 0 :
            nodo.der=self.rota_der(nodo.der) 
            return self.rotar_izq(nodo)
        
        return nodo
    
    def inorden(self,nodo):
        lista=self._inorden_privado(nodo)
        return lista
    def _inorden_privado(self,nodo):
        if nodo is None :
            return []
        lista=self._inorden_privado(nodo.izq)
        lista.append(nodo.raiz)
        lista += self._inorden_privado(nodo.der)
        return lista
        
    def posorden(self,nodo):
        if nodo is None :
            return []
        lista=self.posorden(nodo.izq)
        lista += self.posorden(nodo.der)
        lista.append(nodo.raiz)
        return lista
    def preorden(self,nodo) :
        if nodo is None :
            return []
        lista=[nodo.raiz]
        lista += self.preorden(nodo.izq)
        lista += self.preorden(nodo.der)
        return lista
        
        
arb=arbol()
elementos = [10, 20, 30, 40, 50, 25]
for e in elementos:
    arb.insertar(e)
alt=arb.altura(arb.val)
list=arb.preorden(arb.val) 
print(alt)
a=int(input('digite el numero a eliminar.......'))
arb.eliminar(a)
list=arb.preorden(arb.val) 
print (list)
print(alt)
