"""
Cookie Clicker Simulator
@Author: Henry Wan
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided
import math

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        """
        Initialize the game
        """
        self._current_cookie = 0
        self._current_cps = 1.0
        self._total_cookie = 0
        self._time = 0.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        time = "Time " + str(self._time)
        cur_cookie = "Current Cookies " + str(self._current_cookie)
        cps = "CPS " + str(self._current_cps)
        total = "Total Cookies " + str(self._total_cookie)
        return  time + '\n' + cur_cookie + '\n' + cps + '\n' + total
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookie
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        history = []
        for item in self._history:
            history.append(item)
        return history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if (self._current_cookie >= cookies):
            return 0.0
        else:
            return math.ceil((cookies - self._current_cookie) / self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if (time > 0):
            self._time += time
            self._current_cookie += time * self._current_cps
            self._total_cookie += time * self._current_cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if (self._current_cookie >= cost):
            self._current_cps += additional_cps
            self._current_cookie -= cost
            new_history = (self._time, item_name, cost, self._total_cookie)
            self._history.append(new_history)


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """ 
    cookiecliker = ClickerState()
    build = build_info
    while (cookiecliker.get_time() <= duration):
        item = strategy(cookiecliker.get_cookies(), cookiecliker.get_cps(), 
                      cookiecliker.get_history(), duration - cookiecliker.get_time(), build)
        if (item == None):
            cookiecliker.wait(duration - cookiecliker.get_time())
            return cookiecliker
        else:
            wait_time = cookiecliker.time_until(build.get_cost(item))
            if (wait_time == 0.0):
                cookiecliker.buy_item(item, build.get_cost(item), build.get_cps(item))
            else:
                if (wait_time <= duration - cookiecliker.get_time()):
                    cookiecliker.wait(wait_time)
                    cookiecliker.buy_item(item, build.get_cost(item), build.get_cps(item))
                else:
                    cookiecliker.wait(duration - cookiecliker.get_time())
                    return cookiecliker
            build.update_item(item)


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    choice = None
    cost = float('inf')
    for item in build_info.build_items():
        if (build_info.get_cost(item) < cost):
            cost = build_info.get_cost(item)
            choice = item
    if (build_info.get_cost(choice) > cookies + time_left * cps):
        choice = None
    return choice

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    choice = None
    cost = float('-inf')
    for item in build_info.build_items():
        if (build_info.get_cost(item) <= cookies + time_left * cps):
            if (build_info.get_cost(item) > cost): 
                cost = build_info.get_cost(item)
                choice = item
    return choice

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement. Always purchase
    the most cost-efficient item
    """
    choice = None
    best = float('inf')
    for item in build_info.build_items():
        temp = build_info.get_cost(item) / build_info.get_cps(item)
        if (temp < best):
            best = temp
            choice = item
    return choice
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("None", SIM_TIME, strategy_none)
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
    

