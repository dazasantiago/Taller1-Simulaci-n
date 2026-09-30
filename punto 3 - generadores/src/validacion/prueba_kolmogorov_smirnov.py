"""Prueba de Kolmogorov-Smirnov sobre una secuencia pseudoaleatoria (lógica pura)."""
from scipy.stats import kstwo

ALPHA_DEFAULT = 0.05


def get_ks_critical_value(n: int, alpha: float = ALPHA_DEFAULT) -> float:
    return float(kstwo.ppf(1 - alpha, n))


def ks_test(sequence: list[float], k: int = 10, alpha: float = ALPHA_DEFAULT) -> dict:
    """Ejecuta la prueba de Kolmogorov-Smirnov sobre una secuencia en [0, 1)."""
    n = len(sequence)
    if n == 0:
        raise ValueError("La secuencia no puede estar vacía.")

    mean = sum(sequence) / n
    minimum = min(sequence)
    maximum = max(sequence)
    step = (maximum - minimum) / k if maximum > minimum else 1.0 / k

    intervals = []
    for i in range(k):
        start = minimum + i * step
        end = start + step
        intervals.append({"number": i + 1, "start": start, "end": end})

    observed_frequencies = []
    for inter in intervals:
        start = inter["start"]
        end = inter["end"]
        is_last = (inter["number"] == k)

        count = 0
        for x in sequence:
            if is_last:
                if start <= x <= end:
                    count += 1
            else:
                if start <= x < end:
                    count += 1

        observed_frequencies.append(count)

    intervals_table = []
    cum_observed_freq = 0
    differences = []

    for i in range(k):
        inter = intervals[i]
        obs_freq = observed_frequencies[i]

        cum_observed_freq += obs_freq
        obs_cum_prob = cum_observed_freq / n
        exp_cum_freq = (i + 1) * (n / k)
        exp_cum_prob = (i + 1) / k
        difference = abs(exp_cum_prob - obs_cum_prob)

        differences.append(difference)
        intervals_table.append({
            "interval": inter["number"],
            "start": inter["start"],
            "end": inter["end"],
            "obs_freq": obs_freq,
            "cum_obs_freq": cum_observed_freq,
            "obs_cum_prob": obs_cum_prob,
            "exp_cum_freq": exp_cum_freq,
            "exp_cum_prob": exp_cum_prob,
            "difference": difference,
            # Spanish backward-compatibility keys
            "intervalo": inter["number"],
            "inicial": inter["start"],
            "final": inter["end"],
            "frec_obt": obs_freq,
            "frec_obt_acum": cum_observed_freq,
            "prob_obt_acum": obs_cum_prob,
            "frec_esp_acum": exp_cum_freq,
            "prob_esp_acum": exp_cum_prob,
            "diferencia": difference,
        })

    d_max = max(differences)
    d_max_p = get_ks_critical_value(n, alpha=alpha)
    passed_test = d_max <= d_max_p

    result = {
        "statistic": d_max,
        "d_max": d_max,
        "critical_value": d_max_p,
        "alpha": alpha,
        "n": n,
        "k": k,
        "minimum": minimum,
        "maximum": maximum,
        "mean": mean,
        "passed_test": passed_test,
        "passes_test": passed_test,
        "intervals_table": intervals_table,
        # Spanish backward-compatibility keys
        "valor_critico": d_max_p,
        "pasa_prueba": passed_test,
        "tabla_intervalos": intervals_table,
    }
    return result


prueba_ks = ks_test

