import os
from run_paraview import run
from get_results import get_df
from results_filter import filter_images
import shutil
from nonconverge import get_fails

# This script gets all of the output files from output_files and generates images and csv files from them
# To extract the files, this is the "main" file that you should run with the following files in the same
# directory: get_results.py, nonconverge.py, results_filter.py, and run_paraview.py

def main():
    # The current working directory (change this to the directory of this script)
    wd = os.path.join(os.getcwd())

    # The folder containing the output file directories
    folder = os.path.join(wd,"output_files")

    # The folder containing all microstructure data
    data = os.path.join(wd,"microstructure_data")

    # The folder where the images will go
    image_folder = os.path.join(data,"images")

    # The folder where the results spreadsheet will go
    results_folder = os.path.join(data,"results")

    if os.path.exists(data):
        shutil.rmtree(data)

    os.mkdir(data)
    os.mkdir(image_folder)
    os.mkdir(results_folder)

    all_dirs = os.listdir(folder)
    files = []
    names = []
    csvs = []
    csvnames = []
    ifiles = []
    inames = []
    for dir in all_dirs:
        if dir.startswith("run_"):
            all_files = os.listdir(os.path.join(folder,dir))
            csv = False
            inputfile = None
            for file in all_files:
                if file.endswith("_exodus.e"):
                    files.append(os.path.join(folder,dir,file))
                    names.append(file)
                    csv = True
                    inputfile = None
                if file.endswith(".csv") and file.startswith("FeCrCo"):
                    csvs.append(os.path.join(folder,dir,file))
                    csvnames.append(file)
                    csv = True
                    inputfile = None
                if not csv:
                    if file.startswith("FeCrCo") and file.endswith(".i"):
                        inputfile = file
            if inputfile != None:
                ifiles.append(inputfile)
                inames.append(os.path.basename(inputfile))

    for i in range(len(files)):
        file = files[i]
        name = names[i]
        img_name = "%s.png" %name[:-9]
        get_df(csvnames[i],csvs[i],results_folder,img_name)
        run(file,name,image_folder,img_name)
    for i in range(len(ifiles)):
        get_fails(inames[i],results_folder)
    filter_images(data)
    
if __name__ == "__main__":
    main()

        
