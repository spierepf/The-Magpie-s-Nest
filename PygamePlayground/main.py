import random
import math
import sys
import pygame
import time
from typing import List, Tuple, Optional, TypeAlias, Set

RGBColor: TypeAlias = Tuple[int, int, int]

pygame.init()
WIDTH: int = 947
HEIGHT: int = 768
screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time and Space Arch")
clock: pygame.time.Clock = pygame.time.Clock()

PORT_RADIUS: int = 20
PORT_COLOR_DEFAULT: RGBColor = (128, 0, 128)
PORT_COLOR_GOOD: RGBColor = (0, 255, 0)
PORT_COLOR_BAD: RGBColor = (255, 0, 0)
PORT_COLOR_ANIM: List[RGBColor] = [(255, 0, 255), (0, 255, 255), (255, 255, 0)]
TIME_AND_SPACE_POS: Tuple[int, int] = (WIDTH // 2, 100)
NUM_PORTS_PER_SIDE: int = 9
ARCH_RADIUS: int = 300
ARCH_CENTER: Tuple[int, int] = (WIDTH // 2, TIME_AND_SPACE_POS[1] + ARCH_RADIUS)
WIRE_LENGTH: int = 600  # fixed wire length


def generate_arch_positions(
    center: Tuple[int, int], radius: int, count: int, angle_offset: List[float]
) -> List[Tuple[int, int]]:
    return [
        (
            int(center[0] + radius * math.cos(math.radians(angle))),
            int(center[1] + radius * math.sin(math.radians(angle))),
        )
        for angle in angle_offset
    ]


left_angles: List[float] = list(
    reversed(
        [180 + i * (80 / (NUM_PORTS_PER_SIDE - 1)) for i in range(NUM_PORTS_PER_SIDE)]
    )
)
right_angles: List[float] = [
    360 - i * (80 / (NUM_PORTS_PER_SIDE - 1)) for i in range(NUM_PORTS_PER_SIDE)
]
left_ports: List[Tuple[int, int]] = generate_arch_positions(
    ARCH_CENTER, ARCH_RADIUS, NUM_PORTS_PER_SIDE, left_angles
)
right_ports: List[Tuple[int, int]] = generate_arch_positions(
    ARCH_CENTER, ARCH_RADIUS, NUM_PORTS_PER_SIDE, right_angles
)
portholes: List[Tuple[int, int]] = left_ports + right_ports

connections: List[Tuple[int, int, RGBColor]] = []
selected: Optional[int] = None
port_colors: List[RGBColor] = [PORT_COLOR_DEFAULT] * len(portholes)
available_indices: List[int] = list(range(len(portholes)))
random.shuffle(available_indices)
correct_pairs: List[Tuple[int, int]] = [
    tuple(sorted((available_indices[i], available_indices[i + 1]))[:2])
    for i in range(0, 6, 2)
]


def draw_portholes() -> None:
    connected_good_ports: Set[int] = set()
    for c in connections:
        idx_pair = tuple(sorted((c[0], c[1])))
        if idx_pair in correct_pairs:
            connected_good_ports.add(c[0])
            connected_good_ports.add(c[1])
    for i, (x, y) in enumerate(portholes):
        color: RGBColor = (
            PORT_COLOR_GOOD if i in connected_good_ports else port_colors[i]
        )
        pygame.draw.circle(screen, color, (x, y), PORT_RADIUS)


def draw_time_and_space() -> None:
    pygame.draw.circle(screen, (255, 255, 255), TIME_AND_SPACE_POS, 30, 4)


def draw_arch_outline() -> None:
    points = generate_arch_outline()
    pygame.draw.polygon(screen, (200, 200, 200), points, 2)


def draw_connections() -> None:
    for idx1, idx2, color in connections:
        p1, p2 = portholes[idx1], portholes[idx2]
        dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        sag_scale = math.sqrt(max(WIRE_LENGTH**2 - dist**2, 0)) / 2
        mid_x = (p1[0] + p2[0]) // 2
        mid_y = (p1[1] + p2[1]) // 2 + int(sag_scale)
        draw_bezier_curve(p1, (mid_x, mid_y), p2, color, thickness=6)


def draw_bezier_curve(
    p0: Tuple[int, int],
    p1: Tuple[int, int],
    p2: Tuple[int, int],
    color: RGBColor,
    thickness: int = 6,
    segments: int = 20,
) -> None:
    prev = p0
    for t in range(1, segments + 1):
        t /= segments
        x = int((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0])
        y = int((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1])
        pygame.draw.line(screen, color, prev, (x, y), thickness)
        prev = (x, y)


def point_in_circle(
    point: Tuple[int, int], center: Tuple[int, int], radius: int
) -> bool:
    return math.hypot(point[0] - center[0], point[1] - center[1]) <= radius


def find_clicked_port(pos: Tuple[int, int]) -> Optional[int]:
    for i, p in enumerate(portholes):
        if point_in_circle(pos, p, PORT_RADIUS):
            return i
    return None


def find_clicked_connection(pos: Tuple[int, int]) -> Optional[int]:
    # For each connection, sample points along the Bezier curve and check proximity
    for i, (idx1, idx2, _) in enumerate(connections):
        p1, p2 = portholes[idx1], portholes[idx2]
        dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        sag_scale = math.sqrt(max(WIRE_LENGTH**2 - dist**2, 0)) / 2
        mid_x = (p1[0] + p2[0]) // 2
        mid_y = (p1[1] + p2[1]) // 2 + int(sag_scale)
        # Sample points along the quadratic Bezier curve
        segments = 20
        for t in range(segments + 1):
            t_norm = t / segments
            x = int(
                (1 - t_norm) ** 2 * p1[0]
                + 2 * (1 - t_norm) * t_norm * (mid_x)
                + t_norm**2 * p2[0]
            )
            y = int(
                (1 - t_norm) ** 2 * p1[1]
                + 2 * (1 - t_norm) * t_norm * (mid_y)
                + t_norm**2 * p2[1]
            )
            if point_in_circle(pos, (x, y), 10):
                return i
    return None


def handle_connection(a: int, b: int) -> None:
    global connections
    idx_pair = tuple(sorted((a, b)))
    occupied: Set[int] = set()
    for c in connections:
        occupied.add(c[0])
        occupied.add(c[1])
    if a in occupied or b in occupied:
        print(f"Cannot connect: porthole {a} or {b} is already occupied.")
        return
    for c in connections:
        if tuple(sorted((c[0], c[1]))) == idx_pair:
            return
    # If already 3 wires, remove a bad one if possible
    if len(connections) >= 3:
        # Find a bad connection (not in correct_pairs)
        for i, c in enumerate(connections):
            if tuple(sorted((c[0], c[1]))) not in correct_pairs:
                port_colors[c[0]] = port_colors[c[1]] = PORT_COLOR_DEFAULT
                del connections[i]
                break
        # If all are good, do not add more
        if len(connections) >= 3:
            print("Maximum wires reached and all are correct. Cannot add more.")
            return
    color: RGBColor = tuple(random.randint(100, 255) for _ in range(3))  # type: ignore
    connections.append((a, b, color))
    if idx_pair in correct_pairs:
        port_colors[a] = port_colors[b] = PORT_COLOR_GOOD
        print(f"✔️ Correct pair: {idx_pair}")
    else:
        port_colors[a] = port_colors[b] = PORT_COLOR_BAD
        print(f"❌ Incorrect pair: {idx_pair}")


def check_victory() -> bool:
    matched = 0
    for cp in correct_pairs:
        for c in connections:
            if tuple(sorted((c[0], c[1]))) == cp:
                matched += 1
                break
    return matched == len(correct_pairs)


def run_win_animation() -> None:
    for _ in range(10):
        for color in PORT_COLOR_ANIM:
            screen.fill((0, 0, 0))
            draw_connections()
            draw_arch_outline()
            for i in range(len(portholes)):
                pygame.draw.circle(screen, color, portholes[i], PORT_RADIUS)
            draw_time_and_space()
            pygame.display.flip()
            pygame.time.wait(100)


def generate_arch_outline() -> List[Tuple[int, int]]:
    outer_radius = ARCH_RADIUS + 40
    inner_radius = ARCH_RADIUS - 40
    outer_angles = [180 + i * (180 / 36) for i in range(37)]  # 180 to 0
    inner_angles = [0 - i * (180 / 36) for i in range(37)]  # 0 to 180

    outer_arc = [
        (
            int(ARCH_CENTER[0] + outer_radius * math.cos(math.radians(angle))),
            int(ARCH_CENTER[1] + outer_radius * math.sin(math.radians(angle))),
        )
        for angle in outer_angles
    ]
    inner_arc = [
        (
            int(ARCH_CENTER[0] + inner_radius * math.cos(math.radians(angle))),
            int(ARCH_CENTER[1] + inner_radius * math.sin(math.radians(angle))),
        )
        for angle in inner_angles
    ]

    return (
        [(outer_arc[0][0], outer_arc[0][1] + PORT_RADIUS * 2)]
        + outer_arc
        + [(outer_arc[-1][0], outer_arc[-1][1] + PORT_RADIUS * 2)]
        + [(inner_arc[0][0], inner_arc[0][1] + PORT_RADIUS * 2)]
        + list((inner_arc))
        + [(inner_arc[-1][0], inner_arc[-1][1] + PORT_RADIUS * 2)]
    )


# Timer variables for hint blinking
HINT_INTERVAL: int = 60  # seconds
HINT_DURATION: int = 2  # seconds
last_hint_time: float = time.time()
hint_active: bool = False
hint_pair: Optional[Tuple[int, int]] = None
hint_start_time: float = 0


def blink_hint_pair(pair: Tuple[int, int], blink_on: bool) -> None:
    color: RGBColor = (255, 255, 255) if blink_on else PORT_COLOR_DEFAULT
    for idx in pair:
        pygame.draw.circle(screen, color, portholes[idx], PORT_RADIUS + 4)


running: bool = True
won: bool = False

while running:
    screen.fill((0, 0, 0))
    draw_connections()
    draw_arch_outline()
    draw_portholes()
    draw_time_and_space()

    # Handle hint blinking
    now = time.time()
    # Only select from unconnected correct pairs
    connected_pairs = set(tuple(sorted((c[0], c[1]))) for c in connections)
    unconnected_correct_pairs = [
        cp for cp in correct_pairs if cp not in connected_pairs
    ]
    if (
        not won
        and now - last_hint_time > HINT_INTERVAL
        and not hint_active
        and unconnected_correct_pairs
    ):
        hint_pair = random.choice(unconnected_correct_pairs)
        hint_active = True
        hint_start_time = now
        print(f"💡 Hint: Blinking pair {hint_pair}")
    if hint_active and hint_pair:
        blink_on = int((now - hint_start_time) * 4) % 2 == 0
        blink_hint_pair(hint_pair, blink_on)
        if now - hint_start_time > HINT_DURATION:
            hint_active = False
            last_hint_time = now
            hint_pair = None

    pygame.display.flip()

    if not won and check_victory():
        run_win_animation()
        won = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            clicked_wire = find_clicked_connection(pos)
            if clicked_wire is not None:
                a, b, _ = connections[clicked_wire]
                port_colors[a] = port_colors[b] = PORT_COLOR_DEFAULT
                print(f"🧹 Removed wire: ({a}, {b})")
                del connections[clicked_wire]
                continue
            idx = find_clicked_port(pos)
            if idx is not None:
                if selected is None:
                    selected = idx
                else:
                    if selected != idx:
                        handle_connection(selected, idx)
                    selected = None

    clock.tick(60)

pygame.quit()
sys.exit()
