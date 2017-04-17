To conduct the motivation-overall section of the paper.

Step 1: Run the file create_file_cosine_sim.py - It will create a human readable file of all citer1 citer2 cited tuples and their citation context similarity uniquely by concatenation. This step is optional and takes very long to process. The final file will be downloaded if initial.py is run.

Step 2: Run the motivation_overall.py file to collate all the other data required for computing the muner of papers as the specific criterion in the paper, i.e, 5 or more citation context of which >=60% are copied exactly from somewhere else (CosSim=1). Results printed to STDOUT.
