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

**If you're planning on continuing to work on code while running and experiment**
Clone a new copy of GLYFE somewhere else in your account on Gray. Modifying the code 
actually modifies what is used to run things because of our silly bash scripts. 
See the general README for slightly more details. I named these new folders 
`isol_repos/exp_name` to remind myself that they need to stay isolated and which experiment 
it was. For instructions, see Getting Started in Datalad Instructions in the shared drive. 
I've also found it convenient to make a new branch (just using git, no fancy datalad stuff) 
to help make pushing and merging easier once the experiement is wrapping up. 

1. If you tried running the code and came here because it raised an Exception, go delete that folder that was created in `experiments`, it should be empty, because your code didn't run.
2. When you're in GLYFE in the terminal, run (replace "my_exp_name with your experiment name") `datalad create -d . -D "Shared experiment for first run of Tidepool data through GLYFE on Gray" experiments/my_exp_name`
3. Check that this worked by running `datalad subdatasets` and look for your new dataset. Also refresh the file tree in VSCode (little button that appears when you hover on the bar that says "DATA [SSH: GRAY.MATHCS.CARLETON.EDU]) to make sure your experiment appeared in the experiments folder.
4. Update the `.gitattributes` file in the root of this new experiment dataset to look like the `gitattributes` file in other experiments. Then, at GLYFE in the terminal, run `datalad save -r -m "Correct .gitattributes file in experiment subdataset"` 
5. In the terminal, **at the root of your new dataset**, run `git config receive.denyCurrentBranch updateInstead` so that this subdataset can receive pushes without getting grumpy.
6. If you're about to run your experiment _right now_, go write down log information in `EXPERIMENT_LOG.md`. Then save again: `datalad save -r -m "Recorded experiment log information for my_exp_name"`
7. Now, you can go back to your local copy of GLYFE, but you'll need to run `datalad update -r --how merge` so that your local copies knows there's a new experiment, and `datalad get experiments/my_exp_name` to actually bring it in.