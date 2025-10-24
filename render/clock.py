import math
import random

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from quart import Blueprint, request, send_file, abort, jsonify

blueprint = Blueprint('clock', __name__)


def create_clock(hour, minute, second):

    bg_image = Image.open(f"assets/clock/clockface_whitebg.png")

    width, height = bg_image.size

    # Calculate center
    center_x = width // 2
    center_y = height // 2

    # Create a drawing object
    draw = ImageDraw.Draw(bg_image)

    is_am = hour < 12
    am_pm_text = "AM" if is_am else "PM"
    font_size = int(height * 0.2)
    try:
        font = ImageFont.truetype("assets/_fonts/Arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    bbox = font.getbbox(am_pm_text)
    text_width, text_height = int(bbox[2] - bbox[0]), int(bbox[3] - bbox[1])
    draw.text((center_x - text_width / 2, center_y + 55), am_pm_text, fill=(0, 0, 0), font=font)

    # Define lengths and colors for clock hands
    hour_hand_length = min(center_x, center_y) * 0.45
    minute_hand_length = min(center_x, center_y) * 0.70
    second_hand_length = min(center_x, center_y) * 0.8

    hour_hand_color = (72, 72, 72)  # Brownish color for a wooden look
    minute_hand_color = (72, 72, 72)  # Dark Gray
    second_hand_color = (200, 40, 40)  # Deep Red

    # Calculate angles
    hour_angle = math.radians(30 * (hour % 12 + minute / 60))
    minute_angle = math.radians(6 * minute)
    second_angle = math.radians(6 * second) if second is not None else None

    # Draw hour hand
    hour_x = center_x + hour_hand_length * math.sin(hour_angle)
    hour_y = center_y - hour_hand_length * math.cos(hour_angle)
    draw.line([(center_x, center_y), (hour_x, hour_y)], fill=hour_hand_color, width=30, joint="curve")

    # Draw minute hand
    minute_x = center_x + minute_hand_length * math.sin(minute_angle)
    minute_y = center_y - minute_hand_length * math.cos(minute_angle)
    draw.line([(center_x, center_y), (minute_x, minute_y)], fill=minute_hand_color, width=20, joint="curve")

    # Optionally draw second hand
    if second is not None:
        second_x = center_x + second_hand_length * math.sin(second_angle)
        second_y = center_y - second_hand_length * math.cos(second_angle)
        draw.line([(center_x, center_y), (second_x, second_y)], fill=second_hand_color, width=15, joint="curve")




    bio = BytesIO()
    bg_image.save(bio, "PNG", optimize=True)
    bio.seek(0)
    return bio


@blueprint.route("/clock")
async def clock():
    """?h=XX&m=XX[&s=XX]"""
    ha = request.args.get("h")
    ma = request.args.get("m")
    sa = request.args.get("s")
    if ha is None:
        return abort(400, "h argument is missing")
    if ma is None:
        return abort(400, "m argument is missing")
    try:
        hour = int(ha)
        minute = int(ma)
        second = int(sa) if sa is not None else sa
    except ValueError:
        abort(400, "At least one argument (h, m, or s) is not a number.")
        return

    if hour > 23:
        abort(400, "Hour can only be from 0-23")

    if minute > 59:
        abort(400, "Minute can only be from 0-59")

    if second is not None and second > 59:
        abort(400, "Second can only be from 0-59")


    return await send_file(
        create_clock(hour, minute, second),
        mimetype="image/png",
        attachment_filename="clock.png"
    )
