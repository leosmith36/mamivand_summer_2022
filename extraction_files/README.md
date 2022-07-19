# Extraction files

These are the files used for extraction the PNG microstructure images from Exodus files generated with MOOSE. The extraction process utilizes Paraview, which is compatible with Windows (whereas Peacock is not).

The combine.py file is used to conglomerate all of the "microstructure_data" folders into one "data" folder, which can then be used as the main input for machine learning models.