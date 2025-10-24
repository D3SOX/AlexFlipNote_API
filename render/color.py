from io import BytesIO
from PIL import Image
from quart import Blueprint, request, send_file, abort

blueprint = Blueprint('color', __name__)

def show_color(color, size):
    print(color)
    im = Image.new(mode="RGB", size=(size, size), color=f"#{color}")
    bio = BytesIO()
    im.save(bio, format='PNG')
    bio.seek(0)
    return bio

@blueprint.route('/color')
async def color():
    """?color=hex&size=size"""
    color = request.args.get('color')
    if color is None:
        abort(400, "You must provide a hex color.")
    else:
        while len(color) < 6:
            color = '0' + color
        print(color)
        try:
            num_color = int(color, base=16)
        except ValueError:
            abort(400, "You did not provide a proper hex.")
        if num_color < 0 or num_color > 16777215:
            abort(400, "You did not provide a proper color hex.")
    size = request.args.get('size')
    if size is None:
        size = 100
    else:
        try:
            size = int(size)
        except ValueError:
            size = 100

    return await send_file(
        show_color(color, size),
        mimetype='image/png',
        attachment_filename=f'{color}.png'
    )
