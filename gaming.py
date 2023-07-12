from vpython import *

def getVelocity(r,v,t):
    return v

def getForce(r,v,t):
    f0 = (ELECTRIC_CHARGE*v.y*B_magnetic)/ELECTRIC_MASS
    f1 = -(ELECTRIC_CHARGE*v.x*B_magnetic)/ELECTRIC_MASS
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

def getElectricForce():
    return ELECTRIC_CHARGE * E_FIELD

# 磁場Bと電場Eの入力
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
B_magnetic: float = B_init * (10 ** 25)  # 磁束密度(T)
E_FIELD: float = E_init * (10 ** 25)  # 電場(N/C)
D_TIME: float = 0.05  # 時間の刻み（s:秒）
ELECTRIC_CHARGE: float = 0.16 * 10**-24  # 正の電荷の値（C:クーロン）
ELECTRIC_MASS: float = 1.673  # 電荷の質量（g）
r = vector(0, 1.0, 0)  # 初期位置(m)
v = vector(getElectricForce(), 0, 0)  # 初期初速度(m/s)
x: float = r.x
y: float = r.y
vx: float = v.x
vy: float = v.y

# 背景設定
BACKGROUND_TITLE:str = 'サイクロトロン放射光のイメージ映像'
BACKGROUND_WIDTH:int = 800
BACKGROUND_HEIGHT:int = 800
BACKGROUND_CENTER = vector(0,0,100)
scene = canvas(title=BACKGROUND_TITLE, width=BACKGROUND_WIDTH, height=BACKGROUND_HEIGHT, autoscale=False, center=BACKGROUND_CENTER, fov=pi/50)

# 荷電粒子オブジェクト
BALL_RADIUS: float = 0.1
BALL_COLOR = color.red
CURVE_COLOR = color.green
ball = sphere(pos=vector(x, y, 100), color=BALL_COLOR, radius=BALL_RADIUS)
ball.pos = vector(x, y, 100)
ball.trail = curve(color=CURVE_COLOR)

# Dの形状オブジェクト
D_POSITION = vector(0, 0, -5.5)
D_AXIS = vector(0, 0, 4.9)
D_RADIUS: float = 20
rod = cylinder(pos=D_POSITION, axis=D_AXIS, radius=D_RADIUS)

# 交流電源オブジェクト
POWER_POSITION:float = vector(0, D_RADIUS+1, -5.0)
POWER_AXIS = vector(0, 0, 4.9)
POWER_RADIUS:float = 1
rod = cylinder(pos=POWER_POSITION, axis=POWER_AXIS, radius=POWER_RADIUS)

# 電場オブジェクト
ELECTRIC_FIELD_POSITION = vector(0, 0, -0.2)
ELECTRIC_FIELD_LENGTH:float = 0.2
ELECTRIC_FIELD_HEIGHT:float = 2*D_RADIUS
ELECTRIC_FIELD_COLOR = vector(10, 10, 0)
mybox = box(pos=ELECTRIC_FIELD_POSITION, length=ELECTRIC_FIELD_LENGTH, height=ELECTRIC_FIELD_HEIGHT, color=ELECTRIC_FIELD_COLOR)

# 排出器オブジェクト
DISCHARGE_POSITION = vector(-D_RADIUS, 0, 0)
DISCHARGE_LENGTH = 10
DISCHARGE_AXIS = vector(0, DISCHARGE_LENGTH, 0)
DISCHARGE_RADIUS: float = 2
rod = cylinder(pos=DISCHARGE_POSITION, axis=DISCHARGE_AXIS, radius=DISCHARGE_RADIUS)
DISCHARGE_LEFT_X = DISCHARGE_POSITION.x-DISCHARGE_RADIUS+BALL_RADIUS
DISCHARGE_RIGHT_X = DISCHARGE_POSITION.x+DISCHARGE_RADIUS-BALL_RADIUS

# サイクロトロンの実行処理
i:int = 0
time:float

while True:
    rate(100)
    time = i * D_TIME
    delta = calcRungeKutta(r, v, time, D_TIME)
    r += delta[0]
    v += delta[1]
    xx:float = x
    yy:float = y
    x = r.x
    y = r.y
    vx = v.x
    vy = v.y

    # 荷電粒子オブジェクトの位置設定
    ball.pos = vector(x, y, 0)
    ball.trail.append(pos=ball.pos)

    # 加速度を与える(y軸を横切ったかを判定)
    if x*xx <= 0 and time > 0:
        if xx < x:
            v.x += getElectricForce()
        elif xx > x:
            v.x -= getElectricForce()
        else:
            v.x += 0

    # 場外判定
    if xx**2 + yy**2 > D_RADIUS**2:
        B_magnetic = 0
        if DISCHARGE_LEFT_X < x < DISCHARGE_RIGHT_X and 0 < y < DISCHARGE_LENGTH:
            print('排出中')
        elif DISCHARGE_LEFT_X < x < DISCHARGE_RIGHT_X and y >= DISCHARGE_LENGTH:
            print('排出成功')
            print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
            break
        else:
            print('排出失敗')
            print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
            break

    # ターミナル上へ速さを出力
    if i % 500 == 0:
        print('速さ%1.2f(m/s)\t' % fabs(sqrt(v.x**2 + v.y**2)))
    i += 1
    
while True:
    scene.waitfor('click')
