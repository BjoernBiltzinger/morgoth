import luigi
import os
from morgoth.utils.download_file import BackgroundDownload
from morgoth.trigger import OpenGBMFile, GBMTriggerFile
from morgoth.configuration import morgoth_config

base_dir = os.environ.get("GBM_TRIGGER_DATA_DIR")


class DownloadTrigdat(luigi.Task):
    grb_name = luigi.Parameter()
    version = luigi.Parameter()
    # uri = luigi.Parameter()

    def requires(self):

        return OpenGBMFile(grb=self.grb_name)

    def output(self):

        trigdat = f"glg_trigdat_all_bn{self.grb_name[3:]}_{self.version}.fit"
        return luigi.LocalTarget(os.path.join(base_dir, self.grb_name, trigdat))

    def run(self):

        info = GBMTriggerFile.from_file(self.input())

        print(info)

        trigdat = f"glg_trigdat_all_bn{self.grb_name[3:]}_{self.version}.fit"

        print(trigdat)

        uri = os.path.join(info.uri, trigdat)

        print(uri)
        store_path = os.path.join(base_dir, info.name)
        dl = BackgroundDownload(
            uri,
            store_path,
            wait_time=morgoth_config["download"]["trigdat"][self.version]["interval"],
            max_time=morgoth_config["download"]["trigdat"][self.version]["max_time"],
        )
        dl.run()


class DownloadTTEFile(luigi.Task):
    grb_name = luigi.Parameter()
    version = luigi.Parameter(default="v00")
    detector = luigi.Parameter()

    def requires(self):

        return OpenGBMFile(grb=self.grb_name)

    def output(self):

        tte = f"glg_tte_{self.detector}_bn{self.grb_name[3:]}_{self.version}.fit"
        return luigi.LocalTarget(os.path.join(base_dir, self.grb_name, tte))

    def run(self):

        info = GBMTriggerFile.from_file(self.input())

        print(info)

        tte = f"glg_tte_{self.detector}_bn{self.grb_name[3:]}_{self.version}.fit"

        uri = os.path.join(info.uri, tte)
        print(uri)

        store_path = os.path.join(base_dir, info.name)
        dl = BackgroundDownload(
            uri,
            store_path,
            wait_time=morgoth_config["download"]["tte"][self.version]["interval"],
            max_time=morgoth_config["download"]["tte"][self.version]["max_time"],
        )
        dl.run()
