class Pokemon:
    def __init__(self):
        self.Species = ""
        self.Ability = ""
        self.Gender = ""
        self.Level = ""
        self.isEgg = "true"
        self.isShiny = "false"
        self.Nature = ""
        self.HP = 0
        self.Atk = 0
        self.Def = 0
        self.SpA = 0
        self.SpD = 0
        self.Spe = 0
        self.MoveOne = ""
        self.MoveTwo = ""
        self.MoveThree = ""
        self.MoveFour = ""

    def pokemon_as_dict(self):
        return {
            "Species": self.Species,
            "Ability": self.Ability,
            "Gender": self.Gender,
            "Level": self.Level,
            "isEgg": self.isEgg,
            "isShiny": self.isShiny,
            "Nature": self.Nature,
            "HP": self.HP,
            "Atk": self.Atk,
            "Def": self.Def,
            "SpA": self.SpA,
            "SpD": self.SpD,
            "Spe": self.Spe,
            "MoveOne": self.MoveOne,
            "MoveTwo": self.MoveTwo,
            "MoveThree": self.MoveThree,
            "MoveFour": self.MoveFour
        }

