import luigi
import os
import shutil
import subprocess
import lxml.etree
import time

os.environ["GBM_TRIGGER_DATA_DIR"] = "./"
from morgoth.trigger import parse_trigger_file_and_write, OpenGBMFile
from morgoth.reports import CreateAllPages
from morgoth.downloaders import DownloadTrigdat
from morgoth.utils.package_data import get_path_of_data_file
from morgoth.handler import form_morgoth_cmd_string
from morgoth.configuration import morgoth_config

for i in range(3):

    v = f"v0{i}"
    morgoth_config["download"]["trigdat"][v]["max_time"] = 10

morgoth_config["luigi"]["n_workers"] = 2


def test_parse_trigger(grb1):

    assert luigi.build(
        [OpenGBMFile(grb=grb1)], local_scheduler=False, scheduler_host="localhost"
    )


def test_auto_pipe(grb1, grb2):

    cmd = form_morgoth_cmd_string(grb1)

    subprocess.Popen(cmd)

    time.sleep(5)

    cmd = form_morgoth_cmd_string(grb2)

    subprocess.Popen(cmd)

    time.sleep(60 * 3)

    # shutil.rmtree(grb)

    # shutil.rmtree(grb2)


# def test_multi_pipeline():

#     ff = get_path_of_data_file("gbm_flt.xml")
#     with open(ff, "r") as f:
#         root = lxml.etree.parse(f)

#     grb = parse_trigger_file_and_write(root)


#     thread1 = threading.Thread(target=go,args=(grb,))
#     thread1.daemon =True
#     thread1.start()
#     # luigi.build(
#     #     [CreateAllPages(grb_name=grb)],
#     #     local_scheduler=False,
#     #     scheduler_host="localhost",
#     #     workers=4,
#     # )

#     ff = get_path_of_data_file("gbm_flt2.xml")
#     with open(ff, "r") as f:
#         root = lxml.etree.parse(f)

#     grb = parse_trigger_file_and_write(root)

#     thread2 = threading.Thread(target=go,args=(grb,))
#     thread2.daemon = True
#     thread2.start()

#     time.sleep(2*60)
#     # luigi.build(
#     #     [CreateAllPages(grb_name=grb)],
#     #     local_scheduler=False,
#     #     scheduler_host="localhost",
#     #     workers=4,
#     # )
