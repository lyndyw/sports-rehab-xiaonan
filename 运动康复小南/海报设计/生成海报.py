from PIL import Image, ImageDraw, ImageFont, ImageOps

# Create 9:16 canvas (1080x1920 for high resolution)
width = 1080
height = 1920

# Create image with white background
img = Image.new('RGB', (width, height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

# Color palette
colors = {
    'orange': '#FF8C42',
    'green': '#4CAF50',
    'blue': '#4A90E2',
    'red': '#E74C3C',
    'yellow': '#FFD93D',
    'gray': '#6B7280',
    'dark': '#1F2937',
    'light_orange': '#FFF0E6',
    'light_green': '#E8F5E9',
    'light_blue': '#E3F2FD',
}

# Load Chinese fonts
def load_chinese_fonts():
    font_paths = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Supplemental/PingFang.ttc",
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, 1)
        except:
            continue
    return ImageFont.load_default()

base_font = load_chinese_fonts()

def get_font(size):
    try:
        return ImageFont.truetype(base_font.path, size)
    except:
        return ImageFont.load_default()

font_title = get_font(64)
font_subtitle = get_font(42)
font_body = get_font(32)
font_small = get_font(26)
font_large = get_font(52)

# Helper functions
def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=4):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_circle(draw, center, radius, fill, outline=None, width=4):
    x, y = center
    draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill=fill, outline=outline, width=width)

def draw_text_left(draw, text, position, font, fill):
    x, y = position
    draw.text((x, y), text, font=font, fill=fill)

def draw_text_centered(draw, text, position, font, fill):
    x, y = position
    try:
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        draw.text((x - text_width//2, y), text, font=font, fill=fill)
    except:
        draw.text((x, y), text, font=font, fill=fill)

def draw_emoji_circle(draw, center, radius, emoji, bg_color):
    x, y = center
    draw_circle(draw, (x, y), radius, bg_color)
    # Draw emoji as text
    try:
        emoji_font = get_font(int(radius * 1.2))
        draw.text((x - radius//2, y - radius//3), emoji, font=emoji_font, fill='#000000')
    except:
        pass

def draw_star(draw, center, size, fill):
    """Draw a simple star"""
    x, y = center
    points = []
    for i in range(5):
        angle = i * 72 - 90
        outer_x = x + size * math.cos(math.radians(angle))
        outer_y = y + size * math.sin(math.radians(angle))
        points.append((outer_x, outer_y))
        inner_angle = angle + 36
        inner_x = x + size * 0.4 * math.cos(math.radians(inner_angle))
        inner_y = y + size * 0.4 * math.sin(math.radians(inner_angle))
        points.append((inner_x, inner_y))
    draw.polygon(points, fill=fill)

import math

# ============ BACKGROUND DECORATION ============
# Top wave with gradient effect
for i in range(100):
    alpha = int(100 - i * 1)
    color = (255, 140, 66, alpha)
    draw.polygon([(0, 0), (width, 0), (width, 60+i), (0, 80+i)], fill=color)

# Title area
draw_text_centered(draw, "糖尿病运动处方", (width//2, 45), font_title, colors['dark'])
draw_text_centered(draw, "72 岁 · 男性 · 控糖目标", (width//2, 125), font_subtitle, colors['gray'])

# ============ PATIENT INFO CARD ============
card_y = 190
card_h = 150
card_margin = 50

draw_rounded_rect(draw, (card_margin, card_y, width-card_margin, card_y+card_h), 25, colors['light_blue'], width=3)

# Patient info with icons
draw_text_centered(draw, "身高：1.65m   |   体重：65kg   |   BMI: 23.9", (width//2, card_y+40), font_body, colors['dark'])
draw_text_centered(draw, "🫀 无心血管问题   |   ⚠️ 风险分层：中危", (width//2, card_y+95), font_body, colors['green'])

# ============ 4-WEEK GOAL SECTION ============
goal_y = card_y + card_h + 40
draw_text_centered(draw, "🎯 4 周运动目标", (width//2, goal_y), font_large, colors['dark'])

goal_card_y = goal_y + 55
draw_rounded_rect(draw, (card_margin, goal_card_y, width-card_margin, goal_card_y+175), 25, colors['light_green'], width=3)

# Goal items with star bullets
goals = ["空腹血糖降低 1-2 mmol/L", "运动耐力提高 20-30%", "生活质量显著改善"]
for i, goal in enumerate(goals):
    star_x = width//2 - 120
    star_y = goal_card_y + 45 + i*52
    # Draw star
    draw_star(draw, (star_x, star_y+10), 12, colors['green'])
    draw_text_left(draw, goal, (star_x+35, star_y+35), font_body, colors['dark'])

# ============ FITT-VP EXERCISE PRESCRIPTION ============
fitt_y = goal_card_y + 205
draw_text_centered(draw, "📋 运动处方 (FITT-VP)", (width//2, fitt_y), font_large, colors['dark'])

# Aerobic exercise card with emoji
aerobic_y = fitt_y + 65
draw_rounded_rect(draw, (card_margin, aerobic_y, width-card_margin, aerobic_y+195), 25, colors['light_orange'], width=3)

draw_emoji_circle(draw, (card_margin+70, aerobic_y+55), 35, "🏃", colors['orange'])
draw_text_left(draw, "有氧运动（核心）", (card_margin+125, aerobic_y+38), font_subtitle, colors['dark'])
draw_text_left(draw, "📅 频率：≥5 天/周", (card_margin+50, aerobic_y+95), font_body, colors['dark'])
draw_text_left(draw, "💓 强度：心率 88-119 次/分 | RPE 11-13", (card_margin+50, aerobic_y+130), font_small, colors['dark'])
draw_text_left(draw, "⏱️ 时间：每次 30-40 分钟 | 累计≥150 分钟/周", (card_margin+50, aerobic_y+165), font_small, colors['dark'])

# Resistance exercise card
resistance_y = aerobic_y + 225
draw_rounded_rect(draw, (card_margin, resistance_y, width-card_margin, resistance_y+195), 25, colors['light_green'], width=3)

draw_emoji_circle(draw, (card_margin+70, resistance_y+55), 35, "💪", colors['green'])
draw_text_left(draw, "抗阻运动（辅助）", (card_margin+125, resistance_y+38), font_subtitle, colors['dark'])
draw_text_left(draw, "📅 频率：2-3 天/周（非连续日）", (card_margin+50, resistance_y+95), font_body, colors['dark'])
draw_text_left(draw, "🏋️ 强度：40-50% 1RM | RPE 11-12", (card_margin+50, resistance_y+130), font_small, colors['dark'])
draw_text_left(draw, "🔢 动作：8-10 个 | 每动作 1-2 组×10-15 次", (card_margin+50, resistance_y+165), font_small, colors['dark'])

# Flexibility & Balance card
balance_y = resistance_y + 225
draw_rounded_rect(draw, (card_margin, balance_y, width-card_margin, balance_y+155), 25, colors['light_blue'], width=3)

draw_emoji_circle(draw, (card_margin+70, balance_y+45), 35, "🧘", colors['blue'])
draw_text_left(draw, "柔韧性与平衡训练", (card_margin+125, balance_y+28), font_subtitle, colors['dark'])
draw_text_left(draw, "🤸 柔韧：≥2 天/周 | 每次 10-15 分钟", (card_margin+50, balance_y+80), font_small, colors['dark'])
draw_text_left(draw, "⚖️ 平衡：≥3 天/周（单脚站立、太极拳、八段锦）", (card_margin+50, balance_y+115), font_small, colors['dark'])

# ============ WEEKLY PLAN ============
weekly_y = balance_y + 185
draw_text_centered(draw, "📅 每周运动计划", (width//2, weekly_y), font_large, colors['dark'])

# Week cards
week1_y = weekly_y + 60
week1_x = card_margin
week1_w = width//2 - 35
week1_h = 165

# Week 1-2
draw_rounded_rect(draw, (week1_x, week1_y, week1_x+week1_w, week1_y+week1_h), 25, colors['light_orange'], width=3)
draw_text_left(draw, "第 1-2 周：适应期", (week1_x+20, week1_y+18), font_body, colors['dark'])
draw.line([(week1_x+20, week1_y+52), (week1_x+week1_w-20, week1_y+52)], fill=colors['orange'], width=2)
draw_text_left(draw, "周一/三/五：快走 20 分 🚶", (week1_x+20, week1_y+65), font_small, colors['dark'])
draw_text_left(draw, "周二：抗阻训练 💪", (week1_x+20, week1_y+98), font_small, colors['dark'])
draw_text_left(draw, "周六：太极拳 30 分 ☯️", (week1_x+20, week1_y+131), font_small, colors['dark'])

# Week 3-4
week2_x = width//2 + 15
draw_rounded_rect(draw, (week2_x, week1_y, week2_x+week1_w, week1_y+week1_h), 25, colors['light_green'], width=3)
draw_text_left(draw, "第 3-4 周：进展期", (week2_x+20, week1_y+18), font_body, colors['dark'])
draw.line([(week2_x+20, week1_y+52), (week2_x+week1_w-20, week1_y+52)], fill=colors['green'], width=2)
draw_text_left(draw, "周一/三/五：快走 30 分 🚶", (week2_x+20, week1_y+65), font_small, colors['dark'])
draw_text_left(draw, "周二/六：抗阻训练 💪", (week2_x+20, week1_y+98), font_small, colors['dark'])
draw_text_left(draw, "周四：太极拳 30 分 ☯️", (week2_x+20, week1_y+131), font_small, colors['dark'])

# ============ SAFETY TIPS ============
safety_y = week1_y + week1_h + 35
draw_rounded_rect(draw, (card_margin, safety_y, width-card_margin, safety_y+255), 25, '#FFF5F5', width=3)

draw_emoji_circle(draw, (card_margin+55, safety_y+45), 30, "⚠️", colors['red'])
draw_text_left(draw, "安全注意事项", (card_margin+105, safety_y+30), font_subtitle, colors['red'])

safety_items = [
    ("🩸", "运动前血糖：5.6-13.9 mmol/L", colors['dark']),
    ("🍬", "随身携带快速升糖食物", colors['dark']),
    ("👟", "选择合适的运动鞋和袜子", colors['dark']),
    ("🛑", "出现胸痛/头晕立即停止", colors['red']),
    ("🦶", "运动前后检查足部", colors['dark']),
]

for i, (emoji, text, color) in enumerate(safety_items):
    item_y = safety_y + 95 + i*48
    draw_text_left(draw, f"{emoji} {text}", (card_margin+50, item_y), font_small, color)

# ============ FOOTER ============
footer_y = safety_y + 305
draw_text_centered(draw, "🔄 第 4 周末复评", (width//2, footer_y), font_body, colors['gray'])
draw_text_centered(draw, "运动康复小南 制定", (width//2, footer_y+40), font_small, colors['gray'])
draw_text_centered(draw, "依据：《临床运动处方实践专家共识（2025）》", (width//2, footer_y+78), font_small, colors['gray'])

# Decorative bottom wave
for i in range(60):
    alpha = int(i * 1.5)
    color = (255, 140, 66, alpha)
    draw.polygon([(0, height-80+i), (width, height-100+i), (width, height), (0, height)], fill=color)

# Save the image
img.save('/Users/liyn/Downloads/运动康复小南/海报设计/糖尿病运动处方海报.png', 'PNG')
print("Enhanced poster created successfully!")
