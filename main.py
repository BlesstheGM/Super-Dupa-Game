import sys
import pygame
from game_objects.character import Character
from game_objects.data_mananger import DATA_FILE, get_character_data, initialize_data_file, update_character_coins, update_character_level
from levels.level import Level
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE
import os


def get_rankings():
    """
    Fetch and sort player rankings by custom logic:
    - Sort by coins if there are no deaths.
    - Sort by coins/deaths ratio if there are deaths.
    Returns a list of tuples [(name, level, coins, deaths)].
    """
    initialize_data_file()
    rankings = []
    file_path = os.path.join("data", "characters.txt")  # Relative path to the characters.txt
    with open(file_path, "r") as file:
        for line in file:
            name, level, coins, deaths = line.strip().split(":")
            coins = int(coins)
            level = int(level)
            deaths = int(deaths)
            # Calculate coins/deaths ratio or default to coins if deaths = 0
            score = coins if deaths == 0 else coins / deaths
            rankings.append((name, level, coins, deaths, score))
    
    # Sort by score (highest first), and then by coins if scores are equal
    rankings.sort(key=lambda x: (-x[4], -x[2]))
    return rankings

def avatar_image():
    """Return the default avatar image."""
    avatar_path = os.path.join("assets", "avatar.png")  # Relative path to the avatar image
    return pygame.image.load(avatar_path)

def get_player_name(screen):
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50)
    color_active = pygame.Color('dodgerblue')
    active = True
    name = ""

    clock = pygame.time.Clock()
    rankings = get_rankings()  # Fetch rankings with new sorting logic
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return name
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

        screen.fill((135, 206, 250))  # Background color

        # Prompt text
        prompt_text = font.render("Enter your name", True, (0, 0, 0))
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # Input box
        txt_surface = font.render(name, True, (0, 0, 0))
        width = max(300, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color_active, input_box, 2)

        # Display rankings below the input box
        rankings_text = small_font.render("Click Enter to start", True, (0, 0, 0))
        screen.blit(rankings_text, (SCREEN_WIDTH // 2 - rankings_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        # Load the default avatar
        default_avatar = avatar_image()
        default_avatar = pygame.transform.scale(default_avatar, (50, 50))  # Resize avatar to fit in the box

        # Render top 2 rankings with the default avatar
        for i, (rank_name, level, coins, deaths, _) in enumerate(rankings[:2]):
            ranking_line = f"{rank_name}: {coins} Coins, Level {level}, {deaths} Deaths"
            ranking_rect = pygame.Rect(50, SCREEN_HEIGHT // 2 + 100 + i * 80, SCREEN_WIDTH - 100, 70)
            
            # Draw the rectangular box for the rank
            pygame.draw.rect(screen, (255, 255, 255), ranking_rect)
            pygame.draw.rect(screen, (0, 0, 0), ranking_rect, 3)  # Border for the rectangle
            
            # Draw the default avatar on the left side
            screen.blit(default_avatar, (ranking_rect.x + 10, ranking_rect.y + 10))  # Draw default avatar
            # Render the text to the right of the avatar
            rank_text = small_font.render(ranking_line, True, (0, 0, 0))
            screen.blit(rank_text, (ranking_rect.x + 70, ranking_rect.y + 25))  # Adjust text position to the right

        pygame.display.flip()
        clock.tick(FPS)


def main(name=None):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Super Dupa Game")
    clock = pygame.time.Clock()
    
    # Set icon using relative path
    icon_path = os.path.join("assets", "logo.jpg")  # Relative path to logo
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)

    if not name:
        # Ask name and have an option to start the game
        name = get_player_name(screen)
        # search my name on txt file , find my name continue with the level
    level_number, coin_count, death_count = get_character_data(name)
    update_character_level(name, level_number)
    update_character_coins(name, coin_count)

    character = Character(100, 600, name, level_number, coin_count)
    # Initialize level
    level = Level(screen, character)

    running = True
    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update and render the level
        level.update(keys)
        level.render()
        character.render_paused(screen)

        # Draw the score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Coins: {character.coin_count}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw the name    
        name_text = font.render(f"Name: {character.name}", True, WHITE)
        screen.blit(name_text, ((SCREEN_WIDTH) - name_text.get_width() - 10, 10))

        # Draw the level
        level_text = font.render(f"Level : {character.level}", True, WHITE)
        screen.blit(level_text, ((SCREEN_WIDTH // 2) - level_text.get_width() - 10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
