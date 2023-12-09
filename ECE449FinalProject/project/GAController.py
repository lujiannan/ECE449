
import numpy as np
import skfuzzy as fuzz

from typing import Dict
from typing import Tuple
from skfuzzy import control as ctrl
from kesslergame import KesslerController

class GAController(KesslerController):
    
    def __init__(self, chromosomes) -> None:
        
        # Counts the number of frames evaluated
        self.eval_frames = 0
        
        self.focused_asteroid = None
        
        # Antecedents definition
        ship_speed = ctrl.Antecedent(np.arange(-240, 240, 0.1), "ship_speed")
        asteroid_size = ctrl.Antecedent(np.arange(1, 4, 1), "asteroid_size")
        asteroid_distance = ctrl.Antecedent(np.arange(0, 1280, 0.1), "asteroid_distance")
        asteroid_direction = ctrl.Antecedent(np.arange(-180, 180, 0.1), "asteroid_direction")
        
        # Consequents definition
        ship_turn_rate = ctrl.Consequent(np.arange(-180, 180, 0.1), "ship_turn_rate")
        ship_thrust = ctrl.Consequent(np.arange(-480, 480, 0.1), "ship_thrust")
        fire_bullet = ctrl.Consequent(np.arange(-1, 1, 0.1), "fire_bullet")
        
        # Antecedent fuzzy set declarations
        
        genes = []
        for c, g in enumerate(chromosomes):
            genes.append(g.value[c])
        
        # Declare the fuzzy sets for obtaining the ship's current speed
        ship_speed["NL"] = fuzz.trimf(ship_speed.universe, [-240, -240, -1 * genes[0][0]])
        ship_speed["NS"] = fuzz.trimf(ship_speed.universe, [-1 * genes[0][1], -1 * genes[0][0], 0])
        ship_speed["AZ"] = fuzz.trimf(ship_speed.universe, [-1 * genes[0][0], 0, genes[0][0]])
        ship_speed["PS"] = fuzz.trimf(ship_speed.universe, [0, genes[0][0], genes[0][1]])
        ship_speed["PL"] = fuzz.trimf(ship_speed.universe, [genes[0][0], 240, 240])
        
        # Declare the fuzzy sets for obtaining the closest asteroid's physical size
        asteroid_size["S"] = fuzz.trimf(asteroid_size.universe, [1, 1, 2])
        asteroid_size["M"] = fuzz.trimf(asteroid_size.universe, [1, 2, 3])
        asteroid_size["L"] = fuzz.trimf(asteroid_size.universe, [2, 3, 4])
        asteroid_size["H"] = fuzz.trimf(asteroid_size.universe, [3, 4, 4])
        
        # Declare the fuzzy sets for the bullet impact time which is used to determine the asteroid distance membership
        asteroid_distance["VC"] = fuzz.trimf(asteroid_distance.universe, [0, 0, genes[1][1]])
        asteroid_distance["SC"] = fuzz.trimf(asteroid_distance.universe, [genes[1][0], genes[1][1], genes[1][2]])
        asteroid_distance["IR"] = fuzz.trimf(asteroid_distance.universe, [genes[1][1], genes[1][2], genes[1][3]])
        asteroid_distance["SF"] = fuzz.trimf(asteroid_distance.universe, [genes[1][2], genes[1][3], genes[1][4]])
        asteroid_distance["VF"] = fuzz.trimf(asteroid_distance.universe, [genes[1][3], 1280, 1280])
        
        # Declare the fuzzy sets for obtaining the direction of the closest asteroid relative to the ship
        asteroid_direction["FL"] = fuzz.zmf(asteroid_direction.universe, -1 * genes[2][1], -1 * genes[2][0])
        asteroid_direction["CL"] = fuzz.trimf(asteroid_direction.universe, [-1 * genes[2][1], -1 * genes[2][0], 0])
        asteroid_direction["IF"] = fuzz.trimf(asteroid_direction.universe, [-1 * genes[2][0], 0, genes[2][0]])
        asteroid_direction["CR"] = fuzz.trimf(asteroid_direction.universe, [0, genes[2][0], genes[2][1]])
        asteroid_direction["FR"] = fuzz.smf(asteroid_direction.universe, genes[2][0], genes[2][1])
        
        # Consequent fuzzy set declarations
        
        # Declare the fuzzy sets for obtaining the turn rate required to turn to the firing direction        
        ship_turn_rate["FL"] = fuzz.zmf(ship_turn_rate.universe, -1 * genes[3][2], -1 * genes[3][1])
        ship_turn_rate["SL"] = fuzz.trimf(ship_turn_rate.universe, [-1 * genes[3][1], -1 * genes[3][1], -1 * genes[3][0]])
        ship_turn_rate["AZ"] = fuzz.trimf(ship_turn_rate.universe, [-1 * genes[3][0], 0, genes[3][0]])
        ship_turn_rate["SR"] = fuzz.trimf(ship_turn_rate.universe, [genes[3][0], genes[3][1], genes[3][1]])
        ship_turn_rate["FR"] = fuzz.smf(ship_turn_rate.universe, genes[3][1], genes[3][2])
        
        # Declare the fuzzy sets for obtaining the ship's thrust
        ship_thrust["NL"] = fuzz.trimf(ship_thrust.universe, [-480, -480, -1 * genes[4][0]])
        ship_thrust["NS"] = fuzz.trimf(ship_thrust.universe, [-1 * genes[4][1], -1 * genes[4][0], 0])
        ship_thrust["AZ"] = fuzz.trimf(ship_thrust.universe, [-1 * genes[4][0], 0, genes[4][0]])
        ship_thrust["PS"] = fuzz.trimf(ship_thrust.universe, [0, genes[4][0], genes[4][1]])
        ship_thrust["PL"] = fuzz.trimf(ship_thrust.universe, [genes[4][0], 480, 480])
                
        # Declare the fuzzy sets for determining whether to fire a bullet
        fire_bullet["N"] = fuzz.trimf(fire_bullet.universe, [-1, -1, 0.0])
        fire_bullet["Y"] = fuzz.trimf(fire_bullet.universe, [0.0, 1, 1])
        
        rules = []
        
        rules.append(ctrl.Rule(asteroid_direction["FL"], (ship_turn_rate["FL"], fire_bullet["N"])))
        rules.append(ctrl.Rule(asteroid_direction["CL"], (ship_turn_rate["FL"], fire_bullet["N"])))
        rules.append(ctrl.Rule(asteroid_direction["IF"], (ship_turn_rate["AZ"], fire_bullet["Y"])))
        rules.append(ctrl.Rule(asteroid_direction["CR"], (ship_turn_rate["FR"], fire_bullet["N"])))
        rules.append(ctrl.Rule(asteroid_direction["FR"], (ship_turn_rate["FR"], fire_bullet["N"])))
        
        rules.append(ctrl.Rule(asteroid_distance["VC"] & asteroid_size["H"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_distance["VC"] & asteroid_size["L"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_distance["VC"] & asteroid_size["M"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_distance["VC"] & asteroid_size["S"], ship_thrust["NL"]))
        
        rules.append(ctrl.Rule(asteroid_distance["SC"] & asteroid_size["H"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_distance["SC"] & asteroid_size["L"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_distance["SC"] & asteroid_size["M"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_distance["SC"] & asteroid_size["S"], ship_thrust["AZ"]))
        
        rules.append(ctrl.Rule(asteroid_distance["IR"] & asteroid_size["H"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_distance["IR"] & asteroid_size["L"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_distance["IR"] & asteroid_size["M"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_distance["IR"] & asteroid_size["S"], ship_thrust["AZ"]))
        
        rules.append(ctrl.Rule(asteroid_distance["SF"] & asteroid_size["H"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_distance["SF"] & asteroid_size["L"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_distance["SF"] & asteroid_size["M"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_distance["SF"] & asteroid_size["S"], ship_thrust["PS"]))
        
        rules.append(ctrl.Rule(asteroid_distance["VF"] & asteroid_size["H"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_distance["VF"] & asteroid_size["L"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_distance["VF"] & asteroid_size["M"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_distance["VF"] & asteroid_size["S"], ship_thrust["PL"]))
        
        rules.append(ctrl.Rule(asteroid_direction["FL"] & ship_speed["NL"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_direction["FL"] & ship_speed["NS"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["FL"] & ship_speed["AZ"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["FL"] & ship_speed["PS"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_direction["FR"] & ship_speed["PL"], ship_thrust["NL"]))
        
        rules.append(ctrl.Rule(asteroid_direction["CL"] & ship_speed["NL"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_direction["CL"] & ship_speed["NS"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_direction["CL"] & ship_speed["AZ"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_direction["CL"] & ship_speed["PS"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["CL"] & ship_speed["PL"], ship_thrust["NS"]))
        
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_size["S"], ship_thrust["PL"]))
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_size["M"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_size["L"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_size["H"], ship_thrust["NS"]))
        
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_distance["VC"] & asteroid_size["S"], ship_thrust["PL"]))
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_distance["VC"] & asteroid_size["M"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_distance["VC"] & asteroid_size["L"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_distance["VC"] & asteroid_size["H"], ship_thrust["NL"]))
        
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_distance["SC"] & asteroid_size["S"], ship_thrust["PL"]))
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_distance["SC"] & asteroid_size["M"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_distance["SC"] & asteroid_size["L"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["IF"] & asteroid_distance["SC"] & asteroid_size["H"], ship_thrust["NS"]))
        
        rules.append(ctrl.Rule(asteroid_direction["CR"] & ship_speed["NL"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_direction["CR"] & ship_speed["NS"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_direction["CR"] & ship_speed["AZ"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_direction["CR"] & ship_speed["PS"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["CR"] & ship_speed["PL"], ship_thrust["NS"]))
        
        rules.append(ctrl.Rule(asteroid_direction["FR"] & ship_speed["NL"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_direction["FR"] & ship_speed["NS"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["FR"] & ship_speed["AZ"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_direction["FR"] & ship_speed["PS"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_direction["FR"] & ship_speed["PL"], ship_thrust["NL"]))
        
        rules.append(ctrl.Rule(asteroid_distance["VC"] & ship_speed["NL"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_distance["VC"] & ship_speed["NS"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_distance["VC"] & ship_speed["AZ"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_distance["VC"] & ship_speed["PS"], ship_thrust["NL"]))
        rules.append(ctrl.Rule(asteroid_distance["VC"] & ship_speed["PL"], ship_thrust["NL"]))
        
        rules.append(ctrl.Rule(asteroid_distance["SC"] & ship_speed["NL"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_distance["SC"] & ship_speed["NS"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_distance["SC"] & ship_speed["AZ"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_distance["SC"] & ship_speed["PS"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_distance["SC"] & ship_speed["PL"], ship_thrust["NL"]))
        
        rules.append(ctrl.Rule(asteroid_distance["IR"] & ship_speed["NL"], ship_thrust["PL"]))
        rules.append(ctrl.Rule(asteroid_distance["IR"] & ship_speed["NS"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_distance["IR"] & ship_speed["AZ"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_distance["IR"] & ship_speed["PS"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_distance["IR"] & ship_speed["PL"], ship_thrust["NL"]))
        
        rules.append(ctrl.Rule(asteroid_distance["SF"] & ship_speed["NL"], ship_thrust["PL"]))
        rules.append(ctrl.Rule(asteroid_distance["SF"] & ship_speed["NS"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_distance["SF"] & ship_speed["AZ"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_distance["SF"] & ship_speed["PS"], ship_thrust["NS"]))
        rules.append(ctrl.Rule(asteroid_distance["SF"] & ship_speed["PL"], ship_thrust["NL"]))
        
        rules.append(ctrl.Rule(asteroid_distance["VF"] & ship_speed["NL"], ship_thrust["PL"]))
        rules.append(ctrl.Rule(asteroid_distance["VF"] & ship_speed["NS"], ship_thrust["PL"]))
        rules.append(ctrl.Rule(asteroid_distance["VF"] & ship_speed["AZ"], ship_thrust["PS"]))
        rules.append(ctrl.Rule(asteroid_distance["VF"] & ship_speed["PS"], ship_thrust["AZ"]))
        rules.append(ctrl.Rule(asteroid_distance["VF"] & ship_speed["PL"], ship_thrust["NS"]))
        
        # Add the fuzzy rules to the targetting system
        self.targetting_control = ctrl.ControlSystem()
        for rule in rules:
            self.targetting_control.addrule(rule)
        
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
                
        # Helps to reduce the indecisiveness when there are multiple asteroids closeby by
        # choosing to focusing on the first one detected in the group
        if self.focused_asteroid is not None:
            if (-1 <= (self.focused_asteroid[1] - closest_asteroid_distance) <= 1):
                # Find the distance between the ship's and asteroid's x and y positions
                x_delta = ship_state["position"][0] - self.focused_asteroid[0]["position"][0]
                y_delta = ship_state["position"][1] - self.focused_asteroid[0]["position"][1]
                
                # Obtain the Euclidean distance between the ship and the asteroid
                # To determine the surface to surface distance, the radius of each object must be subtracted
                distance = np.sqrt(x_delta**2 + y_delta**2) - ship_state["radius"] - asteroid["radius"]
                
                # Since we detected at least one other asteroid closeby, we focus on the first one detected
                closest_asteroid = self.focused_asteroid[0]
                closest_asteroid_distance = distance
                
                # Update the focused asteroid's distance (as it changes between timesteps)
                self.focused_asteroid = (self.focused_asteroid[0], distance)
            else:
                self.focused_asteroid = None
        else:
            self.focused_asteroid = (closest_asteroid, closest_asteroid_distance)
            
        # Obtain the magnitude and direction of the asteroid's velocity
        asteroid_velocity = np.sqrt(closest_asteroid["velocity"][0]**2 + closest_asteroid["velocity"][1]**2)
        asteroid_direction = np.arctan2(closest_asteroid["velocity"][1], closest_asteroid["velocity"][0])
        
        # Find the distance between the ship and the closest asteroid's x and y positions
        x_delta = ship_state["position"][0] - closest_asteroid["position"][0]
        y_delta = ship_state["position"][1] - closest_asteroid["position"][1]
        
        # Find the angle between the ship and the intersection point from the asteroid's frame of reference
        asteroid_angle = np.arctan2(y_delta, x_delta) + asteroid_direction
        
        # Find the determinant from the Quadratic formula
        a = asteroid_velocity**2 -  bullet_speed**2
        b = -2 * closest_asteroid_distance * asteroid_velocity * np.cos(asteroid_angle)
        c = closest_asteroid_distance**2
        determinant = b**2 - 4 * a * c
        
        # Evaluate the bullet impact time based on the calculated intercepts
        intercepts = ((-1 * b + np.sqrt(determinant)) / (2 * a), (-1 * b - np.sqrt(determinant)) / (2 * a))
        if intercepts[0] > intercepts[1]:
            bullet_intercept_time = intercepts[1] if intercepts[1] >= 0 else intercepts[0]
        else:
            bullet_intercept_time = intercepts[0] if intercepts[0] >= 0 else intercepts[1]
        
        # Obtain the intercept point from the bullet impact time
        x_intercept = closest_asteroid["position"][0] + (bullet_intercept_time + (1/30)) * closest_asteroid["velocity"][0]
        y_intercept = closest_asteroid["position"][1] + (bullet_intercept_time + (1/30)) * closest_asteroid["velocity"][1]
        
        # Determine the difference between the targetting angle and the current ship heading        
        ship_heading_rad = (np.pi / 180) * ship_state["heading"]
        targetting_angle = np.arctan2((y_intercept - ship_state["position"][1]), (x_intercept - ship_state["position"][0])) - ship_heading_rad
        targetting_angle = (targetting_angle + np.pi) % (2 * np.pi) - np.pi
        
        targetting_system = ctrl.ControlSystemSimulation(self.targetting_control, flush_after_run=1)
        targetting_system.input["ship_speed"] = ship_state["speed"]
        targetting_system.input["asteroid_size"] = closest_asteroid["size"]
        targetting_system.input["asteroid_distance"] = closest_asteroid_distance
        targetting_system.input["asteroid_direction"] = np.degrees(targetting_angle)
        targetting_system.compute()
        
        turn_rate = targetting_system.output["ship_turn_rate"]
        thrust = targetting_system.output["ship_thrust"]
        fire = True if (targetting_system.output["fire_bullet"] >= 0) else False
        
        self.eval_frames += 1
        
        return thrust, turn_rate, fire
        
    @property
    def name(self) -> str:
        return "GA Controller"
