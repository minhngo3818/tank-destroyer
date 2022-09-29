import pygame
from pygame import Sprite
from .settings import Settings as St

# Pass all data from Settings class
stats = St()


def playerFoeCollide(tolerance, player, enemyGroup, scr_width, scr_height):
    for enemy in enemyGroup:
        if pygame.sprite.collide_rect(player, enemy):

            if abs(enemy.rect.right - player.rect.left) < tolerance:
                player.left = False
                enemy.move = False
                enemy.rect.right = player.rect.left

                # (*) Prevent pushing over \left edge
                if enemy.rect.left <= 0:
                    enemy.rect.left = 0

            if abs(enemy.rect.left - player.rect.right) < tolerance:
                player.right = False
                enemy.move = False
                enemy.rect.left = player.rect.right

                # (*) Prevent pushing over right edge
                if enemy.rect.right >= scr_width:
                    enemy.rect.right = scr_width

            if abs(enemy.rect.bottom - player.rect.top) < tolerance:
                player.up = False
                enemy.move = False
                enemy.rect.bottom = player.rect.top

                # (*) Prevent pushing over bottom edge
                if enemy.rect.top <= 0:
                    enemy.rect.top = 0

            if abs(enemy.rect.top - player.rect.bottom) < tolerance:
                player.down = False
                enemy.rect.top = player.rect.bottom

                # (*)
                if enemy.rect.bottom >= scr_height:
                    enemy.rect.bottom = scr_height

            player.hp -= stats.collision_damage        # How to assign class to call an element
    return


def enemiesCollide(enemyGroup):
    pass
    return


def bulletCollideEnemy():
    pass
    return


def playerBossCollide():
    pass
    return
