# py C:/Jen/run_blender.py C:/Jen/test.blend CUBE [0,0,0,1] JPEG
import subprocess, os
import platform, socket, re, uuid, json, psutil, logging
from sys import argv

script, scene_path, object_type, material_color, image_output_format = argv


def getinputinfo():
    """
    put sys.argv parameters in dict()
    """
    input_info = dict()
    input_info['scene-path'] = scene_path
    input_info['object-type'] = object_type
    input_info['material-color'] = [float(el) for el in material_color.strip('[]').split(',')]
    input_info['image-output-format'] = image_output_format
    return input_info


if image_output_format == 'jpg':
    image_output_format = 'JPEG'
if image_output_format == 'png':
    image_output_format = 'PNG'

img_path = os.path.join(os.path.abspath('.'), 'render_img')
console_output = os.path.join(os.path.abspath('.'), 'log.txt')
log_output = os.path.join(os.path.abspath('.'), 'blender_log.txt')

subprocess.call(f'blender -b {scene_path} -o {img_path} -F {image_output_format} \
                --debug \
                -P C:\\Jen\\BlenderScript.py -- {object_type} {material_color} > {console_output}', shell=True)

with open(console_output, "r") as f:
    rend_time_info = dict()
    rend = re.findall(r'Time: (\d\d:\d\d.\d\d)', f.read())
    if len(rend) > 0:
        rend_time_info['rend-time'] = rend[0]
    else:
        rend_time_info['rend-time'] = None


def getsysteminfo():
    """
    put computer specifications in dict()
    """
    try:
        sys_info = dict()
        sys_info['platform'] = platform.system()
        sys_info['platform-release'] = platform.release()
        sys_info['platform-version'] = platform.version()
        sys_info['architecture'] = platform.machine()
        sys_info['hostname'] = socket.gethostname()
        sys_info['ip-address'] = socket.gethostbyname(socket.gethostname())
        sys_info['mac-address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        sys_info['processor'] = platform.processor()
        sys_info['ram'] = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        return sys_info
    except Exception as e:
        logging.exception(e)


with open("run_blender_result.json", "w") as f:
    json.dump([getsysteminfo(), getinputinfo(), rend_time_info], f, indent=4, sort_keys=True)

print('run_blender.py completed')
