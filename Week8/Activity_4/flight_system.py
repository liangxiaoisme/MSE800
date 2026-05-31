class Flight:
    """Base class - data & behaviour shared by every flight."""

    def __init__(self, flight_number, departure, destination,
                 carry_on_allowance, checked_baggage_allowance):
        self.flight_number = flight_number                          # flight code
        self.departure = departure                                  # origin airport
        self.destination = destination                              # arrival airport
        self.carry_on_allowance = carry_on_allowance                # carry-on limit
        self.checked_baggage_allowance = checked_baggage_allowance  # checked-bag limit

    def show_route(self):
        # Method 1: route
        return f"{self.flight_number}: {self.departure} -> {self.destination}"

    def show_baggage(self):
        # Method 2: baggage
        return f"Carry-on {self.carry_on_allowance} | Checked {self.checked_baggage_allowance}"

    def show_summary(self):
        # Method 3: route + baggage
        return f"{self.show_route()} | {self.show_baggage()}"


# ----- Dimension 1: flight TYPE (inherits Flight) -----

class DomesticFlight(Flight):
    """Domestic flight."""

    def flight_type(self):
        return "Domestic"

    def check_in_info(self):
        return "Online check-in available; ID may be checked at bag drop."

    def show_domestic_rule(self):
        return f"{self.flight_type()} rule: {self.check_in_info()}"


class InternationalFlight(Flight):
    """International flight."""

    def flight_type(self):
        return "International"

    def check_visa(self):
        return "Required"

    def show_international_rule(self):
        return f"{self.flight_type()} rule: Visa {self.check_visa()}"


# ----- Dimension 2: flight MODE (mixins, do NOT inherit Flight) -----

class DirectFlight:
    """Direct-flight mixin - no stopover."""

    def flight_mode(self):
        return "Direct"

    def show_stop_info(self):
        return "No stopover"

    def travel_note(self):
        return "Go directly to your departure gate."


class TransitFlight:
    """Transit-flight mixin - has a stopover."""

    def __init__(self, stopover):
        self.stopover = stopover                                    # stopover city

    def flight_mode(self):
        return "Transit"

    def show_stop_info(self):
        return f"Stopover: {self.stopover}"

    def travel_note(self):
        return "Check the next boarding gate during transit."


# ----- Combined classes: TYPE x MODE (multiple inheritance) -----

class DomesticDirectFlight(DomesticFlight, DirectFlight):
    """Domestic + Direct."""

    def show_details(self):
        # Combine inherited info from BOTH parents.
        return f"{self.show_summary()} | Type: {self.flight_type()} {self.flight_mode()}"

    def show_full_trip(self):
        return f"{self.show_details()} | {self.show_stop_info()}"

    def show_summary(self):
        # Direct has no stopover, so summary = route + baggage.
        return f"{self.show_route()} | {self.show_baggage()}"


class DomesticTransitFlight(DomesticFlight, TransitFlight):
    """Domestic + Transit."""

    def __init__(self, flight_number, departure, destination,
                 carry_on_allowance, checked_baggage_allowance, stopover):
        # Call BOTH parents explicitly so it is obvious which parent sets what.
        DomesticFlight.__init__(self, flight_number, departure, destination,
                                carry_on_allowance, checked_baggage_allowance)
        TransitFlight.__init__(self, stopover)

    def show_details(self):
        return f"{self.show_summary()} | Type: {self.flight_type()} {self.flight_mode()}"

    def show_full_trip(self):
        return f"{self.show_details()} | {self.travel_note()}"

    def show_summary(self):
        # Transit adds the stopover to the summary.
        return f"{self.show_route()} | {self.show_baggage()} | {self.show_stop_info()}"


class InternationalDirectFlight(InternationalFlight, DirectFlight):
    """International + Direct."""

    def show_details(self):
        return (f"{self.show_summary()} | Type: {self.flight_type()} "
                f"{self.flight_mode()} | Visa: {self.check_visa()}")

    def show_full_trip(self):
        return f"{self.show_details()} | {self.show_stop_info()}"

    def show_summary(self):
        return f"{self.show_route()} | {self.show_baggage()}"


class InternationalTransitFlight(InternationalFlight, TransitFlight):
    """International + Transit."""

    def __init__(self, flight_number, departure, destination,
                 carry_on_allowance, checked_baggage_allowance, stopover):
        InternationalFlight.__init__(self, flight_number, departure, destination,
                                     carry_on_allowance, checked_baggage_allowance)
        TransitFlight.__init__(self, stopover)

    def show_details(self):
        return (f"{self.show_summary()} | Type: {self.flight_type()} "
                f"{self.flight_mode()} | Visa: {self.check_visa()}")

    def show_full_trip(self):
        return f"{self.show_details()} | {self.travel_note()}"

    def show_summary(self):
        return f"{self.show_route()} | {self.show_baggage()} | {self.show_stop_info()}"


if __name__ == "__main__":
    # One flight of each combination.
    domestic_direct = DomesticDirectFlight(
        "NZ101", "Auckland", "Wellington", "7kg", "Depends on fare")
    domestic_transit = DomesticTransitFlight(
        "NZ202", "Auckland", "Queenstown", "7kg", "Depends on fare", "Christchurch")
    international_direct = InternationalDirectFlight(
        "NZ289", "Auckland", "Shanghai", "7kg", "2 x 23kg")
    international_transit = InternationalTransitFlight(
        "NZ777", "Auckland", "London", "7kg", "2 x 23kg", "Singapore")

    print("=== Air New Zealand Flight Management System ===")
    print(domestic_direct.show_full_trip())
    print(domestic_transit.show_full_trip())
    print(international_direct.show_full_trip())
    print(international_transit.show_full_trip())
