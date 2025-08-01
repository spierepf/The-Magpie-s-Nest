# visualizer.py
import pygame
import math
from typing import List, Tuple, Optional, Sequence, Any

from models import WLED_EFFECTS

WIDTH: int = 1200
HEIGHT: int = 800
BG_COLOR: Tuple[int, int, int] = (30, 30, 30)
FRONT_COLOR: Tuple[int, int, int] = (70, 130, 180)
BACK_COLOR: Tuple[int, int, int] = (180, 130, 70)
PORT_COLOR_ON: Tuple[int, int, int] = (255, 255, 100)
PORT_COLOR_OFF: Tuple[int, int, int] = (80, 80, 80)
PORT_RADIUS: int = 14  # Reduced from 20 to 14 for better spacing
FONT_SIZE: int = 24
ARCH_RADIUS: int = 220  # Reduced from 300 to 220 for better fit
ARCH_OUTLINE_WIDTH: int = 2
TIME_AND_SPACE_RADIUS: int = 30

NUM_PORTS_PER_SIDE: int = 18


# Arch math helpers
def generate_arch_positions(
    center: Tuple[int, int],
    radius: int,
    count: int,
    angle_start: float = 180,
    angle_span: float = 180,
) -> List[Tuple[int, int]]:
    # We want to skip two positions in the center of the arch
    total_positions = count + 2
    angles = [
        angle_start + i * (angle_span / (total_positions - 1))
        for i in range(total_positions)
    ]
    # Skip the two center-most positions
    skip1 = total_positions // 2 - 1
    skip2 = total_positions // 2
    positions = [
        (
            int(center[0] + radius * math.cos(math.radians(angle))),
            int(center[1] + radius * math.sin(math.radians(angle))),
        )
        for i, angle in enumerate(angles)
        if i != skip1 and i != skip2
    ]
    return positions


def generate_arch_outline(
    center: Tuple[int, int], radius: int, port_radius: int
) -> List[Tuple[int, int]]:
    outer_radius = radius + 40
    inner_radius = radius - 40
    outer_angles = [180 + i * (180 / 36) for i in range(37)]
    inner_angles = [0 - i * (180 / 36) for i in range(37)]
    outer_arc = [
        (
            int(center[0] + outer_radius * math.cos(math.radians(angle))),
            int(center[1] + outer_radius * math.sin(math.radians(angle))),
        )
        for angle in outer_angles
    ]
    inner_arc = [
        (
            int(center[0] + inner_radius * math.cos(math.radians(angle))),
            int(center[1] + inner_radius * math.sin(math.radians(angle))),
        )
        for angle in inner_angles
    ]
    return (
        [(outer_arc[0][0], outer_arc[0][1] + port_radius * 2)]
        + outer_arc
        + [(outer_arc[-1][0], outer_arc[-1][1] + port_radius * 2)]
        + [(inner_arc[0][0], inner_arc[0][1] + port_radius * 2)]
        + list(inner_arc)
        + [(inner_arc[-1][0], inner_arc[-1][1] + port_radius * 2)]
    )


def draw_arch(
    surface: pygame.Surface,
    center: Tuple[int, int],
    states: Sequence[Any],
    names: Sequence[str],
    title: str,
    color: Tuple[int, int, int],
    font: pygame.font.Font,
    mouse_pos: Tuple[int, int],
    segment: int,
) -> Optional[str]:
    # Draw arch outline
    outline = generate_arch_outline(center, ARCH_RADIUS, PORT_RADIUS)
    pygame.draw.polygon(surface, (200, 200, 200), outline, ARCH_OUTLINE_WIDTH)
    # Draw title
    title_surf = font.render(title, True, color)
    surface.blit(
        title_surf,
        (center[0] - title_surf.get_width() // 2, center[1] - ARCH_RADIUS - 60),
    )
    # Draw portholes
    ports = generate_arch_positions(center, ARCH_RADIUS, NUM_PORTS_PER_SIDE)
    hovered_name = None
    pride_colors = [
        (228, 3, 3),  # Red
        (255, 140, 0),  # Orange
        (255, 237, 0),  # Yellow
        (0, 128, 38),  # Green
        (0, 77, 255),  # Blue
        (117, 7, 135),  # Violet
    ]
    pride_offset = int(pygame.time.get_ticks() / 120)  # Animate every 120ms
    for i, (x, y) in enumerate(ports):
        state = states[i]
        name = names[i]
        color_fill = PORT_COLOR_OFF

        if state is not None and state.on:
            effect_index = state.fx or 0
            if WLED_EFFECTS[effect_index] == "Pride 2015":
                # Animate pride rainbow: shift colors over time
                color_fill = pride_colors[(i + pride_offset) % len(pride_colors)]
            elif state.seg:
                if state.seg[0].fx is not None:
                    if WLED_EFFECTS[state.seg[0].fx] == "Pride 2015":
                        color_fill = pride_colors[
                            (i + pride_offset) % len(pride_colors)
                        ]
                    elif WLED_EFFECTS[state.seg[0].fx] == "Solid":
                        rgb = state.seg[0].col[0]
                        color_fill = tuple(rgb)
                    elif WLED_EFFECTS[state.seg[0].fx] == "Blink":
                        rgb = state.seg[0].col[0] if i % 2 == 0 else [0, 0, 0]
                        color_fill = tuple(rgb)
                    else:
                        print(
                            f"Effect {state.seg[0].fx} {WLED_EFFECTS[state.seg[0].fx]} not supported for {name}"
                        )
                elif state.seg[0].col:
                    rgb = state.seg[segment].col[0]
                    color_fill = tuple(rgb)
            else:
                print(f"No segment data for {name}, skipping")
                continue
        pygame.draw.circle(surface, color_fill, (x, y), PORT_RADIUS)
        pygame.draw.circle(surface, color, (x, y), PORT_RADIUS, 2)
        # Ensure portholes do not overlap with time_and_space
        time_and_space_pos = (center[0], center[1] - ARCH_RADIUS)
        min_dist = PORT_RADIUS + TIME_AND_SPACE_RADIUS + 6
        if math.hypot(x - time_and_space_pos[0], y - time_and_space_pos[1]) < min_dist:
            continue  # Skip drawing if too close to time_and_space
        if math.hypot(mouse_pos[0] - x, mouse_pos[1] - y) < PORT_RADIUS:
            hovered_name = name
    # Draw time_and_space circle last so it is always on top
    time_and_space_pos = (center[0], center[1] - ARCH_RADIUS)
    pygame.draw.circle(
        surface, (255, 255, 255), time_and_space_pos, TIME_AND_SPACE_RADIUS, 4
    )
    return hovered_name


def run_visualizer(
    state_manager: Any,
    front_indices: Sequence[int],
    back_indices: Sequence[int],
) -> None:

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("WLED Arch Visualizer")
    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()
    running = True
    hovered = None
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BG_COLOR)
        # Layout: front arch far left, back arch far right
        front_center = (ARCH_RADIUS + 60, HEIGHT // 2 + 100)
        back_center = (WIDTH - ARCH_RADIUS - 60, HEIGHT // 2 + 100)
        front_states = [state_manager.states[i] for i in front_indices]
        back_states = [state_manager.states[i] for i in back_indices]
        front_names = [state_manager.names[i] for i in front_indices]
        back_names = [state_manager.names[i] for i in back_indices]
        hovered = draw_arch(
            screen,
            front_center,
            front_states,
            front_names,
            "Front",
            FRONT_COLOR,
            font,
            mouse_pos,
            0,  # Segment 0 for front arch
        )
        hovered2 = draw_arch(
            screen,
            back_center,
            back_states,
            back_names,
            "Back",
            BACK_COLOR,
            font,
            mouse_pos,
            1,  # Segment 1 for back arch
        )
        if hovered or hovered2:
            name = hovered or hovered2
            label = font.render(name, True, (255, 255, 255))
            screen.blit(label, (mouse_pos[0] + 10, mouse_pos[1] - 10))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
