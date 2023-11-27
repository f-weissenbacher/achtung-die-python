from players.aiplayers.aiplayer_base import *

class WallAvoidingAIPlayer(AIPlayer):
    def __init__(self,  min_turn_radius, safety_factor=1.05, **aiplayer_kwargs):
        super().__init__(**aiplayer_kwargs)
        #self.min_turn_radius = min_turn_radius
        self.turn_radius = min_turn_radius * safety_factor
        self.center_rect = pygame.rect.Rect(self.xmin + 2*self.turn_radius, self.ymin + 2*self.turn_radius,
                                            (self.xmax - self.xmin) - 4*self.turn_radius,
                                            (self.ymax - self.ymin) - 4*self.turn_radius)


    def __str__(self):
        return f"WallAvoidingAIPlayer '{self.name}' ({self.color_name})"

    def next_action(self, game_state):
        if self.center_rect.collidepoint(*self.pos):
            return PlayerAction.KeepStraight

        possible_actions = self.wall_evasion_actions(self.turn_radius)

        if len(possible_actions) == 0:
            logging.debug(f"{self} is unable to evade the walls!")
            return PlayerAction.KeepStraight

        if PlayerAction.KeepStraight in possible_actions:
            # Go straight as long it is possible
            return PlayerAction.KeepStraight
        else:
            # Choose left or right turn at random
            #return random.choice(possible_actions)
            if PlayerAction.SteerRight in possible_actions:
                return PlayerAction.SteerRight
            else:
                return PlayerAction.SteerLeft


    def wall_evasion_actions(self, turn_radius):
        """ Returns a selection of PlayerActions that the player can take and still be able to avoid a wall collision."""
        actions = [PlayerAction.SteerLeft, PlayerAction.KeepStraight, PlayerAction.SteerRight]
        vel_dir = np.array([np.cos(self.angle), np.sin(self.angle)])
        #player_angle = np.mod(self.angle + np.pi, 2*np.pi) - np.pi

        # outward-facing wall normals
        wall_nvecs = np.array([[-1.,0.], [0.,1.], [1.,0.], [0.,-1.]])
        wall_names = np.array(["left","bottom","right","top"])

        # Get distances to walls in case that current heading is kept
        dist_to_left_wall = self.pos[0] - self.xmin
        dist_to_right_wall = self.xmax - self.pos[0]
        dist_to_bot_wall = self.ymax - self.pos[1]  # y-axis is inverted
        dist_to_top_wall = self.pos[1] - self.ymin  # y-axis is inverted

        wall_distances = np.array([dist_to_left_wall, dist_to_bot_wall, dist_to_right_wall, dist_to_top_wall])
        logging.debug(f"WallAvoidingPlayer {self.idx} wall distances " + "[{:5.1f} {:5.1f} {:5.1f} {:5.1f}]".format(*wall_distances))

        walls_close = wall_distances <= 2.5 * turn_radius
        num_walls_close = np.sum(walls_close)

        if num_walls_close == 0:
            # Player in center zone ==> walls pose no restrictions on movement here
            return actions

        # Determine walls that player is currently moving towards (max 2)
        #vel_nvec_sp = wall_nvecs.dot(vel_dir.T)
        walls_targeted = wall_nvecs.dot(vel_dir.T) >= 0.0

        walls_critical = np.logical_and(walls_close, walls_targeted)
        num_walls_critical = np.sum(walls_critical)

        if num_walls_critical == 0:
            # Player close to one or more walls, but is not moving towards them=> walls only restrict actions if
            # player is very close to one of them
            # Check if the next update would let player collide with walls
            actions = [a for a in actions if self._pos_inside_bounds(self._dryrun_action(a))]
            return actions

        else:
            # One or two walls critical
            # Rotation matrices:
            z_veldir = np.exp(1j * self.angle) # complex numbers to the rescue!
            z_dphi_half = np.exp(1j * 0.5 * self.dphi_per_tick)

            w = np.sqrt(turn_radius**2 - 0.25*self.dist_per_tick**2)
            #left_turn_state = PlayerTurnState.Possible
            #right_turn_state = PlayerTurnState.Possible

            #prior_pos = self.pos - 0.5 * self.dist_per_tick * vel_dir # distance travelled in prior tick

            turn_states = {}
            for turn_dir in ["left","right"]:
                # Vector from halfpoint between current and previous position to center of turning circle
                if turn_dir == "left":
                    w_vec = w * np.array([np.cos(self.angle - np.pi/2), np.sin(self.angle - np.pi/2)])
                else:
                    w_vec = w * np.array([np.cos(self.angle + np.pi / 2), np.sin(self.angle + np.pi / 2)])

                # Center of turn circle
                turn_center = self.pos - 0.5 * self.dist_per_tick * vel_dir + w_vec

                # Calculate critical/extremal points on current turning circle
                extremal_points = [turn_center + turn_radius * np.array([-1., 0.]),  # left
                                   turn_center + turn_radius * np.array([0., 1.]),   # bottom (Y-axis is inverted!)
                                   turn_center + turn_radius * np.array([1., 0.]),   # right
                                   turn_center + turn_radius * np.array([0., -1.]),  # top (Y-axis is inverted!)
                                   ]
                extremal_points = np.asarray(extremal_points)

                # Check if turn is possible at the current position
                x_ok = np.logical_and(extremal_points[:,0] > self.xmin, extremal_points[:,0] < self.xmax)
                y_ok = np.logical_and(extremal_points[:,1] > self.ymin, extremal_points[:,1] < self.ymax)
                extrema_in_bounds = np.logical_and(x_ok, y_ok)

                problematic_extrema = np.argwhere(extrema_in_bounds == False).flatten()

                if len(problematic_extrema) > 0:
                    turn_states[turn_dir] = EvasionTurnState.Impossible
                    logging.debug(f"{self} {turn_dir} turn evasion not possible due to conflict with "
                                  f"{wall_names[problematic_extrema]} wall(s)")
                else:
                    turn_states[turn_dir] = EvasionTurnState.Possible

                    # Check if evasion turn would still be possible in the next tick if no action is taken now
                    extremal_points += self.dist_per_tick * vel_dir

                    x_ok = np.logical_and(extremal_points[:, 0] > self.xmin, extremal_points[:, 0] < self.xmax)
                    y_ok = np.logical_and(extremal_points[:, 1] > self.ymin, extremal_points[:, 1] < self.ymax)
                    extrema_in_bounds = np.logical_and(x_ok, y_ok)

                    problematic_extrema = np.argwhere(extrema_in_bounds[walls_critical] == False).flatten()
                    if problematic_extrema.size > 0:
                        turn_states[turn_dir] = EvasionTurnState.ActionRequired
                        logging.debug(f"{self} {turn_dir} turn evasion requires immediate action. conflict with "
                                      f"{wall_names[problematic_extrema]} wall(s) projected for next tick")


            impossible_turns = [td for td,ts in turn_states.items() if ts == EvasionTurnState.Impossible]
            required_turns = [td for td,ts in turn_states.items() if ts == EvasionTurnState.ActionRequired]
            possible_turns = [td for td,ts in turn_states.items() if ts == EvasionTurnState.Possible]

            if len(impossible_turns) == 0:
                # both left and right turn still possible
                # check if both need immediate action
                if len(required_turns) == 2:
                    # Player has to steer to avoid future collision, but the direction is arbitrary
                    actions = [PlayerAction.SteerLeft, PlayerAction.SteerRight]
                else:
                    # At least 1 turn is non-compulsory, player can choose to go straight as well
                    actions = [PlayerAction.SteerLeft, PlayerAction.KeepStraight,PlayerAction.SteerRight]

            elif len(impossible_turns) == 1:
                # One turn is still possible. Check if it requires immediate action
                if len(required_turns) == 0:
                    # Remaining turn is not compulsory.
                    actions = [PlayerAction.SteerLeft if possible_turns[0] == "left" else PlayerAction.SteerRight]

                    # Check if straight action is possible as well
                    if self._pos_inside_bounds(self._dryrun_action(PlayerAction.KeepStraight)):
                        actions.append(PlayerAction.KeepStraight)
                elif len(required_turns) == 1:
                    # Remaining turn is compulsory
                    actions = [PlayerAction.SteerLeft if required_turns[0] == "left" else PlayerAction.SteerRight]
                else:
                    # This should not happen
                    raise RuntimeError("There should not be more than 1 required evasion turn if the other evasion turn is impossible!")

            else:
                # no evasion turns are possible --> player has already failed, will eventually hit the wall
                actions = []


            logging.debug(f"Possible steering actions for wall evasion {actions}")
            return actions



class RandomSteeringAIPlayer(WallAvoidingAIPlayer):
    def __init__(self, min_turn_radius, turn_angles_deg=(40., 180.), straight_lengths=(0, 200.0), **aiplayer_kwargs):
        super().__init__(min_turn_radius=min_turn_radius, **aiplayer_kwargs)

        self.turn_angles = np.deg2rad(turn_angles_deg)  # minimum/maximum angle of a turn (in radians)
        self.straight_lengths = straight_lengths  # minimum/maximum distance travelled in straight line (in game units)

        self.current_state = None
        self.ticks_till_next_state = 0

    def __str__(self):
        return f"RandomSteeringAIPlayer '{self.name}' ({self.color_name})"


    def _roll_new_state(self):
        # Turn or keep straight

        potential_actions = [PlayerAction.KeepStraight, PlayerAction.SteerLeft,PlayerAction.SteerRight]
        new_state = potential_actions[np.random.randint(0,3)]

        if new_state != PlayerAction.KeepStraight:
            turn_dir = "left" if new_state == PlayerAction.SteerLeft else "right"
            angle = self.turn_angles[0] + np.ptp(self.turn_angles) * np.random.random()
            self.ticks_till_next_state = int(angle/self.dphi_per_tick)
            logging.debug(f"{self} new plan: turn {turn_dir} {np.rad2deg(angle):.2f} degrees == {self.ticks_till_next_state} ticks")
        else:
            length = self.straight_lengths[0] + np.ptp(self.straight_lengths) * np.random.random()
            self.ticks_till_next_state = int(length/self.dist_per_tick)
            logging.debug(f"{self} new plan: keep straight for {length:.1f} game units == {self.ticks_till_next_state} ticks")

        self.current_state = new_state


    def next_action(self, game_state):
        """

        Args:
            game_state: not used

        Returns: next PlayerAction

        """

        self.ticks_till_next_state -= 1
        possible_actions = self.wall_evasion_actions(self.turn_radius)

        if len(possible_actions) == 0:
            return PlayerAction.KeepStraight
        elif len(possible_actions) == 1:
            return possible_actions[0]

        if self.current_state is None or self.ticks_till_next_state <= 0:
            self._roll_new_state()

        if self.current_state in possible_actions:
            return self.current_state
        else:
            return possible_actions[np.random.randint(0,len(possible_actions))]





