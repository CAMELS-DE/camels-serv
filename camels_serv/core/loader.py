import os

import pandas as pd
import geopandas as gpd

from camels_serv.core import config


class BaseLoader:
    def __init__(self, output_dir: str = config.BASEPATH) -> None:
        """
        BaseLoader instance to read the data on disk
        """
        # save the base path
        self.base_path = os.path.abspath(output_dir)

        # derive all paths from the BASEPATH
        self.metadata_path = os.path.join(self.base_path, 'metadata')

        # create the filename template. This can be changed if there
        # are optionally more output structures
        self.filename_template = "{camels_id}_data.csv"

        
        # automatically load metadata
        self.metadata = self.load_metadata()

    def load_metadata(self) -> gpd.GeoDataFrame:
        """
        Load metadata and transform to geodata
        """
        # build the fname
        fname = os.path.join(self.metadata_path, config.METADATA_FILE_NAME)
        df = pd.read_csv(fname)
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y), crs=3035).to_crs(epsg=4326)
        
        return gdf
