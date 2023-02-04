import os
import json

from camels_serv.core import config


class DatasetMetrics:
    def __init__(self, output_dir: str = config.BASEPATH) -> None:
        """
        BaseLoader instance to read the data on disk
        """
        # save the base path
        self.base_path = os.path.abspath(output_dir)

        # derive all paths from the BASEPATH
        self.metadata_path = os.path.join(self.base_path, 'metadata')
        self.metrics_folder = os.path.join(self.base_path, 'metrics')

    def list_metrics(self) -> list[dict]:
        """
        List all figure JSONs found in the diagnostics folder
        """
        files = {}
        for fname in os.listdir(self.metrics_folder):
            # check if this is noe
            if fname.endswith('.plotly.json') or fname.endswith('.description.json'):
                name, typ, ext = os.path.basename(fname).split('.')
                
                # check if the metric exists
                if name in files:
                    files[name][typ] = fname
                else:
                    files[name] = {'name': name, typ: fname}

        return list(files.values())

    def load_plotly_figure(self, name: str) -> dict:
        """"""
        return self._load_metric_resource(name, extension='plotly.json')

    def _load_metric_resource(self, name: str, extension: str = None) -> dict:
        # check if the name has already an extension
        if extension is not None and not name.endswith(extension):
            name = f"{name}.{extension}"
        
        # create the path
        path = os.path.join(self.metrics_folder, name)
        
        # search file
        if not os.path.exists(path):
            raise FileNotFoundError(f"The resource '{path}' was not found.")
        
        # import and return
        with open(path, 'r') as f:
            return json.load(f)
    
    def load_plotly_description(self, name: str) -> dict:
        """"""
        return self._load_metric_resource(name, extension='description.json')

