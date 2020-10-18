import pandas as pd
import numpy as np
import requests
from tqdm import tqdm
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)


df = pd.read_csv('peer_groups.csv', delimiter=';')
df