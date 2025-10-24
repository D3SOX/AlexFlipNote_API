from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('battery', __name__)


def create_battery_icon(charging: bool, percentage: int):

    full_battery_width = 392
    top_corner = (37, 37)
    bottom_max = (37+full_battery_width*(percentage/100), 205)

    if percentage <= 20:
        background_color = (255, 0, 0)
    elif charging:
        background_color = (52, 199, 89)
    else:
        background_color = (255, 255, 255)

    battery_background = Image.open("assets/battery/battery.png")

    draw = ImageDraw.Draw(battery_background)
    draw.rounded_rectangle([top_corner, bottom_max], radius=35, fill=background_color)

    bio = BytesIO()
    battery_background.save(bio, "PNG")
    bio.seek(0)
    return bio


@blueprint.route('/battery/ios')
async def battery_ios():
    """?pct=number&charging=truefalse"""
    percentage = request.args.get('pct')
    charging = request.args.get('charging') == "true"

    try:
        percentage = int(percentage)
    except (ValueError, TypeError):
        abort(400, "Invalid percentage value. It must be an integer.")

    if percentage < 20:
        percentage = 20
    return await send_file(
        create_battery_icon(charging, percentage),
        mimetype='image/png',
        attachment_filename='battery.png'
    )
