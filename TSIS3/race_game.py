import pygame
import sys
import os
import random
import time

from pygame.locals import *

from entities import (
    Player, Enemy, Coin, SpeedBoost, Cone, Checkpoint, LANES
)
from track import Road, TrackEventManager, NotificationBanner
from ui    import (
    Settings, Leaderboard,
    load_fonts, HUD,
    MenuScreen, PauseOverlay, GameOverScreen,
    LeaderboardScreen, SettingsScreen,
)


FPS      = 60
SCREEN_W = 400
SCREEN_H = 600

DIFF_SPEED = {"easy": 4.0, "normal": 5.0, "hard": 7.0}
DIFF_INC   = {"easy": 0.3, "normal": 0.5, "hard": 0.8}  # per level-up

CHECKPOINT_EVERY = 5    # score points between checkpoints
LEVEL_EVERY      = 10   # score points per level
MAX_ENEMIES      = 4



def load_sound(path: str) -> pygame.mixer.Sound | None:
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


class Sounds:
    def __init__(self, settings: Settings):
        self.st    = settings
        a          = os.path.join("assets")
        self.coin  = load_sound(os.path.join(a, "coin_received.wav"))
        self.crash = load_sound(os.path.join(a, "crash.wav"))
        self._set_sfx_vol()
        # music
        try:
            pygame.mixer.music.load(os.path.join(a, "background.wav"))
            pygame.mixer.music.set_volume(settings.data["music_vol"])
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def _set_sfx_vol(self):
        v = self.st.data["sfx_vol"]
        if self.coin:  self.coin.set_volume(v)
        if self.crash: self.crash.set_volume(v)

    def play_coin(self):
        if self.coin: self.coin.play()

    def play_crash(self):
        if self.crash: self.crash.play()

    def apply_settings(self):
        pygame.mixer.music.set_volume(self.st.data["music_vol"])
        self._set_sfx_vol()



class GameState:
    """Everything that needs to reset between runs."""

    def __init__(self, settings: Settings):
        diff        = settings.data.get("difficulty", "normal")
        self.speed  = [DIFF_SPEED[diff]]     # mutable 1-element list shared with sprites
        self.base_inc = DIFF_INC[diff]
        self.score  = 0
        self.coins  = 0
        self.level  = 1

        # sprites
        self.player      = Player()
        self.enemies     = pygame.sprite.Group()
        self.coins_grp   = pygame.sprite.Group()
        self.hazards     = pygame.sprite.Group()   # Cone, SpeedBoost
        self.checkpoints = pygame.sprite.Group()

        e = Enemy(self.speed)
        self.enemies.add(e)

        for _ in range(3):
            c = Coin(self.speed)
            self.coins_grp.add(c)

        # track systems
        self.road        = Road()
        self.events      = TrackEventManager()
        self._cp_score   = CHECKPOINT_EVERY   # next checkpoint trigger score
        self._next_level = LEVEL_EVERY

        # rush-hour timer
        self._rush_timer = 0


    def update(self, pressed) -> list:
        """
        Advance one frame.
        Returns list of string signals: 'CRASH', 'COIN', event names.
        """
        signals = []
        spd     = self.speed[0]

        self.road.update(spd)
        self.player.move(pressed)

        # move enemies
        for e in list(self.enemies):
            scored = e.move(None)
            if scored:
                self.score += 1
                signals.append("SCORE")

        # move coins
        for c in self.coins_grp:
            c.move()

        # move hazards
        for h in self.hazards:
            h.move()

        # move checkpoints
        for cp in self.checkpoints:
            cp.move()
            if cp.check_cross(self.player.rect):
                self.coins  += 5
                signals.append("CHECKPOINT_CROSS")


        if not self.player.is_invincible:
            # enemy
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                signals.append("CRASH")
                return signals

            # cone
            hit_cone = pygame.sprite.spritecollideany(
                self.player,
                pygame.sprite.Group(h for h in self.hazards if isinstance(h, Cone))
            )
            if hit_cone:
                signals.append("CRASH")
                return signals

        # speed boost
        hit_boost = pygame.sprite.spritecollideany(
            self.player,
            pygame.sprite.Group(h for h in self.hazards if isinstance(h, SpeedBoost))
        )
        if hit_boost and self.player.boost_ticks == 0:
            self.player.apply_boost(120)
            hit_boost._spawn()

        # coin collection
        collected = pygame.sprite.spritecollideany(self.player, self.coins_grp)
        if collected:
            self.coins += collected.weight
            collected.reset()
            signals.append("COIN")

        # coin/enemy collision — reset coin
        for coin in self.coins_grp:
            if pygame.sprite.spritecollideany(coin, self.enemies):
                coin.reset()


        events = self.events.update(self.score)
        signals.extend(events)

        # checkpoint gate spawn
        if self.score >= self._cp_score:
            cp = Checkpoint(self.speed, self._cp_score)
            cp.activate()
            self.checkpoints.add(cp)
            self._cp_score += CHECKPOINT_EVERY

        # level-up
        if self.score >= self._next_level:
            self._next_level += LEVEL_EVERY
            self.level += 1
            self.speed[0] = min(self.speed[0] + self.base_inc, 18.0)
            # add an enemy (up to max)
            if len(self.enemies) < MAX_ENEMIES:
                self.enemies.add(Enemy(self.speed))

        # rush hour timer
        if self._rush_timer > 0:
            self._rush_timer -= 1

        return signals

    def handle_event(self, event_name: str):
        """Respond to named track events."""
        if event_name == "RUSH_HOUR":
            if len(self.enemies) < MAX_ENEMIES:
                self.enemies.add(Enemy(self.speed))
            self._rush_timer = 600  # 10 sec

        elif event_name == "NIGHT_MODE":
            self.road.night_alpha = 160

        elif event_name == "LEVEL_UP":
            # ensure cones appear from level 2
            if self.level >= 2 and len([h for h in self.hazards if isinstance(h, Cone)]) < 3:
                self.hazards.add(Cone(self.speed))

        elif event_name == "CHECKPOINT":
            # banner only; gate is spawned by score threshold in update()
            pass

    def draw(self, surface):
        self.road.draw(surface)
        for cp in self.checkpoints:
            if cp.active:
                surface.blit(cp.image, cp.rect)
        for h in self.hazards:
            surface.blit(h.image, h.rect)
        for c in self.coins_grp:
            surface.blit(c.image, c.rect)
        for e in self.enemies:
            surface.blit(e.image, e.rect)
        surface.blit(self.player.image, self.player.rect)



def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("RACER: Arcade Edition")
    clock  = pygame.time.Clock()

    settings    = Settings()
    leaderboard = Leaderboard()
    sounds      = Sounds(settings)
    fonts       = load_fonts()
    big, med, sm, mono = fonts

    # screens
    menu_scr  = MenuScreen(fonts)
    pause_scr = PauseOverlay(fonts)
    go_scr    = GameOverScreen(fonts, leaderboard)
    lb_scr    = LeaderboardScreen(fonts, leaderboard)
    st_scr    = SettingsScreen(fonts, settings)
    hud       = HUD(fonts)
    banner    = NotificationBanner(sm)

    scene     = "MENU"
    game      : GameState | None = None

    def start_game():
        nonlocal game
        sounds.apply_settings()
        try:
            pygame.mixer.music.play(-1)
        except Exception:
            pass
        game = GameState(settings)


    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        if scene == "MENU":
            for event in events:
                result = menu_scr.handle(event)
                if result == "GAME":
                    start_game()
                    scene = "GAME"
                elif result == "LEADERBOARD":
                    scene = "LEADERBOARD"
                elif result == "SETTINGS":
                    scene = "SETTINGS"
                elif result == "QUIT":
                    pygame.quit()
                    sys.exit()
            menu_scr.draw(screen)

        elif scene == "GAME":
            pressed = pygame.key.get_pressed()

            # pause toggle
            for event in events:
                if event.type == KEYDOWN and event.key == pygame.K_p:
                    scene = "PAUSE"

            # update
            signals = game.update(pressed)

            for sig in signals:
                if sig == "CRASH":
                    sounds.play_crash()
                    try:
                        pygame.mixer.music.stop()
                    except Exception:
                        pass
                    go_scr.reset(game.score, game.coins, game.level)
                    scene = "GAMEOVER"
                    break

                elif sig == "COIN":
                    sounds.play_coin()

                elif sig == "CHECKPOINT_CROSS":
                    sounds.play_coin()
                    banner.trigger("CHECKPOINT")

                elif sig in ("CHECKPOINT","LEVEL_UP","NIGHT_MODE","RUSH_HOUR","NARROW"):
                    game.handle_event(sig)
                    banner.trigger(sig)

            banner.update()

            # draw
            game.draw(screen)
            hud.draw(screen, game.score, game.coins, game.level,
                     game.speed[0], game.player)
            banner.draw(screen)

            # pause hint
            hint = mono.render("P — PAUSE", True, (50, 50, 70))
            screen.blit(hint, (SCREEN_W - hint.get_width() - 6, SCREEN_H - 22))

        elif scene == "PAUSE":
            for event in events:
                if event.type == KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_RETURN:
                        scene = "GAME"
                    elif event.key == pygame.K_ESCAPE:
                        scene = "MENU"
            game.draw(screen)
            hud.draw(screen, game.score, game.coins, game.level,
                     game.speed[0], game.player)
            pause_scr.draw(screen)


        elif scene == "GAMEOVER":
            for event in events:
                result = go_scr.handle(event)
                if result == "GAME":
                    start_game()
                    scene = "GAME"
                elif result == "MENU":
                    try:
                        pygame.mixer.music.play(-1)
                    except Exception:
                        pass
                    scene = "MENU"
            # dark background
            screen.fill((30, 5, 40))
            # draw last frame of game faintly
            go_scr.draw(screen)

        elif scene == "LEADERBOARD":
            for event in events:
                result = lb_scr.handle(event)
                if result == "MENU":
                    scene = "MENU"
            lb_scr.draw(screen)

        elif scene == "SETTINGS":
            for event in events:
                result = st_scr.handle(event)
                if result == "MENU":
                    sounds.apply_settings()
                    scene = "MENU"
            st_scr.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()