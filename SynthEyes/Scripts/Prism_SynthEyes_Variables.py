import os


class Prism_SynthEyes_Variables(object):
    def __init__(self, core, plugin):
        self.version = "v2.0.0.beta13"
        self.pluginName = "SynthEyes"
        self.appShortName = "SynthEyes"
        self.pluginType = "App"
        self.platforms = ["Windows", "Linux", "Darwin"]
        self.appType = "3d"
        self.hasQtParent = True
        self.hasIntegration = True
        self.sceneFormats = [".sni"]
        self.appSpecificFormats = self.sceneFormats
        self.outputFormats = [
            ".abc",
            ".fbx",
            ".obj",
            ".usda" "ShotCam",
            "other",
        ]
        self.appColor = [212, 74, 34]
        self.renderPasses = []
        self.pluginDirectory = os.path.abspath(
            os.path.dirname(os.path.dirname(__file__))
        )

        self.appIcon = os.path.join(
            self.pluginDirectory, "UserInterfaces", "syntheyes.ico"
        )
