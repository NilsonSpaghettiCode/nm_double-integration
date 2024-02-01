import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
#Integración doble
'''
Entradas
fx(x,y)
n = Número de intervalos X
m = Número de intervalos Y
R = Superficie -> ((xi,xf), (yi,yf)) == ((a,b), (c,ds))
Salidas

V = volumen bajo la superficie/Integral doble
Nf = númeto final de cuboides
function:Grafica 3d
'''
class Intervalo():

    def __init__(self, a,  b) -> None:
        self.a = a
        self.b = b

    def getRango(self):
        return (self.b-self.a)

    def __str__(self) -> str:
        return (f'Rango de [{self.a},{self.b}]')

class Superficie():
    def __init__(self, invertalo_x:Intervalo, intervalo_y:Intervalo) -> None:
        self.ix = intervalo_x
        self.iy = intervalo_y

class IntegracionSuperficial():

    def __init__(self,fx, nx, my, r:Superficie) -> None:
        '''
        Retorna el volumen bajo R:superficie de una fx(x,y)
        fx: Funcion(x,y) x, y variables independientes
        nx: Intervalos en el eje X
        my: Intervalos en el eje Y
        r: superficie
        '''
        self.fx = fx
        self.nx = nx
        self.my = my
        self.r = r

        self.base_n = 0
        self.base_m = 0
        self.Xi = []
        self.Yi = []
    
    def Ai(self,):
        pass
    
    def base(self, intervalo:Intervalo, cantidad_intervalos):
        base_i = intervalo.getRango()/cantidad_intervalos
        return base_i

    def dominios(self, intervalo:Intervalo, numero_dominios):
        dominios_i = np.linspace(intervalo.a,intervalo.b, numero_dominios, endpoint=False)
        return dominios_i
    
    def getVolumen(self,):
        self.Xi = self.dominios(self.r.ix, self.nx)
        self.Yi = self.dominios(self.r.iy, self.my)

        self.base_n = self.base(self.r.ix, self.nx)
        self.base_m = self.base(self.r.iy, self.my)
        

        X,Y = np.meshgrid(self.Xi,self.Yi, indexing='ij')
        Z = self.calculoAlturas()

        volumen = 0

        cuboides = []
        for i in range(self.nx):
            for j in range(self.my):
                #print(X[i,j], Y[i,j], Z[i,j])
                xi = X[i,j]
                xf = xi+self.base_n

                yi = Y[i,j]
                yf = yi+self.base_m


                largo_n = xf-xi
                ancho_m = yf-yi
                altura_i = Z[i,j]
                area_ij = largo_n * ancho_m

                volumen_ij = area_ij * altura_i
                volumen = volumen + volumen_ij
                cuboide_i = {'x':xi,'y':yi, 'alto':altura_i}
                cuboides.append(cuboide_i)
        return volumen, cuboides

    def calculoAlturas(self):
        fxA = lambda xi: xi+self.base_n/2 
        fyA = lambda yi: yi+self.base_m/2   
        xt = fxA(self.Xi)
        yt = fyA(self.Yi)
        X,Y = np.meshgrid(xt,yt, indexing='ij')
        zt = self.fx(X,Y)
        return zt
def graficar_prismas(prismas_info:list, ax, ancho, profundidad):
    for prisma in prismas_info:
        ax.bar3d(prisma['x'],prisma['y'],0, dx=ancho,dy=profundidad,dz=prisma['alto'],color='w')

#Definición de datos

fx = lambda x, y: (x**2)+(y**2)+2
n_x = 5
m_y = 5
intervalo_x = Intervalo(0,3)
intervalo_y = Intervalo(0,3)
r = Superficie(intervalo_x,intervalo_y)

#Calculo de volumen
Vs = IntegracionSuperficial(fx, n_x,m_y, r)
volumen, cuboides_i = Vs.getVolumen()

print(f'El volumen es: {volumen}')

#Datos para graficación
cantidad_muestras = 20
x = Vs.dominios(intervalo_x, cantidad_muestras)
y = Vs.dominios(intervalo_y, cantidad_muestras)
X,Y = np.meshgrid(x,y, indexing='ij')
Z = fx(X,Y)




#Graficación
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
graficar_prismas(cuboides_i,ax, Vs.base_n, Vs.base_m)
ax.plot_wireframe(X,Y,Z, color='r',antialiased=True)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(f'Integración bajo superficie: {volumen} U^3')
plt.show()


