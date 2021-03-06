from __future__ import division
from itertools import chain
import numpy as np
import pandas as pd
import re
import collections
import math
from percept.tasks.base import Task
from percept.fields.base import Complex, List, Dict, Float
from inputs.inputs import SportsFormats
from percept.utils.models import RegistryCategories, get_namespace
from percept.conf.base import settings
import os
from percept.tasks.train import Train
from sklearn.ensemble import RandomForestClassifier
import pickle
import random
import sqlite3
from pandas.io import sql
from collections import namedtuple


import logging
log = logging.getLogger(__name__)

MAX_FEATURES = 500
DISTANCE_MIN=1
CHARACTER_DISTANCE_MIN = .2
RESET_SCENE_EVERY = 5

def make_df(datalist, labels, name_prefix=""):
    df = pd.DataFrame(datalist).T
    if name_prefix!="":
        labels = [name_prefix + "_" + l for l in labels]
    labels = [l.replace(" ", "_").lower() for l in labels]
    df.columns = labels
    df.index = range(df.shape[0])
    return df

row_types = ["id","info","start","play","sub","data"]

class ProcessGames(Task):
    data = Complex()
    row_data = List()
    speaker_code_dict = Dict()
    speaker_codes = List()
    vectorizer = Complex()

    data_format = SportsFormats.dataframe

    category = RegistryCategories.preprocessors
    namespace = get_namespace(__module__)

    help_text = "Process sports events."

    def train(self, data, target, **kwargs):
        """
        Used in the training phase.  Override.
        """
        self.data = self.predict(data, **kwargs)

    def predict(self, data, **kwargs):
        """
        Used in the predict phase, after training.  Override
        """

        con = sqlite3.connect(settings.DB_PATH)
        c = con.cursor()
        rosters = sql.read_frame("select * from rosters",con)

        tys = []
        for i in xrange(0,rosters.shape[0]):
            year = rosters.iloc[i]['year']
            team = rosters.iloc[i]['team']
            ty = [year,team]
            if ty not in tys:
                tys.append(ty)

        for ty in tys:
            year,team = ty
            ros = rosters[((rosters['year']==year) & (rosters['team']==team))]
            players = list(ros['id'])


        return data