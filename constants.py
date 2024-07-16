from typing import Dict, Sequence
from itertools import combinations
import math
import time

from streamlit import session_state as ss
from scipy.optimize import minimize


def inclusion_exclusion(*arrays):
    n = len(arrays)
    result = 0.0

    for k in range(1, n + 1):
        for combo in combinations(arrays, k):
            term = 1.0
            for array in combo:
                term *= array
            if k % 2 == 1:
                result += term
            else:
                result -= term

    return result


def average(*elements):
    return sum(elements) / len(elements)


class Ore:
    _instance = None
    pre_exp_factor = 10**11
    activation_ener = 50000
    gas_const = 8.314
    per_free_space = 8.5 * 10**-12
    acc_due_to_gravity = 9.81
    fluid_density = 1000

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    minerals = [
        "Iron",
        "Sulphur",
        "Arsenic",
        "Copper",
        "Zinc",
        "Lead",
        "Calcium Carbonate",
        "Iron Carbonate",
        "Silica",
        "Potassium",
        "Sodium",
        "Calcium",
        "Aluminum",
        "Silicon",
    ]

    reagents = [
        "CN (kg/t)",
        "Lime (kg/t)",
        "Collector A (g/t)",
        "Collector B (g/t)",
        "Frother (mL/t)",
    ]

    def identify() -> Dict[str, str]:
        """
        Identifies the ore type based on the mineralogy values.

        Returns:
            A dictionary containing the identified ore type and the reason for identification.
        """
        iron = ss.get("Iron_mineralogy")
        sulphur = ss.get("Sulphur_mineralogy")
        arsenic = ss.get("Arsenic_mineralogy")
        copper = ss.get("Copper_mineralogy")
        zinc = ss.get("Zinc_mineralogy")
        lead = ss.get("Lead_mineralogy")
        calcium_carbonate = ss.get("Calcium Carbonate_mineralogy")
        iron_carbonate = ss.get("Iron Carbonate_mineralogy")
        silica = ss.get("Silica_mineralogy")
        potassium = ss.get("Potassium_mineralogy")
        sodium = ss.get("Sodium_mineralogy")
        calcium = ss.get("Calcium_mineralogy")
        aluminum = ss.get("Aluminum_mineralogy")
        silicon = ss.get("Silicon_mineralogy")

        if iron >= 40 and sulphur >= 40:
            ss["ore_type"] = "Pyrite"
            ss["ore_type_reason"] = (
                f"Iron[{iron}] is 40%+ and Sulphur[{sulphur}] is between 40 and 50%."
            )
        elif arsenic >= 33 and iron >= 25 and sulphur >= 35:
            ss["ore_type"] = "Arsenopyrite"
            ss["ore_type_reason"] = (
                f"Arsenic[{arsenic}] is 33%+, Iron[{iron}] is between 25 and 30%, and Sulphur[{sulphur}] is between 35 and 40%."
            )
        elif copper >= 35 and iron >= 15 and sulphur >= 35:
            ss["ore_type"] = "Chalcopyrite"
            ss["ore_type_reason"] = (
                f"Copper[{copper}] is 35%+, Iron[{iron}] is between 15 and 20%, and Sulphur[{sulphur}] is between 35 and 45%."
            )
        elif zinc >= 50:
            ss["ore_type"] = "Sphalerite"
            ss["ore_type_reason"] = f"Zinc[{zinc}] is 50%+."
        elif lead >= 85:
            ss["ore_type"] = "Galena"
            ss["ore_type_reason"] = f"Lead[{lead}] is 85%+."
        elif calcium_carbonate >= 80:
            ss["ore_type"] = "Calcite"
            ss["ore_type_reason"] = f"Calcium Carbonate[{calcium_carbonate}] is 80%+."
        elif iron_carbonate >= 75:
            ss["ore_type"] = "Siderite"
            ss["ore_type_reason"] = f"Iron Carbonate[{iron_carbonate}] is 75%+."
        elif silica >= 90:
            ss["ore_type"] = "Quartz"
            ss["ore_type_reason"] = f"Silica[{silica}] is 90%+."
        elif potassium >= 60 and sodium >= 60 and calcium >= 60:
            ss["ore_type"] = "Feldspars"
            ss["ore_type_reason"] = (
                f"Potassium[{potassium}], Sodium[{sodium}], and Calcium[{calcium}] are 60%+."
            )
        elif aluminum >= 12 and calcium >= 12:
            ss["ore_type"] = "Montmorillonite"
            ss["ore_type_reason"] = (
                f"Aluminum[{aluminum}] and Calcium[{calcium}] are 12%+."
            )
        elif aluminum >= 38 and silicon >= 46:
            ss["ore_type"] = "Kaolinite"
            ss["ore_type_reason"] = (
                f"Aluminum[{aluminum}] is between 38 and 45% and Silicon[{silicon}] is between 46 and 52%."
            )
        else:
            ss["ore_type"] = "Unknown"
            ss["ore_type_reason"] = "Does not support any of our known reasons."

    def cal_cyanidation_k(temp: float):
        return Ore.pre_exp_factor * math.exp(
            -Ore.activation_ener / (Ore.gas_const * temp)
        )

    def _cyanidation_CF(temp: float):
        CN = ss.get("CN (kg/t)_reagent")
        temp = temp[0]
        return -1 * Ore.cal_cyanidation_k(temp) * ss.get("gold_head_grade") * CN

    def cyanidation():
        temp_0, temp_bounds = 293, (293, 323)
        res = minimize(Ore._cyanidation_CF, temp_0, bounds=[temp_bounds])

        return {
            "gold_dissolution_rate": -1 * res.fun,
            "temperature": res.x[0],
            "k_cyanidation": Ore.cal_cyanidation_k(res.x),
        }

    def _floatation_CF(params: Sequence[float]):
        A, H1, H2, Er, Zp1, Zp2, k, H, temp = params
        Evdw = -A * ((H1 * H2) / (H1 + H2))
        Eedl = (
            2
            * math.pi
            * Ore.per_free_space
            * Er
            * Zp1
            * Zp2
            * math.exp(-k * H)
            / (1 + k * H)
        )
        Eb = Evdw + Eedl
        return -1 * 1 / (1 + math.exp(Eb / (Ore.cal_cyanidation_k(temp) * temp)))

    def flotation():
        A, A_bounds = 15 * 10**-20, (10 * 10**-20, 20 * 10**-20)
        H1, H1_bounds = 50 * 10**-6, (1 * 10**-6, 100 * 10**-6)
        H2, H2_bounds = 100 * 10**-6, (50 * 10**-6, 200 * 10**-6)
        Er, Er_bounds = 6, (2, 10)
        Zp1, Zp1_bounds = 10, (-100, 100)
        Zp2, Zp2_bounds = 10, (-100, 100)
        k, k_bounds = 500, (108, 1000)
        H, H_bounds = 100, (1, 1000)
        temp, temp_bounds = 293, (293, 323)

        res = minimize(
            Ore._floatation_CF,
            [A, H1, H2, Er, Zp1, Zp2, k, H, temp],
            bounds=[
                A_bounds,
                H1_bounds,
                H2_bounds,
                Er_bounds,
                Zp1_bounds,
                Zp2_bounds,
                k_bounds,
                H_bounds,
                temp_bounds,
            ],
        )
        return {
            "flotation_collection_eff": -1 * res.fun,
            "A": res.x[0],
            "H1": res.x[1],
            "H2": res.x[2],
            "Er": res.x[3],
            "Zp1": res.x[4],
            "Zp2": res.x[5],
            "k": res.x[6],
            "H": res.x[7],
            "temperature": res.x[8],
        }

    def _gravity_CF(params):
        d = 2  # TODO: What is it? Input?
        pp, fluid_vis = params
        return (
            -1 * Ore.acc_due_to_gravity * (pp - Ore.fluid_density) / 18 * fluid_vis * d
        )

    def gravity():
        pp, pp_bounds = 3000, (2500, 4000)
        fluid_vis, fluid_vis_bounds = 0.001, (0.0005, 0.005)
        res = minimize(
            Ore._gravity_CF,
            [pp, fluid_vis],
            bounds=[pp_bounds, fluid_vis_bounds],
        )
        return {
            "gravity_recovery": -1 * res.fun,
            "pp": res.x[0],
            "fluid_viscosity": res.x[1],
        }

    def heap_leaching():
        # NOTE: Same as cyanidation
        return {"heap_leaching_k": Ore.cyanidation()["k_cyanidation"]}

    def commuinution():
        # NOTE: Same as cyanidation
        return {"commuinution_k": Ore.cyanidation()["k_cyanidation"]}

    def carbon_adsorption(t: float):
        # Carbon Adsorption
        # qmax =
        # b = 0.1 - 1.0 lper mg [to optimize]
        # C =
        # q = (qmax * C * b) / (1 + b + C)
        ...

    def get_recovery_term(k: float):
        return (1 - math.exp(-k * ss.get("throughput"))) * 100

    def overall_recovery():
        cyanidation = Ore.cyanidation()
        flotation = Ore.flotation()
        gravity = Ore.gravity()
        heap_leaching = Ore.heap_leaching()
        commuinution = Ore.commuinution()

        cyanidation_recovery = Ore.get_recovery_term(cyanidation["k_cyanidation"])
        flotation_recovery = Ore.get_recovery_term(
            flotation["flotation_collection_eff"]
        )
        gravity_recovery = Ore.get_recovery_term(gravity["gravity_recovery"])
        heap_leaching_recovery = Ore.get_recovery_term(heap_leaching["heap_leaching_k"])
        commuinution_recovery = Ore.get_recovery_term(commuinution["commuinution_k"])

        time.sleep(3)

        return {
            "cyanidation": {
                "revovery": cyanidation_recovery,
                "Other params": cyanidation,
            },
            "flotation": {
                "revovery": flotation_recovery,
                "Other params": flotation,
            },
            "gravity": {
                "revovery": gravity_recovery,
                "Other params": gravity,
            },
            "heap_leaching": {
                "revovery": heap_leaching_recovery,
                "Other params": heap_leaching,
            },
            "commuinution": {
                "revovery": commuinution_recovery,
                "Other params": commuinution,
            },
        }
