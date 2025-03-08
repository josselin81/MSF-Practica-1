"""
Práctica 0: Mecánica pulmonar

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Gonzalez Garcia Josselin
Número de control: C21210380
Correo institucional: l21210380@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m 
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,6,3
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)
u1 = np.ones(N) #Escalon unitario
u2 = np.zeros (N); u2 [round(1/dt):round(2/dt)] =1 #Impulso
u3 = (np.linspace(0,tend,N))/tend #Rampa con pendiente 1/10
u4 = np.sin(m.pi/2*t) #Funcion sinusoidal, pi/2 0 250mHz

u = np.stack((u1,u2,u3,u4),axis = 1) #Meter todo en una matriz
signal = ['Escalon', 'Impulso', 'Rampa', 'Sin']


# Componentes del circuito RLC y función de transferencia
R = 3E3
L = 1E-3
C = 220E-6
num = [C*L*R,C*R**2+L,R]
den = [3*C*L*R,5*C*R**2+L,2*R]
sys = ctrl.tf(num,den)
print(sys)

# Componentes del controlador
Cr=1E-6
KI=182
Kp=0.86
Re= 1/(KI*Cr); print('Re=',Re)
Rr= (Kp*Re) ; print('Rr=',Rr)
numPID=[(Rr*Cr)+1]
denPID=[Re*Cr,0]
PID= ctrl.tf(numPID,denPID)
print(PID)

# Sistema de control en lazo cerrado
X = ctrl.series(PID,sys)
sysPID= ctrl.feedback(X,1, sign= -1)
print(sysPID)

# Respuesta del sistema en lazo abierto y en lazo cerrado
# color azul bajo[0.3,0.8,0.8]
# color azul fuerte [0.1,0.3,0.9]
# color rosa [0.8,0.3,0.6]
# Naranja [0.9,0.7,0.8]

fig1 = plt.figure();
plt.plot(t,u1,'-', color = [0.9,0.7,0.8],label = 'Ve(t)')
_,PA = ctrl.forced_response(sys,t,u1,x0)
plt.plot(t,PA,'-', color = [0.3,0.8,0.8],label = 'Vs(t)')
_,VPID= ctrl.forced_response(sysPID,t,u1,x0)
plt.plot(t,VPID,':',linewidth=3, color = [0.8,0.3,0.6],label = 'VPID(t)')
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize = 11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc= 'center', ncol=3 ,fontsize=8, frameon=False)
plt.show()
fig1.savefig('step.pdf',bbox_inches = 'tight')


fig2 = plt.figure();
plt.plot(t,u2,'-', color = [0.9,0.4,0.2],label = 'Ve(t)')
_,PA = ctrl.forced_response(sys,t,u2,x0)
plt.plot(t,PA,'-', color = [0.3,0.8,0.8],label = 'Vs(t)')
_,VPID= ctrl.forced_response(sysPID,t,u2,x0)
plt.plot(t,VPID,':',linewidth=3, color = [0.8,0.3,0.6],label = 'VPID(t)')
plt.xlim(-0.15,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize = 11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc= 'center', ncol=3 ,fontsize=8, frameon=False)
plt.show()
fig1.savefig('step.pdf',bbox_inches = 'tight')

fig3 = plt.figure();
plt.plot(t,u3,'-', color = [0.9,0.4,0.2],label = 'Ve(t)')
_,PA = ctrl.forced_response(sys,t,u3,x0)
plt.plot(t,PA,'-', color = [0.3,0.8,0.8],label = 'Vs(t)')
_,VPID= ctrl.forced_response(sysPID,t,u3,x0)
plt.plot(t,VPID,':',linewidth=3, color = [0.8,0.3,0.6],label = 'VPID(t)')
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize = 11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc= 'center', ncol=3 ,fontsize=8, frameon=False)
plt.show()
fig1.savefig('step.pdf',bbox_inches = 'tight')

fig4 = plt.figure();
plt.plot(t,u4,'-', color = [0.9,0.4,0.2],label = 'Vs(t)')
_,PA = ctrl.forced_response(sys,t,u4,x0)
plt.plot(t,PA,'-', color = [0.3,0.8,0.8],label = 'Vs(t)')
_,VPID= ctrl.forced_response(sysPID,t,u4,x0)
plt.plot(t,VPID,':',linewidth=3, color = [0.8,0.3,0.6],label = 'VPID(t)')
plt.xlim(-0.15,10); plt.xticks(np.arange(0,11,1.0))
plt.ylim(-1,1.2); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t[s]',fontsize = 11)
plt.ylabel('Vi(t) [V]',fontsize=11)
plt.legend(bbox_to_anchor = (0.5,-0.2), loc= 'center', ncol=3 ,fontsize=8, frameon=False)
plt.show()
fig1.savefig('step.pdf',bbox_inches = 'tight')

