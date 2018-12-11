from src.XP.fileUpdate import download_file, openFile


def init():
    global xpban
    xpban = [[""] * 2]
    global sectXP
    sectXP = list()
    global sectLvl
    sectLvl = list()

    download_file("levels.csv", "/levels.csv")
    download_file("sectLevels.csv", "/sectLevels.csv")

    openFile("levels.csv", "r+", sectXP)
    openFile("sectLevels.csv", "r+", sectLvl)
