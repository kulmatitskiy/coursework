from twitter_stream import stream_tweets_to_file

def save_to_file(lines, filename):
    file = open(filename, "w")
    file.write("\n".join(lines))
    file.close()

if __name__ == '__main__':
    shows = ["TheAmericansFX", "HouseofCards", "TrueDetective", "FargoFX", "Suits_USA", "BetterCallSaul",
           "AmericanCrimeTV", "DowntonAbbey", "girlsHBO", "broadcity", "TogethernessHBO", "thexfiles",
           "GreysABC", "BigBang_CBS", "TheGrinderFOX", "Castle_ABC", "BONESonFOX", "CrimMinds_CBS",
           "FamilyGuyonFOX", "TheSimpsons", "Nashville_ABC", "TheGoodWife_CBS", "SiliconHBO",
           "WalkingDead", "LastManABC", "SleepyHollowFOX", "alwayssunny", "HowToGetAwayABC",
           "CSICyber","supergirlcbs","EmpireFOX","LastManFOX","NewGirlonFOX","NBCBlacklist",
           "AmericanDadTBS", "ArcherFX", "BasketsFX", "SHO_Homeland", "LastWeekTonight",
           "WorkaholicsCC"]
    save_to_file(shows, 'shows.txt')
    stream_tweets_to_file('tweets.json', shows)
