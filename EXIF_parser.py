"""
/***************************************************************************
  EXIF_parser.py

  Python 3.x script that takes data from localized photos (in selected folder) and saves it to csv file (in that folder).
  One can open this csv file in QGIS as a point layer (set the Geometry CRS to EPSG:4326) and view the photos by road_inspection_viewer plugin.
  This script requires PyQT5 and exif modules.
  Photo files with .jpg or .jpeg extension.

  version: 0.1.2
  
  --------------------------------------
  Date : 04.12.2019
  Copyright: (C) 2019 by Piotr Michałowski
  Email: piotrm35@hotmail.com
/***************************************************************************
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as published
 * by the Free Software Foundation.
 *
 ***************************************************************************/
"""


import os, sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from exif import Image

		
#========================================================================================================

class EXIF_parser(QWidget):

    HEADER_TUPLE = ('lat', 'lon', 'time_stamp', 'file_names')


    def __init__(self):
        super().__init__()
        self.work()
        sys.exit()

    def work(self):
        try:
            geotagged_images_folder = str(QFileDialog.getExistingDirectory(self, "Select geotagged images folder:"))
            print(geotagged_images_folder)
            result_file_full_path = os.path.join(geotagged_images_folder, "QGIS_CSV_EPSG4326_" + time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime(time.time())) + ".csv")
            result_file = open(result_file_full_path, 'w')
            img_file_names = [f for f in os.listdir(geotagged_images_folder) if os.path.isfile(os.path.join(geotagged_images_folder, f)) and (os.path.splitext(f)[1].upper() == '.JPG' or os.path.splitext(f)[1].upper() == '.JPEG')]
            print(','.join(self.HEADER_TUPLE))
            result_file.write(','.join(self.HEADER_TUPLE) + '\n')
            for img_file_name in img_file_names:
                data_tuple = self.get_data_fom_image(os.path.join(geotagged_images_folder, img_file_name))
                if data_tuple:
                    print(','.join(data_tuple))
                    result_file.write(','.join(data_tuple) + '\n')
        except Exception as e:
            print('work Exception: ' + str(e))
        finally:
            result_file.close()

        
    def get_data_fom_image(self, image_path):
        try:
            with open(image_path, 'rb') as image_file:
                img = Image(image_file)
                img_lat_str = str(img.gps_latitude[0] + img.gps_latitude[1] / 60.0 + img.gps_latitude[2] / (60.0 * 60.0))
                img_lon_str = str(img.gps_longitude[0] + img.gps_longitude[1] / 60.0 + img.gps_longitude[2] / (60.0 * 60.0))
                time_stamp_str = img.datetime_original
                file_names = os.path.basename(image_path)
                return (img_lat_str, img_lon_str, time_stamp_str, file_names)
        except Exception as e:
            print('get_data_fom_image Exception: ' + str(e))
        return None


#========================================================================================================


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EXIF_parser()
    sys.exit(app.exec_())




