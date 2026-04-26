import pygame
import json
import os
from datetime import datetime

SCREEN_W = 400
SCREEN_H = 600

DATA_DIR = "data"
LB_FILE  = os.path.join(DATA_DIR, "leaderboard.json")
ST_FILE  = os.path.join(DATA_DIR, "settings.json")



class Settings:
    DEFAULTS = {"music_vol": 0.2, "sfx_vol": 0.8, "difficulty": "normal"}

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.data = dict(self.DEFAULTS)
        self._load()

    def _load(self):
        try:
            with open(ST_FILE) as f:
                self.data.update(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save(self):
        with open(ST_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def __getattr__(self, key):
        if key in ("data",):
            raise AttributeError(key)
        return self.data.get(key)

    def set(self, key, val):
        self.data[key] = val
        self.save()


class Leaderboard:
    MAX = 10

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.entries = []
        self._load()

    def _load(self):
        try:
            with open(LB_FILE) as f:
                self.entries = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.entries = []

    def add(self, name: str, score: int, coins: int, level: int):
        entry = {
            "name":  name[:12],
            "score": score,
            "coins": coins,
            "level": level,
            "date":  datetime.now().strftime("%Y-%m-%d"),
        }
        self.entries.append(entry)
        self.entries.sort(key=lambda e: e["score"], reverse=True)
        self.entries = self.entries[: self.MAX]
        with open(LB_FILE, "w") as f:
            json.dump(self.entries, f, indent=2)

    def is_high_score(self, score: int) -> bool:
        if len(self.entries) < self.MAX:
            return True
        return score > self.entries[-1]["score"]



def load_fonts():
    """Return (arcade_big, arcade_med, arcade_sm, mono_sm)."""
    ttf = os.path.join("assets", "ARCADECLASSIC.TTF")
    try:
        big  = pygame.font.Font(ttf, 64)
        med  = pygame.font.Font(ttf, 36)
        sm   = pygame.font.Font(ttf, 22)
    except FileNotFoundError:
        big  = pygame.font.SysFont("consolas", 64, bold=True)
        med  = pygame.font.SysFont("consolas", 36, bold=True)
        sm   = pygame.font.SysFont("consolas", 22, bold=True)
    mono = pygame.font.SysFont("consolas", 18, bold=True)
    return big, med, sm, mono



BG_DARK  = (18,  18,  28)
BG_MED   = (28,  28,  45)
GOLD     = (255, 215,   0)
CYAN     = (80,  220, 255)
RED      = (220,  50,  40)
GREEN    = (60,  220,  80)
WHITE    = (255, 255, 255)
GREY     = (140, 140, 160)
PURPLE   = (120,  40, 180)


def _panel(surface, rect, alpha=200):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    s.fill((0, 0, 0, alpha))
    surface.blit(s, (rect.x, rect.y))
    pygame.draw.rect(surface, GREY, rect, 1, border_radius=6)



class HUD:
    def __init__(self, fonts):
        _, _, self.sm, self.mono = fonts
        self._combo_alpha = 0

    def draw(self, surface, score, coins, level, speed, player):
        # top bar background
        _panel(surface, pygame.Rect(0, 0, SCREEN_W, 46))

        # score
        sc_txt = self.mono.render(f"SCORE {score:04d}", True, WHITE)
        surface.blit(sc_txt, (8, 6))

        # coin counter
        coin_txt = self.mono.render(f"COINS {coins:03d}", True, GOLD)
        surface.blit(coin_txt, (SCREEN_W - coin_txt.get_width() - 8, 6))

        # level badge
        lv_txt = self.mono.render(f"LV{level}", True, CYAN)
        surface.blit(lv_txt, (SCREEN_W // 2 - lv_txt.get_width() // 2, 6))

        # speed bar (bottom-right corner)
        bar_x, bar_y, bar_w, bar_h = SCREEN_W - 14, SCREEN_H - 120, 10, 100
        _panel(surface, pygame.Rect(bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4), alpha=160)
        fill = min(int((speed - 4) / 12 * bar_h), bar_h)
        color = GREEN if speed < 10 else (GOLD if speed < 14 else RED)
        pygame.draw.rect(surface, color,
                         pygame.Rect(bar_x, bar_y + bar_h - fill, bar_w, fill))
        spd_l = self.mono.render("SPD", True, GREY)
        spd_s = pygame.transform.rotate(spd_l, 90)
        surface.blit(spd_s, (bar_x - 4, bar_y + bar_h + 4))

        # boost indicator
        if player.boost_ticks > 0:
            b_txt = self.mono.render("  BOOST!", True, GREEN)
            surface.blit(b_txt, (8, SCREEN_H - 28))




class MenuScreen:
    def __init__(self, fonts):
        self.big, self.med, self.sm, self.mono = fonts
        self._t = 0

    def draw(self, surface):
        self._t += 1
        surface.fill(BG_DARK)

        # animated road stripes (cosmetic)
        scroll = (self._t * 4) % 80
        for y in range(-80, SCREEN_H + 80, 80):
            pygame.draw.rect(surface, (50, 52, 55), pygame.Rect(80, y + scroll, 240, 60))
            pygame.draw.rect(surface, (70, 72, 75), pygame.Rect(188, y + scroll, 8, 30))

        # title
        title = self.big.render("RACER", True, RED)
        pulse = abs((self._t % 60) - 30) / 30
        title.set_alpha(int(180 + 75 * pulse))
        surface.blit(title, title.get_rect(center=(SCREEN_W // 2, 160)))

        sub = self.sm.render("ARCADE EDITION", True, GOLD)
        surface.blit(sub, sub.get_rect(center=(SCREEN_W // 2, 220)))

        # menu items
        items = [
            ("ENTER  — PLAY",     WHITE),
            ("L  — LEADERBOARD",  GREY),
            ("S  — SETTINGS",     GREY),
            ("ESC  — QUIT",       GREY),
        ]
        for i, (text, col) in enumerate(items):
            t = self.mono.render(text, True, col)
            surface.blit(t, t.get_rect(center=(SCREEN_W // 2, 320 + i * 36)))

        # footer
        ft = self.mono.render("DODGE  •  COLLECT  •  SURVIVE", True, (60, 60, 90))
        surface.blit(ft, ft.get_rect(center=(SCREEN_W // 2, SCREEN_H - 24)))

    def handle(self, event) -> str:
        """Returns scene name or '' ."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: return "GAME"
            if event.key == pygame.K_l:      return "LEADERBOARD"
            if event.key == pygame.K_s:      return "SETTINGS"
            if event.key == pygame.K_ESCAPE: return "QUIT"
        return ""



class PauseOverlay:
    def __init__(self, fonts):
        _, self.med, self.sm, self.mono = fonts

    def draw(self, surface):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))
        t = self.med.render("PAUSED", True, GOLD)
        surface.blit(t, t.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 40)))
        r = self.mono.render("ENTER to resume  •  ESC to quit", True, WHITE)
        surface.blit(r, r.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 20)))



class GameOverScreen:
    MAX_NAME = 10

    def __init__(self, fonts, leaderboard: Leaderboard):
        self.big, self.med, self.sm, self.mono = fonts
        self.lb     = leaderboard
        self.name   = ""
        self.saved  = False
        self._t     = 0

    def reset(self, score, coins, level):
        self.score  = score
        self.coins  = coins
        self.level  = level
        self.name   = ""
        self.saved  = False
        self._t     = 0
        self.is_hs  = self.lb.is_high_score(score)

    def draw(self, surface):
        self._t += 1
        _panel(surface, pygame.Rect(40, 120, SCREEN_W - 80, SCREEN_H - 200), alpha=230)

        title = self.big.render("GAME OVER", True, RED)
        surface.blit(title, title.get_rect(center=(SCREEN_W // 2, 160)))

        # stats
        lines = [
            (f"SCORE   {self.score:04d}", WHITE),
            (f"COINS   {self.coins:03d}",  GOLD),
            (f"LEVEL   {self.level}",       CYAN),
        ]
        for i, (txt, col) in enumerate(lines):
            s = self.mono.render(txt, True, col)
            surface.blit(s, s.get_rect(center=(SCREEN_W // 2, 250 + i * 30)))

        if self.is_hs and not self.saved:
            hs = self.sm.render("HIGH SCORE!", True, GOLD)
            surface.blit(hs, hs.get_rect(center=(SCREEN_W // 2, 360)))

            prompt = self.mono.render("ENTER YOUR NAME:", True, GREY)
            surface.blit(prompt, prompt.get_rect(center=(SCREEN_W // 2, 390)))

            cursor = "|" if (self._t // 20) % 2 == 0 else " "
            name_surf = self.med.render(self.name + cursor, True, WHITE)
            surface.blit(name_surf, name_surf.get_rect(center=(SCREEN_W // 2, 418)))

            hint = self.mono.render("ENTER to save  •  BACKSPACE to delete", True, (80,80,100))
            surface.blit(hint, hint.get_rect(center=(SCREEN_W // 2, 460)))
        else:
            msg  = "SAVED!" if self.saved else ""
            s    = self.mono.render(msg, True, GREEN)
            surface.blit(s, s.get_rect(center=(SCREEN_W // 2, 380)))
            cont = self.mono.render("ENTER  — PLAY AGAIN   ESC  — MENU", True, GREY)
            surface.blit(cont, cont.get_rect(center=(SCREEN_W // 2, 430)))

    def handle(self, event) -> str:
        if event.type != pygame.KEYDOWN:
            return ""
        if self.is_hs and not self.saved:
            if event.key == pygame.K_RETURN:
                n = self.name.strip() or "AAA"
                self.lb.add(n, self.score, self.coins, self.level)
                self.saved = True
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            else:
                ch = event.unicode
                if ch and ch.isprintable() and len(self.name) < self.MAX_NAME:
                    self.name += ch.upper()
        else:
            if event.key == pygame.K_RETURN: return "GAME"
            if event.key == pygame.K_ESCAPE: return "MENU"
        return ""



class LeaderboardScreen:
    def __init__(self, fonts, leaderboard: Leaderboard):
        _, self.med, self.sm, self.mono = fonts
        self.lb = leaderboard

    def draw(self, surface):
        surface.fill(BG_DARK)
        title = self.med.render("LEADERBOARD", True, GOLD)
        surface.blit(title, title.get_rect(center=(SCREEN_W // 2, 50)))
        pygame.draw.line(surface, GREY, (40, 82), (SCREEN_W - 40, 82), 1)

        headers = ["#", "NAME",     "SCORE", "COINS", "LV", "DATE"]
        col_x   = [14,   50,        170,      255,     315,   345]
        h_col   = CYAN
        for i, (h, x) in enumerate(zip(headers, col_x)):
            t = self.mono.render(h, True, h_col)
            surface.blit(t, (x, 90))

        pygame.draw.line(surface, (50,50,70), (14, 108), (SCREEN_W - 14, 108), 1)

        for rank, entry in enumerate(self.lb.entries):
            y   = 114 + rank * 38
            row_col = GOLD if rank == 0 else (GREY if rank > 2 else WHITE)
            vals = [
                f"{rank+1}",
                entry.get("name", "???")[:10],
                str(entry.get("score", 0)),
                str(entry.get("coins", 0)),
                str(entry.get("level", 1)),
                entry.get("date", "")[-5:],   # MM-DD
            ]
            for val, x in zip(vals, col_x):
                t = self.mono.render(val, True, row_col)
                surface.blit(t, (x, y))
            if rank % 2 == 0:
                bar = pygame.Surface((SCREEN_W - 28, 36), pygame.SRCALPHA)
                bar.fill((255, 255, 255, 8))
                surface.blit(bar, (14, y - 2))

        if not self.lb.entries:
            empty = self.mono.render("No records yet. Start racing!", True, GREY)
            surface.blit(empty, empty.get_rect(center=(SCREEN_W // 2, 300)))

        back = self.mono.render("ESC / ENTER  — back", True, GREY)
        surface.blit(back, back.get_rect(center=(SCREEN_W // 2, SCREEN_H - 24)))

    def handle(self, event) -> str:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return "MENU"
        return ""



class SettingsScreen:
    DIFFICULTIES = ["easy", "normal", "hard"]

    def __init__(self, fonts, settings: Settings):
        _, self.med, self.sm, self.mono = fonts
        self.st      = settings
        self.focus   = 0     # which row is focused
        self.ROWS    = 3     # music, sfx, difficulty

    def draw(self, surface):
        surface.fill(BG_DARK)
        title = self.med.render("SETTINGS", True, CYAN)
        surface.blit(title, title.get_rect(center=(SCREEN_W // 2, 60)))
        pygame.draw.line(surface, GREY, (40, 92), (SCREEN_W - 40, 92), 1)

        rows = [
            ("MUSIC VOL",   self._vol_bar(self.st.data["music_vol"])),
            ("SFX VOL",     self._vol_bar(self.st.data["sfx_vol"])),
            ("DIFFICULTY",  self.st.data["difficulty"].upper()),
        ]

        for i, (label, value) in enumerate(rows):
            y       = 130 + i * 80
            focused = (i == self.focus)
            bg_col  = (30, 40, 60) if focused else (18, 18, 28)
            pygame.draw.rect(surface, bg_col, pygame.Rect(40, y - 8, SCREEN_W - 80, 56), border_radius=6)
            if focused:
                pygame.draw.rect(surface, CYAN, pygame.Rect(40, y - 8, SCREEN_W - 80, 56), 1, border_radius=6)
            lbl  = self.mono.render(label, True, GOLD if focused else GREY)
            val  = self.mono.render(str(value), True, WHITE)
            surface.blit(lbl, (56, y))
            surface.blit(val, (56, y + 24))

        controls = [
            "↑ ↓  — select row",
            "← →  — change value",
            "ESC / ENTER  — back",
        ]
        for i, line in enumerate(controls):
            t = self.mono.render(line, True, (60, 60, 90))
            surface.blit(t, t.get_rect(center=(SCREEN_W // 2, SCREEN_H - 80 + i * 22)))

    def _vol_bar(self, vol: float) -> str:
        filled = int(vol * 10)
        return "|" * filled + "[]" * (10 - filled) + f" {int(vol*100)}%"

    def handle(self, event) -> str:
        if event.type != pygame.KEYDOWN:
            return ""
        if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
            self.st.save()
            return "MENU"
        if event.key == pygame.K_UP:
            self.focus = (self.focus - 1) % self.ROWS
        if event.key == pygame.K_DOWN:
            self.focus = (self.focus + 1) % self.ROWS

        if event.key == pygame.K_LEFT:
            self._adjust(-1)
        if event.key == pygame.K_RIGHT:
            self._adjust(+1)

        return ""

    def _adjust(self, direction: int):
        if self.focus == 0:
            v = round(min(1.0, max(0.0, self.st.data["music_vol"] + direction * 0.1)), 1)
            self.st.set("music_vol", v)
            try:
                pygame.mixer.music.set_volume(v)
            except Exception:
                pass
        elif self.focus == 1:
            v = round(min(1.0, max(0.0, self.st.data["sfx_vol"] + direction * 0.1)), 1)
            self.st.set("sfx_vol", v)
        elif self.focus == 2:
            idx = self.DIFFICULTIES.index(self.st.data["difficulty"])
            idx = (idx + direction) % len(self.DIFFICULTIES)
            self.st.set("difficulty", self.DIFFICULTIES[idx])