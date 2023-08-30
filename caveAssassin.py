import tkinter as tk
import tkinter.messagebox as messagebox
import random
import sys
from transformers import pipeline

scale_factor = 15
npc_names=["an old mage", "a pretty girl", "a strange creep", "a merchant", "a healer"]
gen = pipeline('text-generation', model='EleutherAI/gpt-neo-125M')
class NPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = random.choice(npc_names)
        self.gen = gen
    def answer(self, question, player):
        happy_gen = self.gen
        prompt = f"Question to {self.name}: "+question
        result = happy_gen(prompt, do_sample=True, min_length=12, max_length=512, temperature=0.9, top_k=0, top_p=0.969, repetition_penalty=0.79, num_return_sequences=1)
        player.points += 26
        return result[0]['generated_text']

class DigBot:
    def __init__(self, x, y):
        self.digging = False
        self.x = x
        self.y = y

    def start_digging(self):
        self.digging = True

    def stop_digging(self):
        self.digging = False

class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

weapons = [Weapon("Fists", 5),
            Weapon("Sword", 12),
            Weapon("Gun", 26),
            Weapon("Iron Fist", 50),
            Weapon("Cat'o'nine", 16),
            Weapon("Knife", 10),
            Weapon("Axe", 15),
            Weapon("Mace", 18),
            Weapon("Spear", 17),
            Weapon("Hammer", 10),
            Weapon("Dagger", 11),
            Weapon("Sai", 9),
            Weapon("Nunchucks", 8),
            Weapon("Bo Staff", 7),
            Weapon("Sling", 6),
            Weapon("Crossbow", 13),
            Weapon("Bow", 19),
            Weapon("Blowgun", 4),
            Weapon("Shuriken", 6),
            Weapon("Throwing Knives", 12),
            Weapon("Throwing Axe", 10)]

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.weapon = Weapon("Fists", 5)
        self.bomb = None
        self.points = 0
        self.lives = 3

class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.weapon = random.choice(weapons)
        self.dead = False

class Portal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Dungeon:
    def __init__(self):
        self.dungeon = self.generate_dungeon()

    def generate_dungeon(self):
        #cellular automata that generates a 2D dungeon map. the cells have two states: wall or floor
        #the map is generated by iterating over the cells and applying the following rules:
        #1. if a cell is a wall and has 3 or more walls adjacent to it, it becomes a wall
        #2. if a cell is a floor and has 4 or more walls adjacent to it, it becomes a wall
        #3. if a cell is a wall and has 2 or less walls adjacent to it, it becomes a floor
        #4. if a cell is a floor and has 3 or less walls adjacent to it, it becomes a floor
        
        #initialize the map with random walls and floors
        dungeon = [[random.randint(0, 1) for i in range(50)] for j in range(50)]

        #iterate over the map 5 times
        for i in range(5):
            #create a new map
            new_dungeon = [[0 for i in range(50)] for j in range(50)]
            #iterate over the cells in the map
            for y in range(50):
                for x in range(50):
                    #count the number of walls adjacent to the cell
                    wall_count = 0
                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            if x + i < 0 or x + i > 49 or y + j < 0 or y + j > 49:
                                continue
                            if dungeon[y + j][x + i] == 1:
                                wall_count += 1
                    #apply the rules to the cell
                    if dungeon[y][x] == 1:
                        if wall_count >= 4:
                            new_dungeon[y][x] = 1
                    else:
                        if wall_count >= 5:
                            new_dungeon[y][x] = 1
            #replace the old map with the new map
            dungeon = new_dungeon

        return dungeon
        
    def init_place_objects(self):
        #place the player, bomb, enemy, and portal in the dungeon

        #find a random empty space in the dungeon
        while True:
            x = random.randint(0, 49)
            y = random.randint(0, 49)
            if self.dungeon[y][x] == 0:
                break

        player_x = x * scale_factor
        player_y = y * scale_factor


        while True:
            x = random.randint(0, 49)
            y = random.randint(0, 49)
            if self.dungeon[y][x] == 0:
                break
 
        bomb_x = x * scale_factor
        bomb_y = y * scale_factor

        # Similarly, get the positions for enemy and portal
        
        while True:
            x = random.randint(0, 49)
            y = random.randint(0, 49)
            if self.dungeon[y][x] == 0:
                break

        enemy_x = x * scale_factor
        enemy_y = y * scale_factor

        while True:
            x = random.randint(0, 49)
            y = random.randint(0, 49)
            if self.dungeon[y][x] == 0:
                break
            
        portal_x = x * scale_factor
        portal_y = y * scale_factor

        while True:
            x = random.randint(0, 49)
            y = random.randint(0, 49)
            if self.dungeon[y][x] == 0:
                break

        npc_x = x * scale_factor
        npc_y = y * scale_factor

        return player_x, player_y, bomb_x, bomb_y, enemy_x, enemy_y, portal_x, portal_y, npc_x, npc_y
        
class Game:
    def __init__(self):
        self.window = tk.Tk()
        window_x = scale_factor * 50
        window_y = scale_factor * 60
        canvas_x = scale_factor * 50
        canvas_y = scale_factor * 50
        self.window.geometry(f"{window_x}x{window_y}")
        self.window.title("Cave Assassin--Kill the enemy and go through the portal to the next level!")
        self.canvas = tk.Canvas(self.window, width=canvas_x, height=canvas_y, bg="white")
        self.canvas.pack()
        self.status = tk.Label(self.window, text="Status: ok", fg="green", bg="black", font="Courier 13 bold")
        self.status.pack()
        self.dungeon = Dungeon()
        self.level=1
        self.digbot = DigBot(0, 0)
        self.dug_cells = []
        player_x, player_y, bomb_x, bomb_y, enemy_x, enemy_y, portal_x, portal_y, npc_x, npc_y = self.dungeon.init_place_objects()
        self.player = Player(player_x, player_y)
        self.resurrecting_player = False
        self.bomb = Bomb(bomb_x, bomb_y)
        self.enemy = Enemy(enemy_x, enemy_y)
        self.npc = NPC(npc_x, npc_y)
        self.portal = Portal(portal_x, portal_y)
        self.draw_dungeon()
        self.update_status()
        self.schedule_health_increase()
        self.move_enemy()
        self.window.bind("<Key>", self.key_pressed)
        self.window.mainloop()

    def reset_enemy(self):
        enemy_x, enemy_y = self.dungeon.init_place_objects()[4:6]
        self.enemy = Enemy(enemy_x, enemy_y)
        self.draw_dungeon()
        self.move_enemy()

    def move_enemy(self):
        if not self.enemy.dead:
            player_position = (self.player.x // scale_factor, self.player.y // scale_factor)
            enemy_position = (self.enemy.x // scale_factor, self.enemy.y // scale_factor)

            # Calculate the difference between enemy and player positions
            dx = player_position[0] - enemy_position[0]
            dy = player_position[1] - enemy_position[1]

            # Check if the enemy is in the next cell to the player
            if abs(dx) <= 1 and abs(dy) <= 1:
                self.fight()
            else:
                # Move enemy towards the player (horizontally or vertically)
                if abs(dx) > abs(dy):
                    if dx > 0 and self.can_move_to(enemy_position[0] + 1, enemy_position[1]):
                        self.enemy.x += scale_factor
                    elif dx < 0 and self.can_move_to(enemy_position[0] - 1, enemy_position[1]):
                        self.enemy.x -= scale_factor
                else:
                    if dy > 0 and self.can_move_to(enemy_position[0], enemy_position[1] + 1):
                        self.enemy.y += scale_factor
                    elif dy < 0 and self.can_move_to(enemy_position[0], enemy_position[1] - 1):
                        self.enemy.y -= scale_factor

            self.dungeon.dungeon[enemy_position[1]][enemy_position[0]] = 0
            self.draw_dungeon()
            self.window.after(1000, self.move_enemy)  # Move enemy periodically

    def can_move_to(self, x, y):
        # Check if the enemy can move to the specified cell
        if 0 <= x < 50 and 0 <= y < 50:
            return self.dungeon.dungeon[y][x] == 0
        return False

    def go_to_next_level(self):
        self.player.points += 250
        self.level += 1
        self.enemy.dead = True  # Stop enemy movement
        #initialize the dungeon
        self.dungeon = Dungeon()
        self.digbot = DigBot(0, 0)
        self.dug_cells = []
        player_x, player_y, bomb_x, bomb_y, enemy_x, enemy_y, portal_x, portal_y, npc_x, npc_y = self.dungeon.init_place_objects()
        weapon=self.player.weapon
        health=self.player.health
        points=self.player.points
        lives=self.player.lives
        self.player = Player(player_x, player_y)
        self.player.weapon = weapon
        self.player.health = health
        self.player.points = points
        self.player.lives = lives
        self.bomb = Bomb(bomb_x, bomb_y)
        self.enemy = Enemy(enemy_x, enemy_y)
        self.portal = Portal(portal_x, portal_y)
        self.npc = NPC(npc_x, npc_y)
        self.reset_enemy()
        self.draw_dungeon()
        self.update_status()

    def schedule_health_increase(self):
        #schedule the health increase
        self.window.after(800, self.health_increase)

    def health_increase(self):
        #increase the player's health
        self.player.health += 1
        #if the player's health is greater than 100, set it to 100
        if self.player.health > 100:
            self.player.health = 100
        #update the status label
        self.update_status()
        #schedule the health increase
        self.window.after(800, self.health_increase)

    def draw_dungeon(self):
        #draw the dungeon on the canvas
        #delete everything on the canvas
        self.canvas.delete("all")
        #get the dungeon map
        dungeon = self.dungeon.dungeon
  
        #place the player, bomb, enemy, portal, digbot and npc on the dungeon map
        dungeon[self.player.y // scale_factor][self.player.x // scale_factor] = 2
        if not self.player.bomb:
            dungeon[self.bomb.y // scale_factor][self.bomb.x // scale_factor] = 3
        if not self.enemy.dead:
            dungeon[self.enemy.y // scale_factor][self.enemy.x // scale_factor] = 4
        dungeon[self.portal.y // scale_factor][self.portal.x // scale_factor] = 5
        if self.digbot.digging:
            dungeon[self.digbot.y][self.digbot.x] = 6
        dungeon[self.npc.y // scale_factor][self.npc.x // scale_factor] = 7

        #iterate over the cells in the dungeon
        for y in range(50):
            for x in range(50):
                #wall
                if dungeon[y][x] == 1:
                    self.canvas.create_rectangle(x * scale_factor, y * scale_factor, x * scale_factor + scale_factor, y * scale_factor + scale_factor, fill="black")
                #floor
                elif dungeon[y][x] == 0:
                    self.canvas.create_rectangle(x * scale_factor, y * scale_factor, x * scale_factor + scale_factor, y * scale_factor + scale_factor, fill="white")
                #player
                elif dungeon[y][x] == 2:
                    self.canvas.create_rectangle(x * scale_factor, y * scale_factor, x * scale_factor + scale_factor, y * scale_factor + scale_factor, fill="blue")
                #bomb
                elif dungeon[y][x] == 3:
                    self.canvas.create_rectangle(x * scale_factor, y * scale_factor, x * scale_factor + scale_factor, y * scale_factor + scale_factor, fill="purple")
                #enemy
                elif dungeon[y][x] == 4:
                    self.canvas.create_rectangle(x * scale_factor, y * scale_factor, x * scale_factor + scale_factor, y * scale_factor + scale_factor, fill="red")
                #portal
                elif dungeon[y][x] == 5:
                    self.canvas.create_rectangle(x * scale_factor, y * scale_factor, x * scale_factor + scale_factor, y * scale_factor + scale_factor, fill = "yellow")
                #digbot
                elif (x,y) == (self.digbot.x, self.digbot.y) and self.digbot.digging:
                    self.canvas.create_rectangle(x * scale_factor, y * scale_factor, x * scale_factor + scale_factor, y * scale_factor + scale_factor, fill="grey")
                #npc
                elif dungeon[y][x] == 7:
                    self.canvas.create_rectangle(x * scale_factor, y * scale_factor, x * scale_factor + scale_factor, y * scale_factor + scale_factor, fill="green")

    def update_status(self):
        #create the status string
        status = f"Health: {self.player.health}  Weapon: {self.player.weapon.name}  Damage: {self.player.weapon.damage}"   
        if not self.enemy.dead:
            status += f"\nEnemy health: {self.enemy.health}  Enemy weapon: {self.enemy.weapon.name}  Enemy damage: {self.enemy.weapon.damage}"
        if self.enemy.dead:
            status += "\nEnemy is dead"     
        if self.player.bomb:
            status += "\nPlayer has a bomb"
        if not self.digbot.digging:
            status += "\nDigbot is not digging"
        if self.digbot.digging:
            status += "\nDigbot is digging"
        status += f"\nPoints: {self.player.points} Level: {self.level} Lives: {self.player.lives}"
        status += "\nPress h for help"
        #update the status label
        self.status.config(text=status)

    def pick_up_bomb(self):
        #get the dungeon map
        dungeon = self.dungeon.dungeon
        #delete the bomb from the dungeon
        dungeon[self.bomb.y // scale_factor][self.bomb.x // scale_factor] = 0
        #place the bomb in the player's inventory
        self.player.bomb = self.bomb
        #update the status label
        self.update_status()

    def place_bomb(self):
        #get the dungeon map
        dungeon = self.dungeon.dungeon
        #if the player has a bomb
        if self.player.bomb:
            self.player.bomb.x = self.player.x
            self.player.bomb.y = self.player.y

            #place the bomb in the dungeon
            dungeon[self.player.bomb.y // scale_factor][self.player.bomb.x // scale_factor] = 3
            #remove the bomb from the player's inventory
            self.player.bomb = None
            #update the status label
            self.update_status()
            #schedule the bomb to explode
            self.schedule_bomb()

    def schedule_bomb(self):
        #schedule the bomb to explode
        self.window.after(3000, self.explode_bomb)

    def explode_bomb(self):
        self.player.points += 5
        #get the dungeon map
        dungeon = self.dungeon.dungeon
        #iterate over the cells in the dungeon
        for y in range(50):
            for x in range(50):
                #empty cells in bombs radius
                if (x - self.bomb.x // scale_factor) ** 2 + (y - self.bomb.y // scale_factor) ** 2 <= 8:
                    dungeon[y][x] = 0
        #if player is within 2 cells of the bomb, player takes damage of 50
        if (self.player.x // scale_factor - self.bomb.x // scale_factor) ** 2 + (self.player.y // scale_factor - self.bomb.y // scale_factor) ** 2 <= 4:
            self.player.health -= 50
            if self.player.health <= 0:
                self.player.health = 0
                self.resurrect_player()
        #if enemy is within 2 cells of the bomb, enemy takes damage of 50
        if (self.enemy.x // scale_factor - self.bomb.x // scale_factor) ** 2 + (self.enemy.y // scale_factor - self.bomb.y // scale_factor) ** 2 <= 4:
            self.enemy.health -= 50
            if self.enemy.health <= 0:
                self.enemy.health = 0
                self.enemy.dead = True
                self.player.points += 15*self.enemy.weapon.damage
                #delete the enemy from the dungeon
                self.dungeon.dungeon[self.enemy.y // scale_factor][self.enemy.x // scale_factor] = 0
        #redraw the dungeon
        self.draw_dungeon()
        self.update_status()

    def schedule_digging(self):
        #schedule the digbot to dig
        self.window.after(1000, self.dug)

    def dug(self):
        for x, y in self.dug_cells:
            self.dungeon.dungeon[y][x] = 0
        self.player.points += 1
        self.dug_cells.clear()  # Clear the dug_cells list
        self.digbot.stop_digging()
        self.draw_dungeon()
        self.update_status()

    def conversation_window(self):
        #create a new window
        window = tk.Toplevel(self.window)
        window.title("Conversation")
        window.geometry("300x300")
        #create a label
        label = tk.Label(window, text="Hello, I am "+self.npc.name+". Ask me a question.")
        label.pack()
        #create a frame
        frame = tk.Frame(window)
        frame.pack()
        #create a text input box
        text_input = tk.Entry(frame)
        text_input.pack(side=tk.LEFT)
        text_input.focus()
        answer_text = tk.Text(window, height=12, width=38)
        answer_text.pack()

        #handle the enter key being pressed
        def enter_pressed(event):
            #get the text from the text input box
            text = text_input.get()
            #clear the text input box
            text_input.delete(0, tk.END)
            answer = self.npc.answer(text, self.player)
            #clear the answer text box
            answer_text.delete("1.0", tk.END)
            answer_text.insert(tk.END, answer)
            return
                
        #bind the enter key to the enter_pressed function
        text_input.bind("<Return>", enter_pressed)



    def key_pressed(self, event):
        #if the player has just died, don't do anything
        if self.resurrecting_player:
            return
        #get the dungeon map
        dungeon = self.dungeon.dungeon
        old_x = self.player.x
        old_y = self.player.y
        #move the player in the direction of the key pressed
        if event.keysym == "Up":
            if self.player.y >= scale_factor:
                if dungeon[self.player.y // scale_factor - 1][self.player.x // scale_factor] == 4:
                    self.fight()
                    return
                if dungeon[self.player.y // scale_factor - 1][self.player.x // scale_factor] == 1:
                    if not self.digbot.digging:
                        self.dug_cells.append((self.player.x // scale_factor, self.player.y // scale_factor - 1))
                        self.digbot.x = self.player.x // scale_factor
                        self.digbot.y = self.player.y // scale_factor - 1
                        self.digbot.start_digging()
                        self.schedule_digging()
                if dungeon[self.player.y // scale_factor - 1][self.player.x // scale_factor] == 3:
                    self.pick_up_bomb()
                if dungeon[self.player.y // scale_factor - 1][self.player.x // scale_factor] == 5:
                    if self.enemy.dead:
                        self.go_to_next_level()
                        return
                if dungeon[self.player.y // scale_factor - 1][self.player.x // scale_factor] == 7:
                    self.conversation_window()
                if dungeon[self.player.y // scale_factor - 1][self.player.x // scale_factor] == 0:
                    self.player.y -= scale_factor


        elif event.keysym == "Down":
            if self.player.y <= 48*scale_factor:
                if dungeon[self.player.y // scale_factor + 1][self.player.x // scale_factor] == 4:
                    self.fight()
                    return
                if dungeon[self.player.y // scale_factor + 1][self.player.x // scale_factor] == 1:
                    if not self.digbot.digging:
                        self.dug_cells.append((self.player.x // scale_factor, self.player.y // scale_factor + 1))
                        self.digbot.x = self.player.x // scale_factor
                        self.digbot.y = self.player.y // scale_factor + 1
                        self.digbot.start_digging()
                        self.schedule_digging()
                if dungeon[self.player.y // scale_factor + 1][self.player.x // scale_factor] == 3:
                    self.pick_up_bomb()
                if dungeon[self.player.y // scale_factor + 1][self.player.x // scale_factor] == 5:
                    if self.enemy.dead:
                        self.go_to_next_level()
                        return
                if dungeon[self.player.y // scale_factor + 1][self.player.x // scale_factor] == 7:
                    self.conversation_window()
                if dungeon[self.player.y // scale_factor + 1][self.player.x // scale_factor] == 0:
                    self.player.y += scale_factor
                    
        elif event.keysym == "Left":
            if self.player.x >= scale_factor:
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor - 1] == 4:
                    self.fight()
                    return
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor - 1] == 1:
                    if not self.digbot.digging:
                        self.dug_cells.append((self.player.x // scale_factor - 1, self.player.y // scale_factor))
                        self.digbot.x = self.player.x // scale_factor - 1
                        self.digbot.y = self.player.y // scale_factor
                        self.digbot.start_digging()
                        self.schedule_digging()
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor - 1] == 3:
                    self.pick_up_bomb()
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor - 1] == 5:
                    if self.enemy.dead:
                        self.go_to_next_level()
                        return
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor -1] == 7:
                    self.conversation_window()
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor - 1] == 0:
                    self.player.x -= scale_factor

        elif event.keysym == "Right":
            if self.player.x <= 48*scale_factor:
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor + 1] == 4:
                    self.fight()
                    return
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor + 1] == 1:
                    if not self.digbot.digging:
                        self.dug_cells.append((self.player.x // scale_factor + 1, self.player.y // scale_factor))
                        self.digbot.x = self.player.x // scale_factor + 1
                        self.digbot.y = self.player.y // scale_factor
                        self.digbot.start_digging()
                        self.schedule_digging()
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor + 1] == 3:
                    self.pick_up_bomb()
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor + 1] == 5:
                    if self.enemy.dead:
                        self.go_to_next_level()
                        return
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor + 1] == 7:
                    self.conversation_window()
                if dungeon[self.player.y // scale_factor][self.player.x // scale_factor + 1] == 0:
                    self.player.x += scale_factor

        elif event.keysym == "space":
            if self.player.bomb:
                self.place_bomb()

        elif event.keysym == "h":
            messagebox.showinfo("Help", "Use the arrow keys to move. Use the space bar to place a bomb. Kill the enemy and go through the portal to the next level. You can dig through walls, but it takes time. You can also pick up bombs and use them to kill the enemy and demolish walls. If the enemy is killed by bomb, he's weapon cannot be salvaged like after him dying in combat.")

        #empty the cell the player was in
        dungeon[old_y // scale_factor][old_x // scale_factor] = 0
        #place the player in the new cell
        dungeon[self.player.y // scale_factor][self.player.x // scale_factor] = 2

        #redraw the dungeon and update the status label
        self.update_status()
        self.draw_dungeon()

    def quit(self):
        self.window.destroy()
        sys.exit()

    def resurrect_player(self):
        self.resurrecting_player = True
        dying_place = (self.player.x // scale_factor, self.player.y // scale_factor)
        self.player.lives -= 1
        if self.player.lives == 0:
            self.canvas.delete("all")
            messagebox.showinfo("Game Over", "You have no lives left. Game over.\n" + "Game Points: "+str(self.player.points)+"\n" + "Weapon Bonus: "+str(self.player.weapon.damage*10) + "\nLevel Bonus: "+str(self.level*100)+"\n" + "Total Points: "+str(self.player.points+self.player.weapon.damage*10+self.level*100))
            self.quit()
            return
        self.player.points -= 100
        #lose the bomb
        if self.player.bomb:
            self.player.bomb = None
            #place the bomb where the player died

            self.bomb.x = dying_place[0] * scale_factor
            self.bomb.y = dying_place[1] * scale_factor

        #delete the player from the dungeon
        self.dungeon.dungeon[self.player.y // scale_factor][self.player.x // scale_factor] = 0
        #place the player in a random empty space
        while True:
            x = random.randint(0, 49)
            y = random.randint(0, 49)
            if self.dungeon.dungeon[y][x] == 0:
                break
        self.player.x = x * scale_factor
        self.player.y = y * scale_factor
        self.player.health = 100
        self.player.weapon = Weapon("Fists", 5)
        self.resurrecting_player = False
        return
    
    def fight(self):
        #roll dice to determine who attacks first
        player_roll = random.randint(1, 6)
        enemy_roll = random.randint(1, 6)
        #player attacks
        if player_roll > enemy_roll:
            #player attacks enemy
            self.enemy.health -= self.player.weapon.damage
            #enemy is dead
            if self.enemy.health <= 0:
                self.enemy.health = 0
                self.enemy.dead = True
                self.player.points += 15*self.enemy.weapon.damage
                #delete the enemy from the dungeon
                self.dungeon.dungeon[self.enemy.y // scale_factor][self.enemy.x // scale_factor] = 0
                #open a dialogue box to decide whether to take the enemy's weapon
                if messagebox.askyesno("Enemy is dead", "Do you want to take the enemy's weapon?"):
                    self.player.weapon = self.enemy.weapon
                    self.window.focus_force() 
            self.draw_dungeon()               
            self.update_status()
            return
        #enemy attacks
        else:
            #enemy attacks player
            self.player.health -= self.enemy.weapon.damage
            self.update_status()
            #player is dead
            if self.player.health <= 0:
                self.player.health = 0
                self.resurrect_player()
                self.draw_dungeon()
                self.update_status()
                return
        return

game = Game()
