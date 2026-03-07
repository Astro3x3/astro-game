import pygame
import sys
import random
import math
from pathlib import Path

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Astro Boy Game")
clock = pygame.time.Clock()

NEON_CYAN   = (0, 255, 255)
NEON_PINK   = (255, 0, 200)
NEON_YELLOW = (255, 220, 0)
NEON_GREEN  = (0, 255, 100)
NEON_RED    = (255, 50, 50)
NEON_ORANGE = (255, 140, 0)
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)

WEAPON_AMMO   = {"shotgun": 20, "rocket": 15, "laser": 100, "flamethrower": 100}
WEAPON_COLORS = {"blaster": (0,255,255), "shotgun": (255,140,0), "rocket": (255,50,50),
                 "laser": (0,255,100), "flamethrower": (255,80,0)}

current_level = 1

def load_sprites(folder):
    frames = []
    path = Path(folder)
    if not path.exists():
        return frames
    for file in sorted(path.glob("*.png")):
        frames.append(pygame.image.load(str(file)).convert_alpha())
    return frames

stand_frames = load_sprites("astro_stand")
walk_frames  = load_sprites("astro_walk")
jump_frames  = load_sprites("astro_jump")
shoot_frames = load_sprites("astro_shoot")
if not shoot_frames:
    p = Path("astro_shoot/astro_shoot.png")
    if p.exists():
        shoot_frames = [pygame.image.load(str(p)).convert_alpha()]

def make_placeholder(color, w=40, h=50):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (8, 15, 24, 25), border_radius=4)
    pygame.draw.circle(surf, color, (20, 10), 10)
    pygame.draw.circle(surf, WHITE, (16, 9), 3)
    pygame.draw.circle(surf, WHITE, (24, 9), 3)
    pygame.draw.circle(surf, BLACK, (17, 9), 1)
    pygame.draw.circle(surf, BLACK, (25, 9), 1)
    pygame.draw.rect(surf, color, (10, 40, 8, 10), border_radius=2)
    pygame.draw.rect(surf, color, (22, 40, 8, 10), border_radius=2)
    return surf

if not stand_frames: stand_frames = [make_placeholder(NEON_CYAN)]
if not walk_frames:  walk_frames  = [make_placeholder(NEON_CYAN), make_placeholder((0,200,220))]
if not jump_frames:  jump_frames  = [make_placeholder(NEON_YELLOW), make_placeholder(NEON_YELLOW)]
if not shoot_frames: shoot_frames = [make_placeholder(NEON_PINK)]

player_width  = stand_frames[0].get_width()
player_height = stand_frames[0].get_height()

GROUND_Y = HEIGHT - 70
WORLD_W  = 4000
random.seed(42)

# --- LEVEL 1: DAY ---
sky_surface_day = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    t = y / HEIGHT
    r = int(80  + (180-80)*t)
    g = int(160 + (220-160)*t)
    b = int(255 + (255-255)*t)
    pygame.draw.line(sky_surface_day, (r,g,b), (0,y), (WIDTH,y))

sun_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
pygame.draw.circle(sun_surface, (255, 240, 80, 60), (100,100), 90)
pygame.draw.circle(sun_surface, (255, 230, 50, 120), (100,100), 70)
pygame.draw.circle(sun_surface, (255, 220, 0), (100,100), 55)

cloud_surface = pygame.Surface((WORLD_W*2, HEIGHT), pygame.SRCALPHA)
random.seed(99)
for _ in range(30):
    cx = random.randint(0, WORLD_W*2)
    cy = random.randint(30, 200)
    cr = random.randint(25,60)
    for ox, oy in [(0,0),(-cr//2,cr//3),(cr//2,cr//3),(-cr//3,-cr//4),(cr//3,-cr//4)]:
        pygame.draw.circle(cloud_surface, (255,255,255,160), (cx+ox, cy+oy), cr)

BUILD_W = WORLD_W * 2
build_surface_day = pygame.Surface((BUILD_W, HEIGHT), pygame.SRCALPHA)
palette_day = [(200,220,240),(180,200,230),(210,190,220),(190,210,200)]
bx = 0
random.seed(42)
while bx < BUILD_W:
    bw = random.randint(50,130)
    bh = random.randint(80,220)
    by = GROUND_Y - bh
    col = random.choice(palette_day)
    pygame.draw.rect(build_surface_day, col, (bx,by,bw,bh))
    for wy in range(by+10, GROUND_Y-10, 18):
        for wx in range(bx+6, bx+bw-6, 14):
            if random.random() > 0.3:
                pygame.draw.rect(build_surface_day, (150,200,255,180), (wx,wy,8,10))
    pygame.draw.rect(build_surface_day, (100,120,160,200), (bx,by,bw,3))
    bx += bw + random.randint(8,25)

ground_surface_day = pygame.Surface((WORLD_W, HEIGHT-GROUND_Y), pygame.SRCALPHA)
for y in range(HEIGHT-GROUND_Y):
    v = int(140 + 40*(y/(HEIGHT-GROUND_Y)))
    pygame.draw.line(ground_surface_day, (v, int(v*0.85), int(v*0.6)), (0,y), (WORLD_W,y))
for dx in range(0, WORLD_W, 70):
    pygame.draw.rect(ground_surface_day, (255,255,255,180), (dx, (HEIGHT-GROUND_Y)//2, 40, 3))

# --- LEVEL 2: NIGHT ---
sky_surface_night = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    t = y / HEIGHT
    r = int(5  + (15-5)*t)
    g = int(5  + (20-5)*t)
    b = int(30 + (60-30)*t)
    pygame.draw.line(sky_surface_night, (r,g,b), (0,y), (WIDTH,y))

STAR_W = WORLD_W * 2
star_surface = pygame.Surface((STAR_W, HEIGHT), pygame.SRCALPHA)
for _ in range(400):
    sx = random.randint(0, STAR_W)
    sy = random.randint(0, int(GROUND_Y*0.8))
    r  = random.randint(1,2)
    alpha = random.randint(100,255)
    color = random.choice([(255,255,255,alpha),(0,255,255,alpha),(255,200,255,alpha)])
    pygame.draw.circle(star_surface, color, (sx,sy), r)

GRID_W = WORLD_W * 2
grid_surface = pygame.Surface((GRID_W, HEIGHT-GROUND_Y), pygame.SRCALPHA)
grid_h = HEIGHT - GROUND_Y
for gy in range(0, grid_h, 12):
    alpha = max(20, 80-gy*2)
    pygame.draw.line(grid_surface, (0,200,255,alpha), (0,gy), (GRID_W,gy))
for gx in range(0, GRID_W, 60):
    pygame.draw.line(grid_surface, (0,200,255,40), (gx,0), (gx,grid_h))

build_surface_night = pygame.Surface((BUILD_W, HEIGHT), pygame.SRCALPHA)
palette_night = [(15,30,60),(20,50,40),(50,20,40),(10,40,80)]
bx = 0
random.seed(42)
while bx < BUILD_W:
    bw = random.randint(50,130)
    bh = random.randint(80,220)
    by = GROUND_Y - bh
    col = random.choice(palette_night)
    pygame.draw.rect(build_surface_night, col, (bx,by,bw,bh))
    for wy in range(by+10, GROUND_Y-10, 18):
        for wx in range(bx+6, bx+bw-6, 14):
            if random.random() > 0.3:
                wc = random.choice([(0,200,255,120),(255,200,0,100),(255,0,180,80)])
                pygame.draw.rect(build_surface_night, wc, (wx,wy,8,10))
    roof_col = random.choice([NEON_CYAN, NEON_PINK, NEON_YELLOW])
    pygame.draw.line(build_surface_night, (*roof_col,200), (bx,by), (bx+bw,by), 2)
    bx += bw + random.randint(8,25)

ground_surface_night = pygame.Surface((WORLD_W, HEIGHT-GROUND_Y), pygame.SRCALPHA)
for y in range(HEIGHT-GROUND_Y):
    v = int(10 + 20*(y/(HEIGHT-GROUND_Y)))
    pygame.draw.line(ground_surface_night, (v,v,v+20), (0,y), (WORLD_W,y))
for dx in range(0, WORLD_W, 70):
    pygame.draw.rect(ground_surface_night, (0,200,255,150), (dx, (HEIGHT-GROUND_Y)//2, 40, 3))

RAW_PLATFORMS = [
    (280,  GROUND_Y-110, 130, 14, 0),
    (500,  GROUND_Y-170, 100, 14, 1),
    (720,  GROUND_Y-130, 120, 14, 2),
    (950,  GROUND_Y-200, 110, 14, 0),
    (1150, GROUND_Y-150, 140, 14, 1),
    (1380, GROUND_Y-240, 100, 14, 2),
    (1600, GROUND_Y-170, 130, 14, 0),
    (1820, GROUND_Y-210, 90,  14, 1),
    (2050, GROUND_Y-130, 150, 14, 2),
    (2280, GROUND_Y-190, 110, 14, 0),
    (2500, GROUND_Y-250, 120, 14, 1),
    (2720, GROUND_Y-160, 130, 14, 2),
    (2950, GROUND_Y-220, 100, 14, 0),
    (3200, GROUND_Y-170, 140, 14, 1),
    (3450, GROUND_Y-240, 110, 14, 2),
    (3700, GROUND_Y-130, 150, 14, 0),
]

RAW_PLATFORMS_L2 = [
    (200,  GROUND_Y-100, 120, 14, 0),
    (420,  GROUND_Y-180, 110, 14, 1),
    (650,  GROUND_Y-140, 130, 14, 2),
    (880,  GROUND_Y-210, 100, 14, 0),
    (1100, GROUND_Y-160, 140, 14, 1),
    (1340, GROUND_Y-260, 110, 14, 2),
    (1570, GROUND_Y-180, 120, 14, 0),
    (1800, GROUND_Y-230, 95,  14, 1),
    (2020, GROUND_Y-140, 160, 14, 2),
    (2260, GROUND_Y-200, 120, 14, 0),
    (2480, GROUND_Y-260, 130, 14, 1),
    (2710, GROUND_Y-170, 140, 14, 2),
    (2940, GROUND_Y-230, 110, 14, 0),
    (3180, GROUND_Y-180, 150, 14, 1),
    (3430, GROUND_Y-250, 120, 14, 2),
    (3680, GROUND_Y-140, 160, 14, 0),
]

PLAT_COLORS_DAY = [
    ((100,200,255), (180,220,255)),
    ((255,180,100), (255,230,180)),
    ((120,220,120), (180,255,180)),
]
PLAT_COLORS_NIGHT = [
    (NEON_CYAN,   (0,100,150)),
    (NEON_PINK,   (120,0,100)),
    (NEON_YELLOW, (120,100,0)),
]

def draw_platform_surf(w, h, style, level=1):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    colors = PLAT_COLORS_DAY if level == 1 else PLAT_COLORS_NIGHT
    fg, bg = colors[style]
    pygame.draw.rect(surf, (*bg, 200), (0,0,w,h), border_radius=4)
    pygame.draw.rect(surf, (*fg, 230), (0,0,w,3), border_radius=2)
    for dx in range(8, w-4, 16):
        pygame.draw.circle(surf, (*fg, 180), (dx, h//2), 2)
    return surf

plat_surfs_l1 = {}
for rx,py,pw,ph,style in RAW_PLATFORMS:
    key = (pw,ph,style)
    if key not in plat_surfs_l1:
        plat_surfs_l1[key] = draw_platform_surf(pw,ph,style,1)

plat_surfs_l2 = {}
for rx,py,pw,ph,style in RAW_PLATFORMS_L2:
    key = (pw,ph,style)
    if key not in plat_surfs_l2:
        plat_surfs_l2[key] = draw_platform_surf(pw,ph,style,2)

def get_platforms(cam_x, level=1):
    plats = [(pygame.Rect(-9999, GROUND_Y, 99999, 100), None)]
    raw = RAW_PLATFORMS if level == 1 else RAW_PLATFORMS_L2
    tile = int(cam_x // WORLD_W) - 1
    for t in [tile, tile+1, tile+2]:
        for rx,py,pw,ph,style in raw:
            r = pygame.Rect(t*WORLD_W+rx, py, pw, ph)
            plats.append((r, (pw,ph,style)))
    return plats

class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, life=None, size=None):
        self.x = x; self.y = y; self.color = color
        self.vx = vx if vx is not None else random.uniform(-3,3)
        self.vy = vy if vy is not None else random.uniform(-4,-1)
        self.life = life if life is not None else random.randint(15,35)
        self.max_life = self.life
        self.size = size if size is not None else random.randint(2,5)
    def update(self):
        self.x += self.vx; self.y += self.vy
        self.vy += 0.15; self.life -= 1
    def draw(self, surface, cam_x):
        s = max(1, int(self.size*self.life/self.max_life))
        pygame.draw.circle(surface, self.color, (int(self.x-cam_x), int(self.y)), s)

particles = []

class HealthPickup:
    def __init__(self, x, y):
        self.x = float(x); self.y = float(y)
        self.w = 22; self.h = 22
        self.alive = True
        self.bob_angle = random.uniform(0, math.pi * 2)
        self.bob_offset = 0.0

    def update(self):
        self.bob_angle += 0.07
        self.bob_offset = math.sin(self.bob_angle) * 5

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y + self.bob_offset), self.w, self.h)

    def draw(self, surface, cam_x):
        sx = int(self.x - cam_x)
        sy = int(self.y + self.bob_offset)
        tick = pygame.time.get_ticks()
        pulse = abs(math.sin(tick * 0.005))
        glow_surf = pygame.Surface((self.w + 20, self.h + 20), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 80, 80, int(80 * pulse)), (self.w//2+10, self.h//2+10), self.w//2+8)
        surface.blit(glow_surf, (sx - 10, sy - 10))
        pygame.draw.rect(surface, (200, 30, 30), (sx, sy, self.w, self.h), border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), (sx + 4, sy + 8, 14, 6))
        pygame.draw.rect(surface, (255, 255, 255), (sx + 8, sy + 4, 6, 14))
        pygame.draw.rect(surface, (255, 100, 100), (sx, sy, self.w, self.h), 2, border_radius=5)

# ==============================
# WEAPON PICKUPS
# ==============================
WEAPON_AMMO = {"shotgun": 18, "rocket": 5, "laser": 40, "flamethrower": 40}
WEAPON_COLORS = {"blaster": NEON_CYAN, "shotgun": NEON_ORANGE, "rocket": NEON_RED,
                 "laser": NEON_GREEN, "flamethrower": (255, 80, 0)}

class WeaponPickup:
    LABELS = {"shotgun":"SHOTGUN","rocket":"ROCKET","laser":"LASER","flamethrower":"FLAME"}
    def __init__(self, x, y, wtype):
        self.x = float(x); self.y = float(y); self.w = 32; self.h = 32
        self.alive = True; self.wtype = wtype
        self.bob = random.uniform(0, math.pi * 2)
    def update(self):
        self.bob += 0.07
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y + math.sin(self.bob)*5), self.w, self.h)
    def draw(self, surface, cam_x):
        tick = pygame.time.get_ticks()
        sx = int(self.x - cam_x); sy = int(self.y + math.sin(self.bob)*5)
        col = WEAPON_COLORS.get(self.wtype, NEON_CYAN)
        pulse = abs(math.sin(tick * 0.006))
        gs2 = pygame.Surface((self.w+22, self.h+22), pygame.SRCALPHA)
        pygame.draw.circle(gs2, (*col, int(80*pulse)), (self.w//2+11, self.h//2+11), self.w//2+9)
        surface.blit(gs2, (sx-11, sy-11))
        pygame.draw.rect(surface, (15,15,15), (sx, sy, self.w, self.h), border_radius=8)
        pygame.draw.rect(surface, col, (sx, sy, self.w, self.h), 2, border_radius=8)
        # Icon depending on weapon
        icons = {"shotgun":"⊕","rocket":"⚡","laser":"▶","flamethrower":"⬡"}
        icon_surf = pygame.font.SysFont("consolas", 16, bold=True).render(icons.get(self.wtype,"?"), True, col)
        surface.blit(icon_surf, (sx + self.w//2 - icon_surf.get_width()//2, sy + 4))
        lbl = pygame.font.SysFont("consolas", 9, bold=True).render(self.LABELS[self.wtype], True, col)
        surface.blit(lbl, (sx + self.w//2 - lbl.get_width()//2, sy + self.h - 13))

# ==============================
# SPIKE TRAPS
# ==============================
class SpikeTrap:
    def __init__(self, x, y, w=44):
        self.x = float(x); self.y = float(y); self.w = w; self.h = 18; self.alive = True
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)
    def draw(self, surface, cam_x):
        sx = int(self.x - cam_x); sy = int(self.y)
        pygame.draw.rect(surface, (50,15,15), (sx, sy+9, self.w, 9))
        n = self.w // 11
        for i in range(n):
            tx = sx + i*11 + 5
            pygame.draw.polygon(surface, (180,0,0),   [(tx, sy),   (tx-5, sy+9), (tx+5, sy+9)])
            pygame.draw.polygon(surface, (255,60,60), [(tx, sy+2), (tx-3, sy+9), (tx+3, sy+9)])

# ==============================
# TURRETS
# ==============================
class Turret:
    def __init__(self, x, y):
        self.x = float(x); self.y = float(y); self.w = 32; self.h = 40
        self.alive = True; self.hp = 5; self.max_hp = 5
        self.shoot_timer = random.randint(60,120)
        self.angle = 0.0; self.flash_timer = 0
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)
    def update(self, player_rect, bullets_list):
        dx = player_rect.centerx - (self.x + self.w//2)
        dy = player_rect.centery - (self.y + self.h//2)
        self.angle = math.atan2(dy, dx)
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(80, 160)
            spd = 5
            b = Bullet(self.x+self.w//2, self.y+self.h//2, 1 if dx>0 else -1,
                       is_enemy=True, speed=spd, color=(255,100,0))
            b.vy = math.sin(self.angle) * spd
            b.speed = abs(math.cos(self.angle)) * spd
            bullets_list.append(b)
        if self.flash_timer > 0: self.flash_timer -= 1
    def draw(self, surface, cam_x):
        sx = int(self.x - cam_x); sy = int(self.y)
        flash = self.flash_timer > 0
        base = (200,50,0) if flash else (70,35,0)
        pygame.draw.rect(surface, base, (sx, sy+18, self.w, self.h-18), border_radius=5)
        pygame.draw.rect(surface, (100,50,0), (sx+2, sy+20, self.w-4, self.h-22), border_radius=4)
        # Rivet bolts
        for bx2 in [sx+5, sx+self.w-7]:
            pygame.draw.circle(surface, (150,70,0), (bx2, sy+24), 3)
        cx = sx+self.w//2; cy = sy+10
        pygame.draw.circle(surface, (50,25,0), (cx, cy), 14)
        pygame.draw.circle(surface, (100,50,0) if not flash else (255,100,0), (cx, cy), 11)
        # Barrel
        barrel_len = 22
        ex2 = int(cx + math.cos(self.angle)*barrel_len)
        ey2 = int(cy + math.sin(self.angle)*barrel_len)
        pygame.draw.line(surface, (150,70,0), (cx,cy), (ex2,ey2), 6)
        pygame.draw.line(surface, (255,140,0) if flash else (200,100,0), (cx,cy), (ex2,ey2), 3)
        # Muzzle tip
        pygame.draw.circle(surface, (255,140,0) if flash else (160,80,0), (ex2,ey2), 4)
        # HP bar
        bar_w = 28; filled = int(bar_w * self.hp / self.max_hp)
        pygame.draw.rect(surface, (80,0,0), (sx+2, sy-7, bar_w, 4), border_radius=2)
        pygame.draw.rect(surface, (255,80,0), (sx+2, sy-7, filled, 4), border_radius=2)

# ==============================
# SHIELD ENEMIES
# ==============================
class ShieldEnemy:
    def __init__(self, x, y, patrol_left, patrol_right):
        self.x = float(x); self.y = float(y); self.w = 36; self.h = 48
        self.patrol_left = patrol_left; self.patrol_right = patrol_right
        self.speed = 1.2; self.direction = 1
        self.alive = True; self.hp = 5; self.max_hp = 5
        self.shield_up = True; self.shield_hp = 8; self.shield_max = 8
        self.shoot_timer = random.randint(90,200); self.flash_timer = 0
        self.hover_angle = random.uniform(0, math.pi*2)
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)
    def update(self, player_rect, cam_x, bullets_list):
        self.hover_angle += 0.05
        self.x += self.speed * self.direction
        if self.x < self.patrol_left: self.direction = 1
        if self.x > self.patrol_right: self.direction = -1
        dx = player_rect.centerx - self.x
        self.direction = 1 if dx > 0 else -1
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(120, 220)
            bullets_list.append(Bullet(self.x+self.w//2, self.y+self.h//2, self.direction,
                                       is_enemy=True, color=(0,200,255)))
        if self.flash_timer > 0: self.flash_timer -= 1
    def take_hit(self, bullet_dir):
        """bullet_dir: 1=going right, -1=going left. Shield faces direction enemy is looking."""
        # Shield blocks if bullet travelling INTO the shield side
        bullet_coming_from_right = (bullet_dir < 0)  # bullet going left = came from right
        shield_on_right = (self.direction > 0)
        if self.shield_up and (bullet_coming_from_right == shield_on_right):
            self.shield_hp -= 1
            if self.shield_hp <= 0: self.shield_up = False
            return False   # blocked
        self.hp -= 1; self.flash_timer = 8
        return True
    def draw(self, surface, cam_x):
        sx = int(self.x - cam_x); sy = int(self.y)
        flash = self.flash_timer > 0
        body = (80,120,220) if not flash else (180,200,255)
        pygame.draw.rect(surface, body, (sx+4, sy+14, 28, 26), border_radius=4)
        pygame.draw.circle(surface, (100,140,240) if not flash else (200,220,255), (sx+18,sy+10), 13)
        pygame.draw.circle(surface, (200,220,255), (sx+13,sy+9), 4)
        pygame.draw.circle(surface, (200,220,255), (sx+23,sy+9), 4)
        pygame.draw.circle(surface, (0,0,0), (sx+13,sy+9), 2)
        pygame.draw.circle(surface, (0,0,0), (sx+23,sy+9), 2)
        if self.shield_up:
            sh_ratio = self.shield_hp / self.shield_max
            sh_a = int(200 * sh_ratio)
            sh_x = sx + (self.w + 2) if self.direction == 1 else sx - 14
            sh_s = pygame.Surface((14, 46), pygame.SRCALPHA)
            pygame.draw.rect(sh_s, (0,200,255,sh_a), (0,0,14,46), border_radius=7)
            pygame.draw.rect(sh_s, (200,240,255,min(255,sh_a+60)), (0,0,14,46), 2, border_radius=7)
            surface.blit(sh_s, (sh_x, sy-1))
        bar_w = 32; filled = int(bar_w * self.hp / self.max_hp)
        pygame.draw.rect(surface, (20,20,80), (sx+2, sy-8, bar_w, 4), border_radius=2)
        pygame.draw.rect(surface, (80,140,255), (sx+2, sy-8, filled, 4), border_radius=2)

# ==============================
# DRONE ENEMIES
# ==============================
class Drone:
    def __init__(self, x, y, patrol_left, patrol_right):
        self.x = float(x); self.y = float(y); self.base_y = float(y)
        self.w = 32; self.h = 24
        self.patrol_left = patrol_left; self.patrol_right = patrol_right
        self.speed = 2.2; self.direction = 1
        self.alive = True; self.hp = 2; self.max_hp = 2
        self.shoot_timer = random.randint(40,100); self.flash_timer = 0
        self.bob = random.uniform(0, math.pi*2)
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)
    def update(self, player_rect, cam_x, bullets_list):
        self.bob += 0.09
        self.x += self.speed * self.direction
        if self.x < self.patrol_left: self.direction = 1
        if self.x > self.patrol_right: self.direction = -1
        self.y = self.base_y + math.sin(self.bob) * 20
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(50, 120)
            dx = player_rect.centerx - (self.x+self.w//2)
            dy = player_rect.centery - (self.y+self.h//2)
            tot = max(1, math.sqrt(dx*dx+dy*dy)); spd = 6
            b = Bullet(self.x+self.w//2, self.y+self.h//2,
                       1 if dx>0 else -1, is_enemy=True, speed=abs(dx/tot)*spd, color=NEON_YELLOW)
            b.vy = (dy/tot)*spd; bullets_list.append(b)
        if self.flash_timer > 0: self.flash_timer -= 1
    def draw(self, surface, cam_x):
        sx = int(self.x - cam_x); sy = int(self.y)
        flash = self.flash_timer > 0
        body = (50,50,50) if not flash else (220,220,220)
        pygame.draw.ellipse(surface, body, (sx+2, sy+4, self.w-4, self.h-8))
        # Rotor arms + blades
        for rx2, ry2 in [(sx-5,sy+2),(sx+self.w-5,sy+2),(sx-5,sy+self.h-10),(sx+self.w-5,sy+self.h-10)]:
            pygame.draw.rect(surface, (80,80,80), (rx2, ry2, 10, 5), border_radius=3)
            pygame.draw.ellipse(surface, NEON_YELLOW, (rx2, ry2, 10, 4))
        # Underbelly gun
        pygame.draw.rect(surface, (100,0,0), (sx+self.w//2-3, sy+self.h-6, 6, 10), border_radius=2)
        # Red eye
        pygame.draw.circle(surface, NEON_RED, (sx+self.w//2, sy+self.h//2-1), 5)
        pygame.draw.circle(surface, (255,150,150), (sx+self.w//2, sy+self.h//2-1), 2)
        bar_w = 28; filled = int(bar_w * self.hp / self.max_hp)
        pygame.draw.rect(surface, (80,0,0), (sx+2, sy-6, bar_w, 3), border_radius=1)
        pygame.draw.rect(surface, NEON_RED, (sx+2, sy-6, filled, 3), border_radius=1)


class Bullet:
    def __init__(self, x, y, direction, is_enemy=False, speed=None, color=None):
        self.x = x; self.y = y; self.direction = direction
        self.speed = speed if speed else (12 if not is_enemy else 5)
        self.is_enemy = is_enemy; self.alive = True
        self.w = 14 if not is_enemy else 10; self.h = 5
        self.color = color
        self.vy = 0
    def update(self):
        self.x += self.speed * self.direction
        self.y += self.vy
    def draw(self, surface, cam_x):
        sx = int(self.x-cam_x); sy = int(self.y)
        if self.is_enemy:
            c = self.color if self.color else NEON_RED
            pygame.draw.ellipse(surface, c, (sx,sy-2,self.w,self.h+4))
            pygame.draw.ellipse(surface, (255,180,180), (sx+2,sy,self.w-4,self.h))
        else:
            pygame.draw.ellipse(surface, NEON_CYAN, (sx,sy,self.w,self.h))
            pygame.draw.ellipse(surface, WHITE, (sx+2,sy+1,self.w-4,self.h-2))
        for i in range(3):
            tx = sx - self.direction*(i*5)
            ac = 200-i*60
            tc = (0,ac,ac) if not self.is_enemy else (ac,0,0)
            pygame.draw.circle(surface, tc, (tx, sy+self.h//2), max(1,3-i))
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

bullets = []

class Rocket:
    def __init__(self, x, y):
        self.x = float(x); self.y = float(y)
        self.w = 60; self.h = 80
        self.alive = True
        self.activated = False
        self.launch_vy = 0.0
        self.launch_timer = 0
        self.launching = False
        self.launched = False
        self.anim = 0
        self.bob_angle = 0.0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def get_enter_rect(self):
        return pygame.Rect(int(self.x) - 20, int(self.y) - 10, self.w + 40, self.h + 20)

    def update(self, particles_list):
        self.anim += 1
        if self.launching:
            self.launch_timer -= 1
            if self.launch_timer <= 0:
                self.launch_vy -= 0.5
                self.y += self.launch_vy
                if self.anim % 2 == 0:
                    for _ in range(6):
                        particles_list.append(Particle(
                            self.x + self.w//2 + random.randint(-8,8),
                            self.y + self.h,
                            random.choice([NEON_ORANGE, NEON_YELLOW, (255,200,50)]),
                            random.uniform(-3,3), random.uniform(2,8), life=25, size=random.randint(4,9)
                        ))
                if self.y < -200:
                    self.launched = True
        else:
            self.bob_angle += 0.03
            self.y += math.sin(self.bob_angle) * 0.3

    def draw(self, surface, cam_x):
        sx = int(self.x - cam_x)
        sy = int(self.y)
        tick = pygame.time.get_ticks()

        if not self.launching:
            pulse = abs(math.sin(tick * 0.005))
            glow = pygame.Surface((self.w + 20, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (0, 200, 255, int(80 * pulse)), (0, 0, self.w + 20, 30))
            surface.blit(glow, (sx - 10, sy + self.h - 10))
        else:
            pulse2 = abs(math.sin(tick * 0.02))
            glow2 = pygame.Surface((self.w + 40, 60), pygame.SRCALPHA)
            pygame.draw.ellipse(glow2, (255, 150, 0, int(180 * pulse2)), (0, 0, self.w + 40, 60))
            surface.blit(glow2, (sx - 20, sy + self.h - 20))

        body_color = (220, 220, 240) if not self.launching else (240, 200, 180)
        pygame.draw.rect(surface, body_color, (sx + 10, sy + 20, 40, 55), border_radius=8)
        nose_color = (200, 60, 60)
        pygame.draw.polygon(surface, nose_color, [
            (sx + 30, sy),
            (sx + 10, sy + 25),
            (sx + 50, sy + 25)
        ])
        pygame.draw.circle(surface, (100, 200, 255), (sx + 30, sy + 38), 10)
        pygame.draw.circle(surface, (200, 240, 255), (sx + 30, sy + 38), 7)
        pygame.draw.circle(surface, (0, 0, 0), (sx + 30, sy + 38), 10, 2)
        pygame.draw.polygon(surface, (160, 160, 180), [
            (sx + 10, sy + 65), (sx, sy + 75), (sx + 10, sy + 75)
        ])
        pygame.draw.polygon(surface, (160, 160, 180), [
            (sx + 50, sy + 65), (sx + 60, sy + 75), (sx + 50, sy + 75)
        ])
        pygame.draw.rect(surface, (255, 80, 80), (sx + 10, sy + 50, 40, 6), border_radius=2)
        pygame.draw.rect(surface, (100, 100, 120), (sx + 17, sy + 72, 26, 10), border_radius=3)

        if not self.activated:
            prompt_font = pygame.font.SysFont("consolas", 14, bold=True)
            prompt = prompt_font.render("▶ ENTER ◀", True, NEON_YELLOW)
            shadow = prompt_font.render("▶ ENTER ◀", True, (80, 60, 0))
            surface.blit(shadow, (sx + self.w//2 - prompt.get_width()//2 + 2, sy - 28 + 2))
            surface.blit(prompt, (sx + self.w//2 - prompt.get_width()//2, sy - 28))


class Enemy:
    def __init__(self, x, y, patrol_left, patrol_right):
        self.x = float(x); self.y = float(y)
        self.w = 36; self.h = 44
        self.patrol_left = patrol_left; self.patrol_right = patrol_right
        self.speed = 1.5; self.direction = 1
        self.alive = True; self.hp = 3; self.max_hp = 3
        self.shoot_timer = random.randint(60,180)
        self.flash_timer = 0
        self.hover_angle = random.uniform(0,math.pi*2)
        self.hover_offset = 0.0
    def update(self, player_rect, cam_x, bullets_list):
        self.hover_angle += 0.06
        self.hover_offset = math.sin(self.hover_angle)*5
        self.x += self.speed*self.direction
        if self.x < self.patrol_left: self.direction = 1
        if self.x > self.patrol_right: self.direction = -1
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot_timer = random.randint(90,200)
            dx = player_rect.centerx - self.x
            shoot_dir = 1 if dx > 0 else -1
            bullets_list.append(Bullet(self.x+self.w//2, self.y+self.h//2, shoot_dir, is_enemy=True))
        if self.flash_timer > 0: self.flash_timer -= 1
    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y+self.hover_offset), self.w, self.h)
    def draw(self, surface, cam_x):
        sx = int(self.x-cam_x); sy = int(self.y+self.hover_offset)
        flash = self.flash_timer > 0
        body_col = (255,100,100) if flash else (180,30,60)
        pygame.draw.rect(surface, body_col, (sx+6,sy+14,24,22), border_radius=4)
        head_col = (255,150,150) if flash else (200,40,70)
        pygame.draw.circle(surface, head_col, (sx+18,sy+10), 12)
        pygame.draw.circle(surface, NEON_RED, (sx+13,sy+9), 4)
        pygame.draw.circle(surface, NEON_RED, (sx+23,sy+9), 4)
        pygame.draw.circle(surface, (255,200,200), (sx+13,sy+9), 2)
        pygame.draw.circle(surface, (255,200,200), (sx+23,sy+9), 2)
        pygame.draw.line(surface, NEON_PINK, (sx+18,sy-2), (sx+18,sy-12), 2)
        pygame.draw.circle(surface, NEON_PINK, (sx+18,sy-12), 3)
        bar_w = 30
        filled = int(bar_w * self.hp / self.max_hp)
        pygame.draw.rect(surface, (80,0,0), (sx+3,sy-8,bar_w,4), border_radius=2)
        pygame.draw.rect(surface, NEON_RED, (sx+3,sy-8,filled,4), border_radius=2)
        halo = pygame.Surface((self.w+20,self.h+20), pygame.SRCALPHA)
        pygame.draw.ellipse(halo, (255,0,80,25), (0,0,self.w+20,self.h+20))
        surface.blit(halo, (sx-10,sy-10))

class Boss:
    def __init__(self, x, y, level=1):
        self.x = float(x); self.y = float(y)
        self.w = 90; self.h = 100
        self.alive = True
        self.max_hp = 60; self.hp = 60
        self.flash_timer = 0
        self.phase = 1
        self.direction = -1
        self.speed = 2.0
        self.patrol_left  = x - 300
        self.patrol_right = x + 300
        self.shoot_timer = 80
        self.stomp_timer = 0
        self.stomp_active = False
        self.hover_angle = 0.0
        self.hover_offset = 0.0
        self.anim = 0
        self.level = level
        self.death_explode = 0
        self.spread_timer = 200
        self.warning_flash = 0

    def update(self, player_rect, cam_x, bullets_list, particles_list):
        self.hover_angle += 0.04
        self.hover_offset = math.sin(self.hover_angle) * 8

        if self.hp < self.max_hp * 0.5 and self.phase == 1:
            self.phase = 2
            self.speed = 3.5
            self.warning_flash = 60

        if self.warning_flash > 0:
            self.warning_flash -= 1

        if self.phase == 2:
            dx = player_rect.centerx - (self.x + self.w//2)
            self.x += self.speed * (1 if dx > 0 else -1)
        else:
            self.x += self.speed * self.direction
            if self.x < self.patrol_left: self.direction = 1
            if self.x > self.patrol_right: self.direction = -1

        self.x = max(50, min(WORLD_W - self.w - 50, self.x))

        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            rate = 50 if self.phase == 2 else 80
            self.shoot_timer = rate
            dx = player_rect.centerx - self.x
            shoot_dir = 1 if dx > 0 else -1
            spd = 7 if self.phase == 2 else 5
            bullets_list.append(Bullet(self.x+self.w//2, self.y+self.h//2, shoot_dir, is_enemy=True, speed=spd, color=NEON_ORANGE))

        if self.phase == 2:
            self.spread_timer -= 1
            if self.spread_timer <= 0:
                self.spread_timer = 120
                for angle in [-20, -10, 0, 10, 20]:
                    rad = math.radians(angle)
                    dx2 = player_rect.centerx - self.x
                    base_dir = 1 if dx2 > 0 else -1
                    bx2 = self.x+self.w//2; by2 = self.y+self.h//2
                    vx = math.cos(rad)*6*base_dir
                    vy = math.sin(rad)*6
                    b = Bullet(bx2, by2, base_dir, is_enemy=True, speed=abs(vx), color=(255,100,0))
                    b.vy = vy
                    bullets_list.append(b)
                for _ in range(30):
                    particles_list.append(Particle(
                        self.x+self.w//2, self.y+self.h//2,
                        random.choice([NEON_ORANGE, NEON_RED, NEON_YELLOW]),
                        random.uniform(-8,8), random.uniform(-8,-1), life=30
                    ))

        if self.flash_timer > 0: self.flash_timer -= 1
        self.anim += 1

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y+self.hover_offset), self.w, self.h)

    def draw(self, surface, cam_x):
        sx = int(self.x - cam_x)
        sy = int(self.y + self.hover_offset)
        flash = self.flash_timer > 0
        tick = pygame.time.get_ticks()

        if self.level == 1:
            body_col = (255,180,30) if flash else (220,150,20)
            pygame.draw.rect(surface, (200,100,0), (sx+10,sy+75,20,25), border_radius=4)
            pygame.draw.rect(surface, (200,100,0), (sx+60,sy+75,20,25), border_radius=4)
            pygame.draw.rect(surface, body_col, (sx+8,sy+35,74,50), border_radius=8)
            arm_col = (255,200,50) if flash else (200,130,10)
            pygame.draw.rect(surface, arm_col, (sx-12,sy+40,20,35), border_radius=5)
            pygame.draw.rect(surface, arm_col, (sx+82,sy+40,20,35), border_radius=5)
            pygame.draw.rect(surface, (180,80,0), (sx-16,sy+58,28,10), border_radius=3)
            pygame.draw.rect(surface, (180,80,0), (sx+78,sy+58,28,10), border_radius=3)
            head_col = (255,220,60) if flash else (230,170,20)
            pygame.draw.rect(surface, head_col, (sx+20,sy+5,50,35), border_radius=10)
            for i in range(8):
                angle = i * math.pi/4 + tick*0.003
                rx2 = sx+45 + int(math.cos(angle)*35)
                ry2 = sy+22 + int(math.sin(angle)*25)
                pygame.draw.line(surface, NEON_YELLOW, (sx+45,sy+22), (rx2,ry2), 3)
                pygame.draw.circle(surface, NEON_ORANGE, (rx2,ry2), 4)
            pygame.draw.rect(surface, (30,10,0), (sx+25,sy+12,40,18), border_radius=6)
            visor_col = NEON_ORANGE if self.phase == 2 else NEON_YELLOW
            pygame.draw.rect(surface, visor_col, (sx+27,sy+14,36,14), border_radius=5)
            pygame.draw.circle(surface, (255,100,0), (sx+45,sy+55), 12)
            pygame.draw.circle(surface, (0,0,0), (sx+45,sy+55), 8)
            pulse2 = abs(math.sin(tick*0.008))
            pygame.draw.circle(surface, (*NEON_ORANGE, int(200*pulse2)), (sx+45,sy+55), int(14+6*pulse2))
        else:
            pygame.draw.rect(surface, (60,0,100), (sx+10, sy+75, 20, 25), border_radius=4)
            pygame.draw.rect(surface, (60,0,100), (sx+60, sy+75, 20, 25), border_radius=4)
            body_col = (220,80,80) if flash else (120,0,180)
            pygame.draw.rect(surface, body_col, (sx+8, sy+35, 74, 50), border_radius=8)
            arm_col = (200,60,60) if flash else (100,0,150)
            pygame.draw.rect(surface, arm_col, (sx-12, sy+40, 20, 35), border_radius=5)
            pygame.draw.rect(surface, arm_col, (sx+82, sy+40, 20, 35), border_radius=5)
            pygame.draw.rect(surface, (50,0,80), (sx-16, sy+58, 28, 10), border_radius=3)
            pygame.draw.rect(surface, (50,0,80), (sx+78, sy+58, 28, 10), border_radius=3)
            head_col = (240,100,100) if flash else (150,20,220)
            pygame.draw.rect(surface, head_col, (sx+20, sy+5, 50, 35), border_radius=10)
            visor_col = NEON_RED if self.phase == 2 else (255,100,0)
            pygame.draw.rect(surface, (30,0,50), (sx+25, sy+12, 40, 18), border_radius=6)
            pygame.draw.rect(surface, visor_col, (sx+27, sy+14, 36, 14), border_radius=5)
            glow_pulse = abs(math.sin(tick*0.01))*100
            pygame.draw.rect(surface, (255,int(glow_pulse),0,180), (sx+30, sy+16, 30, 10), border_radius=4)
            pygame.draw.polygon(surface, (80,0,120), [(sx+8,sy+38),(sx+2,sy+25),(sx+18,sy+38)])
            pygame.draw.polygon(surface, (80,0,120), [(sx+82,sy+38),(sx+88,sy+25),(sx+72,sy+38)])
            emblem_col = NEON_YELLOW if self.phase == 2 else NEON_PINK
            pygame.draw.circle(surface, emblem_col, (sx+45, sy+55), 12)
            pygame.draw.circle(surface, (0,0,0), (sx+45, sy+55), 8)
            pulse2 = abs(math.sin(tick*0.008))
            pygame.draw.circle(surface, (*emblem_col, int(200*pulse2)), (sx+45, sy+55), int(14+6*pulse2))

        bar_w = 200
        bar_x = sx + self.w//2 - bar_w//2
        bar_y = sy - 20
        filled = int(bar_w * self.hp / self.max_hp)
        pygame.draw.rect(surface, (60,0,0), (bar_x, bar_y, bar_w, 10), border_radius=4)
        bar_color = NEON_RED if self.phase == 1 else NEON_ORANGE
        pygame.draw.rect(surface, bar_color, (bar_x, bar_y, filled, 10), border_radius=4)
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, 10), 1, border_radius=4)
        boss_label = pygame.font.SysFont("consolas",14,bold=True).render("BOSS", True, WHITE)
        surface.blit(boss_label, (bar_x + bar_w//2 - boss_label.get_width()//2, bar_y-16))

        if self.warning_flash > 0 and (self.warning_flash//5)%2 == 0:
            warn_surf = pygame.Surface((self.w+20, self.h+20), pygame.SRCALPHA)
            pygame.draw.rect(warn_surf, (255,0,0,100), (0,0,self.w+20,self.h+20), border_radius=8)
            surface.blit(warn_surf, (sx-10, sy-10))


def make_enemy_defs(level=1):
    if level == 1:
        return [
            (500,  GROUND_Y-44, 400,  700),
            (1000, GROUND_Y-44, 850,  1200),
            (1500, GROUND_Y-44, 1300, 1750),
            (950,  GROUND_Y-214, 900, 1080),
            (2000, GROUND_Y-44, 1800, 2300),
            (2600, GROUND_Y-44, 2400, 2900),
            (3000, GROUND_Y-44, 2800, 3400),
            (3500, GROUND_Y-44, 3300, 3800),
            (1380, GROUND_Y-254, 1330, 1490),
        ]
    else:
        return [
            (400,  GROUND_Y-44, 300,  700),
            (900,  GROUND_Y-44, 700,  1100),
            (1400, GROUND_Y-44, 1200, 1600),
            (880,  GROUND_Y-224, 800, 1000),
            (1900, GROUND_Y-44, 1700, 2200),
            (2500, GROUND_Y-44, 2300, 2800),
            (2900, GROUND_Y-44, 2700, 3200),
            (3400, GROUND_Y-44, 3200, 3700),
            (1340, GROUND_Y-274, 1290, 1460),
            (600,  GROUND_Y-44, 450,  800),
            (1700, GROUND_Y-44, 1500, 1950),
        ]

def make_health_pickups(level=1):
    positions = [
        (700,  GROUND_Y - 30),
        (1200, GROUND_Y - 30),
        (1800, GROUND_Y - 30),
        (2400, GROUND_Y - 30),
        (3000, GROUND_Y - 30),
        (3600, GROUND_Y - 30),
        (500,  GROUND_Y - 200),
        (1150, GROUND_Y - 180),
        (2280, GROUND_Y - 220),
    ]
    if level == 2:
        positions = [
            (650,  GROUND_Y - 30),
            (1100, GROUND_Y - 30),
            (1700, GROUND_Y - 30),
            (2300, GROUND_Y - 30),
            (2900, GROUND_Y - 30),
            (3500, GROUND_Y - 30),
            (420,  GROUND_Y - 210),
            (1100, GROUND_Y - 190),
            (2260, GROUND_Y - 230),
        ]
    return [HealthPickup(x, y) for x, y in positions]

def make_weapon_pickups(level=1):
    positions = [
        (350,  GROUND_Y-30,  "shotgun"),
        (900,  GROUND_Y-30,  "laser"),
        (1450, GROUND_Y-30,  "rocket"),
        (2100, GROUND_Y-30,  "flamethrower"),
        (2700, GROUND_Y-30,  "shotgun"),
        (3200, GROUND_Y-30,  "laser"),
        (3800, GROUND_Y-30,  "rocket"),
        # On platforms
        (500,  GROUND_Y-200, "flamethrower"),
        (1150, GROUND_Y-180, "shotgun"),
        (2500, GROUND_Y-270, "laser"),
    ]
    if level == 2:
        positions = [
            (300,  GROUND_Y-30,  "laser"),
            (850,  GROUND_Y-30,  "flamethrower"),
            (1400, GROUND_Y-30,  "shotgun"),
            (2000, GROUND_Y-30,  "rocket"),
            (2600, GROUND_Y-30,  "laser"),
            (3100, GROUND_Y-30,  "flamethrower"),
            (3700, GROUND_Y-30,  "shotgun"),
            (420,  GROUND_Y-200, "rocket"),
            (1100, GROUND_Y-180, "laser"),
            (2480, GROUND_Y-280, "flamethrower"),
        ]
    return [WeaponPickup(x, y, w) for x, y, w in positions]

def make_spike_traps(level=1):
    """Spike traps on the ground at dangerous spots."""
    xs = [460, 780, 1250, 1700, 2150, 2600, 3050, 3500, 3850]
    if level == 2:
        xs = [380, 700, 1150, 1620, 2080, 2540, 2990, 3440, 3790]
    return [SpikeTrap(x, GROUND_Y - 16, random.choice([33, 44, 55])) for x in xs]

def make_turrets(level=1):
    defs = [
        (820,  GROUND_Y-40),
        (1600, GROUND_Y-40),
        (2400, GROUND_Y-40),
        (3100, GROUND_Y-40),
        # On elevated positions
        (1150, GROUND_Y-150-40),
        (2280, GROUND_Y-190-40),
    ]
    if level == 2:
        defs = [
            (750,  GROUND_Y-40),
            (1500, GROUND_Y-40),
            (2300, GROUND_Y-40),
            (3000, GROUND_Y-40),
            (3600, GROUND_Y-40),
            (1100, GROUND_Y-160-40),
            (2260, GROUND_Y-200-40),
        ]
    return [Turret(x, y) for x, y in defs]

def make_shield_enemies(level=1):
    defs = [
        (650,  GROUND_Y-48, 500, 800),
        (1300, GROUND_Y-48, 1100,1550),
        (2200, GROUND_Y-48, 2000,2500),
        (3300, GROUND_Y-48, 3100,3600),
    ]
    if level == 2:
        defs = [
            (600,  GROUND_Y-48, 450, 750),
            (1250, GROUND_Y-48, 1050,1500),
            (2150, GROUND_Y-48, 1950,2450),
            (2900, GROUND_Y-48, 2700,3150),
            (3450, GROUND_Y-48, 3250,3700),
        ]
    return [ShieldEnemy(x,y,pl,pr) for x,y,pl,pr in defs]

def make_drones(level=1):
    defs = [
        (3150, GROUND_Y-160, 3000,3400),
        (3700, GROUND_Y-140, 3550,3900),
    ]
    if level == 2:
        defs = [
            (350,  GROUND_Y-160, 200, 550),
            (950,  GROUND_Y-150, 800,1150),

        ]
    return [Drone(x,y,pl,pr) for x,y,pl,pr in defs]


def init_level(level, carry_hp=5, carry_score=0, carry_weapon="blaster", carry_ammo=0):
    random.seed(level * 7 + 13)
    e_defs = make_enemy_defs(level)
    enemies_new = [Enemy(x,y,pl,pr) for x,y,pl,pr in e_defs]
    boss_x = WORLD_W - 600
    boss_new = Boss(boss_x, GROUND_Y - 110, level=level)
    health_pickups = make_health_pickups(level)
    rocket = Rocket(boss_x + 50, GROUND_Y - 90)

    return {
        "enemies": enemies_new,
        "boss": boss_new,
        "boss_dead": False,
        "rocket": rocket,
        "rocket_visible": False,
        "rocket_entered": False,
        "health_pickups": health_pickups,
        "weapon_pickups": make_weapon_pickups(level),
        "spike_traps": make_spike_traps(level),
        "turrets": make_turrets(level),
        "shield_enemies": make_shield_enemies(level),
        "drones": make_drones(level),
        "bullets": [],
        "particles": [],
        "player_rect": pygame.Rect(100, GROUND_Y-player_height, player_width, player_height),
        "velocity_y": 0,
        "on_ground": True,
        "air_frames": 0,
        "facing_right": True,
        "frame_index": 0.0,
        "state": "stand",
        "player_hp": carry_hp,
        "invincible": 0,
        "shoot_cooldown": 0,
        "is_shooting": 0,
        "score": carry_score,
        "kill_count": 0,
        "super_ready": False,
        "super_stacks": 0,
        "mega_ready": False,
        "mega_active": 0,
        "mega_anim": 0,
        "mega_missile_phase": 0,
        "mega_missiles": [],
        "mega_missile_x": 0.0,
        "mega_missile_y": 0.0,
        "mega_impact_timer": 0,
        "super_active": 0,
        "super_cooldown": 0,
        "is_super_pose": 0,
        "shake_x": 0, "shake_y": 0, "shake_timer": 0,
        "cinematic_alpha": 0, "cinematic_bars": 0,
        "camera_x": 0.0,
        "level_complete": False,
        "level_complete_timer": 0,
        "boss_health_bar_flash": 0,
        "show_boss_warning": False,
        "boss_warning_timer": 0,
        "boss_seen": False,
        "player_in_rocket": False,
        "boarding_timer": 0,
        # Weapon system
        "weapon": carry_weapon,
        "weapon_ammo": carry_ammo,
        "weapon_pickup_flash": 0,
        "flame_active": 0,
        "rocket_charge": 0,
    }

font_big   = pygame.font.SysFont("consolas", 28, bold=True)
font_med   = pygame.font.SysFont("consolas", 22, bold=True)
font_small = pygame.font.SysFont("consolas", 18)
KILLS_FOR_SUPER  = 3
SUPER_DURATION   = 300
# Mega cinematic phases:
#  0 = robot descends          (MEGA_ROBOT_DESCENT frames)
#  1 = missile rain + damage   (MEGA_FIRE_FRAMES frames)
#  2 = cleanup explosions      (MEGA_IMPACT_FRAMES frames)
#  3 = robot exits             (MEGA_EXIT_FRAMES frames)
MEGA_ROBOT_DESCENT = 70
MEGA_FIRE_FRAMES   = 200   # duration of missile barrage
MEGA_IMPACT_FRAMES = 60    # post-barrage carnage
MEGA_EXIT_FRAMES   = 55
MEGA_TOTAL = MEGA_ROBOT_DESCENT + MEGA_FIRE_FRAMES + MEGA_IMPACT_FRAMES + MEGA_EXIT_FRAMES
MEGA_MISSILE_SPEED = 7     # pixels per frame falling missiles travel


def _draw_nemesis(surface, rx, ry, firing=False, rage=0.0):
    """Draw the NEMESIS black-and-red mech robot.
    firing=True = arms raised, launching missiles.
    rage 0..1 = how crazed the glow/effects are."""
    tick = pygame.time.get_ticks()
    pulse = abs(math.sin(tick * 0.01))
    rage_pulse = abs(math.sin(tick * 0.025))

    # ---- Dark red aura / shadow behind robot ----
    aura_r = int(90 + 30 * rage * pulse)
    aura = pygame.Surface((aura_r*2, aura_r*2), pygame.SRCALPHA)
    pygame.draw.ellipse(aura, (180, 0, 0, int((40 + 60*rage) * pulse)), (0, 0, aura_r*2, aura_r*2))
    surface.blit(aura, (rx + 70 - aura_r, ry + 90 - aura_r))

    # ---- Legs ----
    leg_col = (18, 0, 0)
    pygame.draw.rect(surface, leg_col,    (rx + 24, ry + 132, 24, 40), border_radius=4)
    pygame.draw.rect(surface, leg_col,    (rx + 92, ry + 132, 24, 40), border_radius=4)
    # Knee armour plates
    pygame.draw.rect(surface, (140, 0, 0), (rx + 20, ry + 144, 32, 12), border_radius=3)
    pygame.draw.rect(surface, (140, 0, 0), (rx + 88, ry + 144, 32, 12), border_radius=3)
    # Feet
    pygame.draw.rect(surface, (25, 0, 0),  (rx + 14, ry + 166, 40, 12), border_radius=4)
    pygame.draw.rect(surface, (25, 0, 0),  (rx + 82, ry + 166, 40, 12), border_radius=4)
    # Thruster glow under feet
    for fx in [rx + 28, rx + 96]:
        ts = pygame.Surface((28, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(ts, (255, 40, 0, int(140 + 80*pulse)), (0, 0, 28, 16))
        surface.blit(ts, (fx - 4, ry + 174))

    # ---- Body ----
    pygame.draw.rect(surface, (12, 0, 0),   (rx + 10, ry + 56, 120, 84), border_radius=10)
    # Red chest panel
    pygame.draw.rect(surface, (160, 0, 0),  (rx + 18, ry + 62, 104, 30), border_radius=6)
    # Rivet detail lines
    for i in range(3):
        pygame.draw.line(surface, (60, 0, 0), (rx+18, ry+72+i*8), (rx+122, ry+72+i*8), 1)
    # Waist band
    pygame.draw.rect(surface, (100, 0, 0),  (rx + 10, ry + 126, 120, 10), border_radius=3)

    # ---- Missile pod shoulder cannons (raised when firing) ----
    arm_raise = -18 if firing else 0
    # Left arm
    pygame.draw.rect(surface, (20, 0, 0),   (rx - 28, ry + 64 + arm_raise, 40, 60), border_radius=7)
    pygame.draw.rect(surface, (120, 0, 0),  (rx - 28, ry + 64 + arm_raise, 40, 10), border_radius=4)
    # Left missile pod (3 barrels)
    for bi in range(3):
        bx2 = rx - 30 + bi * 8
        by2 = ry + 58 + arm_raise
        pygame.draw.rect(surface, (50, 0, 0), (bx2, by2, 6, 18), border_radius=2)
        pygame.draw.rect(surface, (200, 0, 0), (bx2+1, by2, 4, 3))
    # Right arm
    pygame.draw.rect(surface, (20, 0, 0),   (rx + 128, ry + 64 + arm_raise, 40, 60), border_radius=7)
    pygame.draw.rect(surface, (120, 0, 0),  (rx + 128, ry + 64 + arm_raise, 40, 10), border_radius=4)
    # Right missile pod (3 barrels)
    for bi in range(3):
        bx2 = rx + 130 + bi * 8
        by2 = ry + 58 + arm_raise
        pygame.draw.rect(surface, (50, 0, 0), (bx2, by2, 6, 18), border_radius=2)
        pygame.draw.rect(surface, (200, 0, 0), (bx2+1, by2, 4, 3))

    # ---- Shoulder armour spikes ----
    # Left
    pygame.draw.polygon(surface, (100, 0, 0), [(rx+10,ry+58),(rx-4,ry+36),(rx+20,ry+58)])
    pygame.draw.polygon(surface, (60,  0, 0), [(rx+22,ry+58),(rx+10,ry+34),(rx+30,ry+58)])
    # Right
    pygame.draw.polygon(surface, (100, 0, 0), [(rx+130,ry+58),(rx+144,ry+36),(rx+120,ry+58)])
    pygame.draw.polygon(surface, (60,  0, 0), [(rx+118,ry+58),(rx+130,ry+34),(rx+110,ry+58)])

    # ---- Core eye on chest (glows red) ----
    core_r = int(12 + 6 * rage * rage_pulse)
    pygame.draw.circle(surface, (8, 0, 0),   (rx + 70, ry + 98), core_r + 6)
    pygame.draw.circle(surface, (200, 0, 0), (rx + 70, ry + 98), core_r)
    pygame.draw.circle(surface, (255, 80, 80),(rx + 70, ry + 98), max(1, core_r - 5))
    # Core glow ring
    cgs = pygame.Surface(((core_r+14)*2, (core_r+14)*2), pygame.SRCALPHA)
    pygame.draw.circle(cgs, (255, 0, 0, int(90 * rage_pulse * (0.5 + rage*0.5))),
                       (core_r+14, core_r+14), core_r+14)
    surface.blit(cgs, (rx+70-(core_r+14), ry+98-(core_r+14)))

    # ---- Head ----
    pygame.draw.rect(surface, (15, 0, 0),   (rx + 22, ry + 6, 96, 54), border_radius=8)
    # Head armour ridge
    pygame.draw.rect(surface, (80, 0, 0),   (rx + 22, ry + 6, 96, 8),  border_radius=4)
    # Horn / crest spikes on top
    pygame.draw.polygon(surface, (140, 0, 0), [(rx+55,ry+6),(rx+60,ry-18),(rx+65,ry+6)])
    pygame.draw.polygon(surface, (100, 0, 0), [(rx+68,ry+6),(rx+72,ry-12),(rx+76,ry+6)])
    pygame.draw.polygon(surface, (140, 0, 0), [(rx+76,ry+6),(rx+80,ry-18),(rx+85,ry+6)])

    # ---- Visor: single glowing red slit ----
    pygame.draw.rect(surface, (5, 0, 0),    (rx + 28, ry + 22, 84, 22), border_radius=5)
    visor_intensity = int(180 + 75 * rage_pulse * (0.4 + rage * 0.6))
    pygame.draw.rect(surface, (visor_intensity, 0, 0), (rx+30, ry+25, 80, 16), border_radius=4)
    # Visor inner bright line
    pygame.draw.rect(surface, (255, min(255,int(80*rage)), 0), (rx+30, ry+28, 80, 4))
    # Visor flicker glow
    vg = pygame.Surface((80, 16), pygame.SRCALPHA)
    vg.fill((255, 0, 0, int(60 * pulse)))
    surface.blit(vg, (rx + 30, ry + 25))

    # ---- Battle damage scratches ----
    for sx, sy, ex2, ey2 in [(rx+35,ry+70,rx+50,ry+82),(rx+90,ry+65,rx+100,ry+75),(rx+60,ry+108,rx+72,ry+118)]:
        pygame.draw.line(surface, (60,0,0), (sx,sy),(ex2,ey2), 2)

    # ---- Name tag ----
    nf = pygame.font.SysFont("consolas", 13, bold=True)
    ns = nf.render("NEMESIS", True, (220, 0, 0))
    nsh = nf.render("NEMESIS", True, (0, 0, 0))
    surface.blit(nsh, (rx + 70 - ns.get_width()//2 + 1, ry + 178 + 1))
    surface.blit(ns,  (rx + 70 - ns.get_width()//2,     ry + 178))


def draw_mega_cinematic(surface, gs):
    """NEMESIS robot descends → rains missiles → carnage → flies away."""
    tick = pygame.time.get_ticks()
    phase = gs["mega_missile_phase"]
    ma    = gs["mega_anim"]

    # Cinematic letterbox (all phases)
    bar_h = 72
    bar_surf = pygame.Surface((WIDTH, bar_h), pygame.SRCALPHA)
    bar_surf.fill((0, 0, 0, 220))
    surface.blit(bar_surf, (0, 0))
    surface.blit(bar_surf, (0, HEIGHT - bar_h))

    robot_target_y = 48
    robot_w = 160
    rx_center = WIDTH // 2 - robot_w // 2

    # ---- Helper: draw one falling missile ----
    def draw_falling_missile(mx, my, trail_age=0):
        mxi, myi = int(mx), int(my)
        # Trail upward
        for i in range(min(50, trail_age + 1)):
            ty = myi - i * 3
            size = max(1, int(7 * (1 - i/50)))
            if i < 8:   col = (255, 255, 200)
            elif i < 20: col = random.choice([(255,180,0),(255,120,0)])
            else:        col = random.choice([(180,60,0),(120,30,0)])
            pygame.draw.circle(surface, col, (mxi + random.randint(-2,2), ty), size)
        # Missile body (pointing down)
        pygame.draw.ellipse(surface, (30, 30, 30),   (mxi-7, myi-26, 14, 32))
        pygame.draw.polygon(surface, (180, 0, 0), [   # nose tip (bottom)
            (mxi, myi+10), (mxi-7, myi-6), (mxi+7, myi-6)
        ])
        # Fins
        pygame.draw.polygon(surface, (80, 0, 0), [(mxi-7,myi-26),(mxi-16,myi-14),(mxi-7,myi-14)])
        pygame.draw.polygon(surface, (80, 0, 0), [(mxi+7,myi-26),(mxi+16,myi-14),(mxi+7,myi-14)])
        # Nozzle flame (top)
        nf_p = abs(math.sin(tick * 0.06 + mx * 0.1))
        ns2 = pygame.Surface((22, 22), pygame.SRCALPHA)
        pygame.draw.circle(ns2, (255, 120, 0, int(200 * nf_p)), (11, 11), int(8 + 5*nf_p))
        pygame.draw.circle(ns2, (255, 255, 180, 220), (11, 11), 4)
        surface.blit(ns2, (mxi - 11, myi - 38))

    # ================================================================
    if phase == 0:
        # ROBOT DESCENDS — red thrusters blazing
        t = ma / MEGA_ROBOT_DESCENT
        ease = 1 - (1-t)**3
        ry = int(-220 + (robot_target_y + 220) * ease)

        # Heavy thruster exhaust
        if ma % 2 == 0:
            for _ in range(8):
                ex = rx_center + 70 + random.randint(-35, 35)
                ey = ry + 175 + random.randint(0, 20)
                pygame.draw.circle(surface,
                    random.choice([(255,40,0),(220,0,0),(255,120,0),(180,0,0)]),
                    (ex, ey), random.randint(5, 14))

        _draw_nemesis(surface, rx_center, ry, firing=False, rage=t * 0.4)

        # "NEMESIS INBOUND" text
        if (ma // 5) % 2 == 0:
            font_warn = pygame.font.SysFont("consolas", 30, bold=True)
            ws = "⚠  NEMESIS INBOUND  ⚠"
            wt  = font_warn.render(ws, True, (220, 0, 0))
            wsh = font_warn.render(ws, True, (0, 0, 0))
            wx = WIDTH//2 - wt.get_width()//2
            surface.blit(wsh, (wx+2, HEIGHT - bar_h - 42 + 2))
            surface.blit(wt,  (wx,   HEIGHT - bar_h - 42))

    # ================================================================
    elif phase == 1:
        # ROBOT HOVERS + RAINS DOWN MISSILES
        ry = robot_target_y + int(math.sin(tick * 0.005) * 5)
        rage = min(1.0, ma / MEGA_FIRE_FRAMES)
        _draw_nemesis(surface, rx_center, ry, firing=True, rage=rage)

        # Draw all active falling missiles
        for m in gs.get("mega_missiles", []):
            draw_falling_missile(m["x"], m["y"], trail_age=m.get("age", 0))

        # Title
        fade_in = min(1.0, ma / 20)
        if fade_in > 0.05:
            font_mega = pygame.font.SysFont("consolas", 40, bold=True)
            lbl_str = "★  MEGA ROBOT  ★"
            lbl  = font_mega.render(lbl_str, True, (220, 0, 0))
            sh   = font_mega.render(lbl_str, True, (0, 0, 0))
            lbl.set_alpha(int(255 * fade_in))
            sh.set_alpha(int(255 * fade_in))
            lx = WIDTH//2 - lbl.get_width()//2
            surface.blit(sh,  (lx+3, HEIGHT - bar_h - 48 + 3))
            surface.blit(lbl, (lx,   HEIGHT - bar_h - 48))
            sub = font_med.render("MISSILE BARRAGE", True, NEON_YELLOW)
            sub.set_alpha(int(255 * fade_in))
            surface.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT - bar_h - 20))

    # ================================================================
    elif phase == 2:
        # FINAL SALVO EXPLOSIONS — robot hovers triumphantly
        ry = robot_target_y + int(math.sin(tick * 0.005) * 4)
        _draw_nemesis(surface, rx_center, ry, firing=True, rage=1.0)

        # Any remaining missiles still fall
        for m in gs.get("mega_missiles", []):
            draw_falling_missile(m["x"], m["y"], trail_age=m.get("age", 0))

        # Red screen flicker
        if random.random() < 0.3:
            fl = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fl.fill((180, 0, 0, random.randint(10, 40)))
            surface.blit(fl, (0, 0))

        # Title still showing
        font_mega = pygame.font.SysFont("consolas", 40, bold=True)
        lbl_str = "★  MEGA ROBOT  ★"
        fade_out = gs["mega_active"] / max(1, MEGA_EXIT_FRAMES)
        la = int(255 * min(1.0, fade_out * 3))
        lbl  = font_mega.render(lbl_str, True, (220, 0, 0))
        sh   = font_mega.render(lbl_str, True, (0, 0, 0))
        lbl.set_alpha(la); sh.set_alpha(la)
        lx = WIDTH//2 - lbl.get_width()//2
        surface.blit(sh,  (lx+3, HEIGHT - bar_h - 48 + 3))
        surface.blit(lbl, (lx,   HEIGHT - bar_h - 48))

        bar_surf2 = pygame.Surface((WIDTH, bar_h), pygame.SRCALPHA)
        bar_surf2.fill((0, 0, 0, 200))
        surface.blit(bar_surf2, (0, 0))
        surface.blit(bar_surf2, (0, HEIGHT - bar_h))

    # ================================================================
    elif phase == 3:
        # ROBOT FLIES AWAY
        t = ma / MEGA_EXIT_FRAMES
        ease_out = t * t
        ry = int(robot_target_y - 260 * ease_out)

        if ma % 2 == 0:
            for _ in range(int(5 + 12*ease_out)):
                ex = rx_center + 70 + random.randint(-35, 35)
                ey = ry + 175 + random.randint(0, 20)
                pygame.draw.circle(surface,
                    random.choice([(255,40,0),(200,0,0),(255,100,0)]),
                    (ex, ey), random.randint(4, int(8 + 10*ease_out)))

        fade = max(0.0, 1.0 - ease_out * 1.2)
        if fade > 0:
            rs = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            _draw_nemesis(rs, rx_center, ry, firing=False, rage=0.0)
            rs.set_alpha(int(255 * fade))
            surface.blit(rs, (0, 0))

        if fade > 0.1:
            dep = font_med.render("NEMESIS DEPARTING", True, (180, 0, 0))
            dep.set_alpha(int(200 * fade))
            surface.blit(dep, (WIDTH//2 - dep.get_width()//2, HEIGHT - bar_h - 28))


def draw_text_with_shadow(surface, text, font, color, shadow_color, x, y):
    shadow_surf = font.render(text, True, shadow_color)
    text_surf   = font.render(text, True, color)
    surface.blit(shadow_surf, (x+2, y+2))
    surface.blit(text_surf,   (x, y))


def draw_hud(hp, sc, kill_count, super_ready, super_stacks, mega_ready, level):
    tick_hud = pygame.time.get_ticks()

    if level == 1:
        score_color   = (20, 80, 180)
        label_color   = (180, 40, 0)
        hp_color      = (200, 50, 0)
        shadow_color  = (255, 255, 255)
        outline_color = (255,255,255)
        panel_alpha   = 130
    else:
        score_color   = NEON_CYAN
        label_color   = NEON_PINK
        hp_color      = NEON_PINK
        shadow_color  = (0, 0, 0)
        outline_color = (0,0,0)
        panel_alpha   = 160

    # ---- Main HUD panel (bottom-left style) ----
    panel_w, panel_h = 310, 100
    panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel.fill((0, 0, 0, panel_alpha))
    # Accent border line on right + bottom
    pygame.draw.line(panel, (*label_color, 180), (panel_w-1, 0), (panel_w-1, panel_h), 2)
    pygame.draw.line(panel, (*label_color, 180), (0, panel_h-1), (panel_w, panel_h-1), 2)
    screen.blit(panel, (6, 6))

    # Score
    draw_text_with_shadow(screen, f"SCORE  {sc:06d}", font_big, score_color, shadow_color, 14, 10)

    # HP row
    draw_text_with_shadow(screen, "HP", font_small, label_color, shadow_color, 14, 44)
    for i in range(5):
        col = hp_color if i < hp else ((80, 40, 40) if level == 1 else (60,20,40))
        rx = 44 + i * 24
        # Heart shape using two circles + triangle approximation
        pygame.draw.circle(screen, col, (rx + 5, 51), 6)
        pygame.draw.circle(screen, col, (rx + 13, 51), 6)
        pygame.draw.polygon(screen, col, [(rx, 54), (rx + 18, 54), (rx + 9, 64)])
        pygame.draw.circle(screen, outline_color, (rx + 5, 51), 6, 1)
        pygame.draw.circle(screen, outline_color, (rx + 13, 51), 6, 1)

    # Kill gauge row
    draw_text_with_shadow(screen, "KILLS", font_small, label_color, shadow_color, 14, 68)
    gauge_x = 68
    gauge_y = 70
    gauge_w = 180
    gauge_h = 12
    # Background track
    pygame.draw.rect(screen, (30, 30, 30, 200), (gauge_x, gauge_y, gauge_w, gauge_h), border_radius=6)
    # Fill
    fill_w = int(gauge_w * (kill_count / KILLS_FOR_SUPER))
    if fill_w > 0:
        fill_col = NEON_YELLOW if level == 1 else NEON_CYAN
        pygame.draw.rect(screen, fill_col, (gauge_x, gauge_y, fill_w, gauge_h), border_radius=6)
    pygame.draw.rect(screen, outline_color, (gauge_x, gauge_y, gauge_w, gauge_h), 1, border_radius=6)
    # Tick marks
    for i in range(1, KILLS_FOR_SUPER):
        tx = gauge_x + int(gauge_w * i / KILLS_FOR_SUPER)
        pygame.draw.line(screen, outline_color, (tx, gauge_y), (tx, gauge_y + gauge_h), 1)

    # Bank row — stacked super orbs
    draw_text_with_shadow(screen, "BANK", font_small, label_color, shadow_color, 14, 88)
    for i in range(2):
        banked = i < super_stacks
        bx2 = 68 + i * 36
        by2 = 88
        orb_col = (255, 80, 255) if (banked and mega_ready) else ((255, 180, 0) if banked else (40, 35, 10))
        # Orb glow if ready
        if banked:
            glow_s = pygame.Surface((34, 24), pygame.SRCALPHA)
            glow_col = (255, 80, 255, 60) if mega_ready else (255, 180, 0, 50)
            pygame.draw.ellipse(glow_s, glow_col, (0, 0, 34, 24))
            screen.blit(glow_s, (bx2 - 2, by2 - 2))
        pygame.draw.rect(screen, orb_col, (bx2, by2, 28, 16), border_radius=5)
        pygame.draw.rect(screen, outline_color, (bx2, by2, 28, 16), 1, border_radius=5)
        if banked:
            star = font_small.render("★", True, WHITE)
            screen.blit(star, (bx2 + 5, by2 - 1))

    # ---- Level badge (top right) ----
    lv_panel = pygame.Surface((110, 32), pygame.SRCALPHA)
    lv_panel.fill((0, 0, 0, panel_alpha))
    pygame.draw.line(lv_panel, (*label_color, 180), (0, 0), (0, 32), 2)
    pygame.draw.line(lv_panel, (*label_color, 180), (0, 31), (110, 31), 2)
    screen.blit(lv_panel, (WIDTH-116, 6))
    lv_col = NEON_YELLOW if level==2 else (255, 200, 0)
    draw_text_with_shadow(screen, f"LEVEL  {level}", font_small, lv_col, shadow_color, WIDTH-110, 12)

    # ---- Super / Mega announcement (top-center) ----
    if mega_ready:
        pulse_t = abs(math.sin(tick_hud * 0.008))
        banner_w = 440
        mega_bg = pygame.Surface((banner_w, 40), pygame.SRCALPHA)
        mega_bg.fill((60, 0, 60, 170))
        border_col = (255, 50, 255) if (tick_hud//150)%2==0 else NEON_YELLOW
        pygame.draw.rect(mega_bg, (*border_col, 220), (0, 0, banner_w, 40), 2, border_radius=5)
        screen.blit(mega_bg, (WIDTH//2 - banner_w//2, 4))
        txt = "[ Q ]  ★ MEGA ROBOT READY! ★"
        draw_text_with_shadow(screen, txt, font_big, (255, 80, 255), (40, 0, 40),
                              WIDTH//2 - font_big.size(txt)[0]//2, 10)
    elif super_ready:
        banner_w = 380
        s_bg = pygame.Surface((banner_w, 38), pygame.SRCALPHA)
        s_bg.fill((0, 0, 0, 150))
        pygame.draw.rect(s_bg, (*(NEON_YELLOW if level==1 else NEON_CYAN), 180), (0, 0, banner_w, 38), 2, border_radius=5)
        screen.blit(s_bg, (WIDTH//2 - banner_w//2, 5))
        flash_col = (255, 180, 0) if level == 1 else NEON_YELLOW
        txt = "[ Q ]  SUPER LASER READY!"
        draw_text_with_shadow(screen, txt, font_big, flash_col, shadow_color,
                              WIDTH//2 - font_big.size(txt)[0]//2, 10)

    # ---- Controls hint ----
    hint_text = "← → MOVE   ↑ JUMP   SPACE SHOOT   Q SUPER"
    hint_w = font_small.size(hint_text)[0]
    hint_panel = pygame.Surface((hint_w + 20, 24), pygame.SRCALPHA)
    hint_panel.fill((0, 0, 0, 130))
    screen.blit(hint_panel, (WIDTH//2 - hint_w//2 - 10, HEIGHT - 28))
    hint_col = (60, 100, 200) if level == 1 else (100,150,200)
    draw_text_with_shadow(screen, hint_text, font_small, hint_col, shadow_color,
                          WIDTH//2 - hint_w//2, HEIGHT-25)


def get_frame(state, is_shooting, is_super_pose, velocity_y, frame_index):
    if (is_shooting > 0 or is_super_pose > 0) and shoot_frames:
        return shoot_frames[0]
    if state == "walk" and walk_frames:
        return walk_frames[int(frame_index)%len(walk_frames)]
    elif state == "jump" and jump_frames:
        return jump_frames[-1] if velocity_y > 1 else jump_frames[0]
    return stand_frames[0] if stand_frames else None

def draw_background(cam_x, level):
    if level == 1:
        screen.blit(sky_surface_day, (0,0))
        screen.blit(sun_surface, (WIDTH-250 - int(cam_x*0.01) % 100, 20))
        cloud_scroll = int(cam_x*0.15) % (WORLD_W*2)
        screen.blit(cloud_surface, (-cloud_scroll, 0))
        screen.blit(cloud_surface, (WORLD_W*2-cloud_scroll, 0))
        build_scroll = int(cam_x*0.3) % BUILD_W
        screen.blit(build_surface_day, (-build_scroll, 0))
        screen.blit(build_surface_day, (BUILD_W-build_scroll, 0))
        ground_scroll = int(cam_x) % WORLD_W
        screen.blit(ground_surface_day, (-ground_scroll, GROUND_Y))
        screen.blit(ground_surface_day, (WORLD_W-ground_scroll, GROUND_Y))
    else:
        screen.blit(sky_surface_night, (0,0))
        star_scroll = int(cam_x*0.05) % STAR_W
        screen.blit(star_surface, (-star_scroll,0))
        screen.blit(star_surface, (STAR_W-star_scroll,0))
        build_scroll = int(cam_x*0.3) % BUILD_W
        screen.blit(build_surface_night, (-build_scroll,0))
        screen.blit(build_surface_night, (BUILD_W-build_scroll,0))
        grid_scroll = int(cam_x) % GRID_W
        screen.blit(grid_surface, (-grid_scroll, GROUND_Y))
        screen.blit(grid_surface, (GRID_W-grid_scroll, GROUND_Y))
        ground_scroll = int(cam_x) % WORLD_W
        screen.blit(ground_surface_night, (-ground_scroll, GROUND_Y))
        screen.blit(ground_surface_night, (WORLD_W-ground_scroll, GROUND_Y))


def draw_start_screen():
    """Simple title screen."""
    t = pygame.time.get_ticks()
    screen.fill((5, 5, 20))

    # Title
    pulse = abs(math.sin(t * 0.002))
    title_col = tuple(int(a * (0.7 + 0.3 * pulse)) for a in NEON_CYAN)
    title = pygame.font.SysFont("consolas", 64, bold=True).render("ASTRO BOY", True, title_col)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 160))

    sub = pygame.font.SysFont("consolas", 20, bold=True).render("CITY DEFENDER", True, NEON_YELLOW)
    screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 240))

    # Controls
    lines = [
        ("← →   Move",       WHITE),
        ("↑      Jump",       WHITE),
        ("SPACE  Shoot",      WHITE),
        ("Q      Super / Mega", WHITE),
    ]


    # Blinking press enter
    if (t // 500) % 2 == 0:
        enter = pygame.font.SysFont("consolas", 22, bold=True).render("PRESS ENTER TO PLAY", True, NEON_CYAN)
        screen.blit(enter, (WIDTH//2 - enter.get_width()//2, 460))


# ==============================
# WEAPON FIRE HELPERS
# ==============================
def fire_weapon(gs, screen_particles=None):
    """Fire the current weapon. Returns list of new bullets to add."""
    weapon = gs["weapon"]
    pr = gs["player_rect"]
    facing = gs["facing_right"]
    bx2 = pr.right if facing else pr.left - 14
    by2 = pr.centery - 2
    dir2 = 1 if facing else -1
    new_bullets = []

    if weapon == "blaster":
        gs["shoot_cooldown"] = 18
        b = Bullet(bx2, by2, dir2)
        new_bullets.append(b)
        for _ in range(5):
            gs["particles"].append(Particle(
                bx2+(7 if facing else 0), by2, NEON_CYAN,
                random.uniform(1,4)*dir2, random.uniform(-2,2), life=10))

    elif weapon == "shotgun":
        if gs["weapon_ammo"] <= 0:
            gs["weapon"] = "blaster"; return fire_weapon(gs)
        gs["shoot_cooldown"] = 30
        gs["weapon_ammo"] -= 1
        for angle in [-0.25, -0.12, 0, 0.12, 0.25]:
            b = Bullet(bx2, by2, dir2, speed=11, color=NEON_ORANGE)
            b.vy = math.sin(angle) * 11
            b.speed = math.cos(angle) * 11
            new_bullets.append(b)
        for _ in range(12):
            gs["particles"].append(Particle(bx2, by2, NEON_ORANGE,
                random.uniform(-3,3)*dir2, random.uniform(-3,3), life=14, size=3))

    elif weapon == "laser":
        if gs["weapon_ammo"] <= 0:
            gs["weapon"] = "blaster"; return fire_weapon(gs)
        gs["shoot_cooldown"] = 4   # rapid fire
        gs["weapon_ammo"] -= 1
        b = Bullet(bx2, by2, dir2, speed=18, color=NEON_GREEN)
        b.w = 20; b.h = 3
        new_bullets.append(b)
        gs["particles"].append(Particle(bx2, by2, NEON_GREEN,
            random.uniform(-1,1), random.uniform(-1,1), life=8, size=4))

    elif weapon == "rocket":
        if gs["weapon_ammo"] <= 0:
            gs["weapon"] = "blaster"; return fire_weapon(gs)
        gs["shoot_cooldown"] = 45
        gs["weapon_ammo"] -= 1
        b = Bullet(bx2, by2, dir2, speed=9, color=NEON_RED)
        b.w = 22; b.h = 8
        b.is_rocket_proj = True
        new_bullets.append(b)
        for _ in range(8):
            gs["particles"].append(Particle(bx2, by2, NEON_ORANGE,
                random.uniform(-2,0)*dir2, random.uniform(-2,2), life=18, size=5))

    elif weapon == "flamethrower":
        if gs["weapon_ammo"] <= 0:
            gs["weapon"] = "blaster"; return fire_weapon(gs)
        gs["shoot_cooldown"] = 3
        gs["weapon_ammo"] -= 1
        gs["flame_active"] = 12
        # Spawn many short-range particles that act as bullets
        for _ in range(6):
            spread = random.uniform(-0.3, 0.3)
            spd = random.uniform(6, 12)
            b = Bullet(bx2, by2, dir2, speed=spd*math.cos(spread), color=(255, random.randint(60,160), 0))
            b.vy = math.sin(spread)*spd
            b.w = 10; b.h = 10
            b.is_flame = True
            b.life = random.randint(8, 14)
            new_bullets.append(b)
        for _ in range(10):
            gs["particles"].append(Particle(bx2, by2, (255, random.randint(80,200), 0),
                random.uniform(3,10)*dir2, random.uniform(-3,3), life=random.randint(8,16), size=random.randint(4,9)))

    gs["is_shooting"] = 10
    return new_bullets


def explode_rocket_proj(gs, bx2, by2):
    """Create explosion when rocket projectile hits something."""
    gs["shake_timer"] = max(gs["shake_timer"], 20)
    for _ in range(40):
        gs["particles"].append(Particle(bx2, by2,
            random.choice([NEON_RED, NEON_ORANGE, NEON_YELLOW, WHITE]),
            random.uniform(-8,8), random.uniform(-9,-1), life=random.randint(20,45), size=random.randint(4,10)))
    # Damage enemies/boss in radius
    BLAST_R = 120
    for e in gs["enemies"]:
        if e.alive:
            dx = (e.x+e.w//2) - bx2; dy = (e.y+e.h//2) - by2
            if dx*dx+dy*dy < BLAST_R*BLAST_R:
                e.hp -= 2; e.flash_timer = 8
                if e.hp <= 0:
                    e.alive = False; gs["score"] += 100; gs["kill_count"] += 1
    for se in gs["shield_enemies"]:
        if se.alive:
            dx = (se.x+se.w//2) - bx2; dy = (se.y+se.h//2) - by2
            if dx*dx+dy*dy < BLAST_R*BLAST_R:
                se.hp -= 2; se.flash_timer = 8
                if se.hp <= 0: se.alive = False; gs["score"] += 150
    for t2 in gs["turrets"]:
        if t2.alive:
            dx = (t2.x+t2.w//2) - bx2; dy = (t2.y+t2.h//2) - by2
            if dx*dx+dy*dy < BLAST_R*BLAST_R:
                t2.hp -= 2; t2.flash_timer = 8
                if t2.hp <= 0: t2.alive = False; gs["score"] += 200
    for d in gs["drones"]:
        if d.alive:
            dx = (d.x+d.w//2) - bx2; dy = (d.y+d.h//2) - by2
            if dx*dx+dy*dy < BLAST_R*BLAST_R:
                d.hp -= 2; d.flash_timer = 8
                if d.hp <= 0: d.alive = False; gs["score"] += 120
    boss = gs["boss"]
    if boss.alive:
        dx = (boss.x+boss.w//2) - bx2; dy = (boss.y+boss.h//2) - by2
        if dx*dx+dy*dy < (BLAST_R+60)*(BLAST_R+60):
            boss.hp -= 4; boss.flash_timer = 8
            if boss.hp <= 0:
                boss.alive = False; gs["boss_dead"] = True; gs["score"] += 500


def draw_weapon_hud(surface, weapon, ammo):
    """Draw current weapon indicator bottom-right."""
    panel_w, panel_h = 180, 46
    px = WIDTH - panel_w - 10; py = HEIGHT - panel_h - 10
    panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    panel.fill((0,0,0,150))
    col = WEAPON_COLORS.get(weapon, NEON_CYAN)
    pygame.draw.rect(panel, (*col, 140), (0,0,panel_w,panel_h), 2, border_radius=8)
    surface.blit(panel, (px, py))
    wf = pygame.font.SysFont("consolas", 13, bold=True)
    icons = {"blaster":"◉","shotgun":"⊕","rocket":"⚡","laser":"▶","flamethrower":"⬡"}
    name_lbl = wf.render(f"{icons.get(weapon,'?')} {weapon.upper()}", True, col)
    surface.blit(name_lbl, (px+8, py+6))
    if weapon != "blaster":
        ammo_lbl = wf.render(f"AMMO: {ammo}", True, WHITE if ammo > 2 else NEON_RED)
        surface.blit(ammo_lbl, (px+8, py+24))
        # Ammo pips
        max_ammo = WEAPON_AMMO.get(weapon, 1)
        for i in range(max_ammo):
            pip_col = col if i < ammo else (50,50,50)
            pygame.draw.rect(surface, pip_col,
                (px + panel_w - 14 - i*10, py+28, 8, 12), border_radius=3)
    else:
        inf = wf.render("∞ UNLIMITED", True, NEON_CYAN)
        surface.blit(inf, (px+8, py+24))


# ==============================
# GAME STATE
# ==============================
gs = init_level(1)
game_over = False
game_won  = False
game_state = "start"   # "start" | "playing" | "over" | "won"
running   = True
tr_alpha  = 0
tr_dir    = 0
tr_pending_level = None

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "start":
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                    game_state = "playing"
                    gs = init_level(1)
            elif game_state in ("over", "won"):
                if event.key == pygame.K_r:
                    gs = init_level(1)
                    game_over = False; game_won = False
                    game_state = "playing"
                    current_level = 1
                    tr_alpha = 0; tr_dir = 0; tr_pending_level = None
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    game_state = "start"

    # ---- START SCREEN ----
    if game_state == "start":
        draw_start_screen()
        pygame.display.update()
        continue

    if tr_dir == 1:
        tr_alpha = min(255, tr_alpha + 8)
        if tr_alpha >= 255 and tr_pending_level is not None:
            current_level = tr_pending_level
            gs = init_level(current_level, carry_hp=gs["player_hp"], carry_score=gs["score"],
                            carry_weapon=gs["weapon"], carry_ammo=gs["weapon_ammo"])
            tr_pending_level = None
            tr_dir = -1
    elif tr_dir == -1:
        tr_alpha = max(0, tr_alpha - 8)
        if tr_alpha == 0:
            tr_dir = 0

    if game_state in ("over", "won") or game_over or game_won:
        if game_over: game_state = "over"
        if game_won:  game_state = "won"
        draw_background(gs["camera_x"], current_level)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        screen.blit(overlay, (0,0))
        if game_state == "won":
            t1 = font_big.render("★  YOU WIN!  ★", True, NEON_YELLOW)
            t2 = font_big.render(f"Final Score: {gs['score']}", True, NEON_CYAN)
            t3 = font_small.render("R = play again   ENTER = title screen", True, WHITE)
            screen.blit(t1, (WIDTH//2-t1.get_width()//2, HEIGHT//2-70))
            screen.blit(t2, (WIDTH//2-t2.get_width()//2, HEIGHT//2-20))
            screen.blit(t3, (WIDTH//2-t3.get_width()//2, HEIGHT//2+40))
        else:
            t1 = font_big.render("GAME OVER", True, NEON_RED)
            t2 = font_big.render(f"Score: {gs['score']}", True, NEON_CYAN)
            t3 = font_small.render("R = restart   ENTER = title screen", True, WHITE)
            screen.blit(t1, (WIDTH//2-t1.get_width()//2, HEIGHT//2-60))
            screen.blit(t2, (WIDTH//2-t2.get_width()//2, HEIGHT//2))
            screen.blit(t3, (WIDTH//2-t3.get_width()//2, HEIGHT//2+50))
        pygame.display.update()
        continue

    if gs["level_complete"]:
        gs["level_complete_timer"] -= 1
        draw_background(gs["camera_x"], current_level)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,120))
        screen.blit(overlay, (0,0))
        msg = font_big.render("★  LEVEL CLEAR!  ★", True, NEON_YELLOW)
        sub = font_med.render("Advancing to next level...", True, WHITE)
        screen.blit(msg, (WIDTH//2-msg.get_width()//2, HEIGHT//2-40))
        screen.blit(sub, (WIDTH//2-sub.get_width()//2, HEIGHT//2+10))
        if gs["level_complete_timer"] <= 0:
            if current_level == 1:
                tr_dir = 1
                tr_pending_level = 2
            else:
                game_won = True
            gs["level_complete"] = False
        if tr_alpha > 0:
            ov = pygame.Surface((WIDTH, HEIGHT))
            ov.fill((0,0,0)); ov.set_alpha(tr_alpha)
            screen.blit(ov, (0,0))
        pygame.display.update()
        continue

    keys = pygame.key.get_pressed()
    moving = False

    if not gs["player_in_rocket"]:
        if keys[pygame.K_LEFT]:
            gs["player_rect"].x -= 5
            gs["facing_right"] = False; moving = True
        if keys[pygame.K_RIGHT]:
            gs["player_rect"].x += 5
            gs["facing_right"] = True; moving = True
        if keys[pygame.K_UP] and gs["on_ground"]:
            gs["velocity_y"] = -12
            gs["on_ground"] = False
            for _ in range(8):
                gs["particles"].append(Particle(
                    gs["player_rect"].centerx, gs["player_rect"].bottom,
                    NEON_CYAN, random.uniform(-2,2), random.uniform(0,3)
                ))

    gs["shoot_cooldown"] = max(0, gs["shoot_cooldown"]-1)
    gs["flame_active"]   = max(0, gs["flame_active"]-1)
    if keys[pygame.K_SPACE] and gs["shoot_cooldown"] == 0 and not gs["player_in_rocket"]:
        new_bullets = fire_weapon(gs)
        gs["bullets"].extend(new_bullets)

    gs["super_cooldown"] = max(0, gs["super_cooldown"]-1)
    if keys[pygame.K_q] and gs["super_cooldown"] == 0 and not gs["player_in_rocket"]:
        if gs["mega_ready"]:
            gs["mega_ready"] = False
            gs["super_stacks"] = 0
            gs["super_ready"] = False
            gs["mega_active"] = MEGA_TOTAL
            gs["mega_anim"] = 0
            gs["mega_missile_phase"] = 0
            gs["mega_missiles"] = []
            gs["super_cooldown"] = 180
            gs["shake_timer"] = MEGA_TOTAL
            gs["cinematic_bars"] = 40; gs["cinematic_alpha"] = 0
            for _ in range(80):
                gs["particles"].append(Particle(
                    WIDTH//2 + gs["camera_x"], HEIGHT//2,
                    random.choice([NEON_PINK, NEON_YELLOW, WHITE, NEON_CYAN]),
                    random.uniform(-14,14), random.uniform(-14,4), life=60, size=random.randint(4,12)
                ))
        elif gs["super_ready"]:
            gs["super_active"] = SUPER_DURATION
            gs["super_ready"] = False
            gs["super_stacks"] = max(0, gs["super_stacks"] - 1)
            gs["super_cooldown"] = 120
            gs["is_super_pose"] = SUPER_DURATION+20
            gs["shake_timer"] = SUPER_DURATION
            gs["cinematic_bars"] = 30; gs["cinematic_alpha"] = 0
            for _ in range(80):
                gs["particles"].append(Particle(
                    gs["player_rect"].centerx, gs["player_rect"].centery,
                    random.choice([NEON_CYAN,NEON_YELLOW,WHITE,NEON_PINK]),
                    random.uniform(-12,12), random.uniform(-12,3), life=50, size=random.randint(4,10)
                ))

    gs["is_super_pose"] = max(0, gs["is_super_pose"]-1)

    if gs["super_active"] > 0:
        gs["super_active"] -= 1
        if gs["shake_timer"] > 0:
            gs["shake_timer"] -= 1
            intensity = 10 if gs["super_active"] > SUPER_DURATION*0.8 else 6
            gs["shake_x"] = random.randint(-intensity,intensity)
            gs["shake_y"] = random.randint(-intensity,intensity)
        else:
            gs["shake_x"] = 0; gs["shake_y"] = 0

        if gs["cinematic_bars"] > 0:
            gs["cinematic_bars"] -= 1
            gs["cinematic_alpha"] = min(70, gs["cinematic_alpha"]+3)
        elif gs["super_active"] < 30:
            gs["cinematic_alpha"] = max(0, gs["cinematic_alpha"]-3)

        laser_y   = gs["player_rect"].centery
        laser_x   = gs["player_rect"].right if gs["facing_right"] else -9999
        laser_end = 99999 if gs["facing_right"] else gs["player_rect"].left
        laser_rect = pygame.Rect(min(laser_x,laser_end), laser_y-60, abs(laser_end-laser_x), 120)

        for e in gs["enemies"]:
            if not e.alive: continue
            if laser_rect.colliderect(e.get_rect()):
                e.hp -= 0.22; e.flash_timer = 4
                if e.hp <= 0:
                    e.alive = False; gs["score"] += 150
                    for _ in range(50):
                        gs["particles"].append(Particle(
                            e.x+e.w//2, e.y+e.h//2,
                            random.choice([NEON_CYAN,NEON_YELLOW,WHITE,NEON_PINK]),
                            random.uniform(-8,8), random.uniform(-9,-1), life=55, size=random.randint(3,8)
                        ))

        boss = gs["boss"]
        if boss.alive and laser_rect.colliderect(boss.get_rect()):
            boss.hp -= 0.45; boss.flash_timer = 4
            if boss.hp <= 0:
                boss.alive = False; gs["boss_dead"] = True
                gs["score"] += 500
                for _ in range(100):
                    gs["particles"].append(Particle(
                        boss.x+boss.w//2, boss.y+boss.h//2,
                        random.choice([NEON_CYAN,NEON_YELLOW,NEON_ORANGE,WHITE,NEON_PINK]),
                        random.uniform(-12,12), random.uniform(-12,-1), life=80, size=random.randint(4,12)
                    ))

        beam_sx = gs["player_rect"].right - int(gs["camera_x"]) if gs["facing_right"] else 0
        beam_ex = WIDTH if gs["facing_right"] else gs["player_rect"].left - int(gs["camera_x"])
        for _ in range(8):
            px = random.randint(int(beam_sx),int(beam_ex))
            gs["particles"].append(Particle(
                px+gs["camera_x"], laser_y,
                random.choice([NEON_CYAN,WHITE,NEON_YELLOW]),
                random.uniform(-3,3), random.uniform(-6,-1), life=18, size=random.randint(2,5)
            ))

    # ---- MEGA ACTIVE STATE MACHINE ----
    if gs["mega_active"] > 0:
        gs["mega_active"] -= 1
        gs["mega_anim"] += 1
        phase = gs["mega_missile_phase"]

        # Screen shake
        shake_map = {0: 3, 1: 6, 2: 10, 3: 2}
        intensity = shake_map.get(phase, 2)
        gs["shake_x"] = random.randint(-intensity, intensity)
        gs["shake_y"] = random.randint(-intensity, intensity)
        if gs["mega_active"] == 0:
            gs["shake_x"] = 0; gs["shake_y"] = 0

        # ---- PHASE 0: robot descends ----
        if phase == 0:
            if gs["mega_anim"] >= MEGA_ROBOT_DESCENT:
                gs["mega_missile_phase"] = 1
                gs["mega_anim"] = 0

        # ---- PHASE 1: missile barrage ----
        elif phase == 1:
            # Spawn missiles — starts slow, ramps up to a storm
            ramp = min(1.0, gs["mega_anim"] / 60)
            spawn_chance = 0.15 + 0.55 * ramp   # 15% → 70% per frame
            if random.random() < spawn_chance:
                # Spread launches across the visible world area
                mx = gs["camera_x"] + random.uniform(-50, WIDTH + 50)
                gs["mega_missiles"].append({
                    "x": mx,
                    "y": float(-20 - random.randint(0, 60)),
                    "vx": random.uniform(-1.5, 1.5),
                    "vy": MEGA_MISSILE_SPEED + random.uniform(0, 4),
                    "age": 0,
                })

            # Update missiles
            for m in gs["mega_missiles"]:
                m["x"] += m["vx"]
                m["y"] += m["vy"]
                m["age"] += 1

            # Check missile impacts
            for m in list(gs["mega_missiles"]):
                if m["y"] > GROUND_Y + 20:
                    m["dead"] = True
                    # Explosion particles at ground level
                    for _ in range(25):
                        gs["particles"].append(Particle(
                            m["x"], GROUND_Y,
                            random.choice([NEON_RED, NEON_ORANGE, NEON_YELLOW, (255,80,0)]),
                            random.uniform(-8, 8), random.uniform(-10, -2),
                            life=40, size=random.randint(3, 9)
                        ))
                    # Damage nearby enemies
                    for e in gs["enemies"]:
                        if not e.alive: continue
                        if abs(e.x - m["x"]) < 120:
                            e.hp -= 1.5; e.flash_timer = 8
                            if e.hp <= 0:
                                e.alive = False
                                gs["score"] += 200
                                gs["kill_count"] += 1
                                if gs["kill_count"] >= KILLS_FOR_SUPER:
                                    gs["kill_count"] = 0
                                    gs["super_stacks"] = min(2, gs["super_stacks"] + 1)
                                    if gs["super_stacks"] >= 2:
                                        gs["mega_ready"] = True; gs["super_ready"] = False
                                    else:
                                        gs["super_ready"] = True
                    # Damage boss if nearby
                    boss2 = gs["boss"]
                    if boss2.alive and abs(boss2.x + boss2.w//2 - m["x"]) < 150:
                        boss2.hp -= 3; boss2.flash_timer = 8
                        if boss2.hp <= 0:
                            boss2.alive = False; gs["boss_dead"] = True
                            gs["score"] += 800
                            for _ in range(120):
                                gs["particles"].append(Particle(
                                    boss2.x+boss2.w//2, boss2.y+boss2.h//2,
                                    random.choice([NEON_RED, NEON_ORANGE, NEON_YELLOW, WHITE]),
                                    random.uniform(-14,14), random.uniform(-14,-1),
                                    life=90, size=random.randint(4,13)
                                ))

            gs["mega_missiles"] = [m for m in gs["mega_missiles"] if not m.get("dead") and m["y"] < GROUND_Y + 30]

            if gs["mega_anim"] >= MEGA_FIRE_FRAMES:
                gs["mega_missile_phase"] = 2
                gs["mega_anim"] = 0

        # ---- PHASE 2: cleanup — any remaining missiles land, big explosions ----
        elif phase == 2:
            for m in gs["mega_missiles"]:
                m["x"] += m["vx"]
                m["y"] += m["vy"]
                m["age"] += 1
            for m in list(gs["mega_missiles"]):
                if m["y"] > GROUND_Y + 20:
                    m["dead"] = True
                    for _ in range(20):
                        gs["particles"].append(Particle(
                            m["x"], GROUND_Y,
                            random.choice([NEON_RED, NEON_ORANGE, (255,80,0)]),
                            random.uniform(-7,7), random.uniform(-9,-2), life=35, size=random.randint(3,8)
                        ))
            gs["mega_missiles"] = [m for m in gs["mega_missiles"] if not m.get("dead")]

            # Random ground explosions (aftermath)
            if random.random() < 0.4:
                ex = gs["camera_x"] + random.uniform(0, WIDTH)
                for _ in range(15):
                    gs["particles"].append(Particle(
                        ex, GROUND_Y - random.randint(0, 30),
                        random.choice([NEON_RED, NEON_ORANGE, NEON_YELLOW]),
                        random.uniform(-6,6), random.uniform(-8,-1), life=30, size=random.randint(3,8)
                    ))

            if gs["mega_anim"] >= MEGA_IMPACT_FRAMES:
                gs["mega_missile_phase"] = 3
                gs["mega_anim"] = 0
                gs["mega_missiles"] = []

        # ---- PHASE 3: robot exits ----
        elif phase == 3:
            pass   # just visuals

    gs["velocity_y"] += 0.5
    gs["player_rect"].y += int(gs["velocity_y"])
    gs["on_ground"] = False
    plats = get_platforms(gs["camera_x"], current_level)
    for plat_rect, _ in plats:
        if gs["player_rect"].colliderect(plat_rect):
            if gs["velocity_y"] >= 0:
                gs["player_rect"].bottom = plat_rect.top
                gs["velocity_y"] = 0; gs["on_ground"] = True; break
            elif gs["velocity_y"] < 0:
                gs["player_rect"].top = plat_rect.bottom; gs["velocity_y"] = 0

    if gs["player_rect"].top > HEIGHT+100:
        gs["player_hp"] = 0

    gs["is_shooting"] = max(0, gs["is_shooting"]-1)
    if gs["on_ground"]: gs["air_frames"] = 0
    else: gs["air_frames"] += 1

    if gs["air_frames"] > 3: gs["state"] = "jump"
    elif moving: gs["state"] = "walk"
    else: gs["state"] = "stand"
    if gs["state"] == "walk": gs["frame_index"] += 0.15
    else: gs["frame_index"] = 0.0

    for hp_item in gs["health_pickups"]:
        if not hp_item.alive: continue
        hp_item.update()
        if gs["player_rect"].colliderect(hp_item.get_rect()):
            if gs["player_hp"] < 5:
                hp_item.alive = False
                gs["player_hp"] = min(5, gs["player_hp"] + 1)
                gs["score"] += 50
                for _ in range(20):
                    gs["particles"].append(Particle(
                        hp_item.x + hp_item.w//2, hp_item.y + hp_item.h//2,
                        random.choice([(255, 80, 80), (255, 200, 200), WHITE]),
                        random.uniform(-4, 4), random.uniform(-5, -1), life=30, size=random.randint(2, 6)
                    ))

    # ---- WEAPON PICKUPS ----
    for wp in gs["weapon_pickups"]:
        if not wp.alive: continue
        wp.update()
        if gs["player_rect"].colliderect(wp.get_rect()):
            wp.alive = False
            gs["weapon"] = wp.wtype
            gs["weapon_ammo"] = WEAPON_AMMO[wp.wtype]
            gs["weapon_pickup_flash"] = 80
            gs["score"] += 25
            col = WEAPON_COLORS.get(wp.wtype, NEON_CYAN)
            for _ in range(30):
                gs["particles"].append(Particle(
                    wp.x+wp.w//2, wp.y+wp.h//2, col,
                    random.uniform(-5,5), random.uniform(-6,-1), life=35, size=random.randint(3,8)
                ))

    # ---- SPIKE TRAP DAMAGE ----
    if gs["invincible"] == 0 and not gs["player_in_rocket"]:
        for sp in gs["spike_traps"]:
            if sp.alive and gs["player_rect"].colliderect(sp.get_rect()):
                gs["player_hp"] -= 1; gs["invincible"] = 60
                for _ in range(15):
                    gs["particles"].append(Particle(
                        gs["player_rect"].centerx, gs["player_rect"].bottom,
                        NEON_RED, random.uniform(-3,3), random.uniform(-4,-1), life=20))
                if gs["player_hp"] <= 0: game_over = True

    # ---- TURRET UPDATE + BULLET COLLISIONS ----
    for t2 in gs["turrets"]:
        if t2.alive:
            t2.update(gs["player_rect"], gs["bullets"])
    # Turret hit by player bullets
    for b in gs["bullets"][:]:
        if b.is_enemy: continue
        br = b.get_rect()
        for t2 in gs["turrets"]:
            if not t2.alive: continue
            if br.colliderect(t2.get_rect()):
                if hasattr(b, 'is_rocket_proj') and b.is_rocket_proj:
                    b.alive = False
                    explode_rocket_proj(gs, b.x, b.y)
                    break
                b.alive = False; t2.hp -= 1; t2.flash_timer = 8
                for _ in range(8):
                    gs["particles"].append(Particle(b.x, b.y, NEON_ORANGE,
                        random.uniform(-3,3), random.uniform(-4,-1), life=18))
                if t2.hp <= 0:
                    t2.alive = False; gs["score"] += 200
                    for _ in range(30):
                        gs["particles"].append(Particle(t2.x+t2.w//2, t2.y+t2.h//2,
                            random.choice([NEON_ORANGE,NEON_RED,NEON_YELLOW]),
                            random.uniform(-6,6), random.uniform(-7,-1), life=40, size=random.randint(3,8)))
                break

    # ---- SHIELD ENEMY UPDATE + BULLET COLLISIONS ----
    for se in gs["shield_enemies"]:
        if se.alive:
            se.update(gs["player_rect"], gs["camera_x"], gs["bullets"])
    for b in gs["bullets"][:]:
        if b.is_enemy: continue
        br = b.get_rect()
        for se in gs["shield_enemies"]:
            if not se.alive: continue
            if br.colliderect(se.get_rect()):
                if hasattr(b, 'is_rocket_proj') and b.is_rocket_proj:
                    b.alive = False
                    explode_rocket_proj(gs, b.x, b.y)
                    break
                hit_landed = se.take_hit(b.direction)
                b.alive = False
                if hit_landed:
                    for _ in range(10):
                        gs["particles"].append(Particle(b.x, b.y, (80,140,255),
                            random.uniform(-3,3), random.uniform(-4,-1), life=18))
                    if se.hp <= 0:
                        se.alive = False; gs["score"] += 150
                        gs["kill_count"] += 1
                        if gs["kill_count"] >= KILLS_FOR_SUPER:
                            gs["kill_count"] = 0
                            gs["super_stacks"] = min(2, gs["super_stacks"]+1)
                            gs["mega_ready"] = gs["super_stacks"] >= 2
                            if not gs["mega_ready"]: gs["super_ready"] = True
                        for _ in range(30):
                            gs["particles"].append(Particle(
                                se.x+se.w//2, se.y+se.h//2,
                                random.choice([(80,140,255),NEON_CYAN,WHITE]),
                                random.uniform(-5,5), random.uniform(-6,-1), life=40))
                else:
                    # Shield block spark
                    for _ in range(6):
                        gs["particles"].append(Particle(b.x, b.y, (0,200,255),
                            random.uniform(-4,4), random.uniform(-4,-1), life=12, size=3))
                break

    # ---- DRONE UPDATE + BULLET COLLISIONS ----
    for d in gs["drones"]:
        if d.alive:
            d.update(gs["player_rect"], gs["camera_x"], gs["bullets"])
    for b in gs["bullets"][:]:
        if b.is_enemy: continue
        br = b.get_rect()
        for d in gs["drones"]:
            if not d.alive: continue
            if br.colliderect(d.get_rect()):
                if hasattr(b, 'is_rocket_proj') and b.is_rocket_proj:
                    b.alive = False
                    explode_rocket_proj(gs, b.x, b.y)
                    break
                b.alive = False; d.hp -= 1; d.flash_timer = 8
                for _ in range(10):
                    gs["particles"].append(Particle(b.x, b.y, NEON_YELLOW,
                        random.uniform(-4,4), random.uniform(-5,-1), life=20))
                if d.hp <= 0:
                    d.alive = False; gs["score"] += 120
                    gs["kill_count"] += 1
                    if gs["kill_count"] >= KILLS_FOR_SUPER:
                        gs["kill_count"] = 0
                        gs["super_stacks"] = min(2, gs["super_stacks"]+1)
                        gs["mega_ready"] = gs["super_stacks"] >= 2
                        if not gs["mega_ready"]: gs["super_ready"] = True
                    for _ in range(20):
                        gs["particles"].append(Particle(
                            d.x+d.w//2, d.y+d.h//2,
                            random.choice([NEON_YELLOW,NEON_RED,WHITE]),
                            random.uniform(-6,6), random.uniform(-7,-1), life=35))
                break

    # ---- ROCKET PROJECTILE EXPLOSION CHECK ----
    for b in gs["bullets"][:]:
        if b.is_enemy: continue
        if hasattr(b,'is_rocket_proj') and b.is_rocket_proj:
            if b.y >= GROUND_Y - 10:
                b.alive = False
                explode_rocket_proj(gs, b.x, b.y)

    # ---- NEW ENEMY PLAYER BODY DAMAGE ----
    if gs["invincible"] == 0 and not gs["player_in_rocket"]:
        for se in gs["shield_enemies"]:
            if se.alive and gs["player_rect"].colliderect(se.get_rect()):
                gs["player_hp"] -= 1; gs["invincible"] = 90
                for _ in range(10):
                    gs["particles"].append(Particle(
                        gs["player_rect"].centerx, gs["player_rect"].centery, NEON_RED))
                if gs["player_hp"] <= 0: game_over = True
                break
        for d in gs["drones"]:
            if gs["invincible"] > 0: break
            if d.alive and gs["player_rect"].colliderect(d.get_rect()):
                gs["player_hp"] -= 1; gs["invincible"] = 90
                for _ in range(10):
                    gs["particles"].append(Particle(
                        gs["player_rect"].centerx, gs["player_rect"].centery, NEON_RED))
                if gs["player_hp"] <= 0: game_over = True

    # Weapon pickup flash timer
    if gs["weapon_pickup_flash"] > 0: gs["weapon_pickup_flash"] -= 1

    for b in gs["bullets"][:]:
        b.update()
        bsx = b.x - gs["camera_x"]
        if bsx < -100 or bsx > WIDTH+100: b.alive = False

    for b in gs["bullets"][:]:
        if b.is_enemy: continue
        br = b.get_rect()
        for e in gs["enemies"]:
            if not e.alive: continue
            if br.colliderect(e.get_rect()):
                if hasattr(b,'is_rocket_proj') and b.is_rocket_proj:
                    b.alive = False
                    explode_rocket_proj(gs, b.x, b.y)
                    break
                dmg = 1 if not hasattr(b,'is_flame') else 0.5
                b.alive = False; e.hp -= dmg; e.flash_timer = 8
                for _ in range(12):
                    gs["particles"].append(Particle(b.x, b.y, NEON_PINK))
                if e.hp <= 0:
                    e.alive = False; gs["score"] += 100
                    gs["kill_count"] += 1
                    if gs["kill_count"] >= KILLS_FOR_SUPER:
                        gs["kill_count"] = 0
                        gs["super_stacks"] = min(2, gs["super_stacks"] + 1)
                        if gs["super_stacks"] >= 2:
                            gs["mega_ready"] = True
                            gs["super_ready"] = False
                        else:
                            gs["super_ready"] = True
                    for _ in range(25):
                        gs["particles"].append(Particle(
                            e.x+e.w//2, e.y+e.h//2,
                            random.choice([NEON_RED,NEON_YELLOW,NEON_PINK]),
                            random.uniform(-5,5), random.uniform(-6,-1), life=40
                        ))
                break

    boss = gs["boss"]
    if boss.alive:
        for b in gs["bullets"][:]:
            if b.is_enemy: continue
            br = b.get_rect()
            if br.colliderect(boss.get_rect()):
                if hasattr(b,'is_rocket_proj') and b.is_rocket_proj:
                    b.alive = False
                    explode_rocket_proj(gs, b.x, b.y)
                    continue
                dmg = 4 if getattr(b,'is_flame',False) else 1
                b.alive = False; boss.hp -= dmg; boss.flash_timer = 6
                for _ in range(15):
                    gs["particles"].append(Particle(b.x, b.y, NEON_ORANGE,
                        random.uniform(-4,4), random.uniform(-4,-1), life=20))
                if boss.hp <= 0:
                    boss.alive = False; gs["boss_dead"] = True
                    gs["score"] += 500
                    for _ in range(100):
                        gs["particles"].append(Particle(
                            boss.x+boss.w//2, boss.y+boss.h//2,
                            random.choice([NEON_CYAN,NEON_YELLOW,NEON_ORANGE,WHITE,NEON_PINK]),
                            random.uniform(-12,12), random.uniform(-12,-1), life=80, size=random.randint(4,12)
                        ))

    if gs["invincible"] == 0 and not gs["player_in_rocket"]:
        for b in gs["bullets"][:]:
            if not b.is_enemy: continue
            if b.get_rect().colliderect(gs["player_rect"]):
                b.alive = False; gs["player_hp"] -= 1; gs["invincible"] = 90
                for _ in range(10):
                    gs["particles"].append(Particle(gs["player_rect"].centerx, gs["player_rect"].centery, NEON_RED))
                if gs["player_hp"] <= 0: game_over = True

    gs["bullets"] = [b for b in gs["bullets"] if b.alive]
    gs["invincible"] = max(0, gs["invincible"]-1)

    for e in gs["enemies"]:
        if e.alive:
            e.update(gs["player_rect"], gs["camera_x"], gs["bullets"])

    if boss.alive:
        boss.update(gs["player_rect"], gs["camera_x"], gs["bullets"], gs["particles"])

    # ---- BOSS "INCOMING" — only trigger once when boss first appears on screen ----
    if boss.alive and not gs["boss_seen"]:
        boss_screen_x = boss.x - gs["camera_x"]
        if 0 <= boss_screen_x <= WIDTH:
            gs["boss_seen"] = True
            gs["show_boss_warning"] = True
            gs["boss_warning_timer"] = 180   # show for 3 seconds

    if gs["boss_warning_timer"] > 0:
        gs["boss_warning_timer"] -= 1
        if gs["boss_warning_timer"] == 0:
            gs["show_boss_warning"] = False

    # ---- ROCKET LOGIC ----
    rocket = gs["rocket"]
    if gs["boss_dead"] and not gs["rocket_visible"]:
        gs["rocket_visible"] = True
        rocket.x = boss.x + boss.w//2 - rocket.w//2
        rocket.y = GROUND_Y - rocket.h
        for _ in range(60):
            gs["particles"].append(Particle(
                rocket.x + rocket.w//2, rocket.y + rocket.h//2,
                random.choice([NEON_CYAN, NEON_YELLOW, WHITE, (200, 255, 200)]),
                random.uniform(-10, 10), random.uniform(-12, -2), life=60, size=random.randint(3, 10)
            ))

    if gs["rocket_visible"] and not rocket.launching and not rocket.launched:
        rocket.update(gs["particles"])

        if gs["player_rect"].colliderect(rocket.get_enter_rect()) and not gs["player_in_rocket"]:
            gs["player_in_rocket"] = True
            gs["boarding_timer"] = 80
            rocket.activated = True
            gs["player_rect"].centerx = int(rocket.x + rocket.w // 2)
            gs["player_rect"].bottom = int(rocket.y + rocket.h - 5)
            for _ in range(30):
                gs["particles"].append(Particle(
                    rocket.x + rocket.w//2, rocket.y + rocket.h//2,
                    random.choice([NEON_CYAN, NEON_YELLOW, WHITE]),
                    random.uniform(-5,5), random.uniform(-6,-1), life=40, size=4
                ))

    if gs["player_in_rocket"]:
        gs["boarding_timer"] = max(0, gs["boarding_timer"] - 1)
        if gs["boarding_timer"] == 0 and not rocket.launching:
            rocket.launching = True
            rocket.launch_timer = 30
            gs["shake_timer"] = 80

    if rocket.launching and gs["shake_timer"] > 0:
        gs["shake_timer"] -= 1
        gs["shake_x"] = random.randint(-4, 4)
        gs["shake_y"] = random.randint(-4, 4)

    if rocket.launched and not gs["level_complete"]:
        gs["level_complete"] = True
        gs["level_complete_timer"] = 120
        gs["shake_x"] = 0; gs["shake_y"] = 0

    if rocket.launching:
        rocket.update(gs["particles"])

    gs["particles"] = [p for p in gs["particles"] if p.life > 0]
    for p in gs["particles"]: p.update()

    target_cam = gs["player_rect"].centerx - WIDTH//2
    gs["camera_x"] += (target_cam - gs["camera_x"]) * 0.1

    # ==============================
    # DRAW
    # ==============================
    draw_background(gs["camera_x"], current_level)

    plat_surfs = plat_surfs_l1 if current_level == 1 else plat_surfs_l2
    for plat_rect, key in plats:
        if key is None: continue
        sx2 = plat_rect.x - int(gs["camera_x"])
        if -200 < sx2 < WIDTH+200:
            screen.blit(plat_surfs[key], (sx2, plat_rect.y))

    for hp_item in gs["health_pickups"]:
        if not hp_item.alive: continue
        hx_screen = hp_item.x - gs["camera_x"]
        if -50 < hx_screen < WIDTH + 50:
            hp_item.draw(screen, int(gs["camera_x"]))

    # Draw weapon pickups
    for wp in gs["weapon_pickups"]:
        if not wp.alive: continue
        wx_screen = wp.x - gs["camera_x"]
        if -60 < wx_screen < WIDTH+60:
            wp.draw(screen, int(gs["camera_x"]))

    # Draw spike traps
    for sp in gs["spike_traps"]:
        spx = sp.x - gs["camera_x"]
        if -60 < spx < WIDTH+60:
            sp.draw(screen, int(gs["camera_x"]))

    # Draw turrets
    for t2 in gs["turrets"]:
        if t2.alive:
            txs = t2.x - gs["camera_x"]
            if -80 < txs < WIDTH+80:
                t2.draw(screen, int(gs["camera_x"]))

    # Draw shield enemies
    for se in gs["shield_enemies"]:
        if se.alive:
            ses = se.x - gs["camera_x"]
            if -80 < ses < WIDTH+80:
                se.draw(screen, int(gs["camera_x"]))

    # Draw drones
    for d in gs["drones"]:
        if d.alive:
            ds = d.x - gs["camera_x"]
            if -80 < ds < WIDTH+80:
                d.draw(screen, int(gs["camera_x"]))

    if gs["rocket_visible"]:
        rx_screen = rocket.x - gs["camera_x"]
        if -100 < rx_screen < WIDTH + 100:
            rocket.draw(screen, int(gs["camera_x"]))

    for e in gs["enemies"]:
        if e.alive:
            exs = e.x - gs["camera_x"]
            if -100 < exs < WIDTH+100:
                e.draw(screen, int(gs["camera_x"]))

    if boss.alive:
        bxs = boss.x - gs["camera_x"]
        if -200 < bxs < WIDTH+200:
            boss.draw(screen, int(gs["camera_x"]))

    for b in gs["bullets"]: b.draw(screen, int(gs["camera_x"]))
    for p in gs["particles"]: p.draw(screen, gs["camera_x"])

    if not gs["player_in_rocket"]:
        # Flamethrower cone glow
        if gs["flame_active"] > 0:
            flame_dir = 1 if gs["facing_right"] else -1
            fx = gs["player_rect"].centerx - int(gs["camera_x"])
            fy = gs["player_rect"].centery
            cone_surf = pygame.Surface((200, 80), pygame.SRCALPHA)
            for ci in range(18):
                frac = ci/18
                ca = int(80*(1-frac)*min(1,gs["flame_active"]/8))
                cr = 255; cg = int(100+random.randint(-20,40)); cb = 0
                spread = int(35*frac)
                rect_w = int(180*frac)+10; rect_h = spread*2+8
                if flame_dir == 1:
                    pygame.draw.rect(cone_surf, (cr,cg,cb,ca), (int(190*frac), 40-spread-4, rect_w, rect_h), border_radius=4)
                else:
                    pygame.draw.rect(cone_surf, (cr,cg,cb,ca), (0, 40-spread-4, rect_w, rect_h), border_radius=4)
            sx_off = fx if flame_dir == 1 else fx - 200
            screen.blit(cone_surf, (sx_off, fy-40))

        if gs["invincible"] == 0 or (gs["invincible"]//6)%2 == 0:
            img = get_frame(gs["state"], gs["is_shooting"], gs["is_super_pose"], gs["velocity_y"], gs["frame_index"])
            if img:
                if not gs["facing_right"]: img = pygame.transform.flip(img, True, False)
                screen.blit(img, (gs["player_rect"].x - int(gs["camera_x"]), gs["player_rect"].y))
            else:
                pygame.draw.rect(screen, NEON_CYAN, (
                    gs["player_rect"].x-int(gs["camera_x"]), gs["player_rect"].y,
                    gs["player_rect"].width, gs["player_rect"].height), border_radius=4)

    # Screen shake
    if gs["shake_x"] or gs["shake_y"]:
        tmp = screen.copy(); screen.fill((0,0,0))
        screen.blit(tmp, (gs["shake_x"], gs["shake_y"]))

    # Super laser beam
    if gs["super_active"] > 0:
        beam_x   = gs["player_rect"].right - int(gs["camera_x"]) + gs["shake_x"] if gs["facing_right"] else 0
        beam_end = WIDTH if gs["facing_right"] else gs["player_rect"].left - int(gs["camera_x"]) + gs["shake_x"]
        beam_y   = gs["player_rect"].centery + gs["shake_y"]
        progress = gs["super_active"] / SUPER_DURATION
        tick = pygame.time.get_ticks()
        pulse = abs(math.sin(tick*0.015))*0.4+0.6
        halo_h = int(200*progress)
        halo_surf = pygame.Surface((WIDTH, halo_h*2), pygame.SRCALPHA)
        pygame.draw.rect(halo_surf, (0,200,255,int(35*progress)), (0,0,WIDTH,halo_h*2))
        screen.blit(halo_surf, (0, beam_y-halo_h))
        glow_h = int(100*progress*pulse)
        glow_surf = pygame.Surface((WIDTH, glow_h*2+2), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (0,255,255,int(90*progress)), (0,0,WIDTH,glow_h*2+2), border_radius=8)
        screen.blit(glow_surf, (0, beam_y-glow_h))
        body_h = int(55*progress*pulse)
        pygame.draw.rect(screen, (0,180,255), (beam_x,beam_y-body_h//2,beam_end-beam_x,body_h), border_radius=6)
        core_h = max(8, int(26*progress))*random.choice([1,1,1,2])
        pygame.draw.rect(screen, (180,255,255), (beam_x,beam_y-core_h//2,beam_end-beam_x,core_h), border_radius=4)
        white_h = max(4, int(12*progress))
        pygame.draw.rect(screen, WHITE, (beam_x,beam_y-white_h//2,beam_end-beam_x,white_h))
        if gs["super_active"] > SUPER_DURATION-8:
            fa = int(200*(gs["super_active"]-(SUPER_DURATION-8))/8)
            fs = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA); fs.fill((0,255,255,fa)); screen.blit(fs,(0,0))
        if gs["super_active"]%2==0:
            arc_y2 = beam_y
            for ax in range(int(beam_x),int(beam_end),30):
                arc_y2 += random.randint(-10,10)
                arc_y2 = max(beam_y-20, min(beam_y+20, arc_y2))
                pygame.draw.line(screen,(200,255,255),(ax,arc_y2),(ax+30,arc_y2+random.randint(-8,8)),2)
        lbl = font_big.render("★  SUPER LASER  ★", True, NEON_YELLOW)
        sh  = font_big.render("★  SUPER LASER  ★", True, (80,60,0))
        screen.blit(sh,  (WIDTH//2-lbl.get_width()//2+2, HEIGHT//2-60+2))
        screen.blit(lbl, (WIDTH//2-lbl.get_width()//2,   HEIGHT//2-60))

    # Mega laser cinematic
    if gs["mega_active"] > 0:
        draw_mega_cinematic(screen, gs)

    if gs["cinematic_alpha"] > 0 and gs["mega_active"] == 0:
        bh = int(gs["cinematic_alpha"])
        bs = pygame.Surface((WIDTH,bh), pygame.SRCALPHA)
        bs.fill((0,0,0,220)); screen.blit(bs,(0,0)); screen.blit(bs,(0,HEIGHT-bh))

    # Boss incoming — only when boss is visible on screen for first time
    if gs["show_boss_warning"] and gs["boss_warning_timer"] > 0:
        if (gs["boss_warning_timer"]//8)%2==0:
            warn_bg = pygame.Surface((380, 75), pygame.SRCALPHA)
            warn_bg.fill((0,0,0,170))
            pygame.draw.rect(warn_bg, (*NEON_RED, 180), (0, 0, 380, 75), 2, border_radius=6)
            screen.blit(warn_bg, (WIDTH//2-190, HEIGHT//2-85))
            warn_txt = font_big.render("⚠  BOSS INCOMING  ⚠", True, NEON_RED)
            screen.blit(warn_txt, (WIDTH//2-warn_txt.get_width()//2, HEIGHT//2-78))
            dist_txt = font_small.render("Defeat the boss to advance!", True, WHITE)
            screen.blit(dist_txt, (WIDTH//2-dist_txt.get_width()//2, HEIGHT//2-44))

    # Phase 2 rage warning
    if boss.alive and boss.warning_flash > 0 and (boss.warning_flash//5)%2==0:
        rage_bg = pygame.Surface((320, 44), pygame.SRCALPHA)
        rage_bg.fill((0,0,0,150))
        screen.blit(rage_bg, (WIDTH//2-160, HEIGHT//2-60))
        rage = font_big.render("BOSS ENRAGED!", True, NEON_ORANGE)
        screen.blit(rage, (WIDTH//2-rage.get_width()//2, HEIGHT//2-50))

    # Rocket boarding prompt
    if gs["player_in_rocket"] and not rocket.launching:
        board_bg = pygame.Surface((300, 40), pygame.SRCALPHA)
        board_bg.fill((0,0,0,160))
        screen.blit(board_bg, (WIDTH//2-150, HEIGHT//2-50))
        board_txt = font_big.render("🚀 LAUNCHING...", True, NEON_YELLOW)
        screen.blit(board_txt, (WIDTH//2-board_txt.get_width()//2, HEIGHT//2-40))

    draw_weapon_hud(screen, gs["weapon"], gs["weapon_ammo"])

    # Weapon pickup flash overlay
    if gs["weapon_pickup_flash"] > 0:
        flash_frac = gs["weapon_pickup_flash"] / 80
        col = WEAPON_COLORS.get(gs["weapon"], NEON_CYAN)
        fov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        fov.fill((*col, int(60*flash_frac)))
        screen.blit(fov, (0,0))
        wf = pygame.font.SysFont("consolas", 32, bold=True)
        icons = {"blaster":"◉","shotgun":"⊕","rocket":"⚡","laser":"▶","flamethrower":"⬡"}
        pick_txt = wf.render(f"{icons.get(gs['weapon'],'?')} {gs['weapon'].upper()} EQUIPPED!", True, col)
        sh_txt   = wf.render(f"{icons.get(gs['weapon'],'?')} {gs['weapon'].upper()} EQUIPPED!", True, (0,0,0))
        screen.blit(sh_txt, (WIDTH//2-pick_txt.get_width()//2+2, HEIGHT//2-80+2))
        screen.blit(pick_txt, (WIDTH//2-pick_txt.get_width()//2, HEIGHT//2-80))

    draw_hud(gs["player_hp"], gs["score"], gs["kill_count"], gs["super_ready"], gs["super_stacks"], gs["mega_ready"], current_level)

    if tr_alpha > 0:
        ov = pygame.Surface((WIDTH,HEIGHT)); ov.fill((0,0,0)); ov.set_alpha(tr_alpha)
        screen.blit(ov,(0,0))

    pygame.display.update()

pygame.quit()
sys.exit()