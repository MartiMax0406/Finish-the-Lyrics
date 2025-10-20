import pygame, sys, random, lyricsgenius


API_TOKEN = "wRZuPZcOecCnZhkZHNO8HBXEybpbv3J8wPiutBPm2G_bGMBtFcSgKFkDucHv32qA"
genius = lyricsgenius.Genius(API_TOKEN)
genius.timeout = 15
genius.retries = 3

def get_lyrics(artist, title):
    try:
        song = genius.search_song(title, artist)
        if song and song.lyrics:
            lines = [l.strip() for l in song.lyrics.split("\n") if l.strip()]
            # Entfernt Zeilen wie [Verse 1]
            lines = [l for l in lines if not l.startswith("[")]
            return lines
    except:
        pass
    return None


# -----------------------------
# PYGAME SETUP
# -----------------------------
pygame.init()
WIDTH, HEIGHT = 900, 560
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Finish the Lyrics")

# Schriftarten und Farben
font = pygame.font.SysFont("segoeui", 32)
small = pygame.font.SysFont("segoeui", 24)
big = pygame.font.SysFont("segoeui", 42, bold=True)

BG = (20, 20, 30)
CARD = (35, 35, 50)
TEXT = (240, 240, 255)
ACCENT = (120, 180, 255)
CORRECT = (80, 255, 120)
WRONG = (255, 90, 90)
BUTTON = (70, 100, 180)
BUTTON_HOVER = (100, 140, 220)

# -----------------------------
# SONGS
# -----------------------------
songs = [
    ("Ed Sheeran", "Shape of You"),
    ("Adele", "Hello"),
    ("The Weeknd", "Blinding Lights"),
    ("Eminem", "Lose Yourself"),
    ("Queen", "Bohemian Rhapsody")
]

# -----------------------------
# FUNKTION: Neuen Song laden
# -----------------------------
def new_song():
    random.shuffle(songs)
    for a, t in songs:
        lyr = get_lyrics(a, t)
        if lyr:
            i = random.randint(1, len(lyr) - 2)
            shown = [lyr[i-1], "_____", lyr[i+1]]
            return a, t, lyr, i, shown
    return None, None, None, None, None

# -----------------------------
# START
# -----------------------------
artist, title, lyrics, idx, shown = new_song()
user_text = ""
result = ""
color_result = TEXT
button = pygame.Rect(WIDTH - 180, HEIGHT - 70, 150, 45)
clock = pygame.time.Clock()

# -----------------------------
# GAME LOOP
# -----------------------------
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # Eingabe-Tasten
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                if user_text.strip().lower() in lyrics[idx].lower():
                    result, color_result = "Richtig!", CORRECT
                else:
                    result, color_result = f"Falsch!\nRichtig war:\n{lyrics[idx]}", WRONG
            elif e.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += e.unicode

        # Button-Klick
        elif e.type == pygame.MOUSEBUTTONDOWN and button.collidepoint(e.pos):
            artist, title, lyrics, idx, shown = new_song()
            user_text = ""
            result = ""
            color_result = TEXT

    # -----------------------------
    # ZEICHNEN
    # -----------------------------
    win.fill(BG)
    # Titel
    title_text = big.render("Finish the Lyrics", True, ACCENT)
    win.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 40))
    song_text = small.render(f"{artist} – {title}", True, (180, 180, 200))
    win.blit(song_text, (WIDTH//2 - song_text.get_width()//2, 90))

    # Lyrics-Kasten
    pygame.draw.rect(win, CARD, (100, 150, WIDTH-200, 160), border_radius=15)
    y = 180
    for line in shown:
        line_surface = font.render(line, True, TEXT)
        win.blit(line_surface, (WIDTH//2 - line_surface.get_width()//2, y))
        y += 45

    # Eingabezeile
    pygame.draw.rect(win, CARD, (100, 340, WIDTH-200, 50), border_radius=10)
    input_surface = small.render(user_text or "Tippe deine Antwort...", True, ACCENT)
    win.blit(input_surface, (WIDTH//2 - input_surface.get_width()//2, 352))

    # Ergebnisanzeige
    if result:
        y = 415
        for line in result.split("\n"):
            r_text = small.render(line, True, color_result)
            win.blit(r_text, (WIDTH//2 - r_text.get_width()//2, y))
            y += 28

    # Button rechts unten
    hover = button.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(win, BUTTON_HOVER if hover else BUTTON, button, border_radius=10)
    label = small.render("Neuer Song", True, TEXT)
    win.blit(label, (button.centerx - label.get_width()//2, button.centery - label.get_height()//2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
