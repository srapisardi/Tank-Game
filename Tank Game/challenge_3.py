from superwires import games, color
import math

games.init(screen_width=800, screen_height=600,fps=60)


class Blue(games.Sprite):
    image = games.load_image("blue_tank.png")
    NEXT_SHOT = 50

    def __init__(self):
        super(Blue,self).__init__(image = Blue.image,
                                  x = 40,
                                  y = games.screen.height/2)

        self.missile_wait = 0

        self.score = games.Text(value=5,
                                size = 50,
                                color = color.blue,
                                x = 40,
                                y = 40,
                                is_collideable = False)

        games.screen.add(self.score)

    def update(self):
        if games.keyboard.is_pressed(games.K_d):
            self.angle += 1
        if games.keyboard.is_pressed(games.K_a):
            self.angle -= 1
        if games.keyboard.is_pressed(games.K_w):
            angle = self.angle * math.pi / 180
            self.x += 1 * math.cos(angle)
            self.y -= 1 * -math.sin(angle)


        if self.missile_wait > 0:
            self.missile_wait -= 1
        if games.keyboard.is_pressed(games.K_SPACE) and self.missile_wait == 0:
            shoot = Missile(self.x, self.y, self.angle)
            games.screen.add(shoot)
            self.missile_wait = Blue.NEXT_SHOT

        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
        if self.top < 0:
            self.top = 0
        if self.bottom > games.screen.height:
            self.bottom = games.screen.height

        for sprites in self.overlapping_sprites:
            if self.left > sprites.x:
                self.left = self.x - 27
            if self.right < sprites.x:
                self.right = self.x + 27
            if self.top > sprites.y:
                self.top = self.y - 27
            if self.bottom < sprites.y:
                self.bottom = self.y + 27


    def die(self):
        self.destroy()
        self.score.value -= 1
        explode = Explosion(x = self.x, y = self.y)
        games.screen.add(explode)
        if self.score.value > 0:
            games.screen.add(self)
            self.x = 40
            self.y = games.screen.height/2

        if self.score.value == 0:
            game_over = games.Message(value="Red Wins!",
                                      size = 90,
                                      color = color.black,
                                      x = games.screen.width/2,
                                      y = games.screen.height/2,
                                      lifetime = 5 * games.screen.fps,
                                      after_death = games.screen.quit,
                                      is_collideable = False)

            games.screen.add(game_over)


class Red(games.Sprite):
    image = games.load_image("red_tank.png")
    NEXT_SHOT = 50

    def __init__(self):
        super(Red, self).__init__(image=Red.image,
                                  x = games.screen.width - 40,
                                  y = games.screen.height/2,
                                  angle = 180)
        self.missile_wait = 0

        self.score = games.Text(value = 5,
                                size = 50,
                                color = color.red,
                                x = games.screen.width - 40,
                                y = 40,
                                is_collideable = False)

        games.screen.add(self.score)

    def update(self):
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= 1
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += 1
        if games.keyboard.is_pressed(games.K_UP):
            angle = self.angle * math.pi / 180
            self.x += 1 * math.cos(angle)
            self.y -= 1 * -math.sin(angle)
        if self.missile_wait > 0:
            self.missile_wait -= 1
        if games.keyboard.is_pressed(games.K_RALT) and self.missile_wait == 0:
            shoot = Missile(self.x, self.y, self.angle)
            games.screen.add(shoot)
            self.missile_wait = Red.NEXT_SHOT

        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
        if self.top < 0:
            self.top = 0
        if self.bottom > games.screen.height:
            self.bottom = games.screen.height

        for sprites in self.overlapping_sprites:
            if self.left > sprites.x:
                self.left = self.x - 27
            if self.right < sprites.x:
                self.right = self.x + 27
            if self.top > sprites.y:
                self.top = self.y - 27
            if self.bottom < sprites.y:
                self.bottom = self.y + 27

    def die(self):
        self.destroy()
        self.score.value -= 1
        explode = Explosion(x = self.x, y = self.y)
        games.screen.add(explode)
        if self.score.value > 0:
            games.screen.add(self)
            self.x = games.screen.width - 40
            self.y = games.screen.height/2

        if self.score.value == 0:
            game_over = games.Message(value = "Blue Wins!",
                                                 size = 90,
                                       color = color.black,
                                  x = games.screen.width/2,
                                 y = games.screen.height/2,
                           lifetime = 5 * games.screen.fps,
                           after_death = games.screen.quit,
                                    is_collideable = False)

            games.screen.add(game_over)




class Explosion(games.Animation):
    images =  ["explosion1.bmp",
               "explosion2.bmp",
               "explosion3.bmp",
               "explosion4.bmp",
               "explosion5.bmp",
               "explosion6.bmp",
               "explosion7.bmp",
               "explosion8.bmp",
               "explosion9.bmp"]

    def __init__(self,x,y):
        super(Explosion, self).__init__(images = Explosion.images,
                                        x = x,
                                        y = y,
                                        n_repeats = 1,
                                        repeat_interval = 5,
                                        is_collideable = False)


class Missile(games.Sprite):
    image = games.load_image("missile.png")
    sound = games.load_sound("explosion.wav")
    BUFFER = 60
    LIFE = 40
    VELOCITY = 10

    def __init__(self,tank_x,tank_y,tank_angle):

        missile_angle = tank_angle * math.pi / 180

        buffer_x = Missile.BUFFER * math.cos(missile_angle)
        buffer_y = Missile.BUFFER * math.sin(missile_angle)
        x = tank_x + buffer_x
        y = tank_y + buffer_y

        dx = Missile.VELOCITY * math.cos(missile_angle)
        dy = Missile.VELOCITY * math.sin(missile_angle)

        super(Missile, self).__init__(image = Missile.image,
                                     x = x, y = y,
                                     dx = dx, dy = dy)

    def update(self):
        for sprite in self.overlapping_sprites:
            sprite.die()
            self.destroy()
            explosion = Explosion(self.x, self.y)
            games.screen.add(explosion)
            Missile.sound.play()

    def die(self):
        self.destroy()


class Walls(games.Sprite):
    def _init__(self, image, x, y):
        super(Walls, self).__init__(x = x,
                                    y = y)

    def die(self):
        pass




def main():
    bg = games.load_image("dirt.jpg")
    games.screen.background = bg

    games.music.load("main.mp3")
    games.music.play()

    blue_tank = Blue()
    games.screen.add(blue_tank)

    red_tank = Red()
    games.screen.add(red_tank)

    wall_one = games.load_image("wall_center.jpg")
    w_one = Walls(image = wall_one, x = games.screen.width/2, y = games.screen.height/2)
    games.screen.add(w_one)

    wall_two = games.load_image("wall_h.jpg")
    w_two = Walls(image = wall_two, x = games.screen.width/2, y = 100)
    games.screen.add(w_two)

    wall_three = games.load_image("wall_h.jpg")
    w_three = Walls(image = wall_three, x = games.screen.width/2, y = games.screen.height - 100)
    games.screen.add(w_three)

    wall_four = games.load_image("wall_v.jpg")
    w_four = Walls(image = wall_four, x = games.screen.width - 200, y = games.screen.height/2, angle = 90)
    games.screen.add(w_four)

    wall_five = games.load_image("wall_v.jpg")
    w_five = Walls(image = wall_five, x = 200, y = games.screen.height/2, angle = 90)
    games.screen.add(w_five)

    games.screen.mainloop()


main()
