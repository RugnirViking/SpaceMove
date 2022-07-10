import math
import random
from typing import TYPE_CHECKING, Optional

import pygame
from pygame import Rect

from colors import WHITE
from damagetext import DamageText
from entity import Entity
from explosion import Explosion
from object import Object
from utils import rot_center, ANGULAR_VELOCITY, PAR_SPREAD

if TYPE_CHECKING:
    from engine import Engine


class Player():
    target: Optional[Entity]
    sprite: pygame.image
    angle: float
    angle_target: float

    def __init__(self, img_path, engine):
        self.angle = 0.0
        self.sprite = pygame.image.load(img_path).convert_alpha()
        self.angle_target = 0.0
        self.engine = engine
        self.angular_vel = 0
        self.max_angular_vel = 350
        width, height = self.sprite.get_width(), self.sprite.get_height()  # get size
        self.sprite = pygame.transform.scale(self.sprite, (int(width / 6), int(height / 6)))
        self.target = None
        self.hull = 100.0
        self.max_hull = 100.0
        self.shields = 100.0
        self.max_shields = 100.0
        self.energy = 100.0
        self.max_energy = 100.0
        self.heat = 50
        self.max_heat = 100.0
        self.is_in_radiation = False
        self.lastrad_damage = 5
        self.nextrad_time = 0
        self.x = 0
        self.y = 0
        self.dead = False
        self.explosion_sound = pygame.mixer.Sound("resources/sound/explosion.ogg")
        self.damagesounds = []
        self.damagesounds.append(pygame.mixer.Sound("resources/sound/damagesound1.ogg"))
        self.damagesounds.append(pygame.mixer.Sound("resources/sound/damagesound2.ogg"))
        self.damagesounds.append(pygame.mixer.Sound("resources/sound/damagesound3.ogg"))

        self.shieldshitsound = pygame.mixer.Sound("resources/sound/shieldhit.wav")
        self.shieldsdownsound = pygame.mixer.Sound("resources/sound/shieldsdown.wav")
        self.lasersound = pygame.mixer.Sound("resources/sound/pew.mp3")

        self.minimapradius = 500
        converted = self.engine.minimap_dist_convert(self.minimapradius)
        self.tsurf = pygame.Surface((self.engine.minimap_dist_convert(self.minimapradius) * 2, converted * 2))
        pygame.draw.circle(self.tsurf, (255, 255, 255), (converted, converted), converted)
        self.tsurf.set_alpha(128)
        self.tsurf.set_colorkey((0, 0, 0))

        self.cooldowns = [0, 0]
        self.cooldown_time = [300, 2000]
        self.weapons = [self.firelaser, self.firemissile]
        self.queue = []
        self.lookangle = 0
        self.mouselookmode = False
        self.laserdamage = 10

    def collision_radius(self) -> int:
        return max(self.sprite.get_width(), self.sprite.get_height()) // 2

    def laserhit(self,target):
        target.take_damage(self.laserdamage)


    def firelaser(self):
        if self.engine.gameUIcontroller.selections[0] and self.target:
            a = self.targetAngle() + 180
            spawnpos = (-self.x,-self.y)

            self.engine.projectilemanager.add_projectile(spawnpos[0],spawnpos[1],
                                                         1400 * math.sin((a * (math.pi / 180))),
                                                         1400 * math.cos((a * (math.pi / 180))),
                                                         "resources/img/laserbolt.png",(255,255,255),
                                                         self.target,self.laserhit)
            self.engine.playsound(self.lasersound,0.5)
            self.cooldowns[0] = self.cooldown_time[0]

        elif self.engine.gameUIcontroller.selections[0] and self.mouselookmode:
            a = self.get_angle_to_mouse(self.engine.surface)
            spawnpos = (-self.x,-self.y)

            self.engine.projectilemanager.add_projectile(spawnpos[0],spawnpos[1],
                                                         1400 * math.sin((a * (math.pi / 180))),
                                                         1400 * math.cos((a * (math.pi / 180))),
                                                         "resources/img/laserbolt.png",(255,255,255))
            self.engine.playsound(self.lasersound,0.5)
            self.cooldowns[0] = self.cooldown_time[0]

    def get_angle_to_mouse(self,surf) -> float:
        mx, my = self.engine.mouse_pos
        return (math.atan2(mx - surf.get_rect().centerx, my - surf.get_rect().centery) * (180 / math.pi))%360

    def spawntrailparticle(self,i):
        if self.target:
            a = self.targetAngle() + 180
            for x in range(1):
                self.engine.particlemanager.add_particle([self.engine.width / 2, self.engine.height / 2],
                                                         [400 * math.sin(
                                                             (a + random.randrange(-1, 1, 1)) * (
                                                                         math.pi / 180)),
                                                          400 * math.cos(
                                                              (a + random.randrange(-1, 1, 1)) * (
                                                                          math.pi / 180))],
                                                         (255, 0, 0), random.randint(3, 5), random.random() + 1, 0)

    def firemissile(self):
        if self.engine.gameUIcontroller.selections[1] and self.target:
            a = self.targetAngle() + 180
            for x in range(10):
                self.queue.append([x*10,self.spawntrailparticle,0])
            self.cooldowns[1] = self.cooldown_time[1]

    def update_cooldowns(self, dt):
        for i in range(len(self.cooldowns)):
            if self.cooldowns[i] > 0:
                self.cooldowns[i] -= dt * 1000
                if self.cooldowns[i] < 0:
                    self.weapons[i]()
            else:
                self.weapons[i]()

        for i in range(len(self.queue)):
            if self.queue[i][0] < 0:
                self.queue[i][1](self.queue[i][2])
                del self.queue[i]
                break
            else:
                self.queue[i][0] -= dt * 1000


    def update(self):

        if not self.dead:
            self.update_cooldowns(self.engine.deltaTime)
            self.angle = self.angle % 360

            angle_error = (self.angle - self.angle_target) % 360

            if 0 < angle_error < 180:
                self.angle -= self.max_angular_vel * self.engine.deltaTime
                if angle_error < self.max_angular_vel * self.engine.deltaTime:
                    self.angle = self.angle_target
            elif angle_error > 180:
                self.angle += self.max_angular_vel * self.engine.deltaTime
                if angle_error < self.max_angular_vel * self.engine.deltaTime:
                    self.angle = self.angle_target
            if abs(self.angle - self.angle_target) < 5:
                self.angle = self.angle_target

            # do player control

            err = math.dist((self.x, self.y), (-self.engine.targetpx, -self.engine.targetpy))
            snapped = False
            if err < (400 * self.engine.deltaTime):
                self.x = -self.engine.targetpx
                self.y = -self.engine.targetpy
                snapped = True
            else:
                self.x += 400 * math.sin(self.angle * (math.pi / 180)) * self.engine.deltaTime
                self.y += 400 * math.cos(self.angle * (math.pi / 180)) * self.engine.deltaTime

                width, height = self.engine.surface.get_size()
                if random.random() > 0.5:
                    self.engine.particlemanager.add_particle(
                        [width / 2, height / 2],
                        [400 * math.sin((self.angle + random.randrange(-PAR_SPREAD, PAR_SPREAD, 1)) * (math.pi / 180)),
                         400 * math.cos((self.angle + random.randrange(-PAR_SPREAD, PAR_SPREAD, 1)) * (math.pi / 180))],
                        (255, 255, 255), random.randint(3, 5), random.random() + 1, 0
                    )

            if err > (2000 * self.engine.deltaTime) and not snapped:
                o = self.engine.targetpx + self.x
                a = self.engine.targetpy + self.y
                angle = math.atan2(o, a)
                self.set_new_angle(angle * (180 / math.pi) - 180)

            if self.target:
                if self.target.dead:
                    self.target=None

            if abs(self.x) > 2730 or abs(self.y) > 1330:
                self.engine.alert_sound.set_volume(0.05 * self.engine.mastervolume * self.engine.sound_effect_volume)
                pygame.mixer.Sound.play(self.engine.alert_sound)

                if not self.is_in_radiation:
                    self.is_in_radiation = True
                    self.nextrad_time = self.engine.t + 500

                if self.nextrad_time <= self.engine.t:
                    self.lastrad_damage = self.lastrad_damage * 1.1
                    self.nextrad_time = self.engine.t + 500

                    self.take_damage(self.lastrad_damage * 1.1)
            else:
                self.lastrad_damage = 5
                self.nextrad_time = 0
                self.is_in_radiation = False
                self.engine.alert_sound.set_volume(0.0)

    def draw(self, surf):

        self.update()

        if not self.dead:
            rect = Rect(surf.get_rect().centerx - self.sprite.get_width() / 2,
                        surf.get_rect().centery - self.sprite.get_height() / 2, self.sprite.get_width(),
                        self.sprite.get_height())

            rotangle = 0
            if self.mouselookmode:
                mx, my = pygame.mouse.get_pos()
                rotangle = math.atan2(mx - surf.get_rect().centerx, my - surf.get_rect().centery) * (180 / math.pi)-180
                rotangle = rotangle % 360
                self.lookangle = rotangle
            elif self.target:
                rotangle = self.targetAngle()
                self.lookangle = rotangle
            else:
                rotangle = self.angle
                self.lookangle = rotangle
            rotated_image, rect = rot_center(self.sprite, rect, rotangle)

            surf.blit(rotated_image, rect)


    def set_new_angle(self, angle):
        self.angle_target = angle % 360

    def targetAngle(self) -> float:

        playerpos = (-self.x + self.engine.surface.get_width() / 2,
                     -self.y + self.engine.surface.get_height() / 2)

        o = self.target.x - playerpos[0]
        a = self.target.y - playerpos[1]
        angle = math.atan2(o, a)
        return (angle * (180 / math.pi) - 180) % 360

    def distance_to(self, object: Object) -> float:
        return math.dist(
            (-self.x + self.engine.surface.get_width() / 2, -self.y + self.engine.surface.get_height() / 2),
            (object.x, object.y))

    def die(self):
        self.hull = 0
        self.engine.alert_sound.set_volume(0)
        self.explosion_sound.set_volume(0.95 * self.engine.mastervolume * self.engine.sound_effect_volume)
        pygame.mixer.find_channel(True).play(self.explosion_sound)

        self.engine.explosion_group.add(
            Explosion(self.engine.surface.get_width() / 2, self.engine.surface.get_height() / 2))
        self.engine.explosion_group.add(
            Explosion(self.engine.surface.get_width() / 2 + 45, self.engine.surface.get_height() / 2 - 27, 0.2))
        self.engine.explosion_group.add(
            Explosion(self.engine.surface.get_width() / 2 - 11, self.engine.surface.get_height() / 2 - 42, 1.25))
        self.engine.explosion_group.add(
            Explosion(self.engine.surface.get_width() / 2 - 33, self.engine.surface.get_height() / 2 + 18, 0.7))
        self.dead = True

    def take_damage(self, param):
        if self.shields > 0:
            self.shields -= param

            self.engine.damagetext.append(
                DamageText(self.engine.surface.get_width() / 2, self.engine.surface.get_height() / 2,
                           f"-{round(self.lastrad_damage)}", (0, 180, 255), self.engine.damagefont))
            if self.shields < 0:
                self.shields = 0

                sound = self.shieldsdownsound
                sound.set_volume(0.55 * self.engine.mastervolume * self.engine.sound_effect_volume)
                pygame.mixer.find_channel(True).play(sound)
            else:
                sound = self.shieldshitsound
                sound.set_volume(0.55 * self.engine.mastervolume * self.engine.sound_effect_volume)
                pygame.mixer.find_channel(True).play(sound)
        else:
            self.hull -= param
            self.engine.damagetext.append(
                DamageText(self.engine.surface.get_width() / 2, self.engine.surface.get_height() / 2,
                           f"-{round(self.lastrad_damage)}", (255, 0, 0), self.engine.damagefont))

            sound = random.choice(self.damagesounds)
            sound.set_volume(0.95 * self.engine.mastervolume * self.engine.sound_effect_volume)
            pygame.mixer.find_channel(True).play(sound)
            if self.hull < 0:
                self.die()
