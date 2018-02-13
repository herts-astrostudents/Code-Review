ASYMPTOTE = 0.47
WIDTH = 0.1


def log_OIII_Hb_NII(log_NII_Ha, eps=0):
    return 1.19 + eps + 0.61 / (log_NII_Ha - eps - ASYMPTOTE)


def log_OIII_Hb_NII_lower(log_NII_Ha):
    return log_OIII_Hb_NII(log_NII_Ha, -WIDTH)


def log_OIII_Hb_NII_upper(log_NII_Ha):
    return log_OIII_Hb_NII(log_NII_Ha, WIDTH)
