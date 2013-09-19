#!/bin/bash

echo 'generating train data'
python output_train_rating_libfm.py 

echo 'generating test data'
python output_test_rating_libfm.py 

echo 'done'
