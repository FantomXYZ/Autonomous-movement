import pygame
import os

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
BG_COLOR = (0, 255, 0)
DRAW_COLOR = (255, 255, 255)
DRAW_SIZE = 45

SAVE_FOLDER = "traces"  # Имя папки для сохранения изображений

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Paint")

    drawing = False
    screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen,(255,0,0),(100,500,20,20))

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    pos = pygame.mouse.get_pos()
                    pygame.draw.circle(screen, DRAW_COLOR, pos, DRAW_SIZE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    save_image(screen)

        window.blit(screen, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def save_image(surface):
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
    image_count = len(os.listdir(SAVE_FOLDER))
    image_path = os.path.join(SAVE_FOLDER, f"trace_{image_count}.png")
    pygame.image.save(surface, image_path)
    print(f"Изображение сохранено: {image_path}")

if __name__ == "__main__":
    main()