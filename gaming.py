from vpython import *

def getVelocity(r,v,t):
    return v

def getForce(r,v,t):
    f0 = (e*v.y*B)/m
    f1 = -(e*v.x*B)/m
    return vector(f0, f1, 0)

def calcRungeKutta(r,v,t,h):
    k1 = h * getVelocity(r,v,t)
    m1 = h * getForce(r,v,t)
    k2 = h * getVelocity(r+k1/2,v+m1/2,t+h/2)
    m2 = h * getForce(r+k1/2,v+m1/2,t+h/2)
    k3 = h * getVelocity(r+k2/2,v+m2/2,t+h/2)
    m3 = h * getForce(r+k2/2,v+m2/2,t+h/2)
    k4 = h * getVelocity(r+k3,v+m3,t+h)
    m4 = h * getForce(r+k3,v+m3,t+h)
    delta_r = (k1+k4+2*(k2+k3))/6.0
    delta_v = (m1+m4+2*(m2+m3))/6.0
    return [delta_r, delta_v]

# 磁場Bと電場Eの入力
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

# 物理定数の設定
B = B0 * (10 ** 25)  # 磁束密度(T)#
E = E0 * (10 ** 25)  # 電場(N/C)#
d_t = 0.005  # 時間の刻み# #h=0.05#
e = 0.16 * 10**-24  # 正の電荷(C)# #e=0.16*10**-24#
m = 1.673  # 電荷の質量(yg)# #m=1.673#
r = vector(0, 2.0, 0)  # 初期条件r(m)# #r=vector(0,2.0,0)#
v = vector(e * E, 0, 0)  # 初期条件v(m/s)# #v=vector(e*E,0,0)#

# ビジュアルオブジェクトの設定
ball_radius = 0.1  # 荷電子の半径(m)#　#a=0.1#
d_radius = 20  # Dの半径(m)# #b=20#
cylinder_radius = 0.5  # 円筒の半径(m)# #c=2.0#  #c>a#
cylinder_length = 4  # 円筒の長さ(m)# #d=20#

# 背景設定#
scene = canvas(title='Cyclotron', width=1000, height=1000, autoscale=False, center=vector(0, 0, 0), fov=pi/50)

x = r.x
y = r.y
vx = v.x
vy = v.y

# 荷電粒子#
ball = sphere(pos=vector(x, y, 100), color=color.red, radius=ball_radius)
ball.pos = vector(x, y, 100)
ball.trail = curve(color=color.green)

# Dの形状#
rod = cylinder(pos=vector(0, 0, -5.5), axis=vector(0, 0, 4.9), radius=d_radius)

# 交流電源#
rod = cylinder(pos=vector(0, d_radius+1, -5.0), axis=vector(0, 0, 4.9), radius=1)
mybox = box(pos=vector(0.1, 0, 0.2), length=0.2, height=2 * d_radius, width=0.2, color=vector(5, 5, 0))
mybox = box(pos=vector(-0.1, 0, 0.2), length=0.2, height=2 * d_radius, width=0.2, color=vector(5, 5, 0))

# 電場#
mybox = box(pos=vector(0, 0, -0.2), length=0.2, height=2*d_radius, width=0.2, color=vector(10, 10, 0))

# 排出器#
rod = cylinder(pos=vector(-d_radius, 0, 0), axis=vector(0, cylinder_length, 0), radius=cylinder_radius)

i = 0
while True:
    rate(100)
    time = i * d_t
    delta = calcRungeKutta(r, v, time, d_t)
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
    if l**2 + n**2 > d_radius**2:
        B = 0
        E = 0
        if B == 0 and E == 0 and -d_radius-cylinder_radius+ball_radius < x < -d_radius+cylinder_radius-ball_radius and 0 < y < cylinder_length:
            print('排出中')
        elif B == 0 and E == 0 and -d_radius-cylinder_radius+ball_radius < x < -d_radius+cylinder_radius-ball_radius and y >= cylinder_length:
            print('排出成功')
            print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
            break
        else:
            print('排出失敗')
            print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
            break    
    i += 1

