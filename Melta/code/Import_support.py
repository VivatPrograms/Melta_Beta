from os import walk
from Settings import *

def import_sprite_sheet(path, size_of_one_frame=(64,64), transform=None):
    sheet = pygame.image.load(path).convert_alpha()
    width, height = sheet.get_size()
    w, h = size_of_one_frame
    rows = height//h
    cols = width//w
    frames = []
    for row in range(rows):
        for col in range(cols):
            frame = pygame.Surface(size_of_one_frame, pygame.SRCALPHA)
            crop_rect = pygame.Rect(col * w, row * h, w, h)
            frame.blit(sheet, (0, 0), crop_rect)
            if transform:
                frame = transform(frame)
            frames.append(frame)

    return frames

def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list