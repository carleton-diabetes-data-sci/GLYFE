This folder was created by Erin Watson
(aka _not_ original to De Bois's code) 
to store all outputs from experiments.
This includes plots, results tables and 
terminal outputs.

Each experiment should get a separate subdataset 
so that it stands on its own. 

# Instructions for creating new experiment subdatasets

Go into `/data/datasets` on Gray, this is the shared 
folder where everything is maintained. You should see `GLYFE`
as one of the directories, go there in the command line. 

Make sure that you have a working installation of datalad 
(including git annex). If you're unsure, ask Dave if the 
current method is conda environments, docker containers,
or something else.

See [https://docs.google.com/document/d/1QMlu_VAbRksTsD5c5EauMxsWw7LelWhHhMAd3yiw1GA/edit?usp=sharing]
for another set of these instructions.

1. If you tried running the code and came here because it raised an Exception, go delete that folder that was created in `experiments`, it should be empty, because your code didn't run.
2. When you're in GLYFE in the terminal, run `datalad create -d . -D "Shared experiment for first run of Tidepool data through GLYFE on Gray" experiments/first_tidepool`
3. Check that this worked by running `datalad subdatasets` and look for your new dataset.
4. Now, you can go back to your local copy of GLYFE, but you'll need to run `datalad update --how merge` 