# Custom functions used for the wdss machine
# learning competition




# 'numpy' for array manipulation
import numpy as np

# 'matplotlib.pyplot' and 'seaborn' for graph plotting
import matplotlib.pyplot as plt
import seaborn as sns

# 'scipy.stats' for statistical functions
import scipy.stats

# 'pandas' for tabular data set manipulation
import pandas as pd

# 'datetime' for using 'datetime' data types
import datetime

import sklearn.preprocessing




# Define the 'index_reset' function

# Prerequisites:
# - None

def index_reset(
    dataframe,
):

    '''
    The 'index_reset' function cleanly resets the indexing of
    observations in a pandas dataframe.
    '''

    # 'dataframe_x_1' is 'dataframe' with a reset
    # index and an additional feature called 'index'
    dataframe_x_1 = dataframe.reset_index()

    # 'dataframe_x_f' is 'dataframe_x_1' with the
    # redundant 'index' feature removed
    dataframe_x_f = dataframe_x_1.drop(
        labels = 'index',
        axis = 1,
    )

    # Finally, return 'dataframe_x_f'
    return dataframe_x_f




# Define the 'bayesian_update' function

# Prerequisites:
# - None

def bayesian_update(
    float_x_t,
    vector_m_t_minus,
    matrix_b_t_minus,
    vector_phi,
    matrix_f,
    matrix_sigma,
    float_delta = 1,
    float_s_t_minus = 0,
    int_n_t_minus = 0,
):
    
    '''
    The 'bayesian_update' function carries out an
    optimal bayesian update for the hyperparameters
    of a dynamic linear model.
    '''

    # Create 'matrix_p', the pre-posterior weight matrix
    matrix_p = matrix_f @ matrix_b_t_minus @ matrix_f.T + matrix_sigma

    # Create 'float_q', the variance multiplier
    float_q = float_delta + vector_phi @ matrix_p @ vector_phi

    # Create 'vector_g', the gain vector
    vector_g = (matrix_p @ vector_phi) / float_q

    # Create 'float_e', the residual estimate
    float_e = float_x_t - vector_phi @ matrix_f @ vector_m_t_minus

    # Create 'vector_m_t', the posterior mean vector
    vector_m_t = matrix_f @ vector_m_t_minus + vector_g * float_e

    # Create 'matrix_b_t', the posterior weight matrix
    matrix_b_t = matrix_p / float_delta - np.outer(vector_g, vector_g) * float_q

    # Create 'int_n_t', the posterior sample size
    int_n_t = int_n_t_minus + 1

    # Create 'float_s_t', the posterior sample variance
    float_s_t = (float_delta / int_n_t) * (int_n_t_minus * float_s_t_minus + (float_e ** 2) / float_q)

    # Return all posterior data
    return (
        vector_m_t,
        matrix_b_t,
        int_n_t,
        float_s_t
    )




# Define the 'series_extender' function

# Prerequisites:
# - None

def series_extender(
    series_main,
    int_extension = 0,
):

    '''
    The 'series_extender' function extends an input
    series by the amount given if 'int_extension' is
    positive and shortens it if 'int_extension' is
    negative.

    When extending, new entries are equal to value of
    last valid entry in input series.

    When shortening, the series is cut off at the
    point that's -'int_extension' less than the
    length of the original series.
    '''

    # Create 'int_length', the length of the input
    # series for future reference
    int_length = len(series_main)

    # Check if 'int_extension' is zero
    if int_extension == 0:

        # Return the input series unchanged
        return series_main

    # Check if 'int_extension' is less than zero
    elif int_extension < 0:

        # Create 'int_cut', the index at which
        # 'series_main' is cut
        int_cut = int_length + int_extension

        # Cut 'series_main' to create 'series_main_f'
        series_main_f = series_main.iloc[: int_cut]

        # Return the shortened input series
        return series_main_f

    # Check if 'int_extension' is greater than zero
    elif int_extension > 0:

        # Create 'float_last_value', the value that
        # will be repeated throughout the extension
        float_last_value = series_main[int_length - 1]

        # Create 'vector_repeat', a vector containing
        # the repreats of 'float_last_value' with a
        # length of 'int_extension'
        vector_repeat = np.repeat(
            a = float_last_value,
            repeats = int_extension,
        )

        # Create 'series_repeat' by converting
        # 'vector_repeat' into a pandas series
        series_repeat = pd.Series(
            data = vector_repeat,
        )

        # Finally, append 'series_repeat' to
        # 'series_main' to extend it to create
        # 'series_main_f'
        series_main_f = series_main.append(
            to_append = series_repeat,
            ignore_index = True,
        )

        # Return the extended input series
        return series_main_f




# Define the 'arma_hyperpar_ext' function

# Prerequisites:
# - None

def arma_hyperpar_ext(
    int_ar_terms,
    tuple_hyperpar,
):

    '''
    The 'arma_hyperpar_ext' function adds to the
    tuple of hyperparameters for a DLM the necessary
    terms to include a non-dynamic autoregressive 
    model.

    The number of autoregressive terms added is
    equal to 'int_ar_terms'.
    '''

    # Create 'vector_zeros', the zero vector that
    # would be appeded to the prior mean
    vector_zeros = np.zeros(
        shape = int_ar_terms,
    )

    # Create 'matrix_zeros', the zero matrix that
    # would be appended to 'matrix_sigma'
    matrix_zeros = np.zeros(
        shape = (
            int_ar_terms,
            int_ar_terms
        ),
    )

    # Create 'matrix_unit_diag', the identity
    # matrix that would be appened to both the
    # weight matrix prior and 'matrix_f'
    matrix_unit_diag = np.eye(
        N = int_ar_terms,
    )

    # Create the updated prior mean vector
    vector_m_f = np.append(
        arr = tuple_hyperpar[0],
        values = vector_zeros,
    )

    # Create the updated prior weight matrix
    matrix_b_f = scipy.linalg.block_diag(
        tuple_hyperpar[1],
        0.5 * matrix_unit_diag,
    )

    # Create the updated transition matrix
    matrix_f_f = scipy.linalg.block_diag(
        tuple_hyperpar[2],
        matrix_unit_diag,
    )

    # Create the updated weight offset
    # matrix
    matrix_sigma_f = scipy.linalg.block_diag(
        tuple_hyperpar[3],
        matrix_zeros,
    )

    # Create 'tuple_hyperpar_f', the tuple of
    # updated hyperparameters
    tuple_hyperpar_f = (
        vector_m_f,
        matrix_b_f,
        matrix_f_f,
        matrix_sigma_f
    )

    # Return the modified hyperparameters
    return tuple_hyperpar_f




# Define the 'past_vector' function

# Prerequisites:
# - None

def past_vector(
    series_main,
    int_length,
    int_t,
):

    '''
    The 'past_vector' function returns a
    numpy vector that contains the last 'int_length'
    terms from 'series_main' coming before the
    'int_t'th term in 'series_main'.

    This function is for producing the observation
    vectors to help create autoregressive DLM models.
    '''

    # Create 'int_main_length', the length of
    # 'series_main'
    int_main_length = len(series_main)


    # Section for producing a null output if the
    # time index is outside the range of the series

    # Check if the time index 'int_t' falls outside
    # the index range of 'series_main'
    if (int_t < 0) | (int_t > int_main_length):

        # Produce 'vector_zeros', a zero vector
        # of the required output length
        vector_zeros = np.zeros(
            shape = int_length,
        )

        # Return 'vector_zeros' since the time
        # index is outside the range of 'series_main'
        return vector_zeros



    # Create 'int_cut', the supposed index at which
    # 'series_main' is cut to give the observation vector
    int_cut = int_t - int_length

    # Create 'int_max_cut', the actual index where
    # 'series_main' would be cut
    int_max_cut = np.maximum(
        int_cut,
        0
    )

    # Create 'series_observations', the series of
    # observations to be used for the autoregressive
    # model
    series_observations = series_main[int_max_cut: int_t]
    
    # Convert 'series_observations' into its vector
    # form 'vector_observations'
    vector_observations = np.array(
        object = series_observations,
    )

    # Check is 'vector_observations' is shorter than the
    # required output length
    if int_cut < 0:

        # Create 'vector_zeros', the extra zero vector
        # to be appended in front of 'vector_observations'
        vector_zeros = np.zeros(
            shape = -int_cut
        )

        # Update 'vector_observations' so it has the
        # zero vector in front that gives it the required
        # output length
        vector_observations = np.append(
            vector_zeros,
            vector_observations,
        )

    # Return the final form of 'vector_observations'
    return vector_observations




# Define the 'hyperpar_series_update' function

# Prerequisites:
# - 'arma_hyperpar_ext' // function
# - 'series_extender' // function


def hyperpar_series_update(
    int_ar_terms,
    int_length,
    series_main,
    tuple_hyperpar,
):

    '''
    The 'hyperpar_series_update' function is for
    conveniently updating the hyperparameters of
    the DLM and updating the length of the main
    series using only one function.

    If the input series is empty, the function
    gives back the empty series and hyperparameters
    untouched.
    '''

    # Create 'int_main_length', the length of
    # 'series_main'
    int_main_length = len(series_main)

    # Check if 'series_main' has any data
    if int_main_length > 0:
        
        # Extend the hyperparameters of the DLM to incorporate
        # autoregression parameters reserved for 'series_main_f'
        tuple_hyperpar_f = arma_hyperpar_ext(
            int_ar_terms = int_ar_terms,
            tuple_hyperpar = tuple_hyperpar,
        )

        # Create 'series_main_f', a series with the data of
        # 'series_main' and the length of 'int_length'
        series_main_f = series_extender(
            series_main = series_main,
            int_extension = int_length - int_main_length,
        )

        # Return the updated series and hyperparameters
        return (
            tuple_hyperpar_f,
            series_main_f
        )

    # Return the original inputs if 'series_main' was
    # empty
    return (
        tuple_hyperpar,
        pd.Series()
    )




# Define the 'phi_modification' function

# Prerequisites:
# - 'past_vector' // function

def phi_modification(
    series_main,
    int_length,
    int_t,
    vector_phi,
):

    '''
    The 'phi_modification' function modifies
    the transition vector so it contains past
    observations to allow for the DLM to learn
    the autoregressive parameters.

    Returns the original transition vector if
    the given series has no data.
    '''


    # Create 'int_main_length', the length of
    # 'series_main'
    int_main_length = len(series_main)

    # Check if 'series_main' contains any
    # data
    if int_main_length > 0:

        # Create 'vector_observations', the vector
        # of observations to be appended to
        # 'vector_phi' so autoregressive model is
        # initiated
        vector_observations = past_vector(
            series_main = series_main,
            int_length = int_length,
            int_t = int_t
        )

        # Create 'vector_phi_mod', the expanded
        # version of the transition vector
        vector_phi_f = np.concatenate(
            [
                vector_phi,
                vector_observations
            ],
        )

        # Return the modified 'vector_phi'
        return vector_phi_f

    # Return 'vector_phi' untouched if
    # 'series_main' has no data
    return vector_phi




# Define the 'discreter' function

# Prerequisites:
# - None

def discreter(
    float_num,
):

    '''
    The 'discreter' function simply
    makes the numeric input discrete and
    non negative.
    '''

    # Round 'float_num' to the nearest integer
    float_round_num = round(float_num)

    # Make the output non zero
    float_num_f = np.maximum(
        float_round_num,
        0
    )

    # Return the discrete output
    return float_num_f




# Define the 'filter_arma' function

# Prerequisites:
# - None

def filter_arma(
    series_x,
    tuple_hyperpar,
    vector_phi,
    series_y = pd.Series([]),
    series_z = pd.Series([]),
    float_delta = 1,
    int_ar_terms = 0,
    int_series_cut = 0,
    int_series_pred = 0,
):

    '''
    The 'filter_arma' function fits a DLM model
    to a given series.

    It is possible to use two more series to aid
    with predictions for the main series.
    '''

    # Create 'int_x_length', the length of the main
    # series to be analysed
    int_x_length = len(series_x)

    # Create 'int_x_cut_length, the length of 'series_x'
    # to actually be analysed
    int_x_cut_length = int_x_length - int_series_cut

    int_x_pred_length = int_x_cut_length + int_series_pred

    # This section incorporates autoregression terms
    # reserved for 'series_x_f'
    tuple_hyperpar, series_x_f = hyperpar_series_update(
        int_ar_terms = int_ar_terms,
        int_length = int_x_pred_length,
        series_main = series_x,
        tuple_hyperpar = tuple_hyperpar,
    )

    # This section incorporates autoregression terms
    # reserved for 'series_y_f'
    tuple_hyperpar, series_y_f = hyperpar_series_update(
        int_ar_terms = int_ar_terms,
        int_length = int_x_pred_length,
        series_main = series_y,
        tuple_hyperpar = tuple_hyperpar,
    )

    # This section incorporates autoregression terms
    # reserved for 'series_z_f'
    tuple_hyperpar, series_z_f = hyperpar_series_update(
        int_ar_terms = int_ar_terms,
        int_length = int_x_pred_length,
        series_main = series_z,
        tuple_hyperpar = tuple_hyperpar,
    )

    # Create 'list_predictions', the list on which all
    # model predictions are appended to
    list_predictions = list()

    # For 'int_t', loop from 0 to 'int_x_cut_length' - 1
    for int_t in range(0, int_x_cut_length):

        # Creat the (t+1)th observation
        float_x_t_plus = series_x_f[int_t]

        # Create new 'vector_phi' to include
        # observations from 'series_x_f'
        vector_phi_mod = phi_modification(
            series_main = series_x_f,
            int_length = int_ar_terms,
            int_t = int_t,
            vector_phi = vector_phi,
        )

        # Create new 'vector_phi' to include
        # observations from 'series_y_f'
        vector_phi_mod = phi_modification(
            series_main = series_y_f,
            int_length = int_ar_terms,
            int_t = int_t,
            vector_phi = vector_phi_mod,
        )

        # Create new 'vector_phi' to include
        # observations from 'series_z_f'
        vector_phi_mod = phi_modification(
            series_main = series_z_f,
            int_length = int_ar_terms,
            int_t = int_t,
            vector_phi = vector_phi_mod,
        )

        # Create prediction 'float_prediction'
        float_prediction = vector_phi_mod @ tuple_hyperpar[2] @ tuple_hyperpar[0]

        # Create prediction 'float_prediction_discrete',
        # which is discrete version of 'float_prediction'
        float_prediction_discrete = discreter(
            float_num = float_prediction
        )

        # Append 'float_prediction_discrete' to prediction 
        # list
        list_predictions.append(
            float_prediction_discrete
        )

        # Update the model hyperparameters by first
        # storing the data from 'bayesian_update'
        # function on to 'tuple_p'
        tuple_p = bayesian_update(
            float_x_t = float_x_t_plus,
            vector_m_t_minus = tuple_hyperpar[0],
            matrix_b_t_minus = tuple_hyperpar[1],
            vector_phi = vector_phi_mod,
            matrix_f = tuple_hyperpar[2],
            matrix_sigma = tuple_hyperpar[3],
            float_delta = float_delta,
        )

        # Then redefine 'tuple_hyperpar' with the
        # new hyperparameters
        tuple_hyperpar = (
            tuple_p[0],
            tuple_p[1],
            tuple_hyperpar[2],
            tuple_hyperpar[3],
        )

    # Create a version of the main series that will
    # store the predictions necessary for modifying
    # the transition vectore in future iterations
    series_x_cut = series_extender(
        series_main = series_x,
        int_extension = -int_series_cut,
    )

    # The loop for generating the model predictions
    for int_t in range(int_x_cut_length, int_x_pred_length):

        vector_phi_mod = phi_modification(
            series_main = series_x_cut,
            int_length = int_ar_terms,
            int_t = int_t,
            vector_phi = vector_phi,
        )

        vector_phi_mod = phi_modification(
            series_main = series_y_f,
            int_length = int_ar_terms,
            int_t = int_t,
            vector_phi = vector_phi_mod,
        )

        vector_phi_mod = phi_modification(
            series_main = series_z_f,
            int_length = int_ar_terms,
            int_t = int_t,
            vector_phi = vector_phi_mod,
        )

        int_power = int_t - int_x_cut_length + 1

        matrix_mod_f = np.linalg.matrix_power(
            a = tuple_hyperpar[2],
            n = int_power
        )

        float_prediction = vector_phi_mod @ matrix_mod_f @ tuple_hyperpar[0]
        
        float_prediction_discrete = discreter(
            float_num = float_prediction
        )

        list_predictions.append(
            float_prediction_discrete
        )

        series_prediction_discrete = pd.Series(
            data = float_prediction_discrete
        )

        series_x_cut = series_x_cut.append(
            series_prediction_discrete,
            ignore_index = True
        )

    series_predictions = pd.Series(
        data = list_predictions
    )

    return series_predictions




def zero_one_scaler(
    series_main
):

    minmaxscaler_scale = sklearn.preprocessing.MinMaxScaler(
    feature_range = (0, 1)
    )

    matrix_main = series_main.values.reshape(-1,1)

    matrix_scaled_main = minmaxscaler_scale.fit_transform(
    X = matrix_main
    )

    series_scaled_main = pd.Series(
        data = matrix_scaled_main.reshape(-1)
    )
    
    return (
        series_scaled_main,
        minmaxscaler_scale
    )

def null_detection(
    dataframe
):

    bool_output = dataframe.isnull().any().any()

    return bool_output
