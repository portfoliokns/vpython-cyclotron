from vpython import *

def getVelocity(r,v,t):
    return v

def getForce(r,v,t):
    f0 = (ELECTRIC_CHARGE*v.y*B_MAGNETIC)/ELECTRIC_MASS
    f1 = -(ELECTRIC_CHARGE*v.x*B_MAGNETIC)/ELECTRIC_MASS
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

B_init:float = input('磁場Bの数値を入力してください B=□.□*10^25　　')
B_init = float(B_init)
E_init:float = input('電場Eの数値を入力してください E=□.□*10^25　　')
E_init = float(E_init)

print('磁場の強さは')
print("B=%1.1f*10^25" % B_init)
print('電場の強さは')
print("E=%1.1f*10^25" % E_init)

# 物理定数の設定
B_MAGNETIC: float = B_init * (10 ** 25)  # 磁束密度(T)
E_FIELD: float = E_init * (10 ** 25)  # 電場(N/C)
D_TIME: float = 0.01  # 時間の刻み（s:秒）
ELECTRIC_CHARGE: float = 0.16 * 10**-24  # 正の電荷の値（C:クーロン）
ELECTRIC_MASS: float = 1.673  # 電荷の質量（g）
r = vector(0, 0.1, 0)  # 初期位置(m)
v = vector(ELECTRIC_CHARGE * E_FIELD, 0, 0)  # 初期初速度(m/s)
x: float = r.x
y: float = r.y
vx: float = v.x
vy: float = v.y

# ビジュアルオブジェクトの設定
BALL_RADIUS: float = 0.1  # 荷電子の半径(m)
D_RADIUS: float = 20  # Dの半径(m)
CYLINDER_RADIUS: float = 0.5  # 円筒の半径(m)
CYLINDER_LENGTH: float = 4  # 円筒の長さ(m)

# 背景設定
scene = canvas(title='Cyclotron', width=800, height=800, autoscale=False, center=vector(0, 0, 0), fov=pi/50)

# 荷電粒子
ball = sphere(pos=vector(x, y, 100), color=color.red, radius=BALL_RADIUS)
ball.pos = vector(x, y, 100)
ball.trail = curve(color=color.green)

# Dの形状
rod = cylinder(pos=vector(0, 0, -5.5), axis=vector(0, 0, 4.9), radius=D_RADIUS)

# 交流電源
rod = cylinder(pos=vector(0, D_RADIUS+1, -5.0), axis=vector(0, 0, 4.9), radius=1)
mybox = box(pos=vector(0.1, 0, 0.2), length=0.2, height=2 * D_RADIUS, width=0.2, color=vector(5, 5, 0))
mybox = box(pos=vector(-0.1, 0, 0.2), length=0.2, height=2 * D_RADIUS, width=0.2, color=vector(5, 5, 0))

# 電場
mybox = box(pos=vector(0, 0, -0.2), length=0.2, height=2*D_RADIUS, width=0.2, color=vector(10, 10, 0))

# 排出器
rod = cylinder(pos=vector(-D_RADIUS, 0, 0), axis=vector(0, CYLINDER_LENGTH, 0), radius=CYLINDER_RADIUS)

# サイクロトロンの実行処理
i:int = 0
while True:
    rate(100)
    time = i * D_TIME
    delta = calcRungeKutta(r, v, time, D_TIME)
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
            v.x += ELECTRIC_CHARGE * E_FIELD
        elif l > x:
            v.x -= ELECTRIC_CHARGE * E_FIELD
        else:
            v.x += 0
    if l**2 + n**2 > D_RADIUS**2:
        B_MAGNETIC = 0
        E_FIELD = 0
        if B_MAGNETIC == 0 and E_FIELD == 0 and -D_RADIUS-CYLINDER_RADIUS+BALL_RADIUS < x < -D_RADIUS+CYLINDER_RADIUS-BALL_RADIUS and 0 < y < CYLINDER_LENGTH:
            print('排出中')
        elif B_MAGNETIC == 0 and E_FIELD == 0 and -D_RADIUS-CYLINDER_RADIUS+BALL_RADIUS < x < -D_RADIUS+CYLINDER_RADIUS-BALL_RADIUS and y >= CYLINDER_LENGTH:
            print('排出成功')
            print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
            break
        else:
            print('排出失敗')
            print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
            break
    if i % 500 == 0:
        print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
    i += 1
    
while True:
    scene.waitfor('click')
