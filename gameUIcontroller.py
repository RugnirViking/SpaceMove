import pygame

import colors
from Asteroid import Asteroid
from entity import Entity
from marker import Marker
from utils import QuadEaseInOut, rot_center


class GameUIController:
    def __init__(self, engine):
        self.engine=engine

        self.headerui = pygame.image.load("resources/img/uiheader.png").convert_alpha()
        self.headerui = pygame.transform.scale(self.headerui, (int(self.headerui.get_rect().width/2), int(self.headerui.get_rect().height/2)))
        self.headeruiflipped = pygame.transform.flip(self.headerui, True, False)

        self.sectortext = self.engine.sectorfont.render("Sector 12-1-AB", True, colors.BLACK)
        self.sectortextrect = self.sectortext.get_rect()
        self.sectortextrect.center = (self.engine.surface.get_width()/2, 18)

        self.warning_symbol = pygame.image.load("resources/img/warning.png").convert_alpha()
        w_width, w_height = self.warning_symbol.get_width(), self.warning_symbol.get_height()  # get size
        self.warning_symbol = pygame.transform.scale(self.warning_symbol, (int(w_width/4), int(w_height/4)))

        self.actionbar = pygame.image.load("resources/img/actionbar.png").convert_alpha()

        self.selection = pygame.image.load("resources/img/selection.png").convert_alpha()
        self.disabled_selection = pygame.image.load("resources/img/selectiondisabled.png").convert_alpha()

        self.laser_icon = pygame.image.load("resources/img/laser.png").convert_alpha()
        self.missile_icon = pygame.image.load("resources/img/missile.png").convert_alpha()
        self.bullet_icon = pygame.image.load("resources/img/bullet.png").convert_alpha()
        self.biglaser_icon = pygame.image.load("resources/img/biglaser.png").convert_alpha()
        self.shield_icon = pygame.image.load("resources/img/shield.png").convert_alpha()


        self.disabled_laser_icon = pygame.image.load("resources/img/d_laser.png").convert_alpha()
        self.disabled_missile_icon = pygame.image.load("resources/img/d_missile.png").convert_alpha()
        self.disabled_bullet_icon = pygame.image.load("resources/img/d_bullet.png").convert_alpha()
        self.disabled_biglaser_icon = pygame.image.load("resources/img/d_biglaser.png").convert_alpha()
        self.disabled_shield_icon = pygame.image.load("resources/img/d_shield.png").convert_alpha()

        self.selectionposlist = [[58,-6],[200,-6],[343,-6],[485,-6],[628,-6]]

        self.selections = [False,True,True,True,True]
        self.enabled = [True,True,False,False,False]
        self.icons = [self.laser_icon,self.missile_icon,self.bullet_icon,self.biglaser_icon,self.shield_icon]
        self.disabled_icons = [self.disabled_laser_icon,self.disabled_missile_icon,self.disabled_bullet_icon,self.disabled_biglaser_icon,self.disabled_shield_icon]


    def draw(self,surf,width,height):

        if self.engine.player.is_in_radiation:
            # render the warning symbol partially transparent
            t_surf = pygame.Surface((self.warning_symbol.get_width(), self.warning_symbol.get_height()),
                                    pygame.SRCALPHA)
            a = int(QuadEaseInOut(0,255,500).ease(self.engine.t-self.engine.flash_start_time))
            if self.engine.flashrising:
                a = 255-a
            self.warning_symbol.set_alpha(a)
            w_rect = self.warning_symbol.get_rect()
            w_rect.centerx = self.engine.surface.get_width() - 240
            w_rect.bottom = self.engine.surface.get_height() - 300
            t_surf.blit(self.warning_symbol, (0, 0))
            surf.blit(t_surf, w_rect)

            self.engine.Render_Text("Radiation", self.engine.sectorfont, colors.RED, (w_rect.centerx, w_rect.centery - 80), surf, centered=True)


        pygame.draw.rect(surf, (0, 0, 0), pygame.Rect(0, 0, 80, 50))
        self.engine.Render_Text(str(int(self.engine.clock.get_fps())), self.engine.smallfont2, (255, 0, 0), (24, 18),surf)

        pygame.draw.rect(surf,(0,0,0),pygame.Rect(80,0,surf.get_width()-80,50))

        minirect = pygame.Rect(width-480+6, height-250+6, 480-12, 250-12)
        pygame.draw.rect(surf, (45,45,45), pygame.Rect(width-480+6, height-250+6, 480-12, 250-12))
        pygame.draw.rect(surf, colors.LIGHTGREY, pygame.Rect(width-480+6, height-250+6, 480-12, 250-12),12)

        # draw a circle on the minimap around the player
        surf.blit(self.engine.player.tsurf, (int(minirect.centerx-self.engine.minimap_dist_convert(self.engine.player.minimapradius) - self.engine.player.x / 12),
                              int(minirect.centery-self.engine.minimap_dist_convert(self.engine.player.minimapradius) - self.engine.player.y / 12)))

        pygame.draw.circle(surf,(255,0,0),(int(minirect.centerx-self.engine.player.x/12),int(minirect.centery-self.engine.player.y/12)),6)
        pygame.draw.circle(surf,(255,255,0),(int(minirect.centerx+self.engine.targetpx/12),int(minirect.centery+self.engine.targetpy/12)),2)

        # if the player is close enough to the space station to dock, display a text notification
        if self.engine.player.distance_to(self.engine.station) < 250:
            self.engine.Render_Text("DOCK", self.engine.smallfont2, (255, 255, 255), (135,25), surf, centered=True)


        for object in self.engine.objects:
            if not isinstance(object,Marker):

                if (object.x+self.engine.player.x-width/2)**2 + (object.y+self.engine.player.y-height/2)**2 < self.engine.player.minimapradius**2:
                    if isinstance(object, Entity):
                        if self.engine.player.target == object:
                            # draw a cross on the minimap at the player's targeted enemy
                            tpos = (int(minirect.centerx + (object.x - width / 2) / 12), int(minirect.centery + (object.y - height / 2) / 12))
                            pygame.draw.circle(surf, (255, 255, 0),
                                               (tpos[0]+1,
                                                tpos[1]+1),3)
                            pygame.draw.line(surf, (255, 255, 0),(tpos[0]-5,tpos[1]-5),(tpos[0]+5,tpos[1]+5),2)
                            pygame.draw.line(surf, (255, 255, 0),(tpos[0]-5,tpos[1]+5),(tpos[0]+5,tpos[1]-5),2)
                            if not isinstance(object, Asteroid):
                                pygame.draw.circle(surf, (0, 128, 255),
                                           (int(minirect.centerx + (object.ai.targetpos[0] - width / 2) / 12),
                                            int(minirect.centery + (object.ai.targetpos[1] - height / 2) / 12)), 2)
                        else:
                            pygame.draw.circle(surf, (255, 255, 255),
                                   (int(minirect.centerx + (object.x-width/2) / 12), int(minirect.centery + (object.y-height/2) / 12)), 4)
                            if not isinstance(object, Asteroid):
                                pygame.draw.circle(surf, (0, 128, 255),
                                           (int(minirect.centerx + (object.ai.targetpos[0] - width / 2) / 12),
                                            int(minirect.centery + (object.ai.targetpos[1] - height / 2) / 12)), 2)



        self.engine.Render_Text(f"{round(self.engine.player.x)}, {round(self.engine.player.y)}", self.engine.smallfont2, (255, 255, 255), (width-580, height-20),surf,True)
        mx, my = pygame.mouse.get_pos()
        mp = (mx,my)
        mp_world = self.engine.screen_to_world(mp)
        self.engine.Render_Text(f"{self.engine.is_on_screen(mp_world[0]-surf.get_width()/2,round(mp_world[1]-surf.get_height()/2))} {round(mx)}, {round(my)} ({round(mp_world[0]-surf.get_width()/2)}, {round(mp_world[1]-surf.get_height()/2)})", self.engine.smallfont2, (255, 255, 255), (width-580, height-45),surf,True)

        self.engine.Render_Text(f"{round(self.engine.targetpx)}, {round(self.engine.targetpy)}", self.engine.smallfont2, (255, 255, 255), (width-580, height-70),surf,True)

        if self.engine.player.target:
            twidth, theight = self.engine.player.target.target_sprite.get_width(), self.engine.player.target.target_sprite.get_height()
            self.engine.targetsprite = self.engine.player.target.target_sprite
            trect: pygame.rect.RectType = self.engine.targetsprite.get_rect()
            twidth, theight = trect.width, trect.height
            largest = max(twidth,theight)/1.5
            pygame.draw.circle(surf,(45,45,45),(100,400),int(largest))
            pygame.draw.circle(surf,(165,165,165),(100,400),int(largest),2)

            trect.centerx = 100
            trect.centery = 400
            rotated_image, rrect = rot_center(self.engine.targetsprite, trect, self.engine.player.target.ai.look_angle)
            surf.blit(rotated_image,rrect)

            self.engine.Render_Text(f"Dist: {round(self.engine.player.target.ai.dist_to_player(),1)}", self.engine.smallfont2, (255, 255, 255),
                             (100, 500), surf, True)

        # update and draw all the damagetext
        for text in self.engine.damagetext:
            text.update(self.engine.deltaTime)
            text.draw(surf)
            if not text.active:
                self.engine.damagetext.remove(text)

        # draw the actionbar
        actionbar_surface = pygame.Surface((self.actionbar.get_width(), self.actionbar.get_height()+50), pygame.SRCALPHA)
        actionbar_surface.blit(self.actionbar,(0,actionbar_surface.get_height()-self.actionbar.get_height()))
        # draw the actionbar's buttons
        for i in range(len(self.selections)):

            if self.enabled[i]:
                if self.selections[i]:
                    actionbar_surface.blit(self.selection, (self.selectionposlist[i][0],
                                                            actionbar_surface.get_height() - self.selection.get_height() +
                                                            self.selectionposlist[i][1]))
                actionbar_surface.blit(self.icons[i],(self.selectionposlist[i][0]+26,actionbar_surface.get_height()-self.icons[i].get_height()-24))
            else:
                actionbar_surface.blit(self.disabled_icons[i],(self.selectionposlist[i][0]+26,actionbar_surface.get_height()-self.disabled_icons[i].get_height()-24))
                actionbar_surface.blit(self.disabled_selection, (self.selectionposlist[i][0],
                                                        actionbar_surface.get_height() - self.selection.get_height() +
                                                        self.selectionposlist[i][1]))


        surf.blit(actionbar_surface,(0,height-actionbar_surface.get_height()))
        # render the hp bar under the overlay
        hull_pct = self.engine.player.hull / self.engine.player.max_hull
        hull_rect = pygame.Rect(0,0,int(hull_pct*410),10)
        hull_rect.right = width/2-210
        hull_rect.bottom = 35
        pygame.draw.rect(surf,(0,180,0),hull_rect)


        # render the player shield bar under the overlay
        hull_pct = self.engine.player.shields / self.engine.player.max_shields
        hull_rect = pygame.Rect(0,0,int(hull_pct*420),10)
        hull_rect.right = width/2-215
        hull_rect.bottom = 20
        pygame.draw.rect(surf,(0,80,255),hull_rect)

        # render the player energy bar under the overlay
        hull_pct = self.engine.player.energy / self.engine.player.max_energy
        hull_rect = pygame.Rect(0,0,int(hull_pct*420),10)
        hull_rect.left = width/2+215
        hull_rect.bottom = 20
        pygame.draw.rect(surf,(255,255,0),hull_rect)

        # render the player heat bar under the overlay
        hull_pct = self.engine.player.heat / self.engine.player.max_heat
        hull_rect = pygame.Rect(0,0,int(hull_pct*410),10)
        hull_rect.left = width/2+210
        hull_rect.bottom = 35
        pygame.draw.rect(surf,(200,80,0),hull_rect)

        #  render the overlay
        headerRect = self.headerui.get_rect()
        headerRect.right = width/2+50
        headerRect.top = 0
        surf.blit(self.headerui,headerRect)

        headeruiflipped = self.headeruiflipped.get_rect()
        headeruiflipped.left = width/2-50
        headeruiflipped.top = 0
        surf.blit(self.headeruiflipped,headeruiflipped)

        # render the sector
        surf.blit(self.sectortext,self.sectortextrect)

    def update(self,dt):
        # TODO: move ui updating here from draw
        pass