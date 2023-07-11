from vpython import *

def func1(r,v,t):
    return v

def func2(r,v,t):
    f0 = (e*v.y*B)/m
    f1 = -(e*v.x*B)/m
    return vector(f0, f1, 0)

def runge12(r,v,t,h):
    k1 = h * func1(r,v,t)
    m1 = h * func2(r,v,t)
    k2 = h * func1(r+k1/2,v+m1/2,t+h/2)
    m2 = h * func2(r+k1/2,v+m1/2,t+h/2)
    k3 = h * func1(r+k2/2,v+m2/2,t+h/2)
    m3 = h * func2(r+k2/2,v+m2/2,t+h/2)
    k4 = h * func1(r+k3,v+m3,t+h)
    m4 = h * func2(r+k3,v+m3,t+h)
    delta_r = (k1+k4+2*(k2+k3))/6.0
    delta_v = (m1+m4+2*(m2+m3))/6.0
    return [delta_r, delta_v]

print('*************number example******************')
print('* 排出成功例1：B=1.8*10**25 and E=1.8*10**25 *')
print('* 排出成功例2：B=1.1*10**25 and E=1.1*10**25 *')
print('* 排出成功例3：B=2.5*10**25 and E=2.5*10**25 *')
print('* 排出成功例4：B=1.0*10**25 and E=3.0*10**25 *')
print('* 排出成功例5：B=1.0*10**25 and E=1.0*10**25 *')
print('* 排出失敗例1：B=0.8*10**25 and E=1.8*10**25 *')
print('* 排出失敗例2：B=1.1*10**25 and E=1.3*10**25 *')
print('*********************************************')
print('')

B0 = input('磁場Bの数値を入力してください B=□.□*10^25　　')
B0 = float(B0)
E0 = input('電場Eの数値を入力してください E=□.□*10^25　　')
E0 = float(E0)

print('磁場の強さは')
print("B=%1.1f*10^25" % B0)
print('電場の強さは')
print("E=%1.1f*10^25" % E0)

B = B0 * (10 ** 25)  # 磁束密度(T)#
E = E0 * (10 ** 25)  # 電場(N/C)#

h = 0.05  # 時間の刻み# #h=0.05#
e = 0.16 * 10**-24  # 正の電荷(C)# #e=0.16*10**-24#
m = 1.673  # 電荷の質量(yg)# #m=1.673#
r = vector(0, 2.0, 0)  # 初期条件r(m)# #r=vector(0,2.0,0)#
v = vector(e * E, 0, 0)  # 初期条件v(m/s)# #v=vector(e*E,0,0)#
a = 0.1  # 荷電子の半径(m)#　#a=0.1#
b = 20  # Dの半径(m)# #b=20#
c = 2.0  # 円筒の半径(m)# #c=2.0#  #c>a#
d = b  # 円筒の長さ(m)# #d=20#

# 背景設定#
scene = canvas(title='Cyclotron', width=700, height=700, autoscale=False, center=vector(0, 0, 0), fov=pi/50)
plane = box(pos=vector(0, 0, -5), length=2*b, height=2*b, width=2, color=color.blue, opacity=0.2)

x = r.x
y = r.y
vx = v.x
vy = v.y

# 荷電粒子#
ball = sphere(pos=vector(x, y, 0), color=color.red, radius=a)
ball.pos = vector(x, y, 0)
ball.trail = curve(color=color.green)

# Dの形状#
rod = cylinder(pos=vector(0, 0, -5.0), axis=vector(0, 0, 4.9), radius=b)

# 交流電源#
rod = cylinder(pos=vector(0, b+2, -5.0), axis=vector(0, 0, 4.9), radius=1)
mybox = box(pos=vector(0.5, b+0.5, -0.2), length=0.2, height=2.0, width=0.2, color=vector(5, 5, 0))
mybox = box(pos=vector(-0.5, b+0.5, -0.2), length=0.2, height=2.0, width=0.2, color=vector(5, 5, 0))

# 電場#
mybox = box(pos=vector(0, 0, -0.2), length=0.2, height=2*b, width=0.2, color=vector(10, 10, 0))

# 排出器#
rod = cylinder(pos=vector(-b, 0, 0), axis=vector(0, d, 0), radius=c)

i = 0
while True:
    rate(100)
    time = i * h
    delta = runge12(r, v, time, h)
    r += delta[0]
    v += delta[1]
    l = x
    n = y
    x = r.x
    y = r.y
    vx = v.x
    vy = v.y
    ball.pos = vector(x, y, 0)
    ball.trail.append(pos=ball.pos)
    if x*l <= 0 and time > 0:
        if l < x:
            v.x += e * E
        elif l > x:
            v.x -= e * E
        else:
            v.x += 0
    if l**2 + n**2 > b**2:
        B = 0
        E = 0
        if B == 0 and E == 0 and -b-c+a < x < -b+c-a and 0 < y < d:
            print('排出中')
        elif B == 0 and E == 0 and -b-c+a < x < -b+c-a and y >= d:
            print('排出成功')
            print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
            break
        else:
            print('排出失敗')
            print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
            break    
    i += 1

