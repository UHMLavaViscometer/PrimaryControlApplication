from papirus import PapirusComposite
import matplotlib as mp

def make_content(run_data: dict) -> PapirusComposite:
    """Produce a viscosity graph (and maybe others) and list some key values.
    Key values include: 
    * Viscosity mode (Newtonian, Thixotropic, etc.)
    * Viscosity [cPs]
    * Temperature [K]
    * GPS Coordinates [xx.xxxx, yy.yyyy]"""
    try: 
        # placeholder, this will be where the composite is made
        print("test")
    except Exception as e:
        screen_content = PapirusComposite(False, rotation = 270)
        screen_content.AddText("Something went wrong.", 5, 5)
        screen_content.AddText("Please restart the viscometer.", 5, 30)
        print(e)
        return screen_content
