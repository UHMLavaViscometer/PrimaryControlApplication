# Michael Dodge II
# ME 482: Senior Design Project (Fall 2023)
# Team Lava
from papirus import PapirusComposite

def make_content(run_data: dict) -> PapirusComposite:
    """Produce a viscosity graph (and maybe others) and list some key values.
    Key values include: 
    * Viscosity mode (Newtonian, Thixotropic, etc.)
    * Viscosity [cPs]
    * Temperature [K]
    * GPS Coordinates [xx.xxxx, yy.yyyy]"""
    try: 
        screen_content = PapirusComposite(False, rotation = 0)
        screen_content.AddText(f"Time (s): {run_data['time_since_power_on__ms']/1000.0}", x=5, y=5, size=24)
        screen_content.AddText(f"Torque (raw): {run_data['torque_raw_10bit']}", x=5, y=34, size=24)
        return screen_content
    except Exception as e:
        screen_content = PapirusComposite(False, rotation = 0)
        screen_content.AddText("Something went wrong.", 5, 5)
        screen_content.AddText("Please restart the viscometer.", 5, 30)
        print(e)
        return screen_content
