import requests
from requests.auth import HTTPBasicAuth
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os
import datetime
import shutil
import json


try:
    f = open("config.json", "r")
    config = json.loads(f.read())
    f.close()
except:
    print("Error reading config file.")
    exit(1)

camera_ids = config["camera_ids"]
basicauth_user = config["basic_auth_user"]
basicauth_password = config["basic_auth_password"]
output_path = config["output_directory"]
capture_interval_s = config["capture_interval_s"]
start_hour_utc = config["start_hour_utc"]
stop_hour_utc = config["stop_hour_utc"]
print("camera_ids", camera_ids)
print("output_path", output_path)


def check_time_of_day():
    utc_time = datetime.datetime.utcnow()
    if (utc_time.hour >= start_hour_utc) and (utc_time.hour <= stop_hour_utc):
        return True
    else:
        return False


def get_image_from(camera_id):
    # print("Capturing from ", camera_id)
    url = "http://cam-" + camera_id + ".local:8080/?action=snapshot"
    utc_time = datetime.datetime.utcnow()
    filename = camera_id + "_" + utc_time.strftime("%Y-%m-%dT%H-%M-%SZ") + ".jpg"
    savepath = (
        output_path + camera_id + "/" + utc_time.strftime("%Y-%m-%d") + "/" + utc_time.strftime("%H") + "/" + filename
    )
    try:
        os.makedirs(
            os.path.dirname(savepath), exist_ok=True
        )  # create path if not exists
        r = requests.get(
            url, stream=True, auth=HTTPBasicAuth(basicauth_user, basicauth_password)
        )
        # print("Camera",camera_id,": status code=", r.status_code)
        if r.status_code == 200:
            with open(savepath, "wb") as out_file:
                shutil.copyfileobj(r.raw, out_file)
        else:
            print("Failed. Status code", r.status_code)
        return camera_id + " : " + str(r.status_code)
    except Exception as e:
        print(e)


def capture_all():
    futures = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for camera_id in camera_ids:
            futures.append(executor.submit(get_image_from, camera_id))

    for future in as_completed(futures):
        print(future.result())

while True:
    t0 = time.time()
    print(str(t0))
    if check_time_of_day():
        capture_all()
    d = time.time() - t0
    d = d % capture_interval_s
    time.sleep(capture_interval_s - d)
