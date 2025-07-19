# Dicionário de equivalências de motores (expandido com base nos dados do usuário)
EQUIVALENCIAS_MOTOR = {
    "1.0": ["1.0", "VHCE", "VHC", "VHC E", "C10NE", "C10YE", "SOHC EFI", "SOHC MPFI", "1,0"],
    "1.4": ["1.4", "SPE/4", "ECONOFLEX", "NLEV", "X14YFH", "NEV", "1,4"],
    "SPE/4": ["1.0", "1.4", "SPE/4", "ECONOFLEX", "NLEV", "1,0", "1,4"],
    "ECONOFLEX": ["1.4", "ECONOFLEX", "SPE/4", "NLEV", "1,4"],
    "NLEV": ["1.4", "NLEV", "ECONOFLEX", "SPE/4", "NEV", "1,4"],
    "VHC": ["1.0", "VHCE", "VHC", "VHC E", "1,0"],
    "VHC E": ["1.0", "VHCE", "VHC", "VHC E", "1,0"],
    "VHCE": ["1.0", "VHCE", "VHC", "VHC E", "1,0"],
    "SOHC EFI": ["1.0", "SOHC EFI", "SOHC MPFI", "1,0"],
    "SOHC MPFI": ["1.0", "SOHC EFI", "SOHC MPFI", "1,0"],
    "X14YFH": ["1.4", "X14YFH", "1,4"],
    "C10NE": ["1.0", "C10NE", "1,0"],
    "C10YE": ["1.0", "C10YE", "1,0"],
    "NEV": ["1.4", "NEV", "NLEV", "ECONOFLEX", "SPE/4", "1,4"],
    # Adicione outros conforme necessário
}

def equivalente_motor(motor1, motor2):
    m1 = str(motor1).strip().upper()
    m2 = str(motor2).strip().upper()
    for base, equivalentes in EQUIVALENCIAS_MOTOR.items():
        if m1 in equivalentes and m2 in equivalentes:
            return True
    return m1 == m2

# Dicionário de equivalências de modelos (expandido)
EQUIVALENCIAS_MODELO = {
    "ONIX": ["ONIX", "ONIX PLUS"],
    "PRISMA": ["PRISMA", "PRISMA SEDAN"],
    "CELTA": ["CELTA", "CELTA SPIRIT"],
    "CLASSIC": ["CLASSIC", "CLASSIC SEDAN"],
    "CORSA": ["CORSA", "CORSA SEDAN", "CORSA CLASSIC"],
    "MONTANA": ["MONTANA"],
    "MERIVA": ["MERIVA"],
    "COBALT": ["COBALT"],
    "AGILE": ["AGILE"],
    # Adicione outros conforme necessário
}

def equivalente_modelo(modelo1, modelo2):
    m1 = str(modelo1).strip().upper()
    m2 = str(modelo2).strip().upper()
    for base, equivalentes in EQUIVALENCIAS_MODELO.items():
        if m1 in equivalentes and m2 in equivalentes:
            return True
    return m1 == m2 