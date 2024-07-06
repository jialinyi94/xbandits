import numpy

from fastbandits.core.statistics import update_mean_and_counts


def score(
    t: int,
    mean_rewards: numpy.ndarray,
    trial_counts: numpy.ndarray,
):
    """Compute the UCB score for each arm.

    Parameters
    ----------
    t : int
        the current time step.
    mean_rewards : numpy.ndarray
        a numpy array of shape (..., num_arms) where the mean rewards for each arm are stored.
    trial_counts : numpy.ndarray
        a numpy array of shape (..., num_arms) where the number of trials for each arm are stored.

    Returns
    -------
    scores : numpy.ndarray
        a numpy array of shape (..., num_arms) where the UCB score for each arm is stored.

    ::math::
        UCB = mean_rewards + sqrt(2 * log(t) / trial_counts if trial_counts > 0 else inf
    """
    exploration_bonus = numpy.inf * numpy.ones_like(mean_rewards)
    warmup = trial_counts > 0
    if t > 0:
        exploration_bonus[warmup] = numpy.sqrt(2 * numpy.log(t) / trial_counts[warmup])
    ucb = mean_rewards + exploration_bonus
    return ucb


def select_arm(
    t: int,
    mean_rewards: numpy.ndarray,
    trial_counts: numpy.ndarray,
):
    """Select the arm with the highest UCB score.

    Parameters
    ----------
    t : int
        the current time step.
    mean_rewards : numpy.ndarray
        a numpy array of shape (..., num_arms) where the mean rewards for each arm are stored.
    trial_counts : numpy.ndarray
        a numpy array of shape (..., num_arms) where the number of trials for each arm are stored.

    Returns
    -------
    numpy.ndarray
        a numpy array of shape (...) where the index of the selected arm is stored.
    """
    ucb_scores = score(t, mean_rewards, trial_counts)
    return numpy.argmax(ucb_scores, axis=-1)


def update(
    sel_arms: numpy.ndarray,
    recv_rewards: numpy.ndarray,
    mean_rewards: numpy.ndarray,
    trial_counts: numpy.ndarray,
):
    """Update the states, i.e. mean_reward and trial_count, for the selected arms.

    Parameters
    ----------
    sel_arms : numpy.ndarray
        a numpy array of shape (...) where the index of the selected arm is stored.
    recv_rewards : numpy.ndarray
        a numpy array of shape (...) where the reward for the selected arm is stored.
    mean_rewards : numpy.ndarray
        a numpy array of shape (..., num_arms) where the mean rewards for each arm are stored.
    trial_counts : numpy.ndarray
        a numpy array of shape (..., num_arms) where the number of trials for each arm are stored.

    Returns
    -------
    mean_rewards : numpy.ndarray
        a numpy array of shape (..., num_arms) where the updated mean rewards for each arm are stored.
    trial_counts : numpy.ndarray
        a numpy array of shape (..., num_arms) where the updated number of trials for each arm are stored.
    """
    return update_mean_and_counts(sel_arms, recv_rewards, mean_rewards, trial_counts)
