from django.db import models
import time
import random

GRID_SIZE = 32
BASE_X = 16
BASE_Y = 16

class Robot(models.Model): 
    x = models.IntegerField(default=random.randint(0, GRID_SIZE - 1))
    y = models.IntegerField(default=random.randint(0, GRID_SIZE - 1))
    hasTrash = models.BooleanField(default=False)

    def move(self, occupied):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
        for dx, dy in directions:
            new_x = max(0, min(GRID_SIZE - 1, self.x + dx))
            new_y = max(0, min(GRID_SIZE - 1, self.y + dy))
            if not occupied[new_x][new_y]:
                occupied[self.x][self.y] = False
                self.x = new_x
                self.y = new_y
                self.save()
                occupied[self.x][self.y] = True
                return
        return

    def action(self, occupied):
        if self.hasTrash and (self.x, self.y) == (BASE_X, BASE_Y):
            self.hasTrash = False
            self.save()
            return

        if not self.hasTrash and Trash.objects.filter(x=self.x, y=self.y).exists():
            Trash.objects.filter(x=self.x, y=self.y).first().delete()
            self.hasTrash = True
            self.save()
            return

        if self.hasTrash:
            target = (BASE_X, BASE_Y)
        else:
            trash = Trash.objects.first() 
            target = (trash.x, trash.y) if trash else None

        if target:
            dx = dy = 0
            if target[0] > self.x:
                dx = 1
            elif target[0] < self.x:
                dx = -1
            elif target[1] > self.y:
                dy = 1
            elif target[1] < self.y:
                dy = -1

            new_x = max(0, min(GRID_SIZE - 1, self.x + dx))
            new_y = max(0, min(GRID_SIZE - 1, self.y + dy))
            if not occupied[new_x][new_y]:
                occupied[self.x][self.y] = False
                self.x = new_x
                self.y = new_y
                self.save()
                occupied[self.x][self.y] = True
                return
        return 

    def __str__(self):
        return f"( {self.x}, {self.y} )"

class Trash(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    
    def __str__(self):
        return f"( {self.x}, {self.y} )"
    
def run_simulation():
    occupied = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for robot in Robot.objects.all():
        occupied[robot.x][robot.y] = True
    while Trash.objects.exists():
        for robot in Robot.objects.all():
            robot.action(occupied)
        time.sleep(0.5) 

def start_simulation():
    Robot.objects.all().delete()
    Trash.objects.all().delete()
    for _ in range(5):
        Robot.objects.create(
            x=random.randint(0, GRID_SIZE - 1),
            y=random.randint(0, GRID_SIZE - 1),
            hasTrash=False
        )
    for _ in range(15):
        Trash.objects.create(
            x=random.randint(0, GRID_SIZE - 1),
            y=random.randint(0, GRID_SIZE - 1)
        )
    run_simulation()