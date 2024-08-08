
from controller import DistroReleaseCheck
from flask import render_template

def distro_data():
    distro_data = DistroReleaseCheck()

    context = distro_data.os_info_json
    return render_template('index.html',**context)