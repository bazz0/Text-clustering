import logging
import os
import numpy as np
import Levenshtein
import sklearn.cluster

# Reads and returns the list of files from a directory
def read_directory(mypath):
    current_list_of_files = []

    while True:
        for (_, _, filenames) in os.walk(mypath):
            current_list_of_files = filenames
        logging.info("Reading the directory for the list of file names")
        return current_list_of_files


# Function you will be working with
def creating_subclusters(list_of_terms, name_of_file,path):
    # Your code that converts the cluster into subclusters and saves the output in the output folder with the same name as input file
    # Note the writing to file has to be handled by you.
    words=list_of_terms
    lev_similarity = -1 * np.array([[Levenshtein.distance(w1, w2) for w1 in words] for w2 in words])
    affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(lev_similarity)

    clust=[]
    for cluster_id in np.unique(affprop.labels_):
        exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(words[np.nonzero(affprop.labels_ == cluster_id)])
        cluster_str = ", ".join(cluster)
        clust.append(cluster_str)
    with open(os.path.join(path, name_of_file), "w") as f:
        for i in clust:
            f.write(i)
            f.write('\n')

    pass


# Main function
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

    # Folder where the input files are present
    mypath = "G:/a/parabole-internship-test-py3/input"
    path="G:/a/parabole-internship-test-py3/output"
    list_of_input_files = read_directory(mypath)
    for each_file in list_of_input_files:
        with open(os.path.join(mypath, each_file), "r") as f:
            file_contents = f.read()
        list_of_term_in_cluster = file_contents.split()

        # Sending the terms to be converted to subclusters in your code
        creating_subclusters(list_of_term_in_cluster, each_file,path)


        # End of code