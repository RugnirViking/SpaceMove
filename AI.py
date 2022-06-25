import math


class AI:
    def __init__(self, engine):
        self.engine = engine
        self.targetpos = (1400, 600)
        self.lookpos = (0, 0)
        self.entity = None
        self.look_angle = 0

    def retarget(self, aquire_bearing=False):
        pass

    def dist_to_player(self) -> float:
        return self.engine.distance_to_entity(self.engine.player, self.entity.x, self.entity.y)

class PlayerAI(AI):
    def __init__(self, engine):
        super().__init__(engine, engine.player)


class EnemyAI(AI):
    def __init__(self, engine):
        super().__init__(engine)
        self.target = None

    def retarget(self, aquire_bearing=False):
        from player import Player
        dist = 9999
        if isinstance(self.target, Player):
            dist = self.dist_to_player()
        if isinstance(self.target, Player) and dist > 1000:
            self.targetpos = (self.entity.x, self.entity.y)
            self.target = None
        if not isinstance(self.target, Player):
            if self.dist_to_player() < 450:
                self.target = self.engine.player
        elif aquire_bearing:
            if isinstance(self.target, Player) and dist < 1000:
                #
                # self.targetpos = (-self.engine.px + self.engine.surface.get_width() / 2,
                #               -self.engine.py + self.engine.surface.get_height() / 2)

                # target a position 100 units in front of the player
                playerpos = (-self.engine.px + self.engine.surface.get_width() / 2,
                             -self.engine.py + self.engine.surface.get_height() / 2)
                o = playerpos[0] - self.entity.x
                a = playerpos[1] - self.entity.y
                angle = math.atan2(o, a)

                self.targetpos = (
                    -self.engine.px + self.engine.surface.get_width() / 2 + 300 * math.cos(-angle-math.pi/2),
                    -self.engine.py + self.engine.surface.get_height() / 2 + 300 * math.sin(-angle-math.pi/2)
                )

        if isinstance(self.target, Player):
            playerpos = (-self.engine.px + self.engine.surface.get_width() / 2,
                          -self.engine.py + self.engine.surface.get_height() / 2)
            o = playerpos[0] - self.entity.x
            a = playerpos[1] - self.entity.y
            angle = math.atan2(o, a)
            self.look_angle = angle * (180 / math.pi) - 180
        else:
            self.look_angle = self.entity.angle



class SquarePatrolAI(AI):
    def __init__(self, engine):
        super().__init__(engine)
        self.waypoints = [
            (0, 0),
            (500,0),
            (500,500),
            (0,500),
        ]
        self.updatepos = True
        self.targetpos = self.waypoints[0]
        self.patrolpos = 1

    def retarget(self, aquire_bearing=False):
        if self.updatepos:
            for x,y in  enumerate(self.waypoints):
                self.waypoints[x] = (y[0] + self.entity.x, y[1] + self.entity.y)
            self.targetpos = self.waypoints[self.patrolpos]
            self.updatepos = False

        # if distance to the next waypoint is more than 50
        # move to the next waypoint
        if (self.entity.x - self.targetpos[0])**2 + (self.entity.y - self.targetpos[1])**2 < 50**2:
            # choose the next waypoint from the list
            self.patrolpos+=1
            if self.patrolpos >= len(self.waypoints):
                self.patrolpos = 0
            self.targetpos = self.waypoints[self.patrolpos]

        # if the player is within alert distance
        # switch to an enemyai
        dist = self.entity.dist_to_player()
        if dist < 400:
            self.targetpos = (self.entity.x, self.entity.y)
            self.entity.ai = EnemyAI(self.engine)
            self.entity.ai.entity = self.entity
            self.entity.ai.target = self.engine.player
            self.entity.ai.retarget(True)

        self.look_angle = self.entity.angle
