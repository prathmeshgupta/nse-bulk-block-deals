"""Client Entity Classification Engine for Bulk & Block Deals."""

import re

MF_KEYWORDS = [
    "MUTUAL FUND", " MF ", "TRUSTEE", "HDFC TRUSTEE", "ICICI PRUDENTIAL",
    "NIPPON INDIA", "SBI MUTUAL", "KOTAK MAHINDRA", "AXIS MUTUAL", "UTI MUTUAL",
    "MIRAE ASSET", "BANDHAN", "QUANT MUTUAL", "MOTILAL OSWAL", "DSP MUTUAL",
    "EDELWEISS", "TATA MUTUAL", "INVESCO", "SUNDARAM", "FRANKLIN TEMPLETON"
]

FII_KEYWORDS = [
    "GOVERNMENT PENSION FUND", "NORGES", "SOCIETE GENERALE", "BNP PARIBAS",
    "MORGAN STANLEY", "GOLDMAN SACHS", "CITIGROUP", "BARCLAYS", "BOFA",
    "VANGUARD", "BLACKROCK", "ISHARES", "FIDELITY", "CAPITAL GROUP",
    "ABU DHABI INVESTMENT", "GIC PRIVATE", "TEMASEK", "KUWAIT INVESTMENT",
    "INVESTMENT AUTHORITY", "EMERGING MARKETS", "MAURITIUS", "SINGAPORE"
]

INSURANCE_KEYWORDS = [
    "LIFE INSURANCE", "GENERAL INSURANCE", "LIC OF INDIA", "SBI LIFE",
    "HDFC LIFE", "ICICI PRU LIFE", "MAX LIFE", "BAJAJ ALLIANZ", "NEW INDIA ASSURANCE"
]

AIF_PE_KEYWORDS = [
    "ALTERNATE INVESTMENT FUND", "AIF", "VENTURES", "CAPITAL PARTNERS",
    "GROWTH FUND", "PRIVATE EQUITY", "OPPORTUNITIES FUND", "INDIA INITIATIVE"
]

def classify_client(client_name: str) -> str:
    """Classifies a client name into an institutional participant category."""
    if not isinstance(client_name, str) or not client_name.strip():
        return "UNKNOWN"

    name_upper = client_name.upper()

    for kw in MF_KEYWORDS:
        if kw in name_upper:
            return "DOMESTIC_MUTUAL_FUND"

    for kw in INSURANCE_KEYWORDS:
        if kw in name_upper:
            return "INSURANCE_COMPANY"

    for kw in FII_KEYWORDS:
        if kw in name_upper:
            return "FII_FPI_SOVEREIGN"

    for kw in AIF_PE_KEYWORDS:
        if kw in name_upper:
            return "AIF_PE_VENTURE"

    return "CORPORATE_OR_HNI"
