from postprocessing.results import ResultsSubject
from postprocessing.postprocessing import postprocessing
from preprocessing.preprocessing import preprocessing
import sys
import argparse
from os.path import join
from misc.utils import locate_model, locate_params, locate_search
import misc.constants as cs
from misc.utils import printd
from processing.cross_validation import make_predictions, find_best_hyperparameters
import os
from pathlib import Path

""" This is the source code the benchmark GLYFE for glucose prediction in diabetes.
    For more infos on how to use it, go to its Github repository at: https://github.com/dotXem/GLYFE """


def main(dataset, subject, model, params_name, exp, mode, log, ph, plot):
    printd(dataset, subject, model, params_name, exp, mode, log, ph, plot)

    # retrieve model's parameters
    model_class = locate_model(model)
    search = locate_search(params_name)
    params = locate_params(params_name)
    

    # scale variables in minutes to the benchmark sampling frequency
    ph_f = ph // cs.freq
    hist_f = params["hist"] // cs.freq
    day_len_f = cs.day_len // cs.freq

    """ PREPROCESSING """
    train, valid, test, scalers = preprocessing(dataset, subject, ph_f, hist_f, day_len_f)
    """ MODEL TRAINING & TUNING """
    if search:
        params = find_best_hyperparameters(subject, model_class, params, search, ph_f, train, valid, test)

    raw_results = make_predictions(subject, model_class, params, ph_f, train, valid, test, mode=mode)
    """ POST-PROCESSING """
    raw_results = postprocessing(raw_results, scalers, dataset)

    """ EVALUATION """
    results = ResultsSubject(model, exp, ph, dataset, subject, params=params, results=raw_results)
    printd(results.compute_results())
    if plot:
        dir = os.path.join(cs.path, "plots", params_name, exp, "ph-" + str(ph))
        Path(dir).mkdir(parents=True, exist_ok=True)
        if mode == 'valid':
            file_path = os.path.join(dir, dataset + "_" + subject + "_valid.png")
            results.plot(file_path, 0)
        if mode == 'test':
            for day in range(10): # hard coded for the ohio dataset
                file_path = os.path.join(dir, dataset + "_" + subject + "_test_" + str(day) + ".png")
                results.plot(file_path, day)



if __name__ == "__main__":
    """ The main function contains the following optional parameters:
            --dataset: which dataset to use, should be referenced in misc/datasets.py;
            --subject: which subject to use, part of the dataset, use the spelling in misc/datasets.py;
            --model: model on which the benchmark will be run (e.g., "svr"); need to be lowercase; 
            --params: parameters of the model, usually has the same name as the model (e.g., "svr"); need to be lowercase; 
            --ph: the prediction horizon of the models; default 30 minutes;
            --exp: experimental folder in which the data will be stored, inside the results directory;
            --mode: specify is the model is tested on the validation "valid" set or testing "test" set ;
            --plot: if a plot of the predictions shall be made at the end of the training;
            --log: file where the standard outputs will be redirected to; default: logs stay in stdout; 
            
        Example:
            python main.py --dataset=ohio --subject=559 --model=base --params=base --ph=30 
                        --exp=myexp --mode=valid --plot=1 --log=mylog
    """

    """ ARGUMENTS HANDLER """
    # retrieve and process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--subject", type=str)
    parser.add_argument("--model", type=str)
    parser.add_argument("--params", type=str)
    parser.add_argument("--ph", type=int)
    parser.add_argument("--exp", type=str)
    parser.add_argument("--mode", type=str)
    parser.add_argument("--plot", type=int)
    parser.add_argument("--log", type=str)
    args = parser.parse_args()

    # compute stdout redirection to log file
    if args.log:
        sys.stdout = open(join(cs.path, "logs", args.log + ".log"), "w")

    # README said default params name to model name
    if not args.params:
        args.params = args.model

    main(log=args.log,
         subject=args.subject,
         model=args.model,
         ph=args.ph,
         params_name=args.params,
         exp=args.exp,
         dataset=args.dataset,
         mode=args.mode,
         plot=args.plot)
