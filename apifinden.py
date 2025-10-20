import pygame, sys, random, lyricsgenius


API_TOKEN = "wRZuPZcOecCnZhkZHNO8HBXEybpbv3J8wPiutBPm2G_bGMBtFcSgKFkDucHv32qA"

genius = lyricsgenius.Genius(API_TOKEN,
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True)

def get_lyrics(artist, title):
    song = genius.search_song(title, artist)
    if song:
        return song.lyrics.split("\n")
    return None

# ---------------------------------------
#  Pygame Setup
# ---------------------------------------
pygame.init()
WIDTH, HEIGHT = 800, 450
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Finish the Lyrics - Genius API")
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

# ---------------------------------------
#  Songs
# ---------------------------------------
songs = [
    ("Ed Sheeran", "Shape of You"),
    ("Adele", "Hello"),
    ("The Weeknd", "Blinding Lights"),
    ("Eminem", "Lose Yourself"),
    ("Queen", "Bohemian Rhapsody")
]

random.shuffle(songs)
lyrics = None
for artist, title in songs:
    lyrics = get_lyrics(artist, title)
    if lyrics:
        print(f"Lade: {artist} – {title}")
        break

if not lyrics:
    print("Keine Lyrics gefunden.")
    pygame.quit()
    sys.exit()

# ---------------------------------------
#  Spiel-Logik
# ---------------------------------------
idx = random.randint(1, len(lyrics) - 2)
shown = [lyrics[idx - 1], "_____", lyrics[idx + 1]]
correct = lyrics[idx].lower()
user_input = ""
result = ""

# ---------------------------------------
#  Game Loop
# ---------------------------------------
running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                if user_input.strip().lower() in correct:
                    result = "✅ Richtig!"
                else:
                    result = f"❌ Falsch! Richtige Zeile:\n{lyrics[idx]}"
            elif e.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += e.unicode

    win.fill((25, 25, 35))
    y = 100
    for line in shown:
        win.blit(font.render(line, True, (255, 255, 255)), (50, y))
        y += 50

    win.blit(font.render("Deine Antwort: " + user_input, True, (255, 220, 50)), (50, 300))
    for i, part in enumerate(result.split("\n")):
        win.blit(font.render(part, True, (0, 255, 0)), (50, 340 + i*30))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()  