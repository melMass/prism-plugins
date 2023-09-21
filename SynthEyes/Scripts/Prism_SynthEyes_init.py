from Prism_SynthEyes_externalAccess_Functions import (
    Prism_SynthEyes_externalAccess_Functions,
)
from Prism_SynthEyes_Functions import Prism_SynthEyes_Functions
from Prism_SynthEyes_Integration import Prism_SynthEyes_Integration
from Prism_SynthEyes_Variables import Prism_SynthEyes_Variables


class Prism_SynthEyes(
    Prism_SynthEyes_Variables,
    Prism_SynthEyes_externalAccess_Functions,
    Prism_SynthEyes_Functions,
    Prism_SynthEyes_Integration,
):
    def __init__(self, core):
        Prism_SynthEyes_Variables.__init__(self, core, self)
        Prism_SynthEyes_externalAccess_Functions.__init__(self, core, self)
        Prism_SynthEyes_Functions.__init__(self, core, self)
        Prism_SynthEyes_Integration.__init__(self, core, self)
