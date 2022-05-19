import os

import pandas as pd
import geopandas as gpd
import fiona

from camels_serv import EZG_DIR, INPUT_DIR, OUTPUT_DIR


class ProcessState:
    def __init__(self, input_dir: str = None, output_dir: str = None, ezg_dir: str = None) -> None:
        """
        Process State instance to describe current state of CAMELS-DE processing.
        """
        # input
        if input_dir is None:
            self.input_dir = INPUT_DIR
        elif not os.path.exists(input_dir):
            raise OSError(f'{input_dir} does not exist')
        else:
            self.input_dir = input_dir
        
        # output dir
        if output_dir is None:
            self.output_dir = OUTPUT_DIR
        elif not os.path.exists(output_dir):
            raise OSError(f'{output_dir} does not exist')
        else:
            self.output_dir = output_dir
        
        # ezg dir
        if ezg_dir is None:
            self.ezg_dir = EZG_DIR
        elif not os.path.exists(ezg_dir):
            raise OSError(f'{ezg_dir} does not exist')
        else:
            self.ezg_dir = ezg_dir

        # set the path to pegel file
        self.pegel_file = os.path.join(self.ezg_dir, 'pegel.csv')

        # load the pegel file
        self.pegel = self.load_pegel()
    
    def load_pegel(self) -> gpd.GeoDataFrame:
        """
        Return the current pegel file
        """
        # read in the data
        df = pd.read_csv(self.pegel_file)
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x, df.y))

        return gdf

    def load_ezgs(self) -> gpd.GeoDataFrame:
        """
        Scan the EZGs folder for valid geospatial files and match the
        names in the pegel file
        """
        # get all files
        gdf = gpd.GeoDataFrame()

        for file_name in os.listdir(self.ezg_dir):
            _, extension = os.path.splitext(file_name)
            if extension in fiona.supported_drivers:
                right = gpd.read_file(os.path.join(self.ezg_dir, file_name))
                gdf = gpd.GeoDataFrame(pd.concat([gdf, right]))
        return gdf

    def has_output(self) -> gpd.GeoDataFrame:
        """
        Return the pegel GeoDataFrame enhanced with info about existing output
        """
        # go for each name
        has_out = [os.path.exists(os.path.join(self.output_dir, name)) for name in self.pegel.name]

        # add the info
        self.pegel['has_output'] = has_out

        return self.pegel
    
    def has_discharge(self) -> gpd.GeoDataFrame:
        """
        Check if there is an 'discahrge.csv' file in the output folder
        """
        # go for each folder
        has_dis = [os.path.exists(os.path.join(self.output_dir, name, 'discharge*')) for name in self.pegel.name]

        # add the info
        self.pegel['has_discharge'] = has_dis
        
    def describe(self) -> gpd.GeoDataFrame:
        """
        Return a described GeoDataFrame for all pegel.
        """
        # add output
        gdf = self.has_output()

        return gdf
    