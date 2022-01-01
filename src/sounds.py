import pygame
import os

from pygame import mixer


class Sounds:
    def __init__(self, access):

        mixer.pre_init(44100, -16, 16, 512)
        mixer.init()
        self.access = access
        self.setting = access.setting

        self.gametrack = mixer.Sound("sounds/Theme/BattleInTheWinter.wav")

        self.shoot_effect = mixer.Sound("sounds/Effects/CanonDistanceFire-01.wav")
        self.gatling_effect = mixer.Sound("sounds/Effects/MachineGun.wav")
        self.move_effect = mixer.Sound("sounds/Effects/TankMoving.wav")
        self.laser_effect = mixer.Sound("sounds/Effects/LaserGun.wav")
        self.laser_charge_effect = mixer.Sound("sounds/Button/LaserChargeEffect.wav")
        self.explode_effect = mixer.Sound("sounds/Effects/GiantExplosion.wav")
        self.button_change = mixer.Sound("sounds/Button/button02.wav")
        self.button_access = mixer.Sound("sounds/Button/button05.wav")


        #   Channels
        self.channel1 = mixer.Channel(1)
        self.channel2 = mixer.Channel(2)
        self.channel3 = mixer.Channel(3)
        self.channel4 = mixer.Channel(4)
        self.channel5 = mixer.Channel(5)
        self.channel6 = mixer.Channel(6)
        self.channel7 = mixer.Channel(7)

    def shootPlayer(self):
        self.shoot_effect.set_volume(0.3)
        self.shoot_effect.get_length()
        self.channel4.play(self.shoot_effect)

    def machineGun(self):
        self.gatling_effect.set_volume(0.2)
        self.channel7.play(self.gatling_effect)

    def chargeSound(self):
        self.gatling_effect.set_volume(0.2)
        self.channel1.play(self.laser_charge_effect)

    def shootLaser(self):
        self.gatling_effect.set_volume(0.2)
        self.channel2.play(self.laser_effect)

    def explodeSound(self):
        pass

    def moveSound(self):
        self.move_effect.set_volume(0.3)
        self.channel5.play(self.move_effect, -1)

    def stopmoveSound(self):
        self.channel5.stop()

    def buttonChange(self):
        self.button_change.play()

    def buttonAccess(self):
        self.button_access.set_volume(12)
        self.button_access.play()

    def themeTrack(self):
        self.gametrack.set_volume(1)
        pygame.mixer.Sound.play(self.gametrack, -1)




