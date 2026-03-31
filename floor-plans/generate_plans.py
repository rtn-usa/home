#!/usr/bin/env python3
"""Generate 3 feng shui floor plan layouts as PNG images."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arc
import numpy as np

# Apartment outline (polygon vertices)
OUTER = np.array([
    [300,870],[300,230],[680,130],[1120,350],[1120,130],
    [1370,130],[1370,500],[1630,500],[1630,870],[300,870]
]) / np.array([1920, 1080])  # normalize to 0-1

# Internal wall segments (x1,y1,x2,y2) normalized
def n(coords):
    return [c/1920 if i%2==0 else c/1080 for i,c in enumerate(coords)]

INNER_WALLS = [
    n([300,620,540,620]),   # left bedroom top wall
    n([580,620,580,870]),   # left bedroom right wall
    n([1370,500,1370,870]), # right bedroom wall
    n([920,560,920,740]),   # bathroom left
    n([920,560,1105,560]),  # bathroom top
    n([1105,560,1105,740]), # bathroom right
    n([920,740,1105,740]),  # bathroom bottom
]

# Kitchen counter
KITCHEN_COUNTER_TOP = n([1125,135,1365,135])
KITCHEN_COUNTER_SIDE = n([1125,135,1125,345])

# Window segments
WINDOWS = [
    n([300,290,300,430]),   # left wall window 1
    n([300,460,300,590]),   # left wall window 2
    n([370,213,530,163]),   # angled window 1
    n([560,153,660,137]),   # angled window 2
    n([1630,590,1630,740]), # right bedroom window
]

def setup_ax(fig):
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.88])  # leave room for title
    ax.set_xlim(0.1, 0.95)
    ax.set_ylim(0.95, 0.05)  # flip y so top is top
    ax.set_aspect('equal')
    ax.axis('off')
    return ax

def draw_apartment(ax):
    """Draw the apartment shell - walls, windows, kitchen, bathroom."""
    # Floor fill
    from matplotlib.patches import Polygon
    floor = Polygon(OUTER, closed=True, fc='#F5F0E8', ec='none', zorder=0)
    ax.add_patch(floor)

    # Outer walls
    ax.plot(OUTER[:,0], OUTER[:,1], color='#222', lw=3.5, solid_capstyle='round', solid_joinstyle='round', zorder=5)

    # Inner walls
    for w in INNER_WALLS:
        ax.plot([w[0],w[2]], [w[1],w[3]], color='#222', lw=2.5, solid_capstyle='round', zorder=5)

    # Windows (cyan lines)
    for w in WINDOWS:
        ax.plot([w[0],w[2]], [w[1],w[3]], color='#5BA4E6', lw=3, solid_capstyle='round', zorder=6)

    # Kitchen counter
    kct = KITCHEN_COUNTER_TOP
    ax.plot([kct[0],kct[2]], [kct[1],kct[3]], color='#999', lw=4, solid_capstyle='round', zorder=4)
    kcs = KITCHEN_COUNTER_SIDE
    ax.plot([kcs[0],kcs[2]], [kcs[1],kcs[3]], color='#999', lw=4, solid_capstyle='round', zorder=4)

    # Kitchen labels
    ax.text(1250/1920, 165/1080, 'STOVE', ha='center', va='center', fontsize=5, color='#888', zorder=6)
    ax.text(1330/1920, 165/1080, 'REF', ha='center', va='center', fontsize=5, color='#888', zorder=6)
    ax.text(1150/1920, 280/1080, 'DW', ha='center', va='center', fontsize=5, color='#888', zorder=6)
    ax.text(1150/1920, 240/1080, 'SINK', ha='center', va='center', fontsize=5, color='#888', zorder=6)

    # Bathroom labels
    ax.text(1010/1920, 650/1080, 'BATH', ha='center', va='center', fontsize=6, color='#aaa',
            style='italic', zorder=6)
    ax.text(960/1920, 620/1080, 'W/D', ha='center', va='center', fontsize=5, color='#888', zorder=6)

    # Closets
    c1 = FancyBboxPatch((305/1920, 625/1080), 55/1920, 22/1080,
                          boxstyle="round,pad=0.002", fc='#E8E4DC', ec='#bbb', lw=0.8, zorder=3)
    ax.add_patch(c1)
    ax.text(332/1920, 637/1080, 'CL', ha='center', va='center', fontsize=4, color='#aaa', zorder=6)

    c2 = FancyBboxPatch((1375/1920, 508/1080), 22/1920, 70/1080,
                          boxstyle="round,pad=0.002", fc='#E8E4DC', ec='#bbb', lw=0.8, zorder=3)
    ax.add_patch(c2)
    ax.text(1386/1920, 543/1080, 'CL', ha='center', va='center', fontsize=4, color='#aaa', rotation=90, zorder=6)

    # Door opening indicators (gaps in walls)
    # Left bedroom door
    ax.plot([540/1920, 580/1920], [620/1080, 620/1080], color='#F5F0E8', lw=3, zorder=5)
    # Entry
    ax.plot([1120/1920, 1120/1920], [350/1080, 420/1080], color='#F5F0E8', lw=4, zorder=5)
    ax.text(1130/1920, 385/1080, 'ENTRY', ha='left', va='center', fontsize=5, color='#aaa', zorder=6)
    # Right bedroom door
    ax.plot([1370/1920, 1370/1920], [620/1080, 680/1080], color='#F5F0E8', lw=3, zorder=5)

def draw_furniture(ax, item_type, x, y, w, h, label, rotation=0, color=None):
    """Draw a furniture piece. x,y,w,h in raw pixel coords (1920x1080)."""
    colors = {
        'bed': '#C4A882', 'sofa': '#8FB8A0', 'desk': '#A3B5C7',
        'table': '#D4B896', 'tv': '#555', 'storage': '#BDB5A8',
        'dog': '#D4C4A8', 'chair': '#C9B99A', 'rug': '#EDE6D6',
        'murphy': '#B8A080', 'pullout': '#8FB8A0',
    }
    fc = color or colors.get(item_type, '#ccc')
    xn, yn, wn, hn = x/1920, y/1080, w/1920, h/1080

    if rotation != 0:
        import matplotlib.transforms as transforms
        t = transforms.Affine2D().rotate_deg_around(xn + wn/2, yn + hn/2, rotation) + ax.transData
        rect = FancyBboxPatch((xn, yn), wn, hn, boxstyle="round,pad=0.001",
                               fc=fc, ec='#666', lw=0.8, zorder=3, transform=t)
        ax.add_patch(rect)
        ax.text(xn + wn/2, yn + hn/2, label, ha='center', va='center',
                fontsize=5, color='#333', zorder=7, rotation=rotation,
                fontweight='bold')
    else:
        rect = FancyBboxPatch((xn, yn), wn, hn, boxstyle="round,pad=0.001",
                               fc=fc, ec='#666', lw=0.8, zorder=3)
        ax.add_patch(rect)
        ax.text(xn + wn/2, yn + hn/2, label, ha='center', va='center',
                fontsize=5, color='#333', zorder=7, fontweight='bold')

    # Headboard indicator for beds
    if item_type == 'bed':
        ax.plot([xn, xn+wn], [yn, yn], color='#8B7355', lw=2.5, zorder=4)

def draw_zone(ax, x, y, w, h, color, label):
    """Draw a colored zone overlay."""
    rect = FancyBboxPatch((x/1920, y/1080), w/1920, h/1080,
                           boxstyle="round,pad=0.005", fc=color, alpha=0.08,
                           ec=color, lw=0.5, ls='--', zorder=1)
    ax.add_patch(rect)
    ax.text((x+w/2)/1920, (y+12)/1080, label, ha='center', va='top',
            fontsize=5, color=color, alpha=0.6, zorder=2, style='italic')

def add_fengshui_note(ax, x, y, text, color='#B8860B'):
    """Add a feng shui annotation."""
    ax.text(x/1920, y/1080, f'~ {text}', ha='left', va='center',
            fontsize=4.5, color=color, style='italic', zorder=8,
            bbox=dict(boxstyle='round,pad=0.3', fc='#FFFDE8', ec='#E8D888', lw=0.5, alpha=0.8))

def add_arrow(ax, x1, y1, x2, y2, color='#aaa'):
    ax.annotate('', xy=(x2/1920, y2/1080), xytext=(x1/1920, y1/1080),
                arrowprops=dict(arrowstyle='->', color=color, lw=0.8), zorder=2)

# ============================================================
# LAYOUT 1: "Harmonious Flow"
# ============================================================
def layout1():
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor('#FDFCFA')
    fig.text(0.5, 0.97, 'Layout 1: Harmonious Flow', ha='center', va='top',
             fontsize=22, fontweight='bold', color='#222')
    fig.text(0.5, 0.935, 'Classic Feng Shui  |  Balanced Chi  |  Commanding Positions',
             ha='center', va='top', fontsize=11, color='#888')

    ax = setup_ax(fig)
    draw_apartment(ax)

    # ZONES
    draw_zone(ax, 310, 240, 500, 370, '#4A90D9', 'LIVING / SOCIAL ZONE')
    draw_zone(ax, 310, 630, 260, 230, '#6B8E5B', 'DEN / WORK ZONE')
    draw_zone(ax, 1380, 510, 240, 350, '#9B6B8E', 'MASTER BEDROOM')
    draw_zone(ax, 700, 400, 350, 300, '#D4A06A', 'DINING ZONE')

    # RIGHT BEDROOM - Queen bed commanding position
    # Headboard on solid west wall, facing door
    draw_furniture(ax, 'bed', 1410, 680, 180, 140, 'QUEEN\nBED')
    draw_furniture(ax, 'desk', 1420, 550, 100, 50, 'DESK 1')
    draw_furniture(ax, 'storage', 1540, 550, 30, 120, 'SHELF')
    # Nightstands
    draw_furniture(ax, 'storage', 1410, 830, 40, 30, 'NS')
    draw_furniture(ax, 'storage', 1550, 830, 40, 30, 'NS')

    # LIVING ROOM - Pull-out sofa against solid wall
    draw_furniture(ax, 'pullout', 330, 320, 200, 90, 'PULL-OUT\nSOFA\n(Guest Bed)')
    draw_furniture(ax, 'tv', 620, 290, 8, 100, 'TV')
    draw_furniture(ax, 'storage', 635, 290, 30, 100, 'MEDIA\nCABINET')
    draw_furniture(ax, 'rug', 370, 290, 230, 140, '')  # rug under sofa area

    # Dog area near sofa and windows
    draw_furniture(ax, 'dog', 330, 440, 120, 60, 'DOG\nLOUNGE')

    # Multi-functional seating - poufs/cushions near windows
    draw_furniture(ax, 'chair', 330, 250, 50, 40, 'POUF')
    draw_furniture(ax, 'chair', 400, 250, 50, 40, 'POUF')

    # DINING - Round table near kitchen
    from matplotlib.patches import Circle
    circle = Circle((830/1920, 520/1080), 40/1920, fc='#D4B896', ec='#666', lw=0.8, zorder=3)
    ax.add_patch(circle)
    ax.text(830/1920, 520/1080, 'DINING\nTABLE', ha='center', va='center', fontsize=5, color='#333', zorder=7, fontweight='bold')
    # Chairs around table
    for angle in [0, 90, 180, 270]:
        cx = 830 + 55*np.cos(np.radians(angle))
        cy = 520 + 55*np.sin(np.radians(angle)) * (1920/1080)
        chair = Circle((cx/1920, cy/1080), 12/1920, fc='#C9B99A', ec='#666', lw=0.5, zorder=3)
        ax.add_patch(chair)

    # DEN / LEFT BEDROOM - Converted to work space
    draw_furniture(ax, 'desk', 330, 660, 120, 55, 'DESK 2')
    draw_furniture(ax, 'chair', 370, 720, 35, 30, 'CH')
    draw_furniture(ax, 'storage', 470, 650, 90, 30, 'BOOKSHELF')
    draw_furniture(ax, 'storage', 330, 790, 230, 30, 'STORAGE\nCABINET')

    # FENG SHUI ANNOTATIONS
    add_fengshui_note(ax, 1420, 860, 'Headboard on solid wall = stability')
    add_fengshui_note(ax, 340, 510, 'Sofa faces door = commanding position')
    add_fengshui_note(ax, 690, 570, 'Round table = harmonious chi flow')
    add_fengshui_note(ax, 340, 835, 'Work zone in Knowledge area (NE bagua)')
    add_fengshui_note(ax, 1420, 530, 'Desk faces door = empowered work')

    # Chi flow arrows
    add_arrow(ax, 1120, 400, 900, 500)
    add_arrow(ax, 900, 500, 600, 400)
    add_arrow(ax, 600, 400, 400, 350)

    # Legend
    fig.text(0.03, 0.06, 'FENG SHUI PRINCIPLES:', fontsize=7, fontweight='bold', color='#B8860B')
    fig.text(0.03, 0.04, '• Commanding positions for bed, sofa & desk  • Round dining table for smooth chi  • Dog lounge near earth element (windows/nature views)', fontsize=6, color='#888')
    fig.text(0.03, 0.02, '• Den converts unused bedroom to productive space  • Paired nightstands for balance  • Clear pathways for energy flow  • Pull-out sofa = guest bed + daily seating', fontsize=6, color='#888')

    fig.savefig('/home/user/home/floor-plans/layout1_harmonious_flow.png', dpi=100, bbox_inches='tight', facecolor='#FDFCFA')
    plt.close()
    print("Layout 1 done")

# ============================================================
# LAYOUT 2: "Creative Studio"
# ============================================================
def layout2():
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor('#FDFCFA')
    fig.text(0.5, 0.97, 'Layout 2: Creative Studio', ha='center', va='top',
             fontsize=22, fontweight='bold', color='#222')
    fig.text(0.5, 0.935, 'Work-Life Balance  |  Dual Workspace Near Natural Light  |  Open Flow',
             ha='center', va='top', fontsize=11, color='#888')

    ax = setup_ax(fig)
    draw_apartment(ax)

    # ZONES
    draw_zone(ax, 310, 240, 300, 250, '#6B8E5B', 'WORK ZONE')
    draw_zone(ax, 620, 380, 300, 310, '#D4A06A', 'SOCIAL / DINING')
    draw_zone(ax, 310, 630, 260, 230, '#D4A06A', 'FLEX LOUNGE')
    draw_zone(ax, 1380, 510, 240, 350, '#9B6B8E', 'MASTER BEDROOM')

    # RIGHT BEDROOM - Queen bed
    draw_furniture(ax, 'bed', 1430, 620, 160, 140, 'QUEEN\nBED')
    draw_furniture(ax, 'storage', 1430, 770, 40, 30, 'NS')
    draw_furniture(ax, 'storage', 1550, 770, 40, 30, 'NS')
    draw_furniture(ax, 'storage', 1540, 550, 30, 60, 'SHELF')

    # WORK ZONE - Both desks near windows for natural light
    draw_furniture(ax, 'desk', 330, 280, 130, 55, 'DESK 1\n(Primary)')
    draw_furniture(ax, 'chair', 380, 340, 35, 30, 'CH')
    draw_furniture(ax, 'desk', 330, 400, 130, 55, 'DESK 2\n(Secondary)')
    draw_furniture(ax, 'chair', 380, 460, 35, 30, 'CH')
    draw_furniture(ax, 'storage', 475, 280, 30, 175, 'BOOK\nSHELF')

    # LIVING AREA - Pull-out sofa
    draw_furniture(ax, 'pullout', 650, 420, 200, 85, 'PULL-OUT\nSOFA\n(Guest Bed)')
    draw_furniture(ax, 'tv', 650, 540, 8, 90, 'TV')
    draw_furniture(ax, 'storage', 665, 540, 30, 90, 'MEDIA')

    # Dog area near sofa
    draw_furniture(ax, 'dog', 650, 520, 100, 50, '')  # under/near sofa area
    draw_furniture(ax, 'dog', 870, 420, 80, 60, 'DOG\nBED')

    # Dining - bar-height table near kitchen
    draw_furniture(ax, 'table', 800, 350, 150, 50, 'DINING BAR\n(seats 4)')
    draw_furniture(ax, 'chair', 810, 310, 30, 25, '')
    draw_furniture(ax, 'chair', 850, 310, 30, 25, '')
    draw_furniture(ax, 'chair', 890, 310, 30, 25, '')
    draw_furniture(ax, 'chair', 930, 310, 30, 25, '')

    # FLEX LOUNGE (former left bedroom)
    draw_furniture(ax, 'chair', 340, 670, 80, 60, 'ACCENT\nCHAIR')
    draw_furniture(ax, 'storage', 440, 660, 30, 80, 'SHELF')
    draw_furniture(ax, 'chair', 340, 760, 80, 50, 'FLOOR\nCUSHIONS')
    draw_furniture(ax, 'storage', 330, 830, 230, 25, 'LOW STORAGE / DOG CRATE')

    # Multi-functional seating
    draw_furniture(ax, 'chair', 530, 450, 50, 50, 'POUF')

    # FENG SHUI ANNOTATIONS
    add_fengshui_note(ax, 1430, 850, 'Bed in commanding position, solid wall behind')
    add_fengshui_note(ax, 340, 500, 'Desks face entry = career empowerment')
    add_fengshui_note(ax, 340, 250, 'Natural light on workspace = wood element vitality')
    add_fengshui_note(ax, 660, 650, 'Clear center = open heart of home')
    add_fengshui_note(ax, 350, 640, 'Flex room = creativity & knowledge zone')

    # Chi flow
    add_arrow(ax, 1120, 400, 850, 380)
    add_arrow(ax, 850, 380, 550, 350)
    add_arrow(ax, 550, 350, 400, 300)

    fig.text(0.03, 0.06, 'FENG SHUI PRINCIPLES:', fontsize=7, fontweight='bold', color='#B8860B')
    fig.text(0.03, 0.04, '• Dual workspace by windows channels Wood element energy for creativity & focus  • Dining bar creates social gathering near Fire element (kitchen/stove)', fontsize=6, color='#888')
    fig.text(0.03, 0.02, '• Open center allows chi to circulate freely  • Former bedroom becomes Knowledge/Creativity corner  • Pull-out sofa for guests preserves open flow', fontsize=6, color='#888')

    fig.savefig('/home/user/home/floor-plans/layout2_creative_studio.png', dpi=100, bbox_inches='tight', facecolor='#FDFCFA')
    plt.close()
    print("Layout 2 done")

# ============================================================
# LAYOUT 3: "Social Sanctuary"
# ============================================================
def layout3():
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor('#FDFCFA')
    fig.text(0.5, 0.97, 'Layout 3: Social Sanctuary', ha='center', va='top',
             fontsize=22, fontweight='bold', color='#222')
    fig.text(0.5, 0.935, 'Entertaining-Focused  |  Murphy Guest Bed  |  Large Multifunctional Table',
             ha='center', va='top', fontsize=11, color='#888')

    ax = setup_ax(fig)
    draw_apartment(ax)

    # ZONES
    draw_zone(ax, 310, 240, 520, 370, '#D4A06A', 'LIVING / ENTERTAINING')
    draw_zone(ax, 310, 630, 260, 230, '#6B8E5B', 'WORK NOOK + MURPHY BED')
    draw_zone(ax, 1380, 510, 240, 350, '#9B6B8E', 'MASTER BEDROOM')
    draw_zone(ax, 680, 400, 350, 310, '#4A90D9', 'DINING / GATHERING')

    # RIGHT BEDROOM - Queen bed + desk
    draw_furniture(ax, 'bed', 1430, 640, 160, 140, 'QUEEN\nBED')
    draw_furniture(ax, 'desk', 1430, 555, 100, 45, 'DESK 1')
    draw_furniture(ax, 'storage', 1430, 790, 40, 30, 'NS')
    draw_furniture(ax, 'storage', 1550, 790, 40, 30, 'NS')
    draw_furniture(ax, 'storage', 1550, 555, 40, 90, 'WARD-\nROBE')

    # LIVING ROOM - Sofa facing windows (views!)
    draw_furniture(ax, 'sofa', 460, 320, 200, 80, 'SOFA')
    draw_furniture(ax, 'rug', 400, 280, 320, 160, '')
    draw_furniture(ax, 'tv', 460, 270, 8, 80, 'TV')
    draw_furniture(ax, 'storage', 340, 260, 100, 30, 'CONSOLE\nTABLE')

    # Dog lounge near windows and sofa
    draw_furniture(ax, 'dog', 340, 430, 140, 55, 'DOG LOUNGE\n/ WINDOW SEAT')

    # Multi-functional seating
    draw_furniture(ax, 'chair', 680, 310, 50, 45, 'ARM\nCHAIR')
    draw_furniture(ax, 'chair', 340, 340, 60, 50, 'ACCENT\nCHAIR')

    # LARGE DINING/WORK TABLE
    draw_furniture(ax, 'table', 730, 480, 220, 90, 'LARGE TABLE\n(Dining + Work)\nSeats 6')
    for i in range(3):
        draw_furniture(ax, 'chair', 745+70*i, 445, 30, 25, '')
        draw_furniture(ax, 'chair', 745+70*i, 580, 30, 25, '')

    # Storage along wall
    draw_furniture(ax, 'storage', 700, 610, 200, 25, 'SIDEBOARD / BAR CART')

    # MURPHY BED ROOM (former left bedroom)
    draw_furniture(ax, 'murphy', 330, 660, 180, 30, 'MURPHY BED (folds down)', color='#B8A080')
    draw_furniture(ax, 'desk', 330, 720, 110, 50, 'DESK 2')
    draw_furniture(ax, 'chair', 360, 775, 35, 30, 'CH')
    draw_furniture(ax, 'storage', 460, 710, 90, 30, 'SHELVING')
    draw_furniture(ax, 'storage', 330, 830, 230, 25, 'BUILT-IN STORAGE')

    # Feng Shui annotations
    add_fengshui_note(ax, 1430, 850, 'Private retreat = strong Yin energy for rest')
    add_fengshui_note(ax, 350, 500, 'Sofa faces views = connects to nature chi')
    add_fengshui_note(ax, 700, 650, 'Gathering table at heart of home = community')
    add_fengshui_note(ax, 340, 640, 'Murphy bed: room transforms day/night (Yin/Yang)')
    add_fengshui_note(ax, 340, 240, 'Console behind sofa = protective backing')

    # Chi flow
    add_arrow(ax, 1120, 400, 850, 500)
    add_arrow(ax, 850, 500, 600, 400)
    add_arrow(ax, 600, 400, 400, 350)

    fig.text(0.03, 0.06, 'FENG SHUI PRINCIPLES:', fontsize=7, fontweight='bold', color='#B8860B')
    fig.text(0.03, 0.04, '• Large gathering table at home\'s center activates social/abundance energy  • Murphy bed transforms space: Yang (work) by day, Yin (rest) by night', fontsize=6, color='#888')
    fig.text(0.03, 0.02, '• Sofa facing windows draws in nature chi  • Dog lounge at window seat = grounding earth energy  • Open entertaining flow with clear sightlines to entry', fontsize=6, color='#888')

    fig.savefig('/home/user/home/floor-plans/layout3_social_sanctuary.png', dpi=100, bbox_inches='tight', facecolor='#FDFCFA')
    plt.close()
    print("Layout 3 done")

if __name__ == '__main__':
    layout1()
    layout2()
    layout3()
    print("All 3 layouts generated!")
