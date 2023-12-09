# Authors     : Rasheed Othman (1682673), Jonas Lu, Michael
# Created     : December 1, 2023
# Description : Fuzzy logic based Kessler Game controller.

import math
import numpy as np
import skfuzzy as fuzz

from typing import Dict, Tuple
from skfuzzy import control as ctrl
from kesslergame import KesslerController

class FuzzyController(KesslerController):
    
    def __init__(self) -> None:
        self.eval_frames = 0
        
        bullet_impact_time = ctrl.Antecedent(np.arange(0, 1.0, 0.002), "bullet_impact_time")
        asteroid_direction = ctrl.Antecedent(np.arange(-1 * math.pi, math.pi, 0.1), "asteroid_direction")
        asteroid_size = ctrl.Antecedent(np.arange(1, 4, 1), "asteroid_size")
        ship_speed = ctrl.Antecedent(np.arange(0, 240, 1), "ship_speed")
        
        heading_adjustment = ctrl.Consequent(np.arange(-180, 180, 1), "heading_adjustment")
        thrust_adjustment = ctrl.Consequent(np.arange(-480, 480, 1), "thrust_adjustment")
        shoot_asteroid = ctrl.Consequent(np.arange(-1, 1, 0.1), "shoot_asteroid")
        
        bullet_impact_time["S"] = fuzz.trimf(bullet_impact_time.universe, [0, 0, 0.15])
        bullet_impact_time["M"] = fuzz.trimf(bullet_impact_time.universe, [0, 0.15, 0.3])
        bullet_impact_time["L"] = fuzz.smf(bullet_impact_time.universe, 0.00, 0.3)
        
        asteroid_direction["NL"] = fuzz.zmf(asteroid_direction.universe, -1 * math.pi / 3, -1 * math.pi / 6)
        asteroid_direction["NS"] = fuzz.trimf(asteroid_direction.universe, [-1 * math.pi / 3, -1 * math.pi / 6, 0])
        asteroid_direction["Z"]  = fuzz.trimf(asteroid_direction.universe, [-1 * math.pi / 6, 0, math.pi / 6])
        asteroid_direction["PS"] = fuzz.trimf(asteroid_direction.universe, [0, math.pi / 6, math.pi / 3])
        asteroid_direction["PL"] = fuzz.smf(asteroid_direction.universe, math.pi / 6, math.pi / 3)
        
        asteroid_size["S"] = fuzz.trimf(asteroid_size.universe, [1, 1, 2])
        asteroid_size["M"] = fuzz.trimf(asteroid_size.universe, [1, 2, 3])
        asteroid_size["L"]  = fuzz.trimf(asteroid_size.universe, [2, 3, 4])
        asteroid_size["H"] = fuzz.trimf(asteroid_size.universe, [3, 4, 4])
        
        # ship_speed["S"] = fuzz.trimf(ship_speed.universe, [0, 0, 120])
        # ship_speed["M"]  = fuzz.trimf(ship_speed.universe, [80, 120, 160])
        # ship_speed["L"] = fuzz.trimf(ship_speed.universe, [120, 240, 240])
        
        ship_speed["S"] = fuzz.trimf(ship_speed.universe, [-240, -240, -120])
        ship_speed["M"] = fuzz.trimf(ship_speed.universe, [-240, 120, 240])
        ship_speed["L"] = fuzz.trimf(ship_speed.universe, [120, 240, 240])

        heading_adjustment["NL"] = fuzz.trimf(heading_adjustment.universe, [-180, -180, -36])
        heading_adjustment["NS"] = fuzz.trimf(heading_adjustment.universe, [-108, -36, 0])
        heading_adjustment["Z"]  = fuzz.trimf(heading_adjustment.universe, [-36, 0, 36])
        heading_adjustment["PS"] = fuzz.trimf(heading_adjustment.universe, [0, 36, 108])
        heading_adjustment["PL"] = fuzz.trimf(heading_adjustment.universe, [36, 180, 180])
        
        thrust_adjustment["NL"] = fuzz.trimf(thrust_adjustment.universe, [-480, -480, -160])
        thrust_adjustment["NS"] = fuzz.trimf(thrust_adjustment.universe, [-320, -160, 0])
        thrust_adjustment["Z"]  = fuzz.trimf(thrust_adjustment.universe, [-160, 0, 160])
        thrust_adjustment["PS"] = fuzz.trimf(thrust_adjustment.universe, [0, 160, 320])
        thrust_adjustment["PL"] = fuzz.trimf(thrust_adjustment.universe, [160, 480, 480])
        
        shoot_asteroid["N"] = fuzz.trimf(shoot_asteroid.universe, [-1, -1, 0.0])
        shoot_asteroid["Y"] = fuzz.trimf(shoot_asteroid.universe, [0.0, 1, 1])
        
        # For debugging
        # bullet_impact_time.view()
        # asteroid_direction.view()
        # asteroid_size.view()
        # heading_adjustment.view()
        # thrust_adjustment.view()
        # shoot_asteroid.view()
        

        # rule1 = ctrl.Rule(asteroid_direction["NL"] & bullet_impact_time["L"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["NL"], shoot_asteroid["Y"]))
        # rule2 = ctrl.Rule(asteroid_direction["NL"] & bullet_impact_time["L"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["NL"], shoot_asteroid["Y"]))
        # rule3 = ctrl.Rule(asteroid_direction["NL"] & bullet_impact_time["M"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["NL"], shoot_asteroid["Y"]))
        # rule4 = ctrl.Rule(asteroid_direction["NL"] & bullet_impact_time["M"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["NL"], shoot_asteroid["Y"]))
        # rule5 = ctrl.Rule(asteroid_direction["NL"] & bullet_impact_time["S"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["NL"], shoot_asteroid["Y"]))
        # rule6 = ctrl.Rule(asteroid_direction["NL"] & bullet_impact_time["S"] & asteroid_size["L"], (heading_adjustment["NL"], shoot_asteroid["Y"]))
        # rule7 = ctrl.Rule(asteroid_direction["NL"] & bullet_impact_time["S"] & asteroid_size["H"], (heading_adjustment["NL"], shoot_asteroid["N"]))
        
        # rule8 = ctrl.Rule(asteroid_direction["NS"] & bullet_impact_time["L"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["NS"], shoot_asteroid["Y"]))
        # rule9 = ctrl.Rule(asteroid_direction["NS"] & bullet_impact_time["L"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["NS"], shoot_asteroid["Y"]))
        # rule10 = ctrl.Rule(asteroid_direction["NS"] & bullet_impact_time["M"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["NS"], shoot_asteroid["Y"]))
        # rule11 = ctrl.Rule(asteroid_direction["NS"] & bullet_impact_time["M"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["NS"], shoot_asteroid["Y"]))
        # rule12 = ctrl.Rule(asteroid_direction["NS"] & bullet_impact_time["S"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["NS"], shoot_asteroid["Y"]))
        # rule13 = ctrl.Rule(asteroid_direction["NS"] & bullet_impact_time["S"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["NS"], shoot_asteroid["Y"]))
        
        # rule14 = ctrl.Rule(asteroid_direction["Z"] & bullet_impact_time["L"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["Z"], shoot_asteroid["Y"]))
        # rule15 = ctrl.Rule(asteroid_direction["Z"] & bullet_impact_time["L"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["Z"], shoot_asteroid["Y"]))
        # rule16 = ctrl.Rule(asteroid_direction["Z"] & bullet_impact_time["M"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["Z"], shoot_asteroid["Y"]))
        # rule17 = ctrl.Rule(asteroid_direction["Z"] & bullet_impact_time["M"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["Z"], shoot_asteroid["Y"]))
        # rule18 = ctrl.Rule(asteroid_direction["Z"] & bullet_impact_time["S"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["Z"], shoot_asteroid["Y"]))
        # rule19 = ctrl.Rule(asteroid_direction["Z"] & bullet_impact_time["S"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["Z"], shoot_asteroid["Y"]))
        
        # rule20 = ctrl.Rule(asteroid_direction["PS"] & bullet_impact_time["L"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["PS"], shoot_asteroid["Y"]))
        # rule21 = ctrl.Rule(asteroid_direction["PS"] & bullet_impact_time["L"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["PS"], shoot_asteroid["Y"]))
        # rule22 = ctrl.Rule(asteroid_direction["PS"] & bullet_impact_time["M"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["PS"], shoot_asteroid["Y"]))
        # rule23 = ctrl.Rule(asteroid_direction["PS"] & bullet_impact_time["M"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["PS"], shoot_asteroid["Y"]))
        # rule24 = ctrl.Rule(asteroid_direction["PS"] & bullet_impact_time["S"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["PL"], shoot_asteroid["Y"]))
        # rule25 = ctrl.Rule(asteroid_direction["PS"] & bullet_impact_time["S"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["PL"], shoot_asteroid["Y"]))
        
        # rule26 = ctrl.Rule(asteroid_direction["PL"] & bullet_impact_time["L"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["PL"], shoot_asteroid["Y"]))
        # rule27 = ctrl.Rule(asteroid_direction["PL"] & bullet_impact_time["L"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["PL"], shoot_asteroid["Y"]))
        # rule28 = ctrl.Rule(asteroid_direction["PL"] & bullet_impact_time["M"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["PL"], shoot_asteroid["Y"]))
        # rule29 = ctrl.Rule(asteroid_direction["PL"] & bullet_impact_time["M"] & (asteroid_size["L"] | asteroid_size["H"]), (heading_adjustment["PL"], shoot_asteroid["Y"]))
        # rule30 = ctrl.Rule(asteroid_direction["PL"] & bullet_impact_time["S"] & (asteroid_size["S"] | asteroid_size["M"]), (heading_adjustment["PL"], shoot_asteroid["Y"]))
        # rule31 = ctrl.Rule(asteroid_direction["PL"] & bullet_impact_time["S"] & asteroid_size["L"], (heading_adjustment["PL"], shoot_asteroid["Y"]))
        # rule32 = ctrl.Rule(asteroid_direction["PL"] & bullet_impact_time["S"] & asteroid_size["H"], (heading_adjustment["PL"], shoot_asteroid["N"]))
        
        rules = []
        
        rules.append(ctrl.Rule(asteroid_direction["PL"], heading_adjustment["PL"]))
        rules.append(ctrl.Rule(asteroid_direction["PS"], heading_adjustment["PS"]))
        rules.append(ctrl.Rule(asteroid_direction["Z"], heading_adjustment["Z"]))
        rules.append(ctrl.Rule(asteroid_direction["NS"], heading_adjustment["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["NL"], heading_adjustment["NL"]))
        
        rules.append(ctrl.Rule(bullet_impact_time["L"] & asteroid_size["H"], thrust_adjustment["PS"]))
        rules.append(ctrl.Rule(bullet_impact_time["L"] & asteroid_size["L"], thrust_adjustment["PS"]))
        rules.append(ctrl.Rule(bullet_impact_time["L"] & asteroid_size["M"], thrust_adjustment["PS"]))
        rules.append(ctrl.Rule(bullet_impact_time["L"] & asteroid_size["S"], thrust_adjustment["PL"]))
        
        rules.append(ctrl.Rule(bullet_impact_time["M"] & asteroid_size["H"], thrust_adjustment["Z"]))
        rules.append(ctrl.Rule(bullet_impact_time["M"] & asteroid_size["L"], thrust_adjustment["Z"]))
        rules.append(ctrl.Rule(bullet_impact_time["M"] & asteroid_size["M"], thrust_adjustment["Z"]))
        rules.append(ctrl.Rule(bullet_impact_time["M"] & asteroid_size["S"], thrust_adjustment["PS"]))
        
        rules.append(ctrl.Rule(bullet_impact_time["S"] & asteroid_size["H"], thrust_adjustment["NL"]))
        rules.append(ctrl.Rule(bullet_impact_time["S"] & asteroid_size["L"], thrust_adjustment["NL"]))
        rules.append(ctrl.Rule(bullet_impact_time["S"] & asteroid_size["M"], thrust_adjustment["NL"]))
        rules.append(ctrl.Rule(bullet_impact_time["S"] & asteroid_size["S"], thrust_adjustment["NL"]))
        
        rules.append(ctrl.Rule(asteroid_direction["NL"] & ship_speed["L"], ()))
        
        rules.append(ctrl.Rule(asteroid_size["H"], thrust_adjustment["NS"]))
        rules.append(ctrl.Rule(asteroid_size["L"], thrust_adjustment["NS"]))
        rules.append(ctrl.Rule(asteroid_size["M"], thrust_adjustment["Z"]))
        rules.append(ctrl.Rule(asteroid_size["S"], thrust_adjustment["PS"]))
        
        rules.append(ctrl.Rule(bullet_impact_time["L"] & ship_speed["L"], thrust_adjustment["NL"]))
        rules.append(ctrl.Rule(bullet_impact_time["L"] & ship_speed["M"], thrust_adjustment["PS"]))
        rules.append(ctrl.Rule(bullet_impact_time["L"] & ship_speed["S"], thrust_adjustment["PL"]))
        
        rules.append(ctrl.Rule(bullet_impact_time["M"] & ship_speed["L"], thrust_adjustment["NL"]))
        rules.append(ctrl.Rule(bullet_impact_time["M"] & ship_speed["M"], thrust_adjustment["NL"]))
        rules.append(ctrl.Rule(bullet_impact_time["M"] & ship_speed["S"], thrust_adjustment["NS"]))
        
        rules.append(ctrl.Rule(bullet_impact_time["S"] & ship_speed["L"], thrust_adjustment["NL"]))
        rules.append(ctrl.Rule(bullet_impact_time["S"] & ship_speed["M"], thrust_adjustment["NS"]))
        rules.append(ctrl.Rule(bullet_impact_time["S"] & ship_speed["S"], thrust_adjustment["Z"]))
        
        self.targetting_control = ctrl.ControlSystem()
        for rule in rules:
            self.targetting_control.addrule(rule)

        # self.targetting_control = ctrl.ControlSystem()
        # localVars = locals()
        # # change the range of loop to (1, 1 + # of rules)
        # for i in range(1,42):
        #     try:
        #         ruleVar = localVars[f"rule{i}"]
        #     except Exception as e:
        #         print(f"Error: {e}")
        #     self.targetting_control.addrule(ruleVar)
        
    # def actions(self, ship_state: Dict, game_state: Dict) -> Tuple[float, float, bool]:
    #     """
    #     Method processed each time step by this controller.
    #     """
        
    #     closest_asteroid = None
        
    #     ship_radius = ship_state["radius"]
    #     ship_x_pos = ship_state["position"][0]
    #     ship_y_pos = ship_state["position"][1]
        
    #     for asteroid in game_state["asteroids"]:
            
    #         euclidean_distance = math.sqrt((ship_x_pos - asteroid["position"][0])**2 + (ship_y_pos - asteroid["position"][1])**2)
    #         euclidean_distance = euclidean_distance - ship_radius - asteroid["radius"]
            
    #         if closest_asteroid is None:
    #             closest_asteroid = dict(asteroid=asteroid, distance=euclidean_distance)
    #         else:
    #             if closest_asteroid["distance"] > euclidean_distance:
    #                 closest_asteroid["asteroid"] = asteroid
    #                 closest_asteroid["distance"] = euclidean_distance
        
    #     bullet_speed = 800
        
    #     asteroid_ship_delta_x = ship_x_pos - closest_asteroid["asteroid"]["position"][0]
    #     asteroid_ship_delta_y = ship_y_pos - closest_asteroid["asteroid"]["position"][1]
    #     asteroid_ship_delta_theta = math.atan2(asteroid_ship_delta_y, asteroid_ship_delta_x)
    #     asteroid_direction = math.atan2(closest_asteroid["asteroid"]["velocity"][1], closest_asteroid["asteroid"]["velocity"][0])
    #     asteroid_velocity = math.sqrt(closest_asteroid["asteroid"]["velocity"][0]**2 + closest_asteroid["asteroid"]["velocity"][1]**2)
        
    #     determinant = 4 * (((closest_asteroid["distance"] * asteroid_velocity * math.cos(asteroid_ship_delta_theta + asteroid_direction))**2) - (closest_asteroid["distance"]**2 * (asteroid_velocity**2 - bullet_speed**2)))

    #     intercepts = [
    #         (2 * closest_asteroid["distance"] * asteroid_velocity * math.cos(asteroid_ship_delta_theta + asteroid_direction) + math.sqrt(determinant)) / (2 * (asteroid_velocity**2 - bullet_speed**2)),
    #         (2 * closest_asteroid["distance"] * asteroid_velocity * math.cos(asteroid_ship_delta_theta + asteroid_direction) - math.sqrt(determinant)) / (2 * (asteroid_velocity**2 - bullet_speed**2))
    #     ]
        
    #     if intercepts[0] > intercepts[1]:
    #         bullet_intercept_time = intercepts[1] if intercepts[1] >= 0 else intercepts[0]
    #     else:
    #         bullet_intercept_time = intercepts[0] if intercepts[0] >= 0 else intercepts[1]
            
    #     x_intercept = closest_asteroid["asteroid"]["position"][0] + bullet_intercept_time * closest_asteroid["asteroid"]["velocity"][0]
    #     y_intercept = closest_asteroid["asteroid"]["position"][1] + bullet_intercept_time * closest_asteroid["asteroid"]["velocity"][1]
        
    #     shooting_angle = math.atan2((y_intercept - ship_y_pos), (x_intercept - ship_x_pos)) - ((math.pi / 180) * ship_state["heading"])
    #     shooting_angle = (shooting_angle + math.pi) % (2 * math.pi) - math.pi
        
    #     targetting_system = ctrl.ControlSystemSimulation(self.targetting_control, flush_after_run=1)
    #     targetting_system.input["bullet_impact_time"] = bullet_intercept_time
    #     targetting_system.input["asteroid_direction"] = shooting_angle
    #     targetting_system.input["asteroid_size"] = closest_asteroid["asteroid"]["size"]
    #     targetting_system.input["ship_speed"] = ship_state["speed"]
    #     targetting_system.compute()
        
    #     fire = True if targetting_system.output["shoot_asteroid"] >= 0 else False
    #     thrust = targetting_system.output["thrust_adjustment"]
    #     heading = targetting_system.output["heading_adjustment"]
        
    #     self.eval_frames += 1
        
    #     # print(f"Thrust: {thrust} m/s^2, Intercept Time: {bullet_intercept_time} s, Target Angle: {shooting_angle} degrees, Ship Angle: {heading} degrees, Fire: {fire}")
    #     # print(thrust, bullet_intercept_time, shooting_angle, heading, fire)
    #     print(closest_asteroid["distance"])
        
    #     return thrust, heading, fire
    
    def actions(self, ship_state: Dict, game_state: Dict) -> Tuple[float, float, bool]:
        
        bullet_speed = 800
        closest_asteroid = None
        closest_asteroid_distance = np.infty
        
        for asteroid in game_state["asteroids"]:
            
            # Find the distance between the ship's and asteroid's x and y positions
            x_delta = ship_state["position"][0] - asteroid["position"][0]
            y_delta = ship_state["position"][1] - asteroid["position"][1]
            
            # Obtain the Euclidean distance between the ship and the asteroid
            # To determine the surface to surface distance, the radius of each object must be subtracted
            distance = np.sqrt(x_delta**2 + y_delta**2) - ship_state["radius"] - asteroid["radius"]
            
            # Update the closest asteroid based on the Euclidean distance
            if (closest_asteroid_distance > distance):
                closest_asteroid = asteroid
                closest_asteroid_distance = distance
        
        # Obtain the magnitude and direction of the asteroid's velocity
        asteroid_velocity = np.sqrt(closest_asteroid["velocity"][0]**2 + closest_asteroid["velocity"][1]**2)
        asteroid_direction = np.arctan2(closest_asteroid["velocity"][1], closest_asteroid["velocity"][0])
        
        # Find the distance between the ship and the closest asteroid's x and y positions
        x_delta = ship_state["position"][0] - closest_asteroid["position"][0]
        y_delta = ship_state["position"][1] - closest_asteroid["position"][1]
        
        # Find the angle between the ship and the intersection point from the asteroid's frame of reference
        asteroid_angle = np.arctan2(y_delta, x_delta) + asteroid_direction
        
        # Find the determinant from the Quadratic formula
        a = asteroid_velocity**2 - bullet_speed**2
        b = -2 * closest_asteroid_distance * asteroid_velocity * np.cos(asteroid_angle)
        c = closest_asteroid_distance**2
        determinant = b**2 - (4 * a * c)
        
        # Evaluate the bullet impact time based on the calculated intercepts
        intercepts = ((-1 * b + np.sqrt(determinant)) / (2 * a), (-1 * b - np.sqrt(determinant)) / (2 * a))
        if intercepts[0] > intercepts[1]:
            bullet_intercept_time = intercepts[1] if intercepts[1] >= 0 else intercepts[0]
        else:
            bullet_intercept_time = intercepts[0] if intercepts[0] >= 0 else intercepts[1]
        
        # Obtain the intercept point from the bullet impact time
        x_intercept = closest_asteroid["position"][0] + bullet_intercept_time * closest_asteroid["velocity"][0]
        y_intercept = closest_asteroid["position"][1] + bullet_intercept_time * closest_asteroid["velocity"][1]
        
        # Determine the difference between the targetting angle and the current ship heading
        # targetting_angle = (np.pi / 2) - (np.arctan2(y_delta, x_delta) + np.arctan2((y_intercept - ship_state["position"][1]), (x_intercept - ship_state["position"][0])))
        # targetting_angle = targetting_angle - ((np.pi / 180) * ship_state["heading"])
        # targetting_angle = (targetting_angle + np.pi) % (2 * np.pi) - np.pi
        
        targetting_angle = math.atan2((y_intercept - ship_state["position"][1]), (x_intercept - ship_state["position"][0])) - ((math.pi / 180) * ship_state["heading"])
        targetting_angle = (targetting_angle + math.pi) % (2 * math.pi) - math.pi
        
        targetting_system = ctrl.ControlSystemSimulation(self.targetting_control, flush_after_run=1)
        targetting_system.input["ship_speed"] = ship_state["speed"]
        targetting_system.input["asteroid_size"] = closest_asteroid["size"]
        targetting_system.input["bullet_impact_time"] = bullet_intercept_time
        targetting_system.input["asteroid_direction"] = targetting_angle
        targetting_system.compute()
        
        turn_rate = targetting_system.output["heading_adjustment"]
        thrust = targetting_system.output["thrust_adjustment"]
        fire = True
        # fire = True if targetting_system.output["shoot_asteroid"] >= 0 else False
        
        self.eval_frames += 1
        
        # print(ship_state["speed"], closest_asteroid["size"], closest_asteroid_distance, targetting_angle, turn_rate, thrust, fire)
        # print(f"T: {bullet_intercept_time:.4f}, D: {closest_asteroid_distance:.4f}, A: {np.degrees(targetting_angle):.4f}")
        print(f"D: {closest_asteroid_distance:.2f}, A: {targetting_angle:.2f}, TR: {turn_rate:.2f}, TH: {thrust:.2f}")
        
        return thrust, turn_rate, fire
    
    @property
    def name(self) -> str:
        return "Fuzzy Controller"

# For debugging
fc = FuzzyController()