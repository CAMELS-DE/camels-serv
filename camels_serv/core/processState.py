import os

import pandas as pd
import geopandas as gpd
import fiona

from camels_serv.core import config


class ProcessState:
    def __init__(self, output_dir: str = config.BASEPATH) -> None:
        """
        Process State instance to describe current state of CAMELS-DE processing.
        """
        # save the base path
        self.base_path = os.path.abspath(output_dir)

        # derive all paths from the BASEPATH
        self.metadata_path = os.path.join(self.base_path, 'metadata')

        
        # automatically load metadata
        self.metadata = self.load_metadata()

    def load_metadata(self) -> gpd.GeoDataFrame:
        """
        Load metadata and transform to geodata
        """
        # build the fname
        fname = os.path.join(self.metadata_path, config.METADATA_FILE_NAME)
        df = pd.read_csv(fname)
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y))
        
        return gdf


    def has_output(self, base_df: gpd.GeoDataFrame = None) -> gpd.GeoDataFrame:
        """
        Return the pegel GeoDataFrame enhanced with info about existing output
        """
        if base_df is None:
            # create a copy
            base_df = self.metadata.copy()

        # go for each name
        base_df['has_out'] = [os.path.exists(os.path.join(self.base_path, p)) for p in self.metadata.camels_path]

        return base_df
        
    def describe(self) -> gpd.GeoDataFrame:
        """
        Return a described GeoDataFrame for all pegel.
        """
        # add output
        gdf = self.has_output()

        return gdf
    